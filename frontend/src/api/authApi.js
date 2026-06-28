import axios from "axios";

const AUTH_API = axios.create({
  baseURL:
    "http://import.meta.env.VITE_API_URL/api"
});

export default AUTH_API;