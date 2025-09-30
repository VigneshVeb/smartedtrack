import React, { useState } from "react";
import apiClient from "../utils/apiClient";
import { useAuth } from "../context/AuthProvider";

const AttendancePage: React.FC = () => {
  const { user } = useAuth();
  const [studentId, setStudentId] = useState("");
  const [date, setDate] = useState("");
  const [status, setStatus] = useState("present");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await apiClient.post(
        "/students/mark-attendance/",
        {
          student_id: studentId,
          date: date,
          status: status,
        }
      );

      setMessage("✅ Attendance marked successfully!");
    } catch (err: any) {
      console.error(err);
      setMessage("❌ Failed to mark attendance.");
    }
  };

  return (
    <div>
      <h1>Attendance</h1>
      <p>Logged in as: {user?.username}</p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        />
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="present">Present</option>
          <option value="absent">Absent</option>
        </select>
        <button type="submit">Mark Attendance</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AttendancePage;
