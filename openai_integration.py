"""
OpenAI API Integration for Emotion Cipher System
Provides emotion analysis, text processing, and AI-powered features
"""

from openai import OpenAI
from typing import List, Dict, Optional, Tuple
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenAIClient:
    """OpenAI API client for emotion analysis and text processing"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client
        
        Args:
            api_key (Optional[str]): OpenAI API key. If None, uses OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_emotion(self, text: str) -> Dict[str, any]:
        """
        Analyze emotions in the given text
        
        Args:
            text (str): Text to analyze for emotions
            
        Returns:
            Dict[str, any]: Emotion analysis results
        """
        prompt = f"""
        Analyze the emotional content of the following text and provide:
        1. Primary emotion (joy, sadness, anger, fear, surprise, disgust, neutral)
        2. Secondary emotions (if any)
        3. Emotion intensity (1-10 scale)
        4. Emotional keywords found in the text
        5. Sentiment (positive, negative, neutral)
        
        Text to analyze: "{text}"
        
        Please respond in JSON format with keys: primary_emotion, secondary_emotions, intensity, keywords, sentiment, explanation
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert emotion analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "primary_emotion": "unknown",
                    "secondary_emotions": [],
                    "intensity": 5,
                    "keywords": [],
                    "sentiment": "neutral",
                    "explanation": result
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "primary_emotion": "error",
                "secondary_emotions": [],
                "intensity": 0,
                "keywords": [],
                "sentiment": "neutral"
            }
    
    def generate_emotion_cipher(self, original_text: str, target_emotion: str) -> str:
        """
        Generate an emotion cipher that encodes feelings into text
        This creates a cipher where emotions are embedded into the message structure
        
        Args:
            original_text (str): Original text to cipher
            target_emotion (str): Target emotion to encode into the cipher
            
        Returns:
            str: Emotion-ciphered text that encodes the target emotion
        """
        prompt = f"""
        Create an EMOTION CIPHER by transforming the following text to encode the emotion "{target_emotion}":
        
        Original text: "{original_text}"
        Target emotion to encode: {target_emotion}
        
        CIPHER RULES for Emotion Encoding:
        1. Preserve the core message meaning
        2. Embed emotional indicators that can be decoded later
        3. Use word choice, tone, and emotional markers that represent {target_emotion}
        4. Create a cipher where the emotion is encoded in the language structure
        5. Make it appear natural but with clear emotional encoding
        
        Return only the emotion-ciphered text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in emotional text transformation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating emotion cipher: {str(e)}"
    
    def decode_emotion_cipher(self, ciphered_text: str) -> dict:
        """
        Decode an emotion cipher back to original emotion and meaning
        This reverses the emotion cipher process to extract encoded feelings
        
        Args:
            ciphered_text (str): The emotion-ciphered text to decode
            
        Returns:
            dict: Contains decoded emotion and core message
        """
        prompt = f"""
        DECODE this EMOTION CIPHER by analyzing the emotional encoding:
        
        Emotion-ciphered text: "{ciphered_text}"
        
        CIPHER DECODING PROCESS:
        1. Analyze the emotional markers and indicators in the text
        2. Identify what emotion was encoded into this cipher
        3. Extract the core message without the emotional encoding
        4. Determine the confidence of your decoding
        
        This is an EMOTION CIPHER where feelings were encoded into the message structure.
        Decode both the emotion and the original meaning.
        
        Respond with a JSON object:
        {{
            "decoded_emotion": "the specific emotion that was encoded in the cipher",
            "core_message": "the original message before emotion encoding",
            "confidence": "high/medium/low",
            "cipher_indicators": "what clues revealed the encoded emotion"
        }}
        
        Provide only the JSON response.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            import json
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                # If not valid JSON, return structured response
                return {
                    "decoded_emotion": "unknown",
                    "core_message": result_text,
                    "confidence": "low",
                    "cipher_indicators": "parsing error"
                }
                
        except Exception as e:
            return {
                "error": f"Failed to decode emotion cipher: {str(e)}",
                "decoded_emotion": "error",
                "core_message": ciphered_text,
                "confidence": "low",
                "cipher_indicators": "system error"
            }
    
    def generate_emotional_summary(self, texts: List[str]) -> Dict[str, any]:
        """
        Generate an emotional summary of multiple texts
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            Dict[str, any]: Emotional summary and patterns
        """
        combined_text = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])
        
        prompt = f"""
        Analyze the emotional patterns across these texts:
        
        {combined_text}
        
        Provide:
        1. Overall emotional theme
        2. Emotional progression/changes
        3. Dominant emotions
        4. Emotional consistency score (1-10)
        5. Key emotional insights
        
        Respond in JSON format.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in emotional pattern analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.4
            )
            
            result = response.choices[0].message.content.strip()
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {
                    "overall_theme": "mixed",
                    "emotional_progression": "unclear",
                    "dominant_emotions": ["neutral"],
                    "consistency_score": 5,
                    "insights": [result]
                }
                
        except Exception as e:
            return {"error": str(e)}


class EmotionProcessor:
    """High-level emotion processing combining OpenAI capabilities"""
    
    def __init__(self, openai_client: OpenAIClient):
        """
        Initialize emotion processor
        
        Args:
            openai_client (OpenAIClient): Configured OpenAI client
        """
        self.openai_client = openai_client
        self.emotion_cache = {}
    
    def process_emotion_cipher(self, text: str, operation: str = "analyze", 
                              target_emotion: Optional[str] = None) -> Dict[str, any]:
        """
        Process emotion cipher operations
        
        Args:
            text (str): Input text
            operation (str): Operation type - "analyze", "encode", "decode"
            target_emotion (Optional[str]): Target emotion for encoding
            
        Returns:
            Dict[str, any]: Processing results
        """
        results = {
            "original_text": text,
            "operation": operation,
            "timestamp": None
        }
        
        if operation == "analyze":
            results["emotion_analysis"] = self.openai_client.analyze_emotion(text)
            
        elif operation == "encode":
            if not target_emotion:
                raise ValueError("target_emotion required for encode operation")
            results["target_emotion"] = target_emotion
            results["encoded_text"] = self.openai_client.generate_emotion_cipher(text, target_emotion)
            results["original_analysis"] = self.openai_client.analyze_emotion(text)
            results["encoded_analysis"] = self.openai_client.analyze_emotion(results["encoded_text"])
            
        elif operation == "decode":
            results["decode_analysis"] = self.openai_client.decode_emotion_cipher(text)
            results["emotion_analysis"] = self.openai_client.analyze_emotion(text)
            
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        return results


def demo_openai_integration():
    """Demonstrate OpenAI integration functionality"""
    print("=== OpenAI Integration Demo ===")
    
    # Note: This demo requires a valid OpenAI API key
    try:
        # Create OpenAI client (will fail gracefully if no API key)
        openai_client = OpenAIClient()
        
        # Test emotion analysis
        test_text = "I'm feeling absolutely wonderful today! The sunshine makes me so happy!"
        print(f"Analyzing emotion in: {test_text}")
        
        emotion_result = openai_client.analyze_emotion(test_text)
        print(f"Emotion analysis: {emotion_result}")
        
        # Test emotion cipher generation
        cipher_text = openai_client.generate_emotion_cipher(test_text, "sadness")
        print(f"Emotion cipher (sadness): {cipher_text}")
        
        # Test cipher decoding
        decode_result = openai_client.decode_emotion_cipher(cipher_text)
        print(f"Cipher decode analysis: {decode_result}")
        
    except ValueError as e:
        print(f"Demo skipped: {e}")
        print("To run the demo, set your OPENAI_API_KEY environment variable")
        
    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    demo_openai_integration()