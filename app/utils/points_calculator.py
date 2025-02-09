import math
from datetime import time
from app.models.receipt import Receipt

def calculate_points(receipt: Receipt) -> int:
    points = 0
    debug_info = []
    
    # Rule 1: One point for every alphanumeric character in retailer name
    retailer_points = sum(c.isalnum() for c in receipt.retailer)
    points += retailer_points
    debug_info.append(f"Retailer points: {retailer_points} (for '{receipt.retailer}')")
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith(".00"):
        points += 50
        debug_info.append("Round dollar bonus: 50")
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    try:
        total_float = float(receipt.total)
        total_cents = round(total_float * 100)
        if total_cents % 25 == 0:
            points += 25
            debug_info.append("Multiple of 0.25 bonus: 25")
    except ValueError:
        debug_info.append("Error: Invalid total format")
    
    # Rule 4: 5 points for every two items
    pair_points = (len(receipt.items) // 2) * 5
    points += pair_points
    debug_info.append(f"Pair points: {pair_points} ({len(receipt.items)} items)")
    
    # Debug all item descriptions before processing
    debug_info.append("Item descriptions before processing:")
    for item in receipt.items:
        debug_info.append(f"  - Raw: '{item.shortDescription}'")
        debug_info.append(f"    Trimmed: '{item.shortDescription.strip()}'")
        debug_info.append(f"    Length: {len(item.shortDescription.strip())}")
    
    # Rule 5: Points for item descriptions that are multiples of 3
    for item in receipt.items:
        # Remove only leading and trailing whitespace, keep internal spaces
        trimmed_desc = item.shortDescription.strip()
        trimmed_length = len(trimmed_desc)
        debug_info.append(f"Processing item: '{trimmed_desc}' (length: {trimmed_length})")
        
        if trimmed_length > 0 and trimmed_length % 3 == 0:
            try:
                item_price = float(item.price)
                item_points = math.ceil(item_price * 0.2)
                points += item_points
                debug_info.append(
                    f"Description points: {item_points} for '{trimmed_desc}' "
                    f"(length {trimmed_length}, price {item.price}, calculation: "
                    f"{item_price} * 0.2 = {item_price * 0.2}, ceiling = {item_points})"
                )
            except ValueError:
                debug_info.append(f"Error: Invalid price format for item '{trimmed_desc}'")
    
    # Rule 6: 6 points if the day in the purchase date is odd
    if receipt.purchaseDate.day % 2 == 1:
        points += 6
        debug_info.append("Odd day bonus: 6")
    
    # Rule 7: 10 points if purchase time is between 2:00pm and 4:00pm
    if time(14, 0) <= receipt.purchaseTime < time(16, 0):
        points += 10
        debug_info.append("Afternoon time bonus: 10")
    
    print("\nPoint Calculation Debug Info:")
    for info in debug_info:
        print(f"- {info}")
    print(f"Total points: {points}\n")
    
    return points