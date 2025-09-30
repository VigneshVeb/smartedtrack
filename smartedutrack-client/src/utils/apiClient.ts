import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000", // backend root
  withCredentials: true, // ✅ important for Django session cookie
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
