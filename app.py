"""
AI Prompt Reconstructor & Enhancer - FULLY FIXED VERSION
Fixes:
  1. Template case mismatch (Index.html -> index.html)
  2. Missing /validate_api_key endpoint
  3. Missing response fields (transcript_length, segments, transcript_preview)
  4. youtube-transcript-api v1.x compatibility
  5. JSON parse: strip markdown fences before parsing Gemini responses
"""

from flask import Flask, render_template, request, jsonify
import re
import json
import os
import requests
from dotenv import load_dotenv
import traceback

load_dotenv()

# SMART IMPORT
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_AVAILABLE = True
except ImportError:
    YT_AVAILABLE = False

GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except Exception:
    pass

app = Flask(__name__, template_folder='templates', static_folder='static')

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
model = None
AI_MODE = "builtin"


def configure_genai(api_key=None):
    global AI_MODE, model
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
    if not key_to_use:
        AI_MODE = "builtin"
        model = None
        return False
    if GEMINI_AVAILABLE:
        try:
            import google.generativeai as genai
            genai.configure(api_key=key_to_use)
            model = genai.GenerativeModel('gemini-1.5-flash')
            AI_MODE = "gemini"
            return True
        except Exception as e:
            print(f"Gemini library config failed: {str(e)}")
    AI_MODE = "gemini-rest"
    return True


def gemini_call_rest(prompt, api_key):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "topK": 40, "topP": 0.95, "maxOutputTokens": 2048}
    }
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        raise Exception(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(f"REST call failed: {str(e)}")


configure_genai(GEMINI_API_KEY)


# ============================================
# YOUTUBE TRANSCRIPT
# ============================================
def extract_video_id(url):
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url.strip()):
        return url.strip()
    return None


def get_text_from_entry(entry):
    """FIX: Support both v0.x dict-style and v1.x attribute-style entries."""
    try:
        return entry['text']
    except (TypeError, KeyError):
        pass
    try:
        return entry.text
    except AttributeError:
        return str(entry)


def get_transcript(video_id):
    if not YT_AVAILABLE:
        return {'success': False, 'error': 'youtube-transcript-api not installed'}
    try:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except Exception:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        segments = list(transcript_list)
        full_text = ' '.join([get_text_from_entry(e) for e in segments])

        if full_text.strip():
            return {'success': True, 'transcript': full_text, 'segments': len(segments)}
        return {'success': False, 'error': 'Transcript is empty'}
    except Exception as e:
        return {'success': False, 'error': f'Could not fetch transcript: {str(e)}'}


# ============================================
# BUILT-IN AI ENGINE
# ============================================
class BuiltInAI:
    @staticmethod
    def analyze_content(transcript):
        text_lower = transcript.lower()
        words = text_lower.split()
        word_count = len(words)
        categories = {
            'programming': ['code', 'python', 'javascript', 'function', 'api', 'github'],
            'ai_ml': ['ai', 'machine learning', 'neural', 'model', 'gemini'],
            'business': ['business', 'marketing', 'startup', 'revenue', 'strategy'],
            'tutorial': ['tutorial', 'how to', 'guide', 'learn', 'step'],
            'design': ['design', 'ui', 'ux', 'figma', 'layout'],
        }
        detected = {cat: sum(text_lower.count(kw) for kw in kws) for cat, kws in categories.items()}
        detected = {k: v for k, v in detected.items() if v > 0}
        sorted_categories = sorted(detected.items(), key=lambda x: x[1], reverse=True)
        key_phrases = list(set([w for w in words if len(w) > 4]))[:5]
        return {
            'categories': sorted_categories[:3],
            'key_phrases': key_phrases,
            'content_type': 'Tutorial/How-To' if 'tutorial' in text_lower else 'General',
            'word_count': word_count,
            'complexity': 'Advanced' if word_count > 2000 else 'Intermediate' if word_count > 800 else 'Beginner'
        }

    @staticmethod
    def reconstruct_prompts(transcript, analysis):
        key_phrases = analysis['key_phrases']
        primary_topic = ', '.join(key_phrases[:3]) if key_phrases else 'this topic'
        return [
            {'type': '📝 Tutorial Prompt', 'prompt': f"Create a detailed step-by-step tutorial about {primary_topic}.", 'confidence': 85},
            {'type': '🧠 Explainer Prompt', 'prompt': f"Explain {primary_topic} in detail with examples.", 'confidence': 80},
            {'type': '📋 Content Prompt', 'prompt': f"Create content about {primary_topic} covering key aspects.", 'confidence': 75},
        ]

    @staticmethod
    def enhance_prompts(prompts, analysis):
        enhanced = []
        for p in prompts:
            enhanced_prompt = (
                f"You are an expert content creator.\n\n"
                f"MAIN TASK: {p['prompt']}\n\n"
                f"REQUIREMENTS:\n"
                f"1. Use clear structure with headings\n"
                f"2. Provide practical examples\n"
                f"3. Include actionable steps\n"
                f"4. Explain complex concepts simply\n"
                f"5. Add resources for further learning\n\n"
                f"OUTPUT: Professional, engaging content optimized for learning."
            )
            enhanced.append({'type': p['type'], 'original': p['prompt'], 'enhanced': enhanced_prompt, 'improvement_score': 90})
        return enhanced


# ============================================
# GEMINI AI ENGINE
# ============================================
def _parse_gemini_json(response_text):
    """FIX: Strip markdown fences before parsing JSON from Gemini responses."""
    cleaned = re.sub(r'```(?:json)?', '', response_text).strip()
    json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    raise ValueError("No valid JSON found in response")


class GeminiAI:
    @staticmethod
    def process_with_gemini(transcript, api_key=None):
        try:
            prompt = f"""Analyze this transcript:

{transcript[:2000]}

Respond ONLY with raw JSON (no markdown, no backticks):
{{
    "content_type": "type",
    "main_topics": ["topic1", "topic2"],
    "complexity": "Intermediate",
    "reconstructed_prompts": [
        {{"type": "type", "prompt": "prompt", "confidence": 85}}
    ],
    "summary": "summary"
}}"""
            if api_key or AI_MODE == "gemini-rest":
                response_text = gemini_call_rest(prompt, api_key or GEMINI_API_KEY)
            elif model:
                response_text = model.generate_content(prompt).text
            else:
                return {'success': False, 'error': 'No AI model configured'}

            return {'success': True, 'data': _parse_gemini_json(response_text)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def enhance_with_gemini(prompts_data, api_key=None):
        try:
            prompts_text = "\n".join([f"- {p['prompt']}" for p in prompts_data])
            prompt = f"""Enhance these prompts:

{prompts_text}

Respond ONLY with raw JSON (no markdown, no backticks):
{{
    "enhanced_prompts": [
        {{"type": "type", "original": "original", "enhanced": "enhanced", "improvement_score": 95}}
    ]
}}"""
            if api_key or AI_MODE == "gemini-rest":
                response_text = gemini_call_rest(prompt, api_key or GEMINI_API_KEY)
            elif model:
                response_text = model.generate_content(prompt).text
            else:
                return {'success': False, 'error': 'No AI model configured'}

            return {'success': True, 'data': _parse_gemini_json(response_text)}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# ============================================
# ROUTES
# ============================================
@app.route('/')
def index():
    # FIX: template renamed to lowercase index.html (case-sensitive on Linux/Vercel)
    try:
        return render_template('index.html', ai_mode=AI_MODE)
    except Exception as e:
        return f"Error loading template: {str(e)}", 500


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json or {}
        url = data.get('url', '').strip()
        api_key = data.get('api_key', '').strip()

        if api_key:
            configure_genai(api_key)

        if not url:
            return jsonify({'success': False, 'error': 'Please enter a YouTube URL'})

        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({'success': False, 'error': 'Invalid YouTube URL'})

        transcript_result = get_transcript(video_id)
        if not transcript_result['success']:
            return jsonify({'success': False, 'error': transcript_result['error']})

        transcript = transcript_result['transcript']

        # FIX: add the fields the frontend reads but the old code never sent
        transcript_length = len(transcript)
        segments = transcript_result.get('segments', 0)
        transcript_preview = transcript[:400] + ('...' if len(transcript) > 400 else '')

        # Try Gemini first
        if (AI_MODE in ("gemini", "gemini-rest") or api_key) and (model or api_key):
            ai_result = GeminiAI.process_with_gemini(transcript, api_key)
            if ai_result['success']:
                gemini_data = ai_result['data']
                reconstructed = gemini_data.get('reconstructed_prompts', [])
                enhance_result = GeminiAI.enhance_with_gemini(reconstructed, api_key)
                enhanced = (
                    enhance_result['data'].get('enhanced_prompts', [])
                    if enhance_result['success']
                    else BuiltInAI.enhance_prompts(reconstructed, BuiltInAI.analyze_content(transcript))
                )
                return jsonify({
                    'success': True,
                    'video_id': video_id,
                    'ai_mode': 'Google Gemini AI',
                    'transcript_length': transcript_length,
                    'segments': segments,
                    'transcript_preview': transcript_preview,
                    'analysis': {
                        'content_type': gemini_data.get('content_type', 'General'),
                        'main_topics': gemini_data.get('main_topics', []),
                        'complexity': gemini_data.get('complexity', 'Intermediate'),
                    },
                    'reconstructed_prompts': reconstructed,
                    'enhanced_prompts': enhanced
                })

        # Built-in fallback
        analysis = BuiltInAI.analyze_content(transcript)
        reconstructed = BuiltInAI.reconstruct_prompts(transcript, analysis)
        enhanced = BuiltInAI.enhance_prompts(reconstructed, analysis)

        return jsonify({
            'success': True,
            'video_id': video_id,
            'ai_mode': 'Built-in AI Engine (Free)',
            'transcript_length': transcript_length,
            'segments': segments,
            'transcript_preview': transcript_preview,
            'analysis': {
                'content_type': analysis['content_type'],
                'main_topics': analysis['key_phrases'],
                'complexity': analysis['complexity'],
            },
            'reconstructed_prompts': reconstructed,
            'enhanced_prompts': enhanced
        })

    except Exception as e:
        print(f"Analysis error: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})


# FIX: /validate_api_key was called by frontend but never existed in backend (404)
@app.route('/validate_api_key', methods=['POST'])
def validate_api_key():
    try:
        data = request.json or {}
        api_key = data.get('api_key', '').strip()

        if not api_key:
            return jsonify({'success': False, 'error': 'No API key provided'})

        test_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={api_key}"
        )
        payload = {"contents": [{"parts": [{"text": "Say OK"}]}], "generationConfig": {"maxOutputTokens": 5}}
        response = requests.post(test_url, headers={"Content-Type": "application/json"}, json=payload, timeout=15)

        if response.status_code == 200:
            configure_genai(api_key)
            return jsonify({'success': True, 'message': 'API key is valid ✅'})
        elif response.status_code == 403 or response.status_code == 400:
            return jsonify({'success': False, 'error': 'Invalid API key ❌'})
        elif response.status_code == 429:
            return jsonify({'success': False, 'error': 'Rate limit reached — key is valid but quota exceeded'})
        else:
            return jsonify({'success': False, 'error': f'API returned status {response.status_code}'})

    except requests.Timeout:
        return jsonify({'success': False, 'error': 'Validation timed out.'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Validation error: {str(e)}'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': f'Server error: {str(error)}'}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 AI Prompt Reconstructor & Enhancer")
    print("=" * 60)
    print(f"🤖 AI Mode: {AI_MODE.upper()}")
    print(f"📦 YouTube API: {'✅ Available' if YT_AVAILABLE else '❌ Not installed'}")
    print(f"🔑 Gemini SDK: {'✅ Available' if GEMINI_AVAILABLE else '⚠️  Using REST fallback'}")
    print("=" * 60 + "\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
