import axios from "axios";

// Set global defaults
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

// Create a custom instance
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000", // Django API base URL
  withCredentials: true,
// ensures cookies are sent
});
axios.defaults.withCredentials = true;

// Optional: manually add CSRF token if needed
apiClient.interceptors.request.use((config) => {
  const csrfToken = getCookie("csrftoken");
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});

// Helper function to read cookies
function getCookie(name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift();
  return null;
}

export default apiClient;
