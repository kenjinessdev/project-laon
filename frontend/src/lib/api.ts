import axios from "axios";

const api = axios.create({
  // change this to BACKEND_URL if data is already present. else use placeholder MOCKAPI_URL
  baseURL: process.env.MOCKAPI_URL,
});

export default api;
