from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from google.cloud.firestore import Query

from friendlyeats.db import db
from friendlyeats.schemas import Rating

router = APIRouter()


@router.get("/ratings/{id}")
async def get_ratings(id: str) -> list[Rating]:
    try:
        # Fetch the ratings data from Firestore for the given restaurant id
        doc_ref = db.collection("restaurants").document(id).collection("ratings")
        ratings = doc_ref.order_by("timestamp", direction=Query.DESCENDING).get()
        # Convert Firestore QuerySnapshot to a list of dictionaries
        ratings_data = [doc.to_dict() for doc in ratings]
        return ratings_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/ratings/{restaurant_id}/add_rating", status_code=status.HTTP_201_CREATED)
async def add_rating(restaurant_id: str, rating: Rating):
    # Get restaurant document reference
    restaurant_ref = db.collection("restaurants").document(restaurant_id)
    rating_collection_ref = restaurant_ref.collection("ratings")

    # Check if the restaurant document exists
    restaurant_snapshot = restaurant_ref.get()
    if not restaurant_snapshot.exists:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant_data = restaurant_snapshot.to_dict()

    # Start a transaction to update the restaurant data and add the new rating
    with db.transaction() as transaction:
        # Calculate the new average rating
        num_ratings = restaurant_data.get("numRatings", 0)
        avg_rating = restaurant_data.get("avgRating", 0)
        new_average = (num_ratings * avg_rating + rating.rating) / (num_ratings + 1)

        # Update the restaurant document
        transaction.update(
            restaurant_ref,
            {
                "numRatings": num_ratings + 1,
                "avgRating": new_average,
            },
        )

        # Add the new rating to the ratings collection
        rating.userId = "123456789"  # Assign random uid for now
        rating_collection_ref.document().set(rating.dict())

    return {"message": "Review added successfully", "restaurant_id": restaurant_id}
