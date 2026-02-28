export interface VerificationResult {
  trust_score: number;
  risk_level: string;
  resume_skills: string[];
  github_skills: string[];
  match_percentage: number;
}