
from pydantic import BaseModel


class Restaurant(BaseModel):
    id : str
    avgRating : int
    category : str
    city : str
    name : str
    numRatings: str
    photo : str
    price : int

class RestaurantResponse(BaseModel):
    data : Restaurant

class RestaurantDocument(BaseModel):
    id : str
    data : Restaurant
       
class RestaurantsResponse(BaseModel):
    data : list[Restaurant]
