from decimal import Decimal

from bs4 import BeautifulSoup


class PriceNotFoundError(Exception):
    """Raised when the price element is not found in the HTML."""


def parse_price(html: str) -> Decimal:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.select_one(".price_color")
    if tag is None:
        raise PriceNotFoundError("Price element '.price_color' not found in the HTML.")
    text = tag.get_text(strip=True)
    return Decimal(text.removeprefix("£"))
