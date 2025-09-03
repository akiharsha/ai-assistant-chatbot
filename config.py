"""
Configuration file for IndicSahayak AI Assistant
Supports multiple deployment methods and model configurations
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for IndicSahayak"""
    
    # Application settings
    APP_NAME = "IndicSahayak"
    APP_VERSION = "1.0.0"
    SUPPORTED_LANGUAGES = ["Hindi", "Telugu", "English"]
    
    # Model configurations
    MODELS = {
        "huggingface": {
            "default_model": "microsoft/DialoGPT-medium",
            "multilingual_model": "facebook/mbart-large-50-many-to-many-mmt",
            "hindi_model": "ai4bharat/IndicBART",
            "telugu_model": "ai4bharat/IndicBART",
            "api_url": "https://api-inference.huggingface.co/models",
            "timeout": 30
        },
        "local": {
            "ollama_model": "llama2:7b",
            "local_api_url": "http://localhost:11434/api/generate",
            "timeout": 60
        },
        "dify": {
            "api_url": "https://api.dify.ai/v1",
            "workflow_id": "your-workflow-id",
            "timeout": 30
        }
    }
    
    # API Keys (should be set as environment variables)
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")
    
    # Response settings
    MAX_TOKENS = 200
    TEMPERATURE = 0.7
    TOP_P = 0.9
    
    # Feedback settings
    MIN_FEEDBACK_LENGTH = 10
    MAX_FEEDBACK_LENGTH = 500
    
    # UI settings
    MAX_CHAT_HISTORY = 50
    AUTO_DETECT_LANGUAGE = True
    
    @classmethod
    def get_model_config(cls, method: str) -> Dict[str, Any]:
        """Get configuration for a specific method"""
        return cls.MODELS.get(method, {})
    
    @classmethod
    def is_api_key_available(cls, method: str) -> bool:
        """Check if API key is available for a method"""
        if method == "huggingface":
            return bool(cls.HUGGINGFACE_API_KEY)
        elif method == "dify":
            return bool(cls.DIFY_API_KEY)
        return True  # Local methods don't need API keys

# Language-specific configurations
LANGUAGE_CONFIG = {
    "Hindi": {
        "script": "Devanagari",
        "script_range": (0x0900, 0x097F),
        "common_greetings": ["नमस्ते", "नमस्कार", "आदाब", "सलाम"],
        "cultural_context": "Indian subcontinent, particularly North India"
    },
    "Telugu": {
        "script": "Telugu",
        "script_range": (0x0C00, 0x0C7F),
        "common_greetings": ["నమస్కారం", "వందనలు", "ఆదాబ్"],
        "cultural_context": "Indian subcontinent, particularly South India (Andhra Pradesh, Telangana)"
    },
    "English": {
        "script": "Latin",
        "script_range": (0x0020, 0x007F),
        "common_greetings": ["hello", "hi", "hey", "good morning"],
        "cultural_context": "International, widely used as lingua franca"
    }
}

# System prompt templates for different scenarios
SYSTEM_PROMPT_TEMPLATES = {
    "general": """
You are IndicSahayak, an AI assistant specialized in Hindi and Telugu languages.
Your role is to help users with language learning, translation, and cultural understanding.
Always be respectful, patient, and culturally sensitive.
""",
    "translation": """
You are IndicSahayak, specialized in accurate translations between Hindi, Telugu, and English.
Provide context-aware translations and explain cultural nuances when relevant.
""",
    "learning": """
You are IndicSahayak, a patient language learning tutor for Hindi and Telugu.
Provide clear explanations, examples, and encourage practice.
Adapt your teaching style to the user's proficiency level.
""",
    "cultural": """
You are IndicSahayak, a cultural guide for Hindi and Telugu speaking communities.
Share knowledge about traditions, festivals, etiquette, and regional variations.
Always be respectful and accurate in your cultural information.
"""
}
