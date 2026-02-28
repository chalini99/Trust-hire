"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ResultDashboard from "@/components/ResultDashboard";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-3xl font-bold mb-6">
        TrustHire AI Resume Verification
      </h1>

      <UploadForm setResult={setResult} />
      <ResultDashboard result={result} />
    </div>
  );
}