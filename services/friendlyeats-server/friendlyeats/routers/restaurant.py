from typing import Optional

from fastapi import APIRouter
from google.cloud.firestore import Query
from google.cloud.firestore_v1.base_query import BaseCompositeFilter, FieldFilter

from friendlyeats.db import db
from friendlyeats.schemas import AddRestaurant, Restaurant

router = APIRouter()


@router.get("/restaurants/{id}")
async def get_restaurant(id: str) -> Restaurant:
    # Query restaurants collection by restaurant id
    query = db.collection("restaurants").document(id)
    snapshot = query.get()
    return snapshot.to_dict()


@router.get("/restaurants")
async def get_all_restaurants(
    category: Optional[str] = None,
    city: Optional[str] = None,
    price: Optional[int] = None,
    sort: Optional[str] = "Rating",
) -> list[Restaurant]:
    QUERY_LIMIT = 50
    filters = []
    # Query restaurants collection
    query = db.collection("restaurants")

    # Apply filters
    if category:
        filters.append(["category", "==", category])
    if city:
        filters.append(["city", "==", city])
    if price:
        filters.append(["price", "==", price])

    query = query.where(filter=BaseCompositeFilter("AND", [FieldFilter(*_c) for _c in filters]))

    # Set sorting column
    if sort:
        if sort == "Review":
            query = query.order_by("numRatings", direction=Query.DESCENDING).limit(QUERY_LIMIT)
        else:
            query = query.order_by("avgRating", direction=Query.DESCENDING).limit(QUERY_LIMIT)

    snapshot = query.get()

    if not snapshot:
        return []

    return [Restaurant(id=doc.id, **doc.to_dict()) for doc in snapshot]


@router.post("/restaurants")
async def add_restaurant(restaurant: AddRestaurant):
    # Get restaurant collection
    restaurant_collection = db.collection("restaurants")
    # Add restaurant
    restaurant_collection.add(restaurant.dict())
