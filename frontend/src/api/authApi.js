import axios from "axios";

const AUTH_API = axios.create({
  baseURL:
    "http://127.0.0.1:8000/api"
});

export default AUTH_API;