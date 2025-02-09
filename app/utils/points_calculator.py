import math
from datetime import time
from app.models.receipt import Receipt

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # Rule 1: One point for every alphanumeric character in retailer name
    points += sum(c.isalnum() for c in receipt.retailer)
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith(".00"):
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    try:
        total_float = float(receipt.total)
        if round(total_float * 100) % 25 == 0:
            points += 25
    except ValueError:
        pass
    
    # Rule 4: 5 points for every two items
    points += (len(receipt.items) // 2) * 5
    
    # Rule 5: Points for item descriptions that are multiples of 3
    for item in receipt.items:
        trimmed_desc = item.shortDescription.strip()
        if len(trimmed_desc) > 0 and len(trimmed_desc) % 3 == 0:
            try:
                points += math.ceil(float(item.price) * 0.2)
            except ValueError:
                pass
    
    # Rule 6: 6 points if the day in the purchase date is odd
    if receipt.purchaseDate.day % 2 == 1:
        points += 6
    
    # Rule 7: 10 points if purchase time is between 2:00pm and 4:00pm
    if time(14, 0) <= receipt.purchaseTime < time(16, 0):
        points += 10
    
    return points