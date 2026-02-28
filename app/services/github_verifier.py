"""GitHub verification service."""

import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.config import settings
from app.utils.skill_database import SkillDatabase


class GitHubVerifier:
    """Verify skills through GitHub profile analysis."""
    
    def __init__(self):
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if settings.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {settings.GITHUB_TOKEN}'
        self.skill_db = SkillDatabase()
    
    async def verify_user(self, username: str) -> Dict[str, Any]:
        """Fetch and analyze GitHub user profile."""
        async with aiohttp.ClientSession() as session:
            # Fetch user profile
            user_data = await self._fetch_user(session, username)
            if not user_data:
                raise ValueError(f"GitHub user '{username}' not found")
            
            # Fetch repositories
            repos = await self._fetch_repositories(session, username)
            
            # Extract languages and skills
            languages = await self._extract_languages(session, repos)
            skills = self._analyze_skills(repos, languages)
            
            # Calculate statistics
            stats = self._calculate_stats(user_data, repos, languages)
            
            return {
                'user': {
                    'username': user_data.get('login'),
                    'name': user_data.get('name'),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'created_at': user_data.get('created_at'),
                },
                'languages': languages,
                'skills': skills,
                'stats': stats,
                'repositories': [
                    {
                        'name': repo['name'],
                        'description': repo.get('description'),
                        'language': repo.get('language'),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                    }
                    for repo in repos[:10]  # Top 10 repos
                ]
            }
    
    async def _fetch_user(self, session: aiohttp.ClientSession, username: str) -> Optional[Dict]:
        """Fetch GitHub user data."""
        url = f"{self.base_url}/users/{username}"
        try:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    raise Exception(f"GitHub API error: {response.status}")
        except Exception as e:
            raise Exception(f"Failed to fetch GitHub user: {str(e)}")
    
    async def _fetch_repositories(self, session: aiohttp.ClientSession, username: str) -> List[Dict]:
        """Fetch user's repositories."""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.base_url}/users/{username}/repos"
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated',
                'direction': 'desc'
            }
            
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        batch = await response.json()
                        if not batch:
                            break
                        repos.extend(batch)
                        if len(batch) < per_page:
                            break
                        page += 1
                        # Limit to 300 repos to avoid rate limiting
                        if len(repos) >= 300:
                            break
                    else:
                        break
            except Exception as e:
                break
        
        return repos
    
    async def _extract_languages(self, session: aiohttp.ClientSession, repos: List[Dict]) -> Dict[str, int]:
        """Extract programming languages from repositories."""
        languages = {}
        
        # Collect languages from repo primary language
        for repo in repos:
            if repo.get('language'):
                lang = repo['language'].lower()
                languages[lang] = languages.get(lang, 0) + 1
        
        # For top 10 repos, fetch detailed language stats
        top_repos = sorted(
            repos, 
            key=lambda x: x.get('stargazers_count', 0) + x.get('forks_count', 0), 
            reverse=True
        )[:10]
        
        for repo in top_repos:
            url = f"{self.base_url}/repos/{repo['owner']['login']}/{repo['name']}/languages"
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        lang_data = await response.json()
                        for lang, bytes_count in lang_data.items():
                            lang_lower = lang.lower()
                            # Weight by bytes of code
                            weight = min(bytes_count / 10000, 10)  # Cap at 10
                            languages[lang_lower] = languages.get(lang_lower, 0) + weight
            except:
                continue
        
        return languages
    
    def _analyze_skills(self, repos: List[Dict], languages: Dict[str, int]) -> List[str]:
        """Analyze and extract skills from repositories."""
        skills = set()
        
        # Add programming languages
        for lang in languages.keys():
            normalized = self.skill_db.normalize_skill(lang)
            if normalized in self.skill_db.get_all_skills():
                skills.add(normalized)
            # Also add the original language
            skills.add(lang)
        
        # Analyze repository names and descriptions for frameworks/tools
        for repo in repos:
            # Check repo name
            repo_name = repo.get('name', '').lower()
            description = (repo.get('description') or '').lower()
            
            # Check for known skills in repo name and description
            for skill in self.skill_db.get_all_skills():
                if skill in repo_name or skill in description:
                    skills.add(skill)
            
            # Check for specific patterns
            patterns = {
                'docker': ['docker', 'containerized', 'dockerfile'],
                'kubernetes': ['k8s', 'kubernetes', 'kubectl'],
                'react': ['react', 'jsx', 'next.js', 'nextjs', 'gatsby'],
                'vue': ['vue', 'nuxt', 'vuex'],
                'angular': ['angular', 'ng-', 'ngrx'],
                'django': ['django'],
                'flask': ['flask'],
                'fastapi': ['fastapi', 'fast-api'],
                'spring': ['spring', 'springboot', 'spring-boot'],
                'aws': ['aws', 'amazon', 's3', 'ec2', 'lambda'],
                'machine learning': ['ml', 'machine-learning', 'tensorflow', 'pytorch', 'scikit'],
                'data science': ['data-science', 'pandas', 'numpy', 'jupyter'],
            }
            
            for skill, keywords in patterns.items():
                if any(kw in repo_name or kw in description for kw in keywords):
                    skills.add(skill)
        
        return sorted(list(skills))
    
    def _calculate_stats(self, user_data: Dict, repos: List[Dict], languages: Dict) -> Dict:
        """Calculate GitHub statistics."""
        # Repository stats
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        
        # Activity stats
        recent_repos = 0
        six_months_ago = datetime.now() - timedelta(days=180)
        for repo in repos:
            updated_at = repo.get('updated_at', '')
            if updated_at:
                try:
                    updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                    if updated_date > six_months_ago:
                        recent_repos += 1
                except:
                    pass
        
        # Language diversity
        language_count = len(languages)
        
        # Calculate account age in years
        account_age = 0
        if user_data.get('created_at'):
            try:
                created_date = datetime.fromisoformat(
                    user_data['created_at'].replace('Z', '+00:00')
                )
                account_age = (datetime.now() - created_date).days / 365
            except:
                pass
        
        return {
            'total_repos': len(repos),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'recent_activity': recent_repos,
            'language_diversity': language_count,
            'account_age_years': round(account_age, 1),
            'avg_stars_per_repo': round(total_stars / max(len(repos), 1), 2),
            'has_popular_repos': any(repo.get('stargazers_count', 0) > 50 for repo in repos),
        }
