"""
Hugging Face API client for IndicSahayak
Handles interactions with open-source models on Hugging Face
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
import os
from config import Config

class HuggingFaceClient:
    """Client for interacting with Hugging Face Inference API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.HUGGINGFACE_API_KEY
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_response(
        self, 
        prompt: str, 
        model: str = "microsoft/DialoGPT-medium",
        max_tokens: int = 200,
        temperature: float = 0.7,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generate response using Hugging Face Inference API
        
        Args:
            prompt: Input prompt for the model
            model: Model ID from Hugging Face Hub
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            language: Target language for response
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Prepare the request payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": Config.TOP_P,
                    "return_full_text": False,
                    "do_sample": True
                }
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/{model}",
                headers=self.headers,
                json=payload,
                timeout=Config.MODELS["huggingface"]["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                else:
                    generated_text = str(result)
                
                return {
                    "success": True,
                    "response": generated_text,
                    "model": model,
                    "language": language,
                    "tokens_used": len(generated_text.split())
                }
            
            elif response.status_code == 503:
                # Model is loading, wait and retry
                return self._handle_model_loading(model, prompt, max_tokens, temperature, language)
            
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}",
                    "model": model
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout - model may be overloaded",
                "model": model
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "model": model
            }
    
    def _handle_model_loading(
        self, 
        model: str, 
        prompt: str, 
        max_tokens: int, 
        temperature: float, 
        language: str
    ) -> Dict[str, Any]:
        """
        Handle model loading scenario by waiting and retrying
        """
        max_retries = 3
        wait_time = 10
        
        for attempt in range(max_retries):
            time.sleep(wait_time)
            result = self.generate_response(prompt, model, max_tokens, temperature, language)
            
            if result["success"]:
                return result
            
            wait_time *= 2  # Exponential backoff
        
        return {
            "success": False,
            "error": "Model failed to load after multiple retries",
            "model": model
        }
    
    def translate_text(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """
        Translate text between languages using multilingual models
        """
        # Use a multilingual translation model
        model = "facebook/mbart-large-50-many-to-many-mmt"
        
        # Create translation prompt
        prompt = f"Translate the following {source_lang} text to {target_lang}: {text}"
        
        return self.generate_response(prompt, model, max_tokens=100)
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for Indic languages
        """
        return [
            "microsoft/DialoGPT-medium",
            "facebook/mbart-large-50-many-to-many-mmt",
            "ai4bharat/IndicBART",
            "google/mt5-small",
            "Helsinki-NLP/opus-mt-en-hi",
            "Helsinki-NLP/opus-mt-en-te"
        ]
    
    def test_connection(self) -> bool:
        """
        Test if the API connection is working
        """
        try:
            test_prompt = "Hello, this is a test."
            result = self.generate_response(test_prompt, max_tokens=10)
            return result["success"]
        except:
            return False

class LocalModelClient:
    """Client for local model deployment (Ollama, etc.)"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    def generate_response(
        self, 
        prompt: str, 
        model: str = "llama2:7b",
        max_tokens: int = 200,
        temperature: float = 0.7,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generate response using local model
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "")
                
                return {
                    "success": True,
                    "response": generated_text,
                    "model": model,
                    "language": language,
                    "tokens_used": len(generated_text.split())
                }
            else:
                return {
                    "success": False,
                    "error": f"Local API Error: {response.status_code} - {response.text}",
                    "model": model
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Local model error: {str(e)}",
                "model": model
            }
    
    def test_connection(self) -> bool:
        """
        Test if local model is available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

class DifyClient:
    """Client for Dify.ai platform"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or Config.DIFY_API_KEY
        self.base_url = base_url or Config.MODELS["dify"]["api_url"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_response(
        self, 
        prompt: str, 
        workflow_id: str = None,
        max_tokens: int = 200,
        temperature: float = 0.7,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generate response using Dify.ai workflow
        """
        try:
            workflow_id = workflow_id or Config.MODELS["dify"]["workflow_id"]
            
            payload = {
                "inputs": {
                    "query": prompt,
                    "language": language
                },
                "response_mode": "blocking",
                "user": "indic_sahayak_user"
            }
            
            response = requests.post(
                f"{self.base_url}/workflows/run",
                headers=self.headers,
                json=payload,
                timeout=Config.MODELS["dify"]["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("data", {}).get("outputs", {}).get("answer", "")
                
                return {
                    "success": True,
                    "response": generated_text,
                    "model": "dify_workflow",
                    "language": language,
                    "tokens_used": len(generated_text.split())
                }
            else:
                return {
                    "success": False,
                    "error": f"Dify API Error: {response.status_code} - {response.text}",
                    "model": "dify_workflow"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Dify error: {str(e)}",
                "model": "dify_workflow"
            }
    
    def test_connection(self) -> bool:
        """
        Test if Dify connection is working
        """
        try:
            response = requests.get(
                f"{self.base_url}/workflows",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
