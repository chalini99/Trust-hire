"use client";

import { Card } from "@/components/ui/card";
import TrustMeter from "./TrustMeter";
import SkillChart from "./SkillChart";
import { Badge } from "@/components/ui/badge";

export default function ResultDashboard({ result }: any) {
  if (!result) return null;

  return (
    <Card className="p-6 mt-6">
      <h2 className="text-2xl font-bold">
        AI Verification Result
      </h2>

      <div className="mt-3">
        <Badge variant="secondary">
          Risk Level: {result.risk_level}
        </Badge>
      </div>

      <TrustMeter score={result.trust_score} />

      <p className="mt-4 text-sm">
        Match Percentage: {result.match_percentage}%
      </p>

      <SkillChart skills={result.resume_skills} />
    </Card>
  );
}