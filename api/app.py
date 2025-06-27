import requests
import random
import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Comprehensive meme template database with keywords and caption patterns
MEME_DATABASE = {
    # Popular meme templates with their characteristics
    "Drake Pointing": {
        "keywords": ["choice", "prefer", "better", "vs", "instead", "rather"],
        "patterns": [
            "Not: {topic}\nYes: {topic} but better",
            "{topic}? Nah\n{topic} improved? Yes!",
            "Regular {topic}\nUpgraded {topic}"
        ]
    },
    "Distracted Boyfriend": {
        "keywords": ["temptation", "choice", "new", "old", "switching", "leaving"],
        "patterns": [
            "Me with {topic}",
            "When {topic} looks appealing",
            "Choosing {topic} over everything else"
        ]
    },
    "Woman Yelling at Cat": {
        "keywords": ["argument", "angry", "frustrated", "explaining", "confused", "monday", "blues", "annoyed", "mad"],
        "patterns": [
            "Me explaining {topic}",
            "When someone doesn't understand {topic}",
            "Trying to justify {topic}"
        ]
    },
    "This is Fine": {
        "keywords": ["problem", "crisis", "disaster", "broken", "failing", "chaos", "monday", "blues", "stress", "work"],
        "patterns": [
            "Everything about {topic} is fine",
            "When {topic} goes wrong but you pretend it's okay",
            "Me dealing with {topic} problems"
        ]
    },
    "Expanding Brain": {
        "keywords": ["levels", "evolution", "smart", "genius", "upgrade", "advanced"],
        "patterns": [
            "Basic {topic}\nAdvanced {topic}\nExpert {topic}\nGalaxy brain {topic}",
            "Learning about {topic} be like",
            "Stages of understanding {topic}"
        ]
    },
    "Surprised Pikachu": {
        "keywords": ["unexpected", "obvious", "predictable", "shocked", "surprised"],
        "patterns": [
            "When {topic} happens exactly as expected",
            "Me when {topic} goes wrong (again)",
            "Surprised by {topic} consequences"
        ]
    },
    "Change My Mind": {
        "keywords": ["opinion", "fact", "truth", "debate", "convince"],
        "patterns": [
            "{topic} is the best. Change my mind.",
            "{topic} is overrated. Change my mind.",
            "Everyone should try {topic}. Change my mind."
        ]
    },
    "Two Buttons": {
        "keywords": ["choice", "decision", "dilemma", "difficult", "both"],
        "patterns": [
            "Do {topic} properly\nDo {topic} quickly",
            "Enjoy {topic}\nBe responsible about {topic}",
            "Learn {topic}\nProcrastinate about {topic}"
        ]
    },
    "Monkey Puppet": {
        "keywords": ["awkward", "caught", "embarrassed", "guilty", "oops", "monday", "tired", "sleepy"],
        "patterns": [
            "When someone mentions {topic}",
            "Me pretending I don't know about {topic}",
            "Getting caught with {topic}"
        ]
    },
    "Success Kid": {
        "keywords": ["success", "win", "achievement", "finally", "accomplished"],
        "patterns": [
            "Finally mastered {topic}",
            "Successfully completed {topic}",
            "When {topic} works perfectly"
        ]
    },
    "Tired Spongebob": {
        "keywords": ["tired", "exhausted", "monday", "blues", "sleepy", "drained", "worn out"],
        "patterns": [
            "Me dealing with {topic}",
            "When {topic} hits you hard",
            "Trying to handle {topic} like"
        ]
    },
    "Crying Cat": {
        "keywords": ["sad", "crying", "monday", "blues", "depressed", "upset", "emotional"],
        "patterns": [
            "Me when {topic} happens",
            "Dealing with {topic} be like",
            "When {topic} ruins your day"
        ]
    },
    "Grumpy Cat": {
        "keywords": ["grumpy", "annoyed", "monday", "hate", "dislike", "irritated", "blues"],
        "patterns": [
            "Me when dealing with {topic}",
            "My face when {topic} happens",
            "How I feel about {topic}"
        ]
    }
}

# Universal caption patterns that work with any topic
UNIVERSAL_PATTERNS = [
    "When {topic} hits different",
    "Me trying to understand {topic}",
    "That moment when {topic}",
    "POV: You're dealing with {topic}",
    "Me explaining {topic} to my friends",
    "When someone mentions {topic}",
    "Me vs {topic}",
    "The reality of {topic}",
    "When {topic} actually works",
    "Me after discovering {topic}",
    "Everyone else vs me with {topic}",
    "When {topic} goes exactly as planned",
    "Me pretending to understand {topic}",
    "The truth about {topic}",
    "When {topic} becomes your personality",
    "Me avoiding {topic} responsibilities",
    "When {topic} is life",
    "The stages of {topic}",
    "Me overthinking {topic}",
    "When {topic} hits too close to home",
    "Nobody:\nMe: {topic}",
    "When {topic} is your love language",
    "Me: I don't need {topic}\nAlso me:",
    "When {topic} chooses violence",
    "Me trying to explain {topic} to boomers",
    "When {topic} is your Roman Empire",
    "The {topic} to my problems",
    "When {topic} is giving main character energy",
    "Me when {topic} is actually good",
    "When {topic} hits different at 2am",
    "The way {topic} has me in a chokehold",
    "When {topic} is lowkey fire",
    "Me defending {topic} for no reason",
    "When {topic} is your comfort zone",
    "The {topic} agenda is real",
    "When {topic} is your therapy",
    "Me gatekeeping {topic}",
    "When {topic} is your personality trait",
    "The {topic} experience hits different",
    "When {topic} is sus but you love it",
    "Me trying to avoid {topic}",
    "Living with {topic} be like",
    "When {topic} hits you at 3am",
    "Me explaining why {topic} is important"
]

def extract_keywords(text):
    """Extract meaningful keywords from user input"""
    # Remove common words and extract meaningful terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}

    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

def find_relevant_memes(user_input):
    """Find all meme templates relevant to user input"""
    user_keywords = extract_keywords(user_input)
    user_input_lower = user_input.lower()

    relevant_memes = []

    # Check each meme template for relevance
    for meme_name, meme_data in MEME_DATABASE.items():
        relevance_score = 0

        # Check if any meme keywords match user input
        for keyword in meme_data["keywords"]:
            if keyword in user_input_lower:
                relevance_score += 2
            # Check for partial matches
            for user_keyword in user_keywords:
                if keyword in user_keyword or user_keyword in keyword:
                    relevance_score += 1

        # If relevant, add to list
        if relevance_score > 0:
            relevant_memes.append({
                "name": meme_name,
                "data": meme_data,
                "score": relevance_score
            })

    # Sort by relevance score
    relevant_memes.sort(key=lambda x: x["score"], reverse=True)
    return relevant_memes

def generate_caption_for_topic(topic, pattern=None):
    """Generate a caption for any topic using patterns"""
    if pattern:
        return pattern.format(topic=topic)
    else:
        # Use universal patterns
        return random.choice(UNIVERSAL_PATTERNS).format(topic=topic)

def get_all_meme_templates():
    """Fetch all available meme templates from Imgflip"""
    try:
        response = requests.get("https://api.imgflip.com/get_memes")
        data = response.json()
        return data.get("data", {}).get("memes", [])
    except Exception as e:
        print(f"Error fetching memes: {e}")
        return []

@app.route('/generate-meme', methods=['POST'])
def generate_meme():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "").strip()
        relevant_only = data.get("relevantOnly", False)

        if not user_prompt:
            return jsonify({"error": "Please provide a prompt"}), 400

        if relevant_only:
            print(f"🎯 Generating RELEVANT memes for: '{user_prompt}'")
        else:
            print(f"🎯 Generating ALL available memes for: '{user_prompt}'")

        # Get all available meme templates
        print("⏳ Fetching all meme templates...")
        all_memes = get_all_meme_templates()
        if not all_memes:
            raise Exception("Could not fetch meme templates")

        print(f"📋 Found {len(all_memes)} total meme templates")

        # Find relevant meme types based on user input
        relevant_meme_types = find_relevant_memes(user_prompt)
        print(f"🎯 Found {len(relevant_meme_types)} relevant meme types")

        memes_generated = []
        used_templates = set()

        # Generate multiple memes for each relevant meme type
        for relevant_meme in relevant_meme_types:
            meme_name = relevant_meme["name"]
            meme_data = relevant_meme["data"]

            # Generate multiple captions for each meme type using different patterns
            captions_to_generate = min(len(meme_data["patterns"]), 3)  # Generate up to 3 different captions per meme type

            for i in range(captions_to_generate):
                # Use different templates for variety
                available_templates = [m for m in all_memes if m["id"] not in used_templates]
                if not available_templates:
                    break

                template = random.choice(available_templates)
                used_templates.add(template["id"])

                # Generate caption using specific patterns for this meme type
                if meme_data["patterns"]:
                    caption = meme_data["patterns"][i % len(meme_data["patterns"])].format(topic=user_prompt)
                else:
                    caption = generate_caption_for_topic(user_prompt)

                memes_generated.append({
                    "image": template["url"],
                    "caption": caption,
                    "template_name": template["name"],
                    "meme_type": meme_name,
                    "relevance_score": relevant_meme["score"]
                })

                print(f"✅ Generated: {template['name']} - {caption[:50]}...")

        # Generate universal memes if not relevant_only mode OR if we need more variety
        if not relevant_only or len(memes_generated) < 12:
            if len(memes_generated) == 0:
                print(f"🔄 No relevant memes found, generating universal memes as fallback...")
            elif len(memes_generated) < 12:
                print(f"� Adding universal memes for more variety ({len(memes_generated)} so far)...")
            else:
                print(f"�🎲 Generating memes for ALL remaining templates...")

            available_templates = [m for m in all_memes if m["id"] not in used_templates]
            print(f"📊 Processing {len(available_templates)} additional templates...")

            # Calculate how many more memes we want
            if relevant_only and len(memes_generated) == 0:
                limit = 15  # Fallback when no relevant memes found
            elif relevant_only and len(memes_generated) < 12:
                limit = 12 - len(memes_generated)  # Fill up to 12 total memes
            else:
                limit = 50  # Normal mode

            for template in available_templates[:limit]:
                caption = generate_caption_for_topic(user_prompt)

                memes_generated.append({
                    "image": template["url"],
                    "caption": caption,
                    "template_name": template["name"],
                    "meme_type": "Universal",
                    "relevance_score": 0
                })

                if len(memes_generated) % 25 == 0:  # Progress update every 25 memes
                    print(f"✅ Generated {len(memes_generated)} memes so far...")
        else:
            print(f"🎯 Relevant-only mode: Skipping universal templates")

        # Sort by relevance score (highest first)
        memes_generated.sort(key=lambda x: x["relevance_score"], reverse=True)

        print(f"🎉 Successfully generated {len(memes_generated)} memes!")

        return jsonify({
            "memes": memes_generated,
            "count": len(memes_generated),
            "prompt": user_prompt,
            "total_templates_available": len(all_memes)
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

# For Vercel deployment
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    print("🔥 Starting Universal Meme Generator Server...")
    print("🎯 Generates ALL relevant memes for any topic!")
    print("� No limits - works with any sentence or phrase")
    print("🚀 No AI dependencies - pure pattern-based generation")
    app.run(debug=True)


