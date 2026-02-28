"""Scoring engine for trust and risk assessment."""

from typing import List, Dict, Tuple
from app.models.response import RiskLevel


class ScoringEngine:
    """Calculate trust scores and risk levels."""
    
    def calculate_match_score(
        self,
        resume_skills: List[str],
        github_skills: List[str]
    ) -> Tuple[List[Dict], float]:
        """Calculate skill match score."""
        matched_skills = []
        resume_skills_lower = {skill.lower() for skill in resume_skills}
        github_skills_lower = {skill.lower() for skill in github_skills}
        
        for skill in resume_skills:
            skill_lower = skill.lower()
            found = skill_lower in github_skills_lower
            
            # Check for similar skills
            confidence = 1.0 if found else 0.0
            github_projects = []
            
            if found:
                github_projects = [
                    gs for gs in github_skills 
                    if gs.lower() == skill_lower
                ]
            else:
                # Check for partial matches
                for gs in github_skills_lower:
                    if skill_lower in gs or gs in skill_lower:
                        confidence = 0.5
                        github_projects.append(gs)
                        break
            
            matched_skills.append({
                'skill': skill,
                'found_in_github': found or confidence > 0,
                'confidence': confidence,
                'github_projects': github_projects[:3]  # Top 3 related projects
            })
        
        # Calculate match percentage
        if not resume_skills:
            match_percentage = 0.0
        else:
            matched_count = sum(
                1 for m in matched_skills 
                if m['found_in_github'] or m['confidence'] > 0
            )
            match_percentage = (matched_count / len(resume_skills)) * 100
        
        return matched_skills, match_percentage
    
    def calculate_trust_score(
        self,
        match_percentage: float,
        github_stats: Dict,
        resume_skill_count: int,
        github_skill_count: int
    ) -> float:
        """Calculate overall trust score."""
        # Base score from skill match
        base_score = match_percentage * 0.5  # 50% weight
        
        # GitHub activity score (20% weight)
        activity_score = 0
        if github_stats.get('total_repos', 0) > 0:
            activity_score += min(github_stats['total_repos'] / 50, 1) * 5
        if github_stats.get('recent_activity', 0) > 0:
            activity_score += min(github_stats['recent_activity'] / 10, 1) * 5
        if github_stats.get('total_stars', 0) > 0:
            activity_score += min(github_stats['total_stars'] / 100, 1) * 5
        if github_stats.get('has_popular_repos'):
            activity_score += 5
        
        # Account credibility (15% weight)
        credibility_score = 0
        if github_stats.get('account_age_years', 0) > 1:
            credibility_score += min(github_stats['account_age_years'] / 5, 1) * 10
        if github_stats.get('language_diversity', 0) > 3:
            credibility_score += 5
        
        # Skill depth score (15% weight)
        skill_depth_score = 0
        if github_skill_count > 0:
            if github_skill_count >= resume_skill_count * 0.7:
                skill_depth_score = 15
            elif github_skill_count >= resume_skill_count * 0.5:
                skill_depth_score = 10
            elif github_skill_count >= resume_skill_count * 0.3:
                skill_depth_score = 5
        
        # Final trust score
        trust_score = base_score + activity_score + credibility_score + skill_depth_score
        
        # Normalize to 0-100
        return min(max(trust_score, 0), 100)
    
    def determine_risk_level(self, trust_score: float, match_percentage: float) -> RiskLevel:
        """Determine risk level based on scores."""
        if trust_score >= 75 and match_percentage >= 70:
            return RiskLevel.LOW
        elif trust_score >= 50 and match_percentage >= 40:
            return RiskLevel.MEDIUM
        elif trust_score >= 30 or match_percentage >= 30:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def generate_recommendations(
        self,
        trust_score: float,
        match_percentage: float,
        github_stats: Dict,
        unmatched_skills: List[str]
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        if trust_score < 50:
            recommendations.append("⚠️ Low trust score detected. Further verification recommended.")
        
        if match_percentage < 40:
            recommendations.append("📊 Low skill match percentage. Consider technical assessment.")
        
        if github_stats.get('total_repos', 0) < 5:
            recommendations.append("📁 Limited GitHub activity. Request additional portfolio items.")
        
        if github_stats.get('recent_activity', 0) < 2:
            recommendations.append("📅 No recent GitHub activity. Verify current skill proficiency.")
        
        if len(unmatched_skills) > 5:
            unmatched_sample = ', '.join(unmatched_skills[:5])
            recommendations.append(
                f"🔍 Several claimed skills not found on GitHub: {unmatched_sample}. "
                "Recommend skill-specific assessment."
            )
        
        if not github_stats.get('has_popular_repos'):
            recommendations.append("⭐ No popular repositories found. Consider code review.")
        
        if github_stats.get('account_age_years', 0) < 1:
            recommendations.append("🆕 New GitHub account. Additional verification suggested.")
        
        if trust_score >= 75 and match_percentage >= 70:
            recommendations.append("✅ Strong profile match. Candidate shows good technical credibility.")
        
        if not recommendations:
            recommendations.append("ℹ️ Profile analysis complete. Proceed with standard evaluation.")
        
        return recommendations
