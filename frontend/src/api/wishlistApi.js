import axios from "axios";

const WISHLIST_API =
  axios.create({
    baseURL:
      "http://import.meta.env.VITE_API_URL/api"
  });

export default WISHLIST_API;