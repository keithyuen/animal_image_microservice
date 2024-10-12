# tests/test_app.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

# Set up the database and TestClient
@pytest.fixture(scope="module")
def test_client():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Provide a TestClient for API calls
    with TestClient(app) as client:
        yield client
    
    # Drop the tables after tests are complete
    Base.metadata.drop_all(bind=engine)

# Test the save image endpoint
def test_save_images(test_client):
    response = test_client.post("/save/duck/1")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Saved 1 images"
    assert "images" in data
    assert len(data["images"]) == 1

# Test fetching the last image of a specific animal type
def test_get_last_image(test_client):
    # First, save an image to ensure there's one to retrieve
    test_client.post("/save/dog/1")
    
    # Then, fetch the last image
    response = test_client.get("/last/dog")
    assert response.status_code == 200
    data = response.json()
    assert "animal_type" in data
    assert data["animal_type"] == "dog"
    assert "image_url" in data

# Test fetching all images of all types
def test_get_all_images(test_client):
    # Save multiple images of different types
    test_client.post("/save/bear/1")
    test_client.post("/save/duck/1")
    test_client.post("/save/dog/1")

    # Fetch all images
    response = test_client.get("/all")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert len(data["images"]) >= 3
    # Check that images include different animal types
    types = set(image["animal_type"] for image in data["images"])
    assert "bear" in types
    assert "duck" in types
    assert "dog" in types
