#!/usr/bin/env python3
"""
Test script for the Marathi Font Converter
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from converters.font_detector import FontDetector
from converters.font_mapper import FontMapper

def test_font_detection_and_conversion():
    """Test the font detection and conversion functionality"""
    
    print("🔍 Testing Marathi Font Converter")
    print("=" * 50)
    
    # Initialize components
    detector = FontDetector()
    mapper = FontMapper()
    
    # Test cases with sample DVTT Yogesh text (simulated)
    test_cases = [
        {
            'name': 'DVTT Yogesh Sample',
            'text': 'namaskara',  # Simulated non-Unicode text
            'expected_font': 'dvtt_yogesh'
        },
        {
            'name': 'English Text',
            'text': 'Hello World',
            'expected_font': 'english'
        },
        {
            'name': 'Unicode Marathi',
            'text': 'नमस्कार',
            'expected_font': 'unicode_marathi'
        },
        {
            'name': 'Mixed Content',
            'text': 'Hello नमस्कार World',
            'expected_font': 'unicode_marathi'
        }
    ]
    
    print("\n📋 Running Font Detection Tests:")
    print("-" * 40)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {case['name']}")
        print(f"   Input: '{case['text']}'")
        
        # Detect fonts
        detection = detector.detect_fonts(case['text'])
        dominant_font = detector.get_dominant_font(case['text'])
        
        print(f"   Detected: {dominant_font}")
        
        # Show detailed detection results
        detected_fonts = [font for font, info in detection.items() if info['detected']]
        if detected_fonts:
            print(f"   All detected: {', '.join(detected_fonts)}")
        
        # Test conversion
        converted = mapper.convert_text(case['text'])
        print(f"   Converted: '{converted}'")
        
        if converted != case['text']:
            print("   ✅ Conversion applied")
        else:
            print("   ℹ️  No conversion needed")
    
    print("\n🔧 Testing Conversion Functions:")
    print("-" * 40)
    
    # Test specific conversion functions
    dvtt_sample = "namaskara"  # This would be actual DVTT Yogesh characters in real use
    print(f"\nDVTT Yogesh conversion test:")
    print(f"Input: '{dvtt_sample}'")
    converted_dvtt = mapper.convert_dvtt_yogesh_to_unicode(dvtt_sample)
    print(f"Output: '{converted_dvtt}'")
    
    # Test preservation features
    mixed_text = "Hello namaskara World 123"
    print(f"\nPreservation test:")
    print(f"Input: '{mixed_text}'")
    preserved = mapper.convert_with_preservation(mixed_text)
    print(f"Output: '{preserved}'")
    
    print("\n📊 Testing Statistics:")
    print("-" * 40)
    
    original = "namaskara world"
    converted = mapper.convert_text(original)
    stats = mapper.get_conversion_stats(original, converted)
    
    print(f"Original length: {stats['original_length']}")
    print(f"Converted length: {stats['converted_length']}")
    print(f"Original fonts: {stats['original_fonts']}")
    print(f"Converted fonts: {stats['converted_fonts']}")
    
    print("\n✅ All tests completed!")
    print("\n📝 Note: This is a demonstration with simulated data.")
    print("   In actual use, DVTT Yogesh and DTT Dhruv fonts would have")
    print("   specific character mappings that this system would convert")
    print("   to proper Unicode Devanagari script.")

if __name__ == "__main__":
    test_font_detection_and_conversion()