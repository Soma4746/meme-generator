#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import find_relevant_memes, MEME_DATABASE

def test_keyword_matching():
    print("🔍 Testing keyword matching...")
    
    # Print all available meme templates and their keywords
    print("\n📋 Available meme templates:")
    for meme_name, meme_data in MEME_DATABASE.items():
        print(f"  - {meme_name}: {meme_data['keywords']}")
    
    # Test with "monday blues"
    test_input = "monday blues"
    print(f"\n🎯 Testing with input: '{test_input}'")
    
    relevant_memes = find_relevant_memes(test_input)
    
    print(f"\n✅ Results: Found {len(relevant_memes)} relevant memes")
    for meme in relevant_memes:
        print(f"  - {meme['name']}: score {meme['score']}")

if __name__ == "__main__":
    test_keyword_matching()
