#!/usr/bin/env python3
"""
Emotion Cipher System - Hardcoded Demo Examples
Runs predefined examples to demonstrate the system capabilities
"""

from emotion_cipher_system import EmotionCipherSystem


def hardcoded_demo():
    """Demonstration with predefined hardcoded examples"""
    print("EMOTION CIPHER - Decoding Feelings through Code")
    print("=" * 60)
    print("Hardcoded Examples Demo")
    print("=" * 60)
    
    # Initialize system
    system = EmotionCipherSystem()
    
    # Check system status
    status = system.get_system_status()
    print("System Status:")
    print(f"  Encryption: {'✅ Ready' if status['encryption']['keys_ready'] else '⚙️ Setting up...'}")
    print(f"  Emotion Analysis: {'✅ Available' if status['emotion_analysis']['available'] else '❌ Not configured'}")
    print()
    
    # Hardcoded examples from the original PDF
    examples = [
        {
            "category": "PDF Example 1 - Mixed Emotions",
            "message": "Feeling ecstatic about joining the new AI research team, though a bit anxious about the deadlines ahead."
        },
        {
            "category": "PDF Example 2 - Negative Emotions",
            "message": "I can't believe I failed that test again. I'm so disappointed and frustrated right now."
        },
        {
            "category": "PDF Example 3 - Positive Emotions",
            "message": "Finally got the job offer! I'm thrilled and can't wait to start this new journey."
        },
        {
            "category": "Additional Example - Love & Excitement",
            "message": "I absolutely love this new technology! It's going to revolutionize everything we do."
        },
        {
            "category": "Additional Example - Worry & Stress",
            "message": "I'm really worried about the presentation tomorrow. What if something goes wrong?"
        }
    ]
    
    print("Processing hardcoded examples...")
    
    successful_count = 0
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example['category']}")
        
        # Process in PDF format
        result = system.pdf_format_demo(example['message'])
        
        if result.get('success'):
            successful_count += 1
            print("✅ Processing completed successfully!")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("DEMO SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total Examples: {len(examples)}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {len(examples) - successful_count}")
    print(f"Success Rate: {(successful_count/len(examples))*100:.1f}%")
    
    # System statistics
    final_status = system.get_system_status()
    stats = final_status['statistics']
    print(f"\nSystem Statistics:")
    print(f"  Total Operations: {stats['total_operations']}")
    print(f"  Successful Operations: {stats['successful_operations']}")
    
    print(f"\n✨ Hardcoded demo completed!")
    print(f"💡 To run interactive mode: python emotion_cipher_system.py")


def quick_test():
    """Quick test with a single example"""
    print("EMOTION CIPHER - Quick Test")
    print("=" * 40)
    
    system = EmotionCipherSystem()
    
    test_message = "This is a quick test of the emotion cipher system!"
    print(f"Testing with: '{test_message}'\n")
    
    result = system.pdf_format_demo(test_message)
    
    if result.get('success'):
        print("\n✅ Quick test passed!")
    else:
        print(f"\n❌ Quick test failed: {result.get('error')}")


def batch_test():
    """Test multiple messages in batch mode"""
    print("EMOTION CIPHER - Batch Processing Test")
    print("=" * 50)
    
    system = EmotionCipherSystem()
    
    batch_messages = [
        "I'm excited about machine learning!",
        "This encryption is very secure.",
        "Artificial intelligence is fascinating.",
        "I'm worried about data privacy.",
        "This system works perfectly!"
    ]
    
    print(f"Processing {len(batch_messages)} messages in batch...\n")
    
    for i, message in enumerate(batch_messages, 1):
        print(f"Message {i}/{len(batch_messages)}:")
        result = system.process_message(message, pdf_format=True)
        
        if result.get('success'):
            decrypt_result = system.decrypt_message(
                result['encrypted_message'], 
                pdf_format=True,
                detected_emotion=result.get('detected_emotion', 'Unknown')
            )
            print("✅ Success\n")
        else:
            print(f"❌ Failed: {result.get('error')}\n")
    
    print("Batch test completed!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            quick_test()
        elif sys.argv[1] == "batch":
            batch_test()
        else:
            print("Usage:")
            print("  python demo_hardcoded.py          # Full hardcoded demo")
            print("  python demo_hardcoded.py quick    # Quick single test")
            print("  python demo_hardcoded.py batch    # Batch processing test")
    else:
        hardcoded_demo()