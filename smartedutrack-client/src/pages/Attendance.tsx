import React, { useEffect, useState } from "react";
import apiClient from "../api/apiClient";

interface Student {
  id: number;
  name: string;
}

const Attendance: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [attendance, setAttendance] = useState<Record<number, string>>({});

  useEffect(() => {
    apiClient.get("/students/").then((res) => setStudents(res.data));
  }, []);

  const handleMark = (id: number, status: string) => {
    setAttendance({ ...attendance, [id]: status });
  };

  const handleSubmit = async () => {
    const payload = Object.entries(attendance).map(([student_id, status]) => ({
      student_id,
      status,
      date: new Date().toISOString().split("T")[0],
    }));

    await apiClient.post("/students/mark-attendance/", payload);
    alert("Attendance submitted!");
  };

  return (
    <div>
      <h2>Attendance</h2>
      <table>
        <thead>
          <tr>
            <th>Student</th>
            <th>Present</th>
            <th>Absent</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td>{s.name}</td>
              <td>
                <input
                  type="radio"
                  name={`att_${s.id}`}
                  onChange={() => handleMark(s.id, "present")}
                />
              </td>
              <td>
                <input
                  type="radio"
                  name={`att_${s.id}`}
                  onChange={() => handleMark(s.id, "absent")}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSubmit}>Submit Attendance</button>
    </div>
  );
};

export default Attendance;
