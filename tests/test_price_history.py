from decimal import Decimal

from sqlalchemy import select

from app.models import PriceHistory, Product


def make_product():
    return Product(url="https://books.toscrape.com/item", target_price=Decimal("19.99"))


def test_price_record_is_saved_with_check_time(db_session):
    product = make_product()
    product.price_history.append(PriceHistory(price=Decimal("21.50")))
    db_session.add(product)
    db_session.commit()

    record = db_session.scalars(select(PriceHistory)).one()

    assert record.product_id == product.id
    assert record.price == Decimal("21.50")
    assert record.checked_at is not None


def test_deleting_product_deletes_its_price_history(db_session):
    product = make_product()
    product.price_history.append(PriceHistory(price=Decimal("21.50")))
    product.price_history.append(PriceHistory(price=Decimal("20.50")))
    db_session.add(product)
    db_session.commit()

    db_session.delete(product)
    db_session.commit()

    assert db_session.scalars(select(PriceHistory)).all() == []
