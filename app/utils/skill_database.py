"""Skill database and matching utilities."""

from typing import List, Set
import re


class SkillDatabase:
    """Database of technical skills for matching."""
    
    PROGRAMMING_LANGUAGES = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
        'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl',
        'php', 'objective-c', 'dart', 'lua', 'haskell', 'clojure', 'elixir',
        'c', 'cpp', 'csharp', 'js', 'ts', 'py', 'rb', 'rs', 'kt', 'html',
        'css', 'sql', 'bash', 'shell', 'powershell', 'vba', 'assembly'
    }
    
    FRAMEWORKS = {
        'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'express',
        'spring', 'springboot', 'rails', 'laravel', 'asp.net', '.net',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'nodejs', 'nextjs', 'gatsby', 'svelte', 'ember', 'backbone',
        'jquery', 'bootstrap', 'tailwind', 'material-ui', 'mui', 'ant-design'
    }
    
    DATABASES = {
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
        'oracle', 'sqlserver', 'sqlite', 'dynamodb', 'firebase', 'firestore',
        'neo4j', 'couchdb', 'mariadb', 'influxdb', 'clickhouse'
    }
    
    CLOUD_PLATFORMS = {
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
        'linode', 'vercel', 'netlify', 'cloudflare', 'oracle cloud', 'ibm cloud'
    }
    
    DEVOPS_TOOLS = {
        'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'bitbucket',
        'terraform', 'ansible', 'puppet', 'chef', 'circleci', 'travis', 'github actions',
        'prometheus', 'grafana', 'elk', 'nginx', 'apache', 'tomcat', 'jira',
        'confluence', 'slack', 'datadog', 'newrelic', 'sentry'
    }
    
    DATA_SCIENCE = {
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'data analysis',
        'data science', 'statistics', 'data visualization', 'big data', 'spark',
        'hadoop', 'kafka', 'airflow', 'tableau', 'power bi', 'looker', 'etl',
        'data engineering', 'ml', 'ai', 'artificial intelligence', 'neural networks'
    }
    
    MOBILE = {
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
        'swift', 'swiftui', 'kotlin', 'java', 'cordova', 'phonegap'
    }
    
    @classmethod
    def get_all_skills(cls) -> Set[str]:
        """Get all skills from the database."""
        all_skills = set()
        all_skills.update(cls.PROGRAMMING_LANGUAGES)
        all_skills.update(cls.FRAMEWORKS)
        all_skills.update(cls.DATABASES)
        all_skills.update(cls.CLOUD_PLATFORMS)
        all_skills.update(cls.DEVOPS_TOOLS)
        all_skills.update(cls.DATA_SCIENCE)
        all_skills.update(cls.MOBILE)
        return all_skills
    
    @classmethod
    def normalize_skill(cls, skill: str) -> str:
        """Normalize skill name for matching."""
        skill = skill.lower().strip()
        # Remove special characters except for #, +, -, .
        skill = re.sub(r'[^a-z0-9#+\-.\s]', '', skill)
        # Replace common variations
        replacements = {
            'node.js': 'nodejs',
            'node js': 'nodejs',
            'react.js': 'react',
            'vue.js': 'vue',
            'angular.js': 'angular',
            'aspnet': 'asp.net',
            'asp net': 'asp.net',
            'c sharp': 'c#',
            'c plus plus': 'c++',
            'cpp': 'c++',
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine learning',
            'ai': 'artificial intelligence'
        }
        for old, new in replacements.items():
            if skill == old:
                skill = new
        return skill
