# backend/modules/voice_generator.py

# APPLY PATCH FIRST - before importing bark
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import bark_patch  # ← This must be FIRST

import warnings
warnings.filterwarnings('ignore')

# Environment settings for Bark
os.environ['SUNO_ENABLE_MPS'] = 'False'
os.environ['SUNO_USE_SMALL_MODELS'] = 'True'

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np

# Preload models on first import
print("🎵 Loading Bark AI models...")
try:
    preload_models()
    print("✅ Bark models loaded successfully!")
except Exception as e:
    print(f"⚠️ Warning: Bark preload failed: {e}")
    print("Models will load on first generation.")


def generate_singing_voice(text_chunks, output_path):
    """Generate singing audio using Bark AI"""
    
    print(f"🎤 Generating singing voice with Bark AI...")
    print(f"📊 Processing {len(text_chunks)} chunk(s)")
    
    all_audio = []
    
    for i, chunk in enumerate(text_chunks):
        print(f"  🎵 Chunk {i+1}/{len(text_chunks)}: {chunk[:60]}...")
        
        singing_prompt = f"♪ {chunk} ♪"
        
        try:
            audio_array = generate_audio(
                singing_prompt,
                history_prompt="v2/en_speaker_6",
                text_temp=0.7,
                waveform_temp=0.7
            )
            
            all_audio.append(audio_array)
            duration = len(audio_array) / SAMPLE_RATE
            print(f"  ✅ Chunk {i+1} generated ({duration:.1f}s)")
            
        except Exception as e:
            print(f"  ⚠️ Chunk {i+1} failed: {e}")
            silence = np.zeros(SAMPLE_RATE * 2, dtype=np.float32)
            all_audio.append(silence)
    
    print("🔗 Combining audio chunks...")
    full_audio = np.concatenate(all_audio)
    
    max_val = np.abs(full_audio).max()
    if max_val > 0:
        full_audio = full_audio / max_val * 0.9
    
    full_audio = (full_audio * 32767).astype(np.int16)
    
    write_wav(output_path, SAMPLE_RATE, full_audio)
    
    total_duration = len(full_audio) / SAMPLE_RATE
    print(f"✅ Singing voice complete: {output_path} ({total_duration:.1f}s)")
    
    return output_path


def generate_singing_voice_fast(text, output_path):
    """Fast version for short texts"""
    
    print(f"🎤 Generating singing voice (fast mode)...")
    
    singing_prompt = f"♪ {text} ♪"
    
    audio_array = generate_audio(
        singing_prompt,
        history_prompt="v2/en_speaker_6",
        text_temp=0.7,
        waveform_temp=0.7
    )
    
    max_val = np.abs(audio_array).max()
    if max_val > 0:
        audio_array = audio_array / max_val * 0.9
    
    audio_array = (audio_array * 32767).astype(np.int16)
    
    write_wav(output_path, SAMPLE_RATE, audio_array)
    
    duration = len(audio_array) / SAMPLE_RATE
    print(f"✅ Singing voice complete ({duration:.1f}s)")
    
    return output_path