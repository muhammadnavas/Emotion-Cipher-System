# Emotion Cipher System

A secure emotion-aware text processing system that combines RSA encryption with AI-powered emotion analysis.

## Overview

The Emotion Cipher System allows you to:
- **Encrypt text messages** using RSA-2048 encryption
- **Analyze emotions** in text using AI (OpenAI GPT-3.5-turbo)
- **Interactive processing** with real-time user input
- **Demonstrate capabilities** with predefined examples

## Features

- 🔐 **RSA-2048 Encryption**: Secure text encryption with OAEP padding
- 🤖 **AI Emotion Analysis**: Powered by OpenAI GPT-3.5-turbo for emotion detection
- 💬 **Interactive Mode**: Real-time message processing with user input
- 📝 **Demo Examples**: 5 predefined examples for testing and demonstration
- 🔄 **Complete Processing Cycle**: Encrypt → Analyze → Decrypt with emotion preservation

## Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (for emotion analysis features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muhammadnavas/Emotion-Cipher-System.git
   cd Emotion-Cipher-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API Key**
   
   Set your OpenAI API key as an environment variable:
   ```bash
   set OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### 🎯 Interactive Mode

Run the main system for real-time message processing:

```bash
python emotion_cipher_system.py
```

This provides:
- Interactive message input prompts
- Real-time encryption and emotion analysis
- Session tracking and statistics

### 📝 Demo Examples

Run predefined examples to see the system in action:

```bash
# Full demo with 5 examples
python demo_hardcoded.py

# Quick single test
python demo_hardcoded.py quick

# Batch processing test
python demo_hardcoded.py batch
```

### 💻 Programmatic Usage

```python
from emotion_cipher_system import EmotionCipherSystem

# Initialize the system
system = EmotionCipherSystem()

# Process a message in PDF format
result = system.pdf_format_demo("I'm excited about this project!")

# Process with custom options
result = system.process_message(
    "Hello world!", 
    analyze_emotion=True, 
    pdf_format=True
)
```
 ## Output Format :
```
Input:
"I'm thrilled about this breakthrough!"

Encrypted Output:
Encrypted Text: "a8F2!k9@mP4$nQ7x"
Detected Emotion: Joy + Excitement

Decrypted Output:
Original Message: "I'm thrilled about this breakthrough!"
Detected Emotion: Joy + Excitement
```

## Project Structure

```
DecodeAI/
├── emotion_cipher_system.py    # Main interactive system
├── demo_hardcoded.py          # Hardcoded examples (5 demos)
├── rsa_encryption.py          # RSA encryption core
├── openai_integration.py      # OpenAI emotion analysis
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── keys/                      # RSA key storage (auto-generated)
    ├── private_key.pem
    └── public_key.pem
```

## Demo Examples

The system includes 5 predefined examples:

1. **Mixed Emotions**: "Feeling ecstatic about joining the new AI research team, though a bit anxious about the deadlines ahead."
2. **Negative Emotions**: "I can't believe I failed that test again. I'm so disappointed and frustrated right now."
3. **Positive Emotions**: "Finally got the job offer! I'm thrilled and can't wait to start this new journey."
4. **Love & Excitement**: "I absolutely love this new technology! It's going to revolutionize everything we do."
5. **Worry & Stress**: "I'm really worried about the presentation tomorrow. What if something goes wrong?"

## API Reference

### EmotionCipherSystem

#### Key Methods

- `pdf_format_demo(message)` - Process message in PDF-compliant format
- `process_message(message, analyze_emotion=True, pdf_format=False)` - Core processing
- `decrypt_message(encrypted_message, pdf_format=False, detected_emotion=None)` - Decrypt with options
- `interactive_demo()` - Run interactive session with user input
- `get_system_status()` - Get current system status and capabilities

#### Example Usage

```python
from emotion_cipher_system import EmotionCipherSystem

system = EmotionCipherSystem()

# PDF format processing
result = system.pdf_format_demo("I'm excited!")

# Check system status
status = system.get_system_status()
print(f"Encryption ready: {status['encryption']['keys_ready']}")
print(f"AI available: {status['emotion_analysis']['available']}")
```

## Configuration

### OpenAI API Key

Set your OpenAI API key as an environment variable:

**Windows:**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### System Behavior

- **With API Key**: Full functionality including emotion analysis
- **Without API Key**: Encryption works, but emotion analysis will show "Unknown"
- **Rate Limits**: The system handles OpenAI rate limits gracefully
- **Auto Key Generation**: RSA keys are generated automatically on first run

## Security Features

- **RSA-2048 Encryption**: Uses cryptographically secure 2048-bit RSA keys
- **Local Key Storage**: Private keys are generated and stored locally
- **Secure Processing**: Messages are encrypted before any external API calls
- **No Data Retention**: Only processed emotions (not raw messages) are sent to OpenAI

## Features Explained

### 🔐 RSA Encryption
- **Algorithm**: RSA-2048 with OAEP padding
- **Key Storage**: Local PEM format files
- **Security**: Military-grade encryption standards
- **Performance**: Optimized for text processing

### 🤖 Emotion Analysis
- **Model**: OpenAI GPT-3.5-turbo
- **Format**: "Primary + Secondary" emotion pairs
- **Examples**: Joy + Excitement, Sadness + Disappointment
- **Accuracy**: Contextual emotion understanding

## Error Handling

The system includes robust error handling:

- **API Limits**: Graceful handling of OpenAI rate limits
- **Network Issues**: Retry logic and fallback behaviors  
- **File Operations**: Safe key generation and storage
- **User Input**: Validation and sanitization
- **Encryption Errors**: Clear error messages and recovery

## System Requirements

- **Python**: 3.7+ (tested with 3.10)
- **Memory**: Minimal (< 50MB typical usage)
- **Storage**: ~1MB for keys and system files
- **Network**: Required only for OpenAI emotion analysis

## Getting Started

1. **Set up the environment**:
   ```bash
   pip install -r requirements.txt
   set OPENAI_API_KEY=your_key_here
   ```

2. **Try the interactive mode**:
   ```bash
   python emotion_cipher_system.py
   ```

3. **Run the demo examples**:
   ```bash
   python demo_hardcoded.py
   ```

4. **Test specific functionality**:
   ```bash
   python demo_hardcoded.py quick
   ```

## Troubleshooting

**Common Issues:**

- **"No module named 'cryptography'"**: Run `pip install -r requirements.txt`
- **"OpenAI API key not found"**: Set the OPENAI_API_KEY environment variable
- **"Keys directory not found"**: Keys are auto-generated on first run
- **"Rate limit exceeded"**: Wait a moment and try again (handled gracefully)

**Success Indicators:**
- RSA keys appear in `keys/` directory
- Interactive mode prompts for input
- Demo examples show encrypted output
- Emotions are detected (with API key)

---

**📧 Questions?** Check the troubleshooting section or verify your setup steps. 
