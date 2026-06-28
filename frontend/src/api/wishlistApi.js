import axios from "axios";

const WISHLIST_API =
  axios.create({
    baseURL:
      import.meta.env.VITE_API_URL
  });

export default WISHLIST_API;