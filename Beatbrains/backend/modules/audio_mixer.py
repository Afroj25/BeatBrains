# backend/modules/audio_mixer.py
from pydub import AudioSegment
import os

def mix_with_instrumental(vocal_path, mood, output_path):
    """
    Mix vocals with instrumental background
    Vocals are louder, instrumental is background
    """
    
    print(f"🎶 Mixing vocals with {mood} instrumental...")
    
    # Load files
    vocals = AudioSegment.from_wav(vocal_path)
    
    instrumental_file = f"backend/assets/instrumentals/{mood}.mp3"
    
    # Check if instrumental exists
    if not os.path.exists(instrumental_file):
        print(f"⚠️ Warning: {instrumental_file} not found!")
        print("Using vocals only (no instrumental)")
        vocals.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    instrumental = AudioSegment.from_mp3(instrumental_file)
    
    # VOLUME ADJUSTMENT (Key changes here!)
    # Make vocals LOUDER
    vocals = vocals + 6  # Increase vocals by 6dB
    
    # Make instrumental QUIETER (background music)
    instrumental = instrumental - 15  # Reduce by 15dB (was -8 before)
    
    # Match lengths
    if len(instrumental) < len(vocals):
        # Loop instrumental if too short
        repeats = (len(vocals) // len(instrumental)) + 1
        instrumental = instrumental * repeats
    
    # Trim instrumental to match vocals
    instrumental = instrumental[:len(vocals)]
    
    # Add fade in/out to instrumental for smooth start/end
    instrumental = instrumental.fade_in(1000).fade_out(1000)  # 1 second fades
    
    # Mix: overlay vocals on top of instrumental
    mixed = instrumental.overlay(vocals)
    
    # Optional: Add slight compression to make vocals punchier
    # This increases perceived loudness
    mixed = mixed.normalize()  # Normalize to maximize volume without clipping
    
    # Export
    mixed.export(output_path, format="mp3", bitrate="192k")
    
    print(f"✅ Mixed audio saved: {output_path}")
    print(f"   Vocals: +6dB (louder)")
    print(f"   Instrumental: -15dB (background)")
    
    return output_path


def mix_vocals_only(vocal_path, output_path):
    """
    Export vocals only without instrumental
    Useful for testing or when instrumental is missing
    """
    vocals = AudioSegment.from_wav(vocal_path)
    vocals.export(output_path, format="mp3", bitrate="192k")
    return output_path
