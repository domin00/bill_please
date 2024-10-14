from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for the current bill session
bill_data = {}
users = []


# Define models for the request/response bodies
class Item(BaseModel):
    name: str
    quantity: float
    price: float
    claimed_quantity: Optional[float] = 0.0  # Initially unclaimed
    claimed_by: Optional[str] = None  # Initially unassigned


class Bill(BaseModel):
    items: List[Item]


class User(BaseModel):
    name: str


class AssignItem(BaseModel):
    item_name: str
    user_name: str
    claimed_quantity: float


# POST /bill - Start a new session with a list of items
@app.post("/bill")
async def create_bill(bill: Bill):
    global bill_data, users
    bill_data = {"items": bill.items}  # Start fresh with the new bill
    users = []  # Reset users for the new session
    return {"message": "New bill session started", "bill": bill_data}


# POST /users - Initialize users involved in the split
@app.post("/users")
async def create_users(new_users: List[User]):
    global users
    users = [user.name for user in new_users]  # Add users to the session
    return {"message": "Users added", "users": users}


# GET /users - Retrieve the list of users
@app.get("/users")
async def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"users": users}


# POST /assign-item - Assign part or all of an item to a user
@app.post("/assign-item")
async def assign_item_to_user(assignment: AssignItem):
    global bill_data
    for item in bill_data["items"]:
        if item.name == assignment.item_name:
            if item.claimed_quantity + assignment.claimed_quantity > item.quantity:
                raise HTTPException(status_code=400, detail="Claim exceeds item quantity")
            item.claimed_quantity += assignment.claimed_quantity
            item.claimed_by = assignment.user_name
            return {"message": "Item assigned", "item": item}
    
    raise HTTPException(status_code=404, detail="Item not found")


# GET /split-summary - View the split summary
@app.get("/split-summary")
async def get_split_summary():
    if not bill_data:
        raise HTTPException(status_code=404, detail="No bill data found")
    
    split_summary = {}
    for item in bill_data["items"]:
        if item.claimed_by:
            if item.claimed_by not in split_summary:
                split_summary[item.claimed_by] = 0
            split_summary[item.claimed_by] += item.claimed_quantity * item.price / item.quantity
    
    return {"split_summary": split_summary}


# POST /finalize-split - Finalize and lock the split
@app.post("/finalize-split")
async def finalize_split():
    if not bill_data:
        raise HTTPException(status_code=404, detail="No bill to finalize")
    
    # Optionally, you could add logic here to "lock" the session to prevent further edits
    return {"message": "Bill split finalized", "bill": bill_data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
