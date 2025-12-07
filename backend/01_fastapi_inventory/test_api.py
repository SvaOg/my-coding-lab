from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_index():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Welcome" in data["message"]


# def test_get_item_by_id():
#     response = requests.get("http://localhost:8000/items/1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Nails"
#     assert data["category"] == "consumables"
#     assert data["price"] == 0.10


# def test_get_item_by_invalid_id():
#     response = requests.get("http://localhost:8000/items/999")
#     assert response.status_code == 404
#     data = response.json()
#     assert data["detail"] == "Item with id 999 does not exist."


# def test_get_item_wrong_id_type():
#     response = requests.get("http://localhost:8000/items/aaa")
#     assert response.status_code == 422
#     data = response.json()
#     assert data["detail"][0]["msg"].startswith("Input should be a valid integer")


# def test_query_item_by_parameters():
#     response = requests.get("http://localhost:8000/items?name=Nails")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["selection"][0]["name"] == "Nails"
