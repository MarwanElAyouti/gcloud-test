import axios from "axios"
import { API_ENDPOINT } from "./endpoints"
import { FiltersType } from "./types"

export const fetchRestaurant =  async (id:any) => 
    await axios.get(`${API_ENDPOINT}/restaurants/${id}`).then((response:any) => response.data)

export const fetchRestaurants =  async (filters:FiltersType) => {
    let path = `${API_ENDPOINT}/restaurants?`
    if (Object.keys(filters).length > 0) {
        for (const [key, value] of Object.entries(filters)) {
            if (value && key != "price") path += `${key}=${value}&`
            else if (value && key == "price") path += `${key}=${value.length}&`
        }
    }
    return await axios.get(path).then((response:any) => response.data)    
} 
    
export const fetchReviews = async (id:any) => 
    await axios.get(`${API_ENDPOINT}/ratings/${id}`).then((response:any) => response.data)

export const postReview = async (id:any, review:any) =>
    await axios.post(`${API_ENDPOINT}/ratings/${id}/add_rating`, review).then((response:any) => response.data)
