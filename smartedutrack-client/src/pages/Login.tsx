// src/pages/Login.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../utils/apiClient";
import { useAuth } from "../context/AuthProvider";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setUser } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await apiClient.post("/accounts/login/", { username, password }, { withCredentials: true });
      // If backend returns user details in res.data.user
      if (res.data && res.data.user) {
        setUser(res.data.user);
        // localStorage persistence handled in AuthProvider
        navigate("/attendance");
      } else {
        // maybe your backend returns the user object directly
        setUser(res.data);
        navigate("/attendance");
      }
    } catch (err: any) {
      console.error("Login failed:", err.response?.data || err.message);
      setError("Invalid credentials or server error");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "60px auto", padding: 20 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <div style={{ marginTop: 12 }}>
          <button type="submit">Login</button>
        </div>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Login;
