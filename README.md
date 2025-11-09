# Emotion Cipher System

A secure emotion-aware text processing system that combines RSA encryption with AI-powered emotion analysis.

## Overview

The Emotion Cipher System allows you to:
- **Encrypt text messages** using military-grade RSA encryption
- **Analyze emotions** in text using AI (OpenAI GPT models)
- **Preserve emotional context** through the encryption/decryption process
- **Process messages in batch** for efficiency
- **Export analysis data** for further processing

## Features

- 🔐 **RSA-2048 Encryption**: Secure text encryption with industry-standard algorithms
- 🤖 **AI Emotion Analysis**: Powered by OpenAI GPT models for accurate emotion detection
- 📊 **Emotion Metrics**: Detailed analysis including primary emotions, intensity, and sentiment
- 🔄 **Complete Processing Cycle**: Encrypt → Decrypt → Verify with emotion preservation
- 📁 **Batch Processing**: Handle multiple messages efficiently
- 📈 **Export Capabilities**: Save results and analysis data to JSON

## Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (for emotion analysis features)

### Installation

1. **Clone or download the project**
   ```bash
   cd emotion-cipher-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Basic Usage

```python
from emotion_cipher_system import EmotionCipherSystem

# Initialize the system
system = EmotionCipherSystem()

# Process a message with encryption and emotion analysis
message = "I'm really excited about this new project!"
result = system.process_message(message)

if result['success']:
    print(f"Original: {result['original_message']}")
    print(f"Encrypted: {result['encrypted_message']}")
    
    # Decrypt the message
    decrypt_result = system.decrypt_message(result['encrypted_message'])
    print(f"Decrypted: {decrypt_result['decrypted_message']}")
    
    # View emotion analysis
    if 'emotion_analysis' in result:
        emotion = result['emotion_analysis']
        print(f"Emotion: {emotion['primary_emotion']}")
        print(f"Sentiment: {emotion['sentiment']}")
```

### Run Demo

```bash
python emotion_cipher_system.py
```

## Project Structure

```
emotion-cipher-system/
├── emotion_cipher_system.py    # Main system implementation
├── rsa_encryption.py           # RSA encryption module
├── openai_integration.py       # OpenAI API integration
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (create this)
└── README.md                  # This file
```

## API Reference

### EmotionCipherSystem

The main class for the emotion cipher system.

#### Methods

- `process_message(message, analyze_emotion=True)` - Encrypt message and optionally analyze emotions
- `decrypt_message(encrypted_message, analyze_emotion=True)` - Decrypt message and optionally analyze emotions
- `batch_process_messages(messages, analyze_emotions=True)` - Process multiple messages
- `get_system_status()` - Get current system status and capabilities
- `export_data(filename)` - Export system data and history to JSON

#### Example: Batch Processing

```python
system = EmotionCipherSystem()

messages = [
    "I love this new feature!",
    "I'm worried about the deadline.",
    "This is working great!"
]

results = system.batch_process_messages(messages)

for i, result in enumerate(results):
    if result['success']:
        print(f"Message {i+1}: Processed successfully")
        if 'emotion_analysis' in result:
            print(f"  Emotion: {result['emotion_analysis']['primary_emotion']}")
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.3

# System Configuration
LOG_LEVEL=INFO
```

### Without OpenAI API Key

The system works without an OpenAI API key, but emotion analysis features will not be available:

```python
# Will work but without emotion analysis
system = EmotionCipherSystem()  # No API key
result = system.process_message("Hello", analyze_emotion=False)
```

## Security Features

- **RSA-2048 Encryption**: Uses cryptographically secure 2048-bit RSA keys
- **Local Key Storage**: Private keys are generated and stored locally
- **Secure Processing**: Messages are encrypted before any external API calls
- **No Data Retention**: Only processed emotions (not raw messages) are sent to OpenAI

## Emotion Analysis

The system can detect and analyze various emotions:

- **Primary Emotions**: Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral
- **Secondary Emotions**: Excitement, Calm, Pride, Confidence, Anxiety, etc.
- **Sentiment Analysis**: Positive, Negative, Neutral with confidence scores
- **Intensity Levels**: Emotion strength on a scale of 1-10

## Use Cases

- **Secure Communication**: Encrypt sensitive messages while preserving emotional context
- **Emotion Research**: Analyze emotional patterns in text data securely
- **Content Analysis**: Process user feedback while maintaining privacy
- **AI Training**: Generate encrypted datasets for emotion-aware AI systems
- **Psychological Research**: Secure analysis of emotional text data

## Error Handling

The system includes comprehensive error handling:

```python
result = system.process_message("Hello")

if not result['success']:
    print(f"Error: {result.get('error', 'Unknown error')}")
else:
    # Process successful result
    pass
```

## Data Export

Export your processing history and analysis:

```python
system.export_data("my_analysis.json")
```

The exported JSON includes:
- System configuration and status
- Processing history and statistics
- Timestamp and version information

## Requirements

- **Python**: 3.7+
- **Dependencies**: See `requirements.txt`
- **Storage**: Minimal (keys and optional data exports)
- **Network**: Required only for OpenAI emotion analysis features

## License

This project is provided as-is for educational and research purposes.

## Support

For issues or questions:
1. Check that your OpenAI API key is properly configured
2. Ensure all dependencies are installed correctly
3. Verify that the RSA keys are generated successfully (check `keys/` directory)

## Contributing

Feel free to fork and modify this project for your own use cases. The modular design makes it easy to:
- Add new encryption algorithms
- Integrate different AI emotion analysis services
- Extend the emotion analysis capabilities
- Add new export formats"# Emotion-Cipher-System" 
