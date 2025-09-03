# IndicSahayak - AI Assistant for Indic Languages

🇮🇳 **IndicSahayak** (इंडिक सहायक / ఇండిక్ సహాయక) is an open-source AI assistant specialized in Hindi and Telugu languages, built with a focus on cultural sensitivity and language accuracy.

## Features

- 🌐 **Multilingual Support**: Native support for Hindi (Devanagari) and Telugu (Telugu script)
- 🎯 **Language Learning**: Grammar explanations, vocabulary building, and cultural context
- 🔄 **Translation**: Context-aware translations between Hindi, Telugu, and English
- 🏛️ **Cultural Guidance**: Insights into Indian culture, traditions, and social etiquette
- 📊 **Feedback System**: Comprehensive user feedback collection and analysis
- 🚀 **Multiple Deployment**: Support for Hugging Face API, local models, and Dify.ai

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/indic-sahayak.git
cd indic-sahayak
```

2. Install dependencies:
```bash
pip install -r chatbot/requirements.txt
```

3. Set up environment variables (optional):
```bash
export HUGGINGFACE_API_KEY="your_api_key_here"
export DIFY_API_KEY="your_dify_key_here"
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run chatbot/indic_sahayak.py
```

2. Open your browser and navigate to `http://localhost:8501`

## Usage Examples

### Hindi Conversation
```
User: नमस्ते! मैं हिंदी सीख रहा हूं।
Assistant: नमस्ते! मैं आपकी हिंदी सीखने में मदद कर सकता हूं। आप क्या सीखना चाहते हैं?
```

### Telugu Translation
```
User: Translate "Good morning" to Telugu
Assistant: "Good morning" in Telugu is "శుభోదయం" (Shubhodayam)
```

### Cultural Guidance
```
User: Tell me about Diwali
Assistant: Diwali is the festival of lights celebrated across India...
```

## System Architecture

### Components

1. **Main Application** (`indic_sahayak.py`): Streamlit-based user interface
2. **Configuration** (`config.py`): Model and deployment configurations
3. **API Clients** (`huggingface_client.py`): Integration with various AI services
4. **Feedback System** (`feedback_system.py`): User feedback collection and analysis

### Supported Models

- **Hugging Face**: `microsoft/DialoGPT-medium`, `facebook/mbart-large-50-many-to-many-mmt`
- **Indic Models**: `ai4bharat/IndicBART`
- **Local Models**: Ollama, custom deployments

## Configuration

### Environment Variables

- `HUGGINGFACE_API_KEY`: Your Hugging Face API key
- `DIFY_API_KEY`: Your Dify.ai API key (if using Dify deployment)

### Model Selection

You can choose between different deployment methods in the app:
- **Hugging Face API**: Cloud-based inference
- **Local Model**: Self-hosted models
- **Fallback**: Rule-based responses

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Areas for Contribution

- Language model improvements
- Additional Indic language support
- UI/UX enhancements
- Documentation improvements
- Bug fixes and feature requests

## User Feedback

We collect comprehensive feedback to improve the assistant. The feedback system tracks:
- Response quality and accuracy
- Cultural sensitivity
- Language proficiency
- User satisfaction
- Improvement suggestions

## Roadmap

### Short-term (1 week)
- Performance optimization
- Enhanced examples and vocabulary
- Formal language support
- UI improvements

### Medium-term (2-4 weeks)
- Voice input/output
- Advanced learning modules
- More Indic languages
- Community features

### Long-term (4+ weeks)
- Comprehensive language ecosystem
- Educational partnerships
- Research contributions
- Global impact initiatives

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Hugging Face for providing open-source models
- AI4Bharat for Indic language models
- The open-source community for tools and libraries
- All users who provided feedback and suggestions

## Support

- 📧 Email: support@indicsahayak.ai
- 💬 Discord: [Join our community](https://discord.gg/indicsahayak)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/indic-sahayak/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/indic-sahayak/wiki)

## Citation

If you use IndicSahayak in your research or project, please cite:

```bibtex
@software{indicsahayak2024,
  title={IndicSahayak: AI Assistant for Indic Languages},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/indic-sahayak}
}
```

---

**Made with ❤️ for the Indic language community**
