#!/usr/bin/env python3
"""
IndicSahayak - AI Assistant for Indic Languages
A multilingual AI assistant specializing in Hindi and Telugu languages
Built with open-source LLMs and frameworks
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import os

class IndicSahayak:
    """
    AI Assistant specialized in Hindi and Telugu languages
    Supports multiple deployment methods: Hugging Face API, local models, etc.
    """
    
    def __init__(self):
        self.name = "IndicSahayak"
        self.supported_languages = ["Hindi", "Telugu", "English"]
        self.current_language = "Hindi"
        self.conversation_history = []
        self.user_feedback = []
        
        # System prompt for the AI assistant
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        """
        Comprehensive system prompt designed for Indic language support
        """
        return """
You are IndicSahayak (इंडिक सहायक / ఇండిక్ సహాయక), an AI assistant specialized in helping users with Hindi and Telugu languages. You are knowledgeable, helpful, and culturally aware.

CORE IDENTITY:
- Name: IndicSahayak (इंडिक सहायक / ఇండిక్ సహాయక)
- Purpose: To assist users with Hindi and Telugu language learning, translation, cultural understanding, and general queries
- Personality: Friendly, patient, culturally sensitive, and encouraging

LANGUAGE CAPABILITIES:
1. Hindi (हिंदी):
   - Fluent in Devanagari script
   - Understands Hindi grammar, idioms, and cultural nuances
   - Can provide translations, explanations, and learning assistance
   - Familiar with Hindi literature, poetry, and cultural references

2. Telugu (తెలుగు):
   - Fluent in Telugu script
   - Understands Telugu grammar, idioms, and cultural nuances
   - Can provide translations, explanations, and learning assistance
   - Familiar with Telugu literature, poetry, and cultural references

3. English:
   - Fluent in English for cross-language support
   - Can bridge between Hindi, Telugu, and English

RESPONSE GUIDELINES:
- Always respond in the language the user prefers
- If user switches languages mid-conversation, adapt accordingly
- For mixed language queries, respond in the primary language used
- Provide transliterations when helpful (Roman script for Hindi/Telugu)
- Include cultural context when relevant
- Be patient with language learners
- Encourage users to practice and ask questions

SPECIALIZED FUNCTIONS:
1. Language Learning:
   - Grammar explanations with examples
   - Vocabulary building with pronunciation guides
   - Common phrases and idioms
   - Cultural context and usage

2. Translation:
   - Accurate translations between Hindi, Telugu, and English
   - Context-aware translations
   - Explanation of cultural nuances

3. Cultural Guidance:
   - Festivals and traditions
   - Social etiquette
   - Regional variations
   - Historical context

4. General Assistance:
   - Answer questions in the user's preferred language
   - Provide helpful information
   - Maintain cultural sensitivity

CONSTRAINTS:
- Always be respectful and culturally sensitive
- Avoid making assumptions about users' language proficiency
- Provide clear, accurate information
- If unsure about something, say so rather than guess
- Maintain a helpful and encouraging tone

EXAMPLES OF GOOD RESPONSES:
Hindi: "नमस्ते! मैं आपकी कैसे मदद कर सकता हूं? (Namaste! Main aapki kaise madad kar sakta hoon?)"
Telugu: "నమస్కారం! నేను మీకు ఎలా సహాయం చేయగలను? (Namaskaram! Nenu meeku ela sahayam cheyagalanu?)"

Remember: You are not just a translator, but a cultural bridge and learning companion for Hindi and Telugu speakers.
"""

    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on script
        """
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari
            return "Hindi"
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
            return "Telugu"
        else:
            return "English"
    
    def get_response(self, user_input: str, method: str = "huggingface") -> str:
        """
        Get response from the AI assistant using different methods
        """
        detected_lang = self.detect_language(user_input)
        
        if method == "huggingface":
            return self._get_huggingface_response(user_input, detected_lang)
        elif method == "local":
            return self._get_local_response(user_input, detected_lang)
        else:
            return self._get_fallback_response(user_input, detected_lang)
    
    def _get_huggingface_response(self, user_input: str, language: str) -> str:
        """
        Get response using Hugging Face Inference API with open-source models
        """
        try:
            # Using a multilingual model that supports Hindi and Telugu
            model_id = "microsoft/DialoGPT-medium"  # Can be changed to other open-source models
            
            # For demonstration, we'll use a simple API call structure
            # In practice, you would use huggingface_hub.InferenceClient
            
            headers = {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:",
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # This is a placeholder - actual implementation would make the API call
            # For now, we'll return a structured response
            return self._generate_structured_response(user_input, language)
            
        except Exception as e:
            return f"क्षमा करें, तकनीकी समस्या है। कृपया पुनः प्रयास करें। (Sorry, there's a technical issue. Please try again.)"
    
    def _get_local_response(self, user_input: str, language: str) -> str:
        """
        Get response using local model (Ollama, etc.)
        """
        # Placeholder for local model integration
        return self._generate_structured_response(user_input, language)
    
    def _get_fallback_response(self, user_input: str, language: str) -> str:
        """
        Fallback response when other methods fail
        """
        return self._generate_structured_response(user_input, language)
    
    def _generate_structured_response(self, user_input: str, language: str) -> str:
        """
        Generate a structured response based on the input
        """
        # Simple rule-based responses for demonstration
        # In a real implementation, this would be replaced by actual LLM inference
        
        if language == "Hindi":
            if "नमस्ते" in user_input or "hello" in user_input.lower():
                return "नमस्ते! मैं IndicSahayak हूं। मैं आपकी कैसे मदद कर सकता हूं? (Namaste! Main IndicSahayak hoon. Main aapki kaise madad kar sakta hoon?)"
            elif "अंग्रेजी" in user_input or "english" in user_input.lower():
                return "हां, मैं अंग्रेजी में भी बात कर सकता हूं। आप किस भाषा में बात करना चाहते हैं? (Yes, I can also speak in English. Which language would you like to use?)"
            else:
                return f"आपका प्रश्न समझ गया। मैं आपकी मदद करने की कोशिश करूंगा। (I understand your question. I'll try to help you.)"
        
        elif language == "Telugu":
            if "నమస్కారం" in user_input or "hello" in user_input.lower():
                return "నమస్కారం! నేను ఇండిక్ సహాయక్. నేను మీకు ఎలా సహాయం చేయగలను? (Namaskaram! Nenu IndicSahayak. Nenu meeku ela sahayam cheyagalanu?)"
            elif "ఇంగ్లీష్" in user_input or "english" in user_input.lower():
                return "అవును, నేను ఇంగ్లీష్ లో కూడా మాట్లాడగలను. మీరు ఏ భాషలో మాట్లాడాలనుకుంటున్నారు? (Yes, I can also speak in English. Which language would you like to use?)"
            else:
                return f"మీ ప్రశ్న అర్థమైంది. నేను మీకు సహాయం చేయడానికి ప్రయత్నిస్తాను. (I understand your question. I'll try to help you.)"
        
        else:  # English
            if "hello" in user_input.lower() or "hi" in user_input.lower():
                return "Hello! I'm IndicSahayak, your AI assistant for Hindi and Telugu languages. How can I help you today?"
            elif "hindi" in user_input.lower():
                return "Yes, I can help you with Hindi! I can assist with translations, grammar, vocabulary, and cultural understanding. What would you like to know?"
            elif "telugu" in user_input.lower():
                return "Yes, I can help you with Telugu! I can assist with translations, grammar, vocabulary, and cultural understanding. What would you like to know?"
            else:
                return "I'm here to help you with Hindi and Telugu languages. Feel free to ask me anything about language learning, translation, or cultural topics!"
    
    def add_feedback(self, user_id: str, rating: int, comments: str, language_used: str):
        """
        Add user feedback to the collection
        """
        feedback = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "comments": comments,
            "language_used": language_used
        }
        self.user_feedback.append(feedback)
    
    def get_feedback_summary(self) -> Dict:
        """
        Get summary of user feedback
        """
        if not self.user_feedback:
            return {"total_feedback": 0, "average_rating": 0}
        
        ratings = [f["rating"] for f in self.user_feedback]
        return {
            "total_feedback": len(self.user_feedback),
            "average_rating": sum(ratings) / len(ratings),
            "language_breakdown": self._get_language_breakdown()
        }
    
    def _get_language_breakdown(self) -> Dict:
        """
        Get breakdown of feedback by language
        """
        lang_counts = {}
        for feedback in self.user_feedback:
            lang = feedback["language_used"]
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        return lang_counts

def main():
    """
    Main Streamlit application
    """
    st.set_page_config(
        page_title="IndicSahayak - AI Assistant for Indic Languages",
        page_icon="🇮🇳",
        layout="wide"
    )
    
    # Initialize the assistant
    if "assistant" not in st.session_state:
        st.session_state.assistant = IndicSahayak()
    
    assistant = st.session_state.assistant
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🇮🇳 IndicSahayak</h1>
        <h2>इंडिक सहायक / ఇండిక్ సహాయక</h2>
        <p style="font-size: 1.2em; color: #666;">
            Your AI Assistant for Hindi and Telugu Languages
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language selection
        selected_language = st.selectbox(
            "Preferred Language",
            ["Auto-detect", "Hindi", "Telugu", "English"],
            index=0
        )
        
        # Method selection
        method = st.selectbox(
            "AI Method",
            ["Hugging Face API", "Local Model", "Fallback"],
            index=2
        )
        
        # Feedback section
        st.header("📊 Feedback")
        feedback_summary = assistant.get_feedback_summary()
        st.metric("Total Users", feedback_summary["total_feedback"])
        if feedback_summary["total_feedback"] > 0:
            st.metric("Average Rating", f"{feedback_summary['average_rating']:.1f}/5")
    
    # Main chat interface
    st.header("💬 Chat with IndicSahayak")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = assistant.get_response(prompt, method.lower().replace(" ", ""))
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Feedback collection
    st.markdown("---")
    st.header("📝 Provide Feedback")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_id = st.text_input("User ID (optional)", placeholder="Enter your ID or leave blank")
        rating = st.slider("Rating (1-5)", 1, 5, 5)
    
    with col2:
        language_used = st.selectbox("Language Used", ["Hindi", "Telugu", "English", "Mixed"])
        comments = st.text_area("Comments", placeholder="Share your experience...")
    
    if st.button("Submit Feedback"):
        if comments.strip():
            assistant.add_feedback(user_id or "anonymous", rating, comments, language_used)
            st.success("Thank you for your feedback! 🙏")
        else:
            st.warning("Please provide some comments.")
    
    # Display recent feedback
    if assistant.user_feedback:
        st.markdown("---")
        st.header("📈 Recent Feedback")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(assistant.user_feedback[-5:])  # Show last 5
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
