# backend/modules/text_processor.py
import re

def format_for_singing(text, max_length=500):
    """
    Convert text into singable format optimized for Bark
    Splits into chunks of ~80-120 characters for best quality
    """
    
    # Truncate to max length
    text = text[:max_length].strip()
    
    # Clean up text
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s,.!?\'-]', '', text)  # Remove special chars
    
    # Split by sentences
    sentences = re.split(r'([.!?]+)', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Combine sentences back
    combined = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
            combined.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            combined.append(sentences[i])
            i += 1
    
    # Create chunks (Bark works best with 80-120 char chunks)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in combined:
        sentence_len = len(sentence)
        
        # If adding this sentence keeps us under 120 chars, add it
        if current_length + sentence_len <= 120:
            current_chunk.append(sentence)
            current_length += sentence_len
        else:
            # Save current chunk and start new one
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_len
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # If no chunks created (very short text), just use the text
    if not chunks:
        chunks = [text]
    
    # If text is longer than 120 chars but didn't split, force split by words
    if len(chunks) == 1 and len(chunks[0]) > 120:
        words = chunks[0].split()
        chunks = []
        current = []
        current_len = 0
        
        for word in words:
            if current_len + len(word) + 1 <= 120:
                current.append(word)
                current_len += len(word) + 1
            else:
                if current:
                    chunks.append(' '.join(current))
                current = [word]
                current_len = len(word)
        
        if current:
            chunks.append(' '.join(current))
    
    print(f"📝 Text formatted into {len(chunks)} singing chunk(s):")
    for i, chunk in enumerate(chunks):
        print(f"   Chunk {i+1} ({len(chunk)} chars): {chunk[:70]}...")
    
    return chunks


def add_musical_emphasis(text):
    """
    Add emphasis markers for more expressive singing
    (Experimental - may not work with all Bark versions)
    """
    
    # Add pauses at punctuation
    text = text.replace(',', ', ')
    text = text.replace('.', '. ')
    text = text.replace('!', '! ')
    
    # You can add more musical notation here
    # text = text.replace('dream', '[emphasis] dream')
    
    return text