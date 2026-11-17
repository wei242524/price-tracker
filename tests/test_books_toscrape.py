from decimal import Decimal

import pytest

from app.scrapers.books_toscrape import PriceNotFoundError, parse_price


def test_parse_price_returns_decimal():
    html = '<p class="price_color">£51.77</p>'

    assert parse_price(html) == Decimal("51.77")


def test_parse_price_ignores_surrounding_whitespace():
    html = '<p class="price_color">\n    £51.77\n  </p>'

    assert parse_price(html) == Decimal("51.77")


def test_parse_price_raises_when_price_is_missing():
    html = "<p>no price here</p>"

    with pytest.raises(PriceNotFoundError):
        parse_price(html)
