
from pydantic import BaseModel


class AddRestaurant(BaseModel):
    avgRating : int = 0
    category : str
    city : str
    name : str
    numRatings: int = 0
    photo : str
    price : int

class Restaurant(AddRestaurant):
   id: str
