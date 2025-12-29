from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from modules.text_processor import format_for_singing
from modules.voice_generator import generate_singing_voice, generate_singing_voice_fast
from modules.audio_mixer import mix_with_instrumental
import os
import time

app = Flask(__name__)
CORS(app)

@app.route('/generate-song', methods=['POST'])
def generate_song():
    try:
        data = request.json
        text = data.get('text', '')
        mood = data.get('mood', 'happy')
        
        # Validate
        if not text or len(text) > 500:
            return jsonify({
                'status': 'error',
                'message': 'Text required (max 500 chars)'
            }), 400
        
        if mood not in ['happy', 'sad', 'motivational']:
            mood = 'happy'
        
        # Generate unique filename
        timestamp = int(time.time())
        temp_vocal = f"output/vocal_{timestamp}.wav"
        final_song = f"output/song_{timestamp}.mp3"
        
        print("=" * 70)
        print(f"🎵 NEW SONG REQUEST")
        print(f"📝 Text ({len(text)} chars): {text[:100]}...")
        print(f"🎭 Mood: {mood}")
        print("=" * 70)
        
        # Choose generation method based on text length
        if len(text) < 100:
            # Fast mode for short texts
            print("⚡ Using fast generation mode")
            generate_singing_voice_fast(text, temp_vocal)
        else:
            # Chunked mode for longer texts
            chunks = format_for_singing(text)
            generate_singing_voice(chunks, temp_vocal)
        
        print(f"🎶 Mixing with {mood} instrumental...")
        mix_with_instrumental(temp_vocal, mood, final_song)
        
        # Cleanup temp file
        if os.path.exists(temp_vocal):
            os.remove(temp_vocal)
        
        print(f"✅ Song complete: {final_song}")
        print("=" * 70)
        
        return jsonify({
            'status': 'success',
            'song_url': f'/output/song_{timestamp}.mp3'
        })
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/output/<filename>')
def serve_audio(filename):
    try:
        file_path = os.path.join('..', 'output', filename)
        return send_file(file_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'message': 'BeatBrains API with Bark AI Singing',
        'endpoints': ['/generate-song', '/output/<filename>']
    })

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    print("=" * 70)
    print("🎵 BeatBrains Backend with Bark AI Starting...")
    print("📁 Output directory ready")
    print("🌐 API available at: http://127.0.0.1:5000")
    print("🔗 CORS enabled")
    print("🎤 Bark AI singing synthesis ready")
    print("=" * 70)
    app.run(debug=True, port=5000, host='127.0.0.1')