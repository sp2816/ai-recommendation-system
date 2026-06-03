import axios from "axios";

const WISHLIST_API =
  axios.create({
    baseURL:
      "http://127.0.0.1:8000/api"
  });

export default WISHLIST_API;