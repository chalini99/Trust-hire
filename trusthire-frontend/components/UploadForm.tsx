"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function UploadForm({ setResult }: any) {
  const [file, setFile] = useState<File | null>(null);
  const [github, setGithub] = useState("");

  const handleSubmit = async () => {
    if (!file || !github) return;

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("github_username", github);

    const res = await fetch(
      "http://127.0.0.1:8000/api/v1/verify",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-4">
        Upload Resume
      </h2>

      <Input
        type="file"
        onChange={(e) =>
          setFile(e.target.files?.[0] || null)
        }
      />

      <Input
        placeholder="GitHub username"
        className="mt-3"
        value={github}
        onChange={(e) => setGithub(e.target.value)}
      />

      <Button
        className="mt-4 w-full"
        onClick={handleSubmit}
      >
        Verify Resume
      </Button>
    </div>
  );
}