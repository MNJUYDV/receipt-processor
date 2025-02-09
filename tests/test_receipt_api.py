import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def example_receipts():
    return {
        "walgreens_receipt": {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        },
        "target_single_item": {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        },
        "mm_corner_market": {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ],
            "total": "9.00"
        }
    }

def test_process_walgreens_receipt(example_receipts):
    """Test processing the Walgreens receipt"""
    receipt = example_receipts["walgreens_receipt"]
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    receipt_id = response.json()["id"]
    
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json()["points"]
    
    # Let's verify each rule for the Walgreens receipt:
    # Receipt details:
    # - Retailer: "Walgreens" (9 alphanumeric chars)
    # - Total: "2.65"
    # - Items:
    #   1. "Pepsi - 12-oz" ($1.25) - length 13 (not multiple of 3)
    #   2. "Dasani" ($1.40) - length 6 (multiple of 3)
    # - Date: "2022-01-02" (even day)
    # - Time: "08:13" (not between 2-4 PM)
    #
    # Points breakdown:
    # 1. Retailer name: 9 points (CONFIRMED)
    # 2. Round dollar: 0 points (not ending in .00)
    # 3. Multiple of 0.25: 0 points (2.65 not multiple of 0.25)
    # 4. Item pairs: 5 points (one pair)
    # 5. Description length:
    #    - "Pepsi - 12-oz": 0 points (length 13, not multiple of 3)
    #    - "Dasani": 1 point (length 6, ceil(1.40 * 0.2) = 1)
    # 6. Odd day: 0 points (2nd is even)
    # 7. Time bonus: 0 points (not between 2-4 PM)
    #
    # Total: 15 points (9 + 5 + 1)
    expected_points = 15
    assert points == expected_points, f"Got {points} points, expected {expected_points}"

def test_process_target_single_item(example_receipts):
    """Test processing the Target receipt with a single item"""
    receipt = example_receipts["target_single_item"]
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    receipt_id = response.json()["id"]
    
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json()["points"]
    
    # Points breakdown for Target receipt:
    # - 6 points for retailer name "Target"
    # - 25 points for total being multiple of 0.25
    expected_points = 31  # 6 + 25
    assert points == expected_points

def test_process_mm_corner_market(example_receipts):
    """Test processing M&M Corner Market receipt (example from requirements)"""
    receipt = example_receipts["mm_corner_market"]
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    receipt_id = response.json()["id"]
    
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json()["points"]
    
    # Points breakdown:
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - 14 points for alphanumeric characters in retailer name
    # - 10 points for time between 2:00pm and 4:00pm
    # - 10 points for 4 items (2 pairs @ 5 points each)
    expected_points = 109
    assert points == expected_points

def test_invalid_receipt_data():
    """Test various invalid receipt scenarios"""
    invalid_receipts = [
        {
            # Missing required fields
            "retailer": "Target"
        },
        {
            # Invalid date format
            "retailer": "Target",
            "purchaseDate": "2022-13-45",
            "purchaseTime": "13:01",
            "items": [],
            "total": "0"
        },
        {
            # Invalid time format
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "25:01",
            "items": [],
            "total": "0"
        }
    ]
    
    for invalid_receipt in invalid_receipts:
        response = client.post("/receipts/process", json=invalid_receipt)
        assert response.status_code == 422

def test_get_points_nonexistent_receipt():
    """Test getting points for a non-existent receipt ID"""
    response = client.get("/receipts/nonexistent-id/points")
    assert response.status_code == 404
    assert "detail" in response.json()