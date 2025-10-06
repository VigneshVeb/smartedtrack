// src/context/AuthProvider.tsx
import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  id: number;
  username: string;
  email?: string;
  role?: string;
  // add other fields you expect
}

interface AuthContextType {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // hydrate from localStorage on mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem("user");
      if (raw) {
        setUser(JSON.parse(raw));
      }
    } catch (e) {
      console.warn("Failed to parse stored user", e);
      localStorage.removeItem("user");
    }
  }, []);

  // persist user to localStorage
  useEffect(() => {
    if (user) localStorage.setItem("user", JSON.stringify(user));
    else localStorage.removeItem("user");
  }, [user]);

  const logout = () => {
    // Clear local state and localStorage; also optionally call backend logout endpoint
    localStorage.removeItem("user");
    setUser(null);
    // If you have a /logout/ endpoint that clears session cookie, optionally call it here.
  };

  return <AuthContext.Provider value={{ user, setUser, logout }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
