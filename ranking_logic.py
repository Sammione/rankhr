# from sentence_transformers import SentenceTransformer, util
import numpy as np
import re
from typing import List, Dict, Any

# Global variable for the model (lazy loaded)
_model = None

def get_model():
    """Lazy load the AI model to prevent startup timeouts"""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print("Loading AI model for the first time... this may take a moment.")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_util():
    """Lazy load the utility module"""
    from sentence_transformers import util
    return util

# Define skills and keywords for different role types
ROLE_SKILLS = {
    'tech': {
        'frontend': ['react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css', 'sass', 'scss', 'tailwind', 'bootstrap', 'next.js', 'vue.js', 'angular.js', 'frontend', 'front-end', 'ui', 'ux', 'responsive design', 'web development'],
        'backend': ['python', 'java', 'node.js', 'nodejs', 'express', 'django', 'flask', 'spring', 'spring boot', 'c#', 'net', 'php', 'laravel', 'ruby', 'rails', 'go', 'golang', 'rust', 'backend', 'server-side', 'api', 'rest', 'graphql', 'microservices'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'database', 'orm', 'nosql', 'database design', 'query optimization'],
        'devops': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins', 'gitlab', 'github actions', 'terraform', 'ansible', 'devops', 'cloud', 'deployment', 'monitoring'],
        'mobile': ['ios', 'android', 'react native', 'flutter', 'kotlin', 'swift', 'mobile development', 'mobile app'],
        'general_tech': ['git', 'github', 'gitlab', 'version control', 'agile', 'scrum', 'software engineering', 'programming', 'coding', 'debugging', 'testing', 'unit testing', 'integration testing']
    },
    'business': {
        'finance': ['accounting', 'finance', 'bookkeeping', 'tax', 'audit', 'payroll', 'financial analysis', 'budgeting', 'cost accounting', 'financial reporting', 'excel', 'erp', 'sap'],
        'management': ['management', 'project management', 'team leadership', 'strategic planning', 'operations', 'business analysis', 'process improvement', 'kpi', 'performance management'],
        'sales': ['sales', 'business development', 'client relations', 'negotiation', 'crm', 'salesforce', 'lead generation', 'pipeline management', 'revenue growth'],
        'marketing': ['marketing', 'digital marketing', 'social media', 'seo', 'content marketing', 'brand management', 'campaign management', 'analytics', 'google analytics', 'email marketing'],
        'hr': ['hr', 'human resources', 'recruitment', 'talent acquisition', 'employee relations', 'training', 'performance management', 'hr policies', 'compliance', 'onboarding']
    },
    'creative': {
        'design': ['graphic design', 'ui design', 'ux design', 'visual design', 'adobe creative suite', 'photoshop', 'illustrator', 'indesign', 'figma', 'sketch', 'prototyping'],
        'content': ['content creation', 'copywriting', 'content writing', 'blogging', 'video editing', 'photography', 'videography', 'content strategy', 'storytelling'],
        'media': ['social media', 'video production', 'animation', 'motion graphics', '3d modeling', 'after effects', 'premiere pro', 'media production']
    }
}

# Define role-specific irrelevant skills (skills that should be penalized for each role type)
ROLE_IRRELEVANT_SKILLS = {
    'tech': ['accounting', 'finance', 'bookkeeping', 'tax', 'audit', 'payroll', 'financial analysis', 'budgeting', 'cost accounting', 'management', 'hr', 'human resources', 'administration', 'secretarial', 'reception', 'customer service', 'sales', 'marketing', 'business development'],
    'business': ['react', 'vue', 'angular', 'javascript', 'python', 'java', 'node.js', 'c#', 'programming', 'coding', 'debugging', 'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp'],
    'creative': ['accounting', 'finance', 'programming', 'coding', 'debugging', 'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'react', 'vue', 'angular', 'javascript', 'python', 'java']
}

def detect_role_type(jd_text: str) -> str:
    """Detect the type of role from the job description"""
    jd_lower = jd_text.lower()
    
    # Keywords to identify role types
    tech_keywords = ['engineer', 'developer', 'software', 'programmer', 'tech', 'it', 'fullstack', 'full-stack', 'devops', 'data scientist', 'ml engineer', 'ai engineer', 'cloud engineer', 'systems', 'architect', 'cybersecurity', 'qa engineer', 'test engineer']
    business_keywords = ['manager', 'director', 'analyst', 'finance', 'accounting', 'accountant', 'audit', 'auditor', 'hr', 'human resources', 'sales', 'marketing', 'business development', 'operations', 'project manager', 'product manager', 'consultant', 'executive']
    creative_keywords = ['designer', 'graphic', 'ui/ux', 'ux/ui', 'visual', 'creative', 'content', 'copywriter', 'video editor', 'photographer', 'animator', 'illustrator', 'art director', 'multimedia']
    
    # Count keyword matches using word boundaries to avoid false positives (e.g., 'it' in 'auditing')
    def count_matches(keywords, text):
        count = 0
        for kw in keywords:
            # Use regex for whole word matching
            pattern = r'\b' + re.escape(kw.lower()) + r'\b'
            if re.search(pattern, text):
                count += 1
        return count

    tech_count = count_matches(tech_keywords, jd_lower)
    business_count = count_matches(business_keywords, jd_lower)
    creative_count = count_matches(creative_keywords, jd_lower)
    
    # Determine role type
    max_count = max(tech_count, business_count, creative_count)
    if max_count == 0:
        return 'general'  # Default for unknown roles
    
    if tech_count == max_count:
        return 'tech'
    elif business_count == max_count:
        return 'business'
    elif creative_count == max_count:
        return 'creative'
    
    return 'general'

def extract_role_keywords(text: str, role_type: str) -> Dict[str, List[str]]:
    """Extract keywords from text grouped by category based on role type"""
    text_lower = text.lower()
    found_skills = {}
    
    if role_type in ROLE_SKILLS:
        for category, skills in ROLE_SKILLS[role_type].items():
            found_skills[category] = [skill for skill in skills if skill in text_lower]
    
    return found_skills

def extract_irrelevant_keywords(text: str, role_type: str) -> List[str]:
    """Extract irrelevant keywords that should be penalized for the specific role type"""
    text_lower = text.lower()
    irrelevant = ROLE_IRRELEVANT_SKILLS.get(role_type, [])
    return [skill for skill in irrelevant if skill in text_lower]

def calculate_match_score(jd_text: str, cv_text: str) -> float:
    """Calculate a sophisticated match score that works for any role type"""
    # Detect role type from JD
    role_type = detect_role_type(jd_text)
    
    # Extract role-specific keywords
    jd_skills = extract_role_keywords(jd_text, role_type)
    cv_skills = extract_role_keywords(cv_text, role_type)
    
    # Extract irrelevant keywords for this role type
    cv_irrelevant_skills = extract_irrelevant_keywords(cv_text, role_type)
    
    # Base semantic similarity score (works for all role types)
    model = get_model()
    util = get_util()
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    base_score = float(util.cos_sim(jd_embedding, cv_embedding)[0][0])
    
    # Calculate skills match based on role type
    total_jd_skills = sum(len(skills) for skills in jd_skills.values())
    matched_skills = 0
    
    for category in jd_skills:
        if jd_skills[category]:  # If JD has skills in this category
            # Count how many of the JD's skills are present in CV
            matched_in_category = sum(1 for skill in jd_skills[category] if skill in cv_skills.get(category, []))
            matched_skills += matched_in_category
    
    # Skills bonus/penalty
    skills_bonus = 0
    if total_jd_skills > 0:
        skills_match_ratio = matched_skills / total_jd_skills
        skills_bonus = skills_match_ratio * 0.3  # Up to 30% bonus for perfect match
    
    # Irrelevant skills penalty (penalize skills not relevant to this role type)
    irrelevant_penalty = len(cv_irrelevant_skills) * 0.05  # 5% penalty per irrelevant skill
    
    # Final score calculation
    final_score = base_score + skills_bonus - irrelevant_penalty
    
    # Ensure score is between 0 and 1
    final_score = max(0, min(1, final_score))
    
    return final_score

def rank_cvs(jd_text, cv_list):
    """
    Ranks a list of CVs based on a Job Description with role-aware matching.
    Works for tech, business, creative, and general roles.
    cv_list should be a list of dictionaries: [{'id': 1, 'text': '...'}, ...]
    """
    # Detect role type for logging/debugging
    role_type = detect_role_type(jd_text)
    
    ranked_results = []
    
    for cv in cv_list:
        cv_text = cv.get('text', '')
        
        # Calculate role-aware match score
        score = calculate_match_score(jd_text, cv_text)
        score_percentage = round(score * 100, 2)
        
        # Determine match level with precision terminology
        match_level = f"{score_percentage}% Precision"
        
        # Internal descriptive label for logging or complex filtering if needed
        if score_percentage >= 80:
            label = "Excellent"
        elif score_percentage >= 60:
            label = "Good"
        elif score_percentage >= 40:
            label = "Moderate"
        elif score_percentage >= 20:
            label = "Poor"
        else:
            label = "Not Suitable"
        
        ranked_results.append({
            "applicant_id": cv.get('id'),
            "name": cv.get('name', 'Unknown'),
            "score": score_percentage,
            "match_level": match_level,
            "precision_label": label,  # Added extra label for internal use
            "role_type": role_type
        })
    
    # Sort by score descending
    return sorted(ranked_results, key=lambda x: x['score'], reverse=True)
