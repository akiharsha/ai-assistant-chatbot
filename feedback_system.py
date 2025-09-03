"""
User Feedback Collection and Analysis System for IndicSahayak
Handles collection, storage, and analysis of user feedback
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
from dataclasses import dataclass, asdict
import uuid

@dataclass
class UserFeedback:
    """Data class for user feedback"""
    feedback_id: str
    user_id: str
    timestamp: str
    rating: int  # 1-5 scale
    language_used: str
    interaction_type: str  # "translation", "learning", "general", "cultural"
    comments: str
    response_quality: int  # 1-5 scale
    cultural_sensitivity: int  # 1-5 scale
    language_accuracy: int  # 1-5 scale
    helpfulness: int  # 1-5 scale
    response_speed: int  # 1-5 scale
    user_satisfaction: int  # 1-5 scale
    would_recommend: bool
    improvement_suggestions: str
    technical_issues: str

class FeedbackCollector:
    """Collects and manages user feedback"""
    
    def __init__(self, storage_file: str = "feedback_data.json"):
        self.storage_file = storage_file
        self.feedback_data: List[UserFeedback] = []
        self.load_feedback_data()
    
    def load_feedback_data(self):
        """Load existing feedback data from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.feedback_data = [UserFeedback(**item) for item in data]
            except Exception as e:
                print(f"Error loading feedback data: {e}")
                self.feedback_data = []
    
    def save_feedback_data(self):
        """Save feedback data to file"""
        try:
            data = [asdict(feedback) for feedback in self.feedback_data]
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving feedback data: {e}")
    
    def add_feedback(self, feedback: UserFeedback):
        """Add new feedback"""
        self.feedback_data.append(feedback)
        self.save_feedback_data()
    
    def create_feedback(
        self,
        user_id: str,
        rating: int,
        language_used: str,
        interaction_type: str,
        comments: str,
        response_quality: int = 5,
        cultural_sensitivity: int = 5,
        language_accuracy: int = 5,
        helpfulness: int = 5,
        response_speed: int = 5,
        user_satisfaction: int = 5,
        would_recommend: bool = True,
        improvement_suggestions: str = "",
        technical_issues: str = ""
    ) -> UserFeedback:
        """Create a new feedback entry"""
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            rating=rating,
            language_used=language_used,
            interaction_type=interaction_type,
            comments=comments,
            response_quality=response_quality,
            cultural_sensitivity=cultural_sensitivity,
            language_accuracy=language_accuracy,
            helpfulness=helpfulness,
            response_speed=response_speed,
            user_satisfaction=user_satisfaction,
            would_recommend=would_recommend,
            improvement_suggestions=improvement_suggestions,
            technical_issues=technical_issues
        )
        self.add_feedback(feedback)
        return feedback
    
    def get_feedback_by_user(self, user_id: str) -> List[UserFeedback]:
        """Get all feedback from a specific user"""
        return [f for f in self.feedback_data if f.user_id == user_id]
    
    def get_feedback_by_language(self, language: str) -> List[UserFeedback]:
        """Get all feedback for a specific language"""
        return [f for f in self.feedback_data if f.language_used == language]
    
    def get_recent_feedback(self, days: int = 7) -> List[UserFeedback]:
        """Get feedback from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            f for f in self.feedback_data 
            if datetime.fromisoformat(f.timestamp) >= cutoff_date
        ]

class FeedbackAnalyzer:
    """Analyzes user feedback and generates insights"""
    
    def __init__(self, feedback_collector: FeedbackCollector):
        self.feedback_collector = feedback_collector
    
    def get_overall_metrics(self) -> Dict[str, Any]:
        """Get overall feedback metrics"""
        if not self.feedback_collector.feedback_data:
            return {"total_feedback": 0}
        
        feedback_data = self.feedback_collector.feedback_data
        
        # Calculate averages
        metrics = {
            "total_feedback": len(feedback_data),
            "average_rating": sum(f.rating for f in feedback_data) / len(feedback_data),
            "average_response_quality": sum(f.response_quality for f in feedback_data) / len(feedback_data),
            "average_cultural_sensitivity": sum(f.cultural_sensitivity for f in feedback_data) / len(feedback_data),
            "average_language_accuracy": sum(f.language_accuracy for f in feedback_data) / len(feedback_data),
            "average_helpfulness": sum(f.helpfulness for f in feedback_data) / len(feedback_data),
            "average_response_speed": sum(f.response_speed for f in feedback_data) / len(feedback_data),
            "average_user_satisfaction": sum(f.user_satisfaction for f in feedback_data) / len(feedback_data),
            "recommendation_rate": sum(f.would_recommend for f in feedback_data) / len(feedback_data) * 100
        }
        
        return metrics
    
    def get_language_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get feedback breakdown by language"""
        language_metrics = {}
        
        for language in ["Hindi", "Telugu", "English", "Mixed"]:
            lang_feedback = self.feedback_collector.get_feedback_by_language(language)
            
            if lang_feedback:
                language_metrics[language] = {
                    "count": len(lang_feedback),
                    "average_rating": sum(f.rating for f in lang_feedback) / len(lang_feedback),
                    "average_language_accuracy": sum(f.language_accuracy for f in lang_feedback) / len(lang_feedback),
                    "average_cultural_sensitivity": sum(f.cultural_sensitivity for f in lang_feedback) / len(lang_feedback),
                    "recommendation_rate": sum(f.would_recommend for f in lang_feedback) / len(lang_feedback) * 100
                }
            else:
                language_metrics[language] = {
                    "count": 0,
                    "average_rating": 0,
                    "average_language_accuracy": 0,
                    "average_cultural_sensitivity": 0,
                    "recommendation_rate": 0
                }
        
        return language_metrics
    
    def get_interaction_type_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get feedback breakdown by interaction type"""
        type_metrics = {}
        
        for interaction_type in ["translation", "learning", "general", "cultural"]:
            type_feedback = [f for f in self.feedback_collector.feedback_data if f.interaction_type == interaction_type]
            
            if type_feedback:
                type_metrics[interaction_type] = {
                    "count": len(type_feedback),
                    "average_rating": sum(f.rating for f in type_feedback) / len(type_feedback),
                    "average_helpfulness": sum(f.helpfulness for f in type_feedback) / len(type_feedback),
                    "average_user_satisfaction": sum(f.user_satisfaction for f in type_feedback) / len(type_feedback)
                }
            else:
                type_metrics[interaction_type] = {
                    "count": 0,
                    "average_rating": 0,
                    "average_helpfulness": 0,
                    "average_user_satisfaction": 0
                }
        
        return type_metrics
    
    def get_improvement_areas(self) -> List[str]:
        """Identify areas for improvement based on feedback"""
        if not self.feedback_collector.feedback_data:
            return []
        
        feedback_data = self.feedback_collector.feedback_data
        
        # Calculate average scores for different aspects
        aspects = {
            "Response Quality": sum(f.response_quality for f in feedback_data) / len(feedback_data),
            "Cultural Sensitivity": sum(f.cultural_sensitivity for f in feedback_data) / len(feedback_data),
            "Language Accuracy": sum(f.language_accuracy for f in feedback_data) / len(feedback_data),
            "Helpfulness": sum(f.helpfulness for f in feedback_data) / len(feedback_data),
            "Response Speed": sum(f.response_speed for f in feedback_data) / len(feedback_data),
            "User Satisfaction": sum(f.user_satisfaction for f in feedback_data) / len(feedback_data)
        }
        
        # Sort by lowest scores (areas needing improvement)
        sorted_aspects = sorted(aspects.items(), key=lambda x: x[1])
        
        # Return top 3 areas for improvement
        return [aspect for aspect, score in sorted_aspects[:3] if score < 4.0]
    
    def get_common_issues(self) -> List[str]:
        """Get common issues mentioned in feedback"""
        issues = []
        
        for feedback in self.feedback_collector.feedback_data:
            if feedback.technical_issues:
                issues.append(feedback.technical_issues)
            if feedback.improvement_suggestions:
                issues.append(feedback.improvement_suggestions)
        
        # Simple frequency analysis (in a real implementation, you'd use NLP)
        issue_counts = {}
        for issue in issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Return most common issues
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        return [issue for issue, count in sorted_issues[:5]]
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive feedback report"""
        return {
            "overall_metrics": self.get_overall_metrics(),
            "language_breakdown": self.get_language_breakdown(),
            "interaction_type_breakdown": self.get_interaction_type_breakdown(),
            "improvement_areas": self.get_improvement_areas(),
            "common_issues": self.get_common_issues(),
            "total_users": len(set(f.user_id for f in self.feedback_collector.feedback_data)),
            "report_generated": datetime.now().isoformat()
        }

class FeedbackVisualizer:
    """Creates visualizations for feedback data"""
    
    def __init__(self, feedback_analyzer: FeedbackAnalyzer):
        self.analyzer = feedback_analyzer
    
    def create_rating_distribution_chart(self) -> str:
        """Create a simple text-based rating distribution chart"""
        if not self.analyzer.feedback_collector.feedback_data:
            return "No feedback data available"
        
        ratings = [f.rating for f in self.analyzer.feedback_collector.feedback_data]
        rating_counts = {i: ratings.count(i) for i in range(1, 6)}
        
        chart = "Rating Distribution:\n"
        for rating in range(5, 0, -1):
            count = rating_counts[rating]
            bar = "█" * (count * 20 // len(ratings))
            chart += f"{rating} stars: {bar} ({count})\n"
        
        return chart
    
    def create_language_performance_chart(self) -> str:
        """Create a text-based language performance chart"""
        language_breakdown = self.analyzer.get_language_breakdown()
        
        chart = "Language Performance:\n"
        for language, metrics in language_breakdown.items():
            if metrics["count"] > 0:
                chart += f"{language}:\n"
                chart += f"  Count: {metrics['count']}\n"
                chart += f"  Avg Rating: {metrics['average_rating']:.1f}/5\n"
                chart += f"  Language Accuracy: {metrics['average_language_accuracy']:.1f}/5\n"
                chart += f"  Cultural Sensitivity: {metrics['average_cultural_sensitivity']:.1f}/5\n"
                chart += f"  Recommendation Rate: {metrics['recommendation_rate']:.1f}%\n\n"
        
        return chart

# Sample feedback data for demonstration
def create_sample_feedback(feedback_collector: FeedbackCollector):
    """Create sample feedback data for demonstration"""
    sample_feedbacks = [
        {
            "user_id": "user_001",
            "rating": 5,
            "language_used": "Hindi",
            "interaction_type": "translation",
            "comments": "बहुत अच्छा अनुवाद मिला। सही व्याकरण और सांस्कृतिक संदर्भ।",
            "response_quality": 5,
            "cultural_sensitivity": 5,
            "language_accuracy": 5,
            "helpfulness": 5,
            "response_speed": 4,
            "user_satisfaction": 5,
            "would_recommend": True,
            "improvement_suggestions": "थोड़ा तेज़ response हो सकता है",
            "technical_issues": ""
        },
        {
            "user_id": "user_002",
            "rating": 4,
            "language_used": "Telugu",
            "interaction_type": "learning",
            "comments": "తెలుగు వ్యాకరణం గురించి బాగా వివరించారు. కొంచెం ఎక్కువ ఉదాహరణలు ఇవ్వవచ్చు.",
            "response_quality": 4,
            "cultural_sensitivity": 5,
            "language_accuracy": 4,
            "helpfulness": 4,
            "response_speed": 5,
            "user_satisfaction": 4,
            "would_recommend": True,
            "improvement_suggestions": "మరిన్ని ఉదాహరణలు జోడించండి",
            "technical_issues": ""
        },
        {
            "user_id": "user_003",
            "rating": 5,
            "language_used": "English",
            "interaction_type": "cultural",
            "comments": "Great cultural insights! Helped me understand Hindi festivals better.",
            "response_quality": 5,
            "cultural_sensitivity": 5,
            "language_accuracy": 5,
            "helpfulness": 5,
            "response_speed": 5,
            "user_satisfaction": 5,
            "would_recommend": True,
            "improvement_suggestions": "",
            "technical_issues": ""
        }
    ]
    
    for feedback_data in sample_feedbacks:
        feedback_collector.create_feedback(**feedback_data)
