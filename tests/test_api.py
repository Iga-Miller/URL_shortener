import pytest
from fastapi.testclient import TestClient
from app.api import app
import time
from app.db import SessionLocal, URLMapping

client = TestClient(app)

@pytest.fixture
def sample_url():
    return "https://www.example.com"

def test_shorten_url(sample_url):
    response = client.post("/shorten", json={"url": sample_url})
    assert response.status_code == 200
    assert "task_id" in response.json()  
    assert response.json()["status"] == "Processing"


def test_redirect_to_url(sample_url):
    response = client.post("/shorten", json={"url": sample_url})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    print(f"Task ID: {task_id}")

    start_time = time.time()
    timeout = 30

    while True:
        task_response = client.get(f"/task_status/{task_id}")
        assert task_response.status_code == 200
        task_data = task_response.json()

        if task_data["status"] == "SUCCESS":
            short_url = task_data["result"]
            print(f"Short URL: {short_url}") 
            break

        if time.time() - start_time > timeout:
            assert False, "Timeout exceeded"
        time.sleep(1)

    print("Wszystkie URL-e w bazie:")
    with SessionLocal() as db:
        for mapping in db.query(URLMapping).all():
            print(f"{mapping.original_url} -> {mapping.short_url}")

    response = client.get(f"/u/{short_url}")
    print(response.text) 
    assert response.status_code in [302, 307], f"Unexpected status code: {response.status_code}"




def test_invalid_url():
    response = client.post("/shorten", json={"url": "invalid-url"})
    assert response.status_code != 200 

def test_home_page():
    response = client.get("/home")
    assert response.status_code == 200
    assert "Skracacz URL" in response.text  

