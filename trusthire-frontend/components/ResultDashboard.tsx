"use client";

import { Card } from "@/components/ui/card";
import TrustMeter from "./TrustMeter";
import { Badge } from "@/components/ui/badge";
import { useEffect, useState } from "react";
import { getInterviewQuestions } from "@/services/interview";

export default function ResultDashboard({ result }: any) {
  // ✅ Hooks must always be at top
  const [questions, setQuestions] = useState<string[]>([]);

  // Safe fallback
  const matchPercentage = Number(result?.match_percentage || 0);

  // Verified and fake skills
  const verified =
    result?.matched_skills
      ?.filter((s: any) => s.found_in_github)
      .map((s: any) => s.skill) || [];

  const fake =
    result?.matched_skills
      ?.filter((s: any) => !s.found_in_github)
      .map((s: any) => s.skill) || [];

  // Risk color
  const riskColor =
    result?.risk_level === "LOW"
      ? "bg-green-500"
      : result?.risk_level === "MEDIUM"
      ? "bg-yellow-500"
      : "bg-red-500";

  // Fetch AI questions
  useEffect(() => {
    if (verified.length > 0) {
      getInterviewQuestions(verified).then((res) => {
        if (res?.questions) {
          setQuestions(res.questions);
        }
      });
    }
  }, [result]);

  // Now safe conditional render
  if (!result) return null;

  return (
    <Card className="p-6 mt-6">
      <h2 className="text-2xl font-bold">AI Resume Verification</h2>

      {/* Risk */}
      <div className="mt-3">
        <Badge className={`${riskColor} text-white`}>
          Risk: {result.risk_level}
        </Badge>
      </div>

      {/* Trust */}
      <TrustMeter score={result.trust_score || 0} />

      <p className="mt-4">
        Match: {matchPercentage.toFixed(2)}%
      </p>

      {/* Verified */}
      <div className="mt-6">
        <h3 className="font-bold text-green-600">
          ✔ Verified Skills
        </h3>
        <div className="flex flex-wrap gap-2 mt-2">
          {verified.map((s: string) => (
            <Badge key={s} className="bg-green-600 text-white">
              {s}
            </Badge>
          ))}
        </div>
      </div>

      {/* Fake */}
      <div className="mt-6">
        <h3 className="font-bold text-red-600">
          ❌ Unverified Skills
        </h3>
        <div className="flex flex-wrap gap-2 mt-2">
          {fake.map((s: string) => (
            <Badge key={s} className="bg-red-600 text-white">
              {s}
            </Badge>
          ))}
        </div>
      </div>

      {/* AI Interview */}
      <div className="mt-6">
        <h3 className="font-bold text-blue-600">
          🤖 AI Interview Questions
        </h3>

        {questions.length > 0 ? (
          <ul className="mt-2 space-y-2">
            {questions.map((q, i) => (
              <li key={i} className="bg-gray-100 p-2 rounded">
                {q}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 mt-2">
            Generating questions...
          </p>
        )}
      </div>
    </Card>
  );
}