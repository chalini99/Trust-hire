"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function SkillChart({ skills }: { skills?: string[] }) {
  // ✅ Fix: handle undefined skills
  if (!skills || skills.length === 0) {
    return <p className="mt-4 text-gray-500">No skills available</p>;
  }

  const data = skills.map((skill) => ({
    name: skill,
    value: 1,
  }));

  return (
    <div className="h-64 mt-6">
      <h3 className="font-semibold text-lg mb-2">Resume Skills</h3>

      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}