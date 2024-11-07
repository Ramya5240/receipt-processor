from controller.receipt_model import Receipt
import math

# In-memory storage for receipts
receipts_db = {}

def calculate_points(receipt: Receipt) -> int:
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += sum(1 for char in receipt.retailer if char.isalnum())

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    if float(receipt.total).is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if float(receipt.total) % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    points += (len(receipt.items) // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    #         multiply the price by 0.2 and round up to the nearest integer.
    for item in receipt.items:
        trimmed_desc = item.shortDescription.strip()
        if len(trimmed_desc) % 3 == 0:
            item_points = math.ceil(float(item.price) * 0.2)
            points += item_points

    # Rule 6: 6 points if the day in the purchase date is odd.
    day = int(receipt.purchaseDate.split("-")[2])
    if day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is between 2:00pm and 4:00pm.
    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10

    return points

def store_receipt(receipt_id: str, points: int):
    # Store receipt points in the in-memory database
    receipts_db[receipt_id] = points

def get_points(receipt_id: str) -> int:
    # Retrieve points from in-memory storage
    return receipts_db.get(receipt_id, None)
