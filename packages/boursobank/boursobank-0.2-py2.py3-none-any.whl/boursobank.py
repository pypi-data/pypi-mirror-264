"""Parses BoursoBank account statements."""

import datetime as dt
import logging
import re
from decimal import Decimal

from pypdf import PdfReader
from rich.console import Console
from rich.table import Table
from rich import print as rich_print
from rich.panel import Panel

__version__ = "0.2"

DATE_RE = r"([0-9]{1,2}/[0-9]{2}/[0-9]{2,4})"

HEADER_VALUE_PATTERN = rf"""\s*
        (?P<date>{DATE_RE})\s+
        (?P<RIB>[0-9]{{5}}\s+[0-9]{{5}}\s+[0-9]{{11}}\s+[0-9]{{2}})\s+
        (
            (?P<devise>[A-Z]{{3}})
            |
            (?P<card_number>[0-9]{{4}}\*{{8}}[0-9]{{4}})
        )\s+
        (?P<periode>(du)?\s+{DATE_RE}\s+(au\s+)?{DATE_RE})\s+
        """

RE_CARD_OWNER = [  # First pattern is tried first
    re.compile(r"Porteur\s+de\s+la\s+carte\s+:\s+(?P<porteur>.*)$", flags=re.M),
    re.compile(
        r"44\s+rue\s+Traversiere\s+CS\s+80134\s+92772\s+"
        r"Boulogne-Billancourt\s+Cedex\s+(?P<porteur>.*)$",
        flags=re.M,
    ),
]


logger = logging.getLogger(__name__)


def parse_decimal(value: str):
    """Parse a French value like 1.234,56 to a Decimal instance."""
    return Decimal(value.replace(".", "").replace(",", "."))


class Line:
    """Represents one line (debit or credit) in a bank statement."""

    PATTERN = re.compile(
        rf"\s+(?P<date>{DATE_RE})\s*(?P<label>.*)\s+"
        rf"(?P<valeur>{DATE_RE})\s+(?P<amount>[0-9.,]+)$"
    )

    def __init__(self, statement, line):
        self.statement = statement
        self.line = line
        self.description = ""
        self.match = self.PATTERN.match(line)

    @property
    def label(self):
        """Line short description."""
        return re.sub(r"\s+", " ", self.match["label"]).strip()

    @property
    def safe_label(self):
        """Line short description without double quotes."""
        return self.label.replace('"', "")

    def add_description(self, description_line):
        """Add a line to a long description."""
        description_line = re.sub("\s+", " ", description_line).strip()
        if not description_line:
            return
        if self.description:
            self.description += "\n"
        self.description += description_line

    @property
    def direction(self):
        """returns '-' for outbound, and '+' for inbound.

        There's two columns in the PDF: Débit, Crédit.

        Sadly we don't really know where they are, and there's
        variations depending on the format, so we have to use an
        heuristic.
        """
        if self.statement.headers["date"] < dt.date(2021, 1, 1):
            column_at = 98
        else:
            column_at = 225

        column = self.match.start("amount")
        return "-" if column < column_at else "+"

    @property
    def amount(self):
        """Raw value for this line, dependless of its 'debit'/'credit' column"""
        return parse_decimal(self.match["amount"])

    @property
    def value(self):
        """Value for this line. Positive for credits, negative for debits."""
        return self.amount if self.direction == "+" else -self.amount

    def __str__(self):
        return f"{self.safe_label} {self.value}"


class AccountLine(Line):
    """Represents one line (debit or credit) in a bank statement."""

    PATTERN = re.compile(
        rf"\s+(?P<date>{DATE_RE})\s*(?P<label>.*)\s+"
        rf"(?P<valeur>{DATE_RE})\s+(?P<amount>[0-9.,]+)$"
    )


class BalanceBeforeLine(AccountLine):
    PATTERN = re.compile(rf"\s+SOLDE\s+AU\s+:\s+{DATE_RE}\s+(?P<amount>[0-9,.]+)$")


class BalanceAfterLine(AccountLine):
    PATTERN = re.compile(r"\s+Nouveau\s+solde\s+en\s+EUR\s+:\s+(?P<amount>[0-9,.]+)$")


class CardLine(Line):
    """Represents one line (debit or credit) in a card statement."""

    PATTERN = re.compile(
        rf"\s*(?P<date>{DATE_RE})\s+CARTE\s+(?P<valeur>{DATE_RE})"
        rf"\s+(?P<label>.*)\s+(?P<amount>[0-9.,]+)$"
    )

    @property
    def direction(self):
        """returns '-' for outbound, and '+' for inbound.

        As it's a card, we have only one column: debits.
        """
        return "-"


class CardLineDebit(CardLine):
    PATTERN = re.compile(
        rf"\s+A\s+VOTRE\s+DEBIT\s+LE\s+{DATE_RE}\s+(?P<amount>[0-9.,]+)$"
    )


class CardLineDebitWithFrancs(CardLineDebit):
    PATTERN = re.compile(
        rf"\s+A\s+VOTRE\s+DEBIT\s+LE\s+{DATE_RE}\s+"
        rf"(?P<amount>[0-9.,]+)\s+(?P<debit_francs>[0-9.,]+)$"
    )


class CardLineWithFrancs(CardLine):
    """Represents one line (debit or credit) in a card statement."""

    PATTERN = re.compile(
        rf"\s*(?P<date>{DATE_RE})\s+CARTE\s+(?P<label>.*)\s+"
        rf"(?P<amount>[0-9.,]+)\s+(?P<amount_francs>[0-9.,]+)$"
    )


class Statement:
    """Represents a bank account statement."""

    LineImpl = Line

    def __init__(self, filename, text, headers, **kwargs):
        self.filename = filename
        self.text = text
        self.headers = headers
        self.lines = []
        super().__init__(**kwargs)

    @classmethod
    def from_string(cls, string, filename="-"):
        """Builds a statement from a string, usefull for tests purposes."""
        headers = cls._parse_header(string, filename)
        if headers.get("card_number"):
            self = CardStatement(filename=filename, text=string, headers=headers)
        else:
            self = AccountStatement(filename=filename, text=string, headers=headers)
        self._parse()
        return self

    @classmethod
    def from_pdf(cls, filename):
        """Builds a statement from a PDF file."""
        buf = []
        for page in PdfReader(filename).pages:
            try:
                buf.append(
                    page.extract_text(extraction_mode="layout", orientations=[0])
                )
            except AttributeError:
                # Maybe just a blank page
                pass  # logger.exception("while parsing PDF %s", filename)
        return cls.from_string("\n".join(buf), filename)

    @classmethod
    def _parse_header(cls, text: str, filename: str) -> dict:
        headers = {}
        for text_line in text.splitlines():
            if values := re.match(HEADER_VALUE_PATTERN, text_line, re.VERBOSE):
                headers["emit_date"] = dt.datetime.strptime(
                    values["date"], "%d/%m/%Y"
                ).date()
                headers["date"] = (
                    dt.datetime.strptime(values["periode"].split()[-1], "%d/%m/%Y")
                    .date()
                    .replace(day=1)
                )
                headers["RIB"] = re.sub(r"\s+", " ", values["RIB"])
                headers["devise"] = values["devise"]
                headers["card_number"] = values["card_number"]
                break
        else:
            logger.warning("Cannot find header values in %s.", filename)
            return {}
        return headers

    def _parse_lines(self, text):
        current_line = None
        for text_line in text.splitlines():
            if text_line.strip() == "":
                if current_line:
                    self.lines.append(current_line)
                current_line = None
            line = self.LineImpl(self, text_line)
            if line.match:
                if current_line:
                    self.lines.append(current_line)
                current_line = line
            elif current_line:
                current_line.add_description(text_line)
        if current_line:
            self.lines.append(current_line)

    def __str__(self):
        buf = [f"Date: {self.headers['date']}", f"RIB: {self.headers['RIB']}"]
        for line in self.lines:
            buf.append(str(line))
        return "\n".join(buf)

    def pretty_print(self, show_desriptions):
        table = Table()
        table.add_column("Label", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for line in self.lines:
            if line.description and show_desriptions:
                table.add_row(line.label + "\n" + line.description, str(line.value))
            else:
                table.add_row(line.label, str(line.value))

        Console().print(table)


class AccountStatement(Statement):
    LineImpl = AccountLine

    def __init__(self, **kwargs):
        self.balance_before = Decimal(0)
        self.balance_after = Decimal(0)
        super().__init__(**kwargs)

    def validate(self):
        """Consistency check.

        It just verifies that all the lines sum to the right total.
        """
        computed = sum(line.value for line in self.lines)
        if self.balance_before + computed != self.balance_after:
            raise ValueError(
                f"Inconsistent total, found: {self.balance_before + computed!r}, "
                f"expected: {self.balance_after!r} in {self.filename}."
            )

    def _parse(self):
        start, stop = self._parse_soldes()
        self._parse_lines("\n".join(self.text.splitlines()[start + 1 : stop]))

    def _parse_soldes(self):
        start = stop = 0
        for lineno, text in enumerate(self.text.splitlines()):
            line = BalanceBeforeLine(self, text)
            if line.match:
                self.balance_before = line.value
                start = lineno
            line = BalanceAfterLine(self, text)
            if line.match:
                self.balance_after = line.value
                stop = lineno
        return start, stop

    def pretty_print(self, show_desriptions):
        table = Table(title=str(self.filename))
        table.add_column("Date")
        table.add_column("RIB")
        table.add_row(str(self.headers["date"]), self.headers["RIB"])
        Console().print(table)
        super().pretty_print(show_desriptions)


class CardStatement(Statement):
    LineImpl = CardLine

    def __init__(self, **kwargs):
        self.card_debit = Decimal(0)
        super().__init__(**kwargs)

    def validate(self):
        """Consistency check.

        It just verifies that all the lines sum to the right total.
        """
        computed = sum(line.value for line in self.lines)
        if computed != self.card_debit:
            raise ValueError(
                f"Inconsistent total, found: {computed!r}, "
                f"expected: {self.card_debit!r} in {self.filename}."
            )

    def _parse(self):
        self._parse_card_owner()
        self._parse_card_debit()
        self._parse_lines(self.text)

    def _parse_card_debit(self):
        for text in self.text.splitlines():
            line = CardLineDebitWithFrancs(self, text)
            if line.match:
                self.card_debit = line.value
                self.LineImpl = CardLineWithFrancs
                return
            line = CardLineDebit(self, text)
            if line.match:
                self.card_debit = line.value
                return

    def _parse_card_owner(self):
        for pattern in RE_CARD_OWNER:
            if match := pattern.search(self.text):
                self.headers["card_owner"] = re.sub(r"\s+", " ", match["porteur"])
                break

    def pretty_print(self, show_descriptions):
        table = Table(title=str(self.filename))
        table.add_column("Date")
        table.add_column("RIB")
        table.add_column("Card number")
        table.add_column("Card debit")
        table.add_column("Card owner")
        table.add_row(
            str(self.headers["date"]),
            self.headers["RIB"],
            self.headers["card_number"],
            str(self.card_debit),
            self.headers["card_owner"],
        )
        Console().print(table)
        super().pretty_print(show_descriptions)


def main():
    args = parse_args()

    logging.getLogger("pypdf._text_extraction._layout_mode._fixed_width_page").setLevel(
        logging.ERROR
    )

    for file in args.files:
        statement = Statement.from_pdf(file)
        if args.debug:
            rich_print(Panel(statement.text))
        statement.pretty_print(args.show_descriptions)
        statement.validate()


def parse_args():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-s", "--show-descriptions", action="store_true")
    parser.add_argument("files", nargs="*", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
