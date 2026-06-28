import axios from "axios";

const API = axios.create({
  baseURL:
    "http://import.meta.env.VITE_API_URL"
});

export default API;