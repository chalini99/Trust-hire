"use client";

import { Progress } from "@/components/ui/progress";

export default function TrustMeter({ score }: { score: number }) {
  return (
    <div className="mt-4">
      <h3 className="font-semibold text-lg">Trust Score</h3>
      <Progress value={score} className="h-4 mt-2" />
      <p className="text-sm mt-1">{score}%</p>
    </div>
  );
}