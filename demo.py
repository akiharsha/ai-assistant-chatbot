#!/usr/bin/env python3
"""
Demo script for IndicSahayak AI Assistant
Tests basic functionality and displays sample interactions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from indic_sahayak import IndicSahayak
from feedback_system import FeedbackCollector, FeedbackAnalyzer, create_sample_feedback
import json

def run_demo():
    """Run a comprehensive demo of IndicSahayak"""
    
    print("🇮🇳 IndicSahayak Demo - AI Assistant for Indic Languages")
    print("=" * 60)
    
    # Initialize the assistant
    assistant = IndicSahayak()
    print(f"✅ Initialized {assistant.name}")
    print(f"📝 Supported Languages: {', '.join(assistant.supported_languages)}")
    print()
    
    # Test language detection
    print("🔍 Testing Language Detection:")
    test_texts = [
        "नमस्ते! मैं हिंदी सीख रहा हूं।",
        "నమస్కారం! నేను తెలుగు నేర్చుకుంటున్నాను।",
        "Hello! I am learning languages."
    ]
    
    for text in test_texts:
        detected_lang = assistant.detect_language(text)
        print(f"  '{text[:30]}...' → {detected_lang}")
    print()
    
    # Test responses
    print("💬 Testing AI Responses:")
    test_queries = [
        ("Hindi", "नमस्ते! मैं आपकी कैसे मदद कर सकता हूं?"),
        ("Telugu", "నమస్కారం! నేను మీకు ఎలా సహాయం చేయగలను?"),
        ("English", "Hello! How can I help you today?")
    ]
    
    for lang, query in test_queries:
        print(f"\n  {lang} Query: {query}")
        response = assistant.get_response(query, method="fallback")
        print(f"  Response: {response}")
    print()
    
    # Test feedback system
    print("📊 Testing Feedback System:")
    feedback_collector = FeedbackCollector("demo_feedback.json")
    
    # Create sample feedback
    create_sample_feedback(feedback_collector)
    
    # Analyze feedback
    analyzer = FeedbackAnalyzer(feedback_collector)
    metrics = analyzer.get_overall_metrics()
    
    print(f"  Total Feedback: {metrics['total_feedback']}")
    if metrics['total_feedback'] > 0:
        print(f"  Average Rating: {metrics['average_rating']:.1f}/5")
        print(f"  Recommendation Rate: {metrics['recommendation_rate']:.1f}%")
    
    # Language breakdown
    lang_breakdown = analyzer.get_language_breakdown()
    print("\n  Language Performance:")
    for lang, metrics in lang_breakdown.items():
        if metrics['count'] > 0:
            print(f"    {lang}: {metrics['count']} users, {metrics['average_rating']:.1f}/5 rating")
    
    # Improvement areas
    improvements = analyzer.get_improvement_areas()
    if improvements:
        print(f"\n  Areas for Improvement: {', '.join(improvements)}")
    
    print()
    
    # Display system prompt
    print("📋 System Prompt Preview:")
    prompt_preview = assistant.system_prompt[:200] + "..."
    print(f"  {prompt_preview}")
    print()
    
    # Configuration info
    print("⚙️ Configuration:")
    print(f"  Max Tokens: 200")
    print(f"  Temperature: 0.7")
    print(f"  Supported Scripts: Devanagari, Telugu, Latin")
    print(f"  Cultural Focus: Indian subcontinent")
    print()
    
    # Demo completion
    print("✅ Demo completed successfully!")
    print("\n🚀 To run the full application:")
    print("   streamlit run indic_sahayak.py")
    print("\n📖 For more information, see the README.md file")

def interactive_demo():
    """Run an interactive demo session"""
    
    print("🎮 Interactive Demo Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print("-" * 40)
    
    assistant = IndicSahayak()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("Available commands:")
                print("  - Type in Hindi, Telugu, or English")
                print("  - 'quit' to exit")
                print("  - 'help' for this message")
                continue
            elif not user_input:
                continue
            
            # Get response
            response = assistant.get_response(user_input, method="fallback")
            print(f"IndicSahayak: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_demo()
    else:
        run_demo()
