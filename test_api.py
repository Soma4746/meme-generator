#!/usr/bin/env python3

import requests
import json

def test_api():
    url = "http://127.0.0.1:5000/generate-meme"
    data = {
        "prompt": "monday blues",
        "relevantOnly": True
    }
    
    print(f"🔍 Testing API with: {data}")
    
    try:
        response = requests.post(url, json=data)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Generated {len(result.get('memes', []))} memes")
            print(f"📋 Response keys: {list(result.keys())}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_api()
