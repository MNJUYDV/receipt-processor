import pytest
from datetime import date, time
from app.services.receipt_service import ReceiptService
from app.models.receipt import Receipt, Item

@pytest.fixture
def receipt_service():
    return ReceiptService()

@pytest.fixture
def sample_receipts():
    return {
        "basic_receipt": Receipt(
            retailer="Target",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(13, 1),
            items=[
                Item(shortDescription="Mountain Dew 12PK", price="6.49")
            ],
            total="6.49"
        ),
        "round_dollar_receipt": Receipt(
            retailer="Shop",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(13, 1),
            items=[
                Item(shortDescription="Item", price="10.00")
            ],
            total="10.00"
        ),
        "multiple_items_receipt": Receipt(
            retailer="Walmart",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(13, 1),
            items=[
                Item(shortDescription="Item 1", price="10.00"),
                Item(shortDescription="Item 2", price="10.00"),
                Item(shortDescription="Item 3", price="10.00"),
                Item(shortDescription="Item 4", price="10.00")
            ],
            total="40.00"
        ),
        "afternoon_time_receipt": Receipt(
            retailer="Store",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(14, 30),
            items=[
                Item(shortDescription="Item", price="5.00")
            ],
            total="5.00"
        ),
        "odd_day_receipt": Receipt(
            retailer="Shop",
            purchaseDate=date(2022, 1, 21),
            purchaseTime=time(13, 1),
            items=[
                Item(shortDescription="Item", price="5.00")
            ],
            total="5.00"
        )
    }

def test_process_receipt_returns_id(receipt_service, sample_receipts):
    """Test that process_receipt returns a valid UUID string"""
    receipt_id = receipt_service.process_receipt(sample_receipts["basic_receipt"])
    assert isinstance(receipt_id, str)
    assert len(receipt_id) > 0

def test_process_receipt_stores_receipt(receipt_service, sample_receipts):
    """Test that processed receipt is stored and retrievable"""
    receipt_id = receipt_service.process_receipt(sample_receipts["basic_receipt"])
    points = receipt_service.get_points(receipt_id)
    assert points is not None
    assert isinstance(points, int)

def test_get_points_nonexistent_receipt(receipt_service):
    """Test that getting points for non-existent receipt returns None"""
    points = receipt_service.get_points("nonexistent-id")
    assert points is None

def test_round_dollar_points(receipt_service, sample_receipts):
    """Test points calculation for round dollar amounts"""
    receipt_id = receipt_service.process_receipt(sample_receipts["round_dollar_receipt"])
    points = receipt_service.get_points(receipt_id)
    
    # Points breakdown:
    # - 4 points for retailer name "Shop"
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - Item has length 4 (not multiple of 3, no points)
    # - Even day (no points)
    # - Regular time (no points)
    expected_points = 85  # 4 + 50 + 25 + 6
    assert points == expected_points

def test_multiple_items_points(receipt_service, sample_receipts):
    """Test points calculation for multiple items"""
    receipt_id = receipt_service.process_receipt(sample_receipts["multiple_items_receipt"])
    points = receipt_service.get_points(receipt_id)
    
    # Points breakdown:
    # - 7 points for retailer name "Walmart"
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - 10 points for two pairs of items (5 points per pair)
    # - Items have lengths 6, 6, 6, 6 (multiples of 3)
    # - Each item worth ceil(10.00 * 0.2) = 2 points
    # - 4 items * 2 points = 8 points for descriptions
    # - 6 points for odd day
    expected_points = 106  # 7 + 50 + 25 + 10 + 8 + 6
    assert points == expected_points

def test_afternoon_time_points(receipt_service, sample_receipts):
    """Test points calculation for afternoon time bonus"""
    receipt_id = receipt_service.process_receipt(sample_receipts["afternoon_time_receipt"])
    points = receipt_service.get_points(receipt_id)
    
    # Points breakdown:
    # - 5 points for retailer name "Store"
    # - 10 points for afternoon time (2:30 PM)
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - Item has length 4 (not multiple of 3, no points)
    # - 6 points for odd day
    expected_points = 96  # 5 + 10 + 50 + 25 + 6
    assert points == expected_points

def test_odd_day_points(receipt_service, sample_receipts):
    """Test points calculation for odd day bonus"""
    receipt_id = receipt_service.process_receipt(sample_receipts["odd_day_receipt"])
    points = receipt_service.get_points(receipt_id)
    
    # Points breakdown:
    # - 4 points for retailer name "Shop"
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - 6 points for odd day
    expected_points = 85  # 4 + 50 + 25 + 6
    assert points == expected_points

def test_description_length_points(receipt_service):
    """Test points calculation for item descriptions that are multiples of 3"""
    receipt = Receipt(
        retailer="Shop",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[
            Item(shortDescription="ABC", price="2.00"),  # Length 3
            Item(shortDescription="ABCDEF", price="3.00"),  # Length 6
            Item(shortDescription="A", price="1.00"),  # Length 1 (not multiple of 3)
        ],
        total="6.00"
    )
    
    receipt_id = receipt_service.process_receipt(receipt)
    points = receipt_service.get_points(receipt_id)
    
    # Points breakdown:
    # - 4 points for retailer name "Shop"
    # - 50 points for round dollar amount
    # - 25 points for multiple of 0.25
    # - 5 points for one pair of items
    # - ceil(2.00 * 0.2) = 1 point for "ABC"
    # - ceil(3.00 * 0.2) = 1 point for "ABCDEF"
    # - 6 points for odd day
    expected_points = 92  # 4 + 50 + 25 + 5 + 1 + 1 + 6
    assert points == expected_points
    