# backend/bark_patch.py
"""
Patch for Bark to work with PyTorch 2.6+
Forces weights_only=False for model loading
"""
import torch
import warnings

# Store original torch.load
_original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    """
    Wrapper for torch.load that forces weights_only=False
    This is safe for Bark models from the official Suno AI repo
    """
    # Force weights_only=False for Bark model loading
    kwargs['weights_only'] = False
    
    # Suppress the warning since we're doing this intentionally
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        return _original_torch_load(*args, **kwargs)

# Monkey patch torch.load
torch.load = patched_torch_load

print("✅ Bark patch applied: weights_only=False for model loading")