import axios from "axios"
import { API_ENDPOINT } from "./endpoints"

export const fetchRestaurant =  async (id:any) =>
    await axios.get(`${API_ENDPOINT}/restaurants/${id}`).then((response:any) => response.data)

export const fetchReviews = async (id:any) =>
    await axios.get(`${API_ENDPOINT}/ratings/${id}`).then((response:any) => response.data)

export const postReview = async (id:any, review:any) =>
    await axios.post(`${API_ENDPOINT}/ratings/${id}/add_rating`, review).then((response:any) => response.data)
