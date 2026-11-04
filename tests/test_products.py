def create_product(client, url="https://example.com/item", target_price="19.99"):
    return client.post(
        "/products",
        json={"url": url, "target_price": target_price},
    )


def test_create_product(client):
    response = create_product(client)
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == "https://example.com/item"
    assert data["target_price"] == "19.99"
    assert "id" in data


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

    create_product(client)

    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_duplicate_url_returns_409(client):
    first = create_product(client, url="https://example.com/item", target_price="19.99")
    assert first.status_code == 201

    response = create_product(
        client, url="https://example.com/item", target_price="29.99"
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Product with this URL already exists"}


def test_create_negative_price_returns_422(client):
    response = create_product(
        client, url="https://example.com/item", target_price="-19.99"
    )
    assert response.status_code == 422
    assert client.get("/products").json() == []


def test_create_too_many_decimals_returns_422(client):
    response = create_product(
        client, url="https://example.com/item", target_price="19.999"
    )
    assert response.status_code == 422
    assert client.get("/products").json() == []


def test_get_product(client):
    create_response = create_product(
        client, url="https://example.com/item", target_price="19.99"
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://example.com/item"
    assert data["target_price"] == "19.99"
    assert data["id"] == product_id


def test_update_product_target_price(client):
    create_response = create_product(
        client, url="https://example.com/item", target_price="19.99"
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.patch(f"/products/{product_id}", json={"target_price": "15.00"})

    assert response.status_code == 200
    data = response.json()
    assert data["target_price"] == "15.00"
    assert data["url"] == "https://example.com/item"


def test_update_product_duplicate_url_returns_409(client):
    item1 = create_product(
        client, url="https://example.com/item1", target_price="19.99"
    )
    assert item1.status_code == 201

    item2 = create_product(
        client, url="https://example.com/item2", target_price="29.99"
    )
    assert item2.status_code == 201

    response = client.patch(
        f"/products/{item2.json()['id']}", json={"url": "https://example.com/item1"}
    )
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Product with this URL already exists"


def test_update_product_not_found(client):
    response = client.patch("/products/999", json={"target_price": "15.00"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product(client):
    create_response = create_product(
        client, url="https://example.com/item", target_price="19.99"
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_product_null_returns_422(client):
    create_response = create_product(
        client, url="https://example.com/item", target_price="19.99"
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = client.patch(f"/products/{product_id}", json={"target_price": None})
    assert response.status_code == 422

    response = client.get(f"/products/{product_id}")
    assert response.json()["target_price"] == "19.99"
