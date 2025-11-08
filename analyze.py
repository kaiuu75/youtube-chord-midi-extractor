"""Audio analysis and chord detection module using autochord."""

import os
from typing import List, Tuple
import autochord


# Mapping from autochord format (e.g., 'C:maj', 'Am:min') to our format (e.g., 'C', 'Am')
# autochord uses MIREX format: ROOT:QUALITY where QUALITY can be 'maj', 'min', etc.
def normalize_chord_name(autochord_name: str) -> str:
    """
    Convert autochord chord name to our format.
    
    Args:
        autochord_name: Chord name from autochord (e.g., 'C:maj', 'Am:min', 'N')
        
    Returns:
        Normalized chord name (e.g., 'C', 'Am', 'N')
    """
    if autochord_name == 'N':
        return 'N'
    
    # Parse MIREX format: ROOT:QUALITY
    if ':' in autochord_name:
        root, quality = autochord_name.split(':', 1)
        
        # Handle minor chords
        if quality == 'min':
            # Check if root already has 'm' suffix (shouldn't happen, but be safe)
            if root.endswith('m'):
                return root
            else:
                return root + 'm'
        # Handle major chords - just return root
        elif quality == 'maj':
            return root
        else:
            # For other qualities, just return root for now
            # Could extend this to handle sus, dim, aug, etc.
            return root
    
    return autochord_name


# Chord name to MIDI notes mapping
# Based on standard chord structures
CHORD_NOTES = {
    # Major chords
    'C': [60, 64, 67],      # C, E, G
    'C#': [61, 65, 68],     # C#, F, G#
    'D': [62, 66, 69],      # D, F#, A
    'D#': [63, 67, 70],     # D#, G, A#
    'E': [64, 68, 71],      # E, G#, B
    'F': [65, 69, 72],      # F, A, C
    'F#': [66, 70, 73],     # F#, A#, C#
    'G': [67, 71, 74],      # G, B, D
    'G#': [68, 72, 75],     # G#, C, D#
    'A': [69, 73, 76],      # A, C#, E
    'A#': [70, 74, 77],     # A#, D, F
    'B': [71, 75, 78],      # B, D#, F#
    
    # Minor chords
    'Cm': [60, 63, 67],     # C, D#, G
    'C#m': [61, 64, 68],    # C#, E, G#
    'Dm': [62, 65, 69],     # D, F, A
    'D#m': [63, 66, 70],    # D#, F#, A#
    'Em': [64, 67, 71],     # E, G, B
    'Fm': [65, 68, 72],     # F, G#, C
    'F#m': [66, 69, 73],    # F#, A, C#
    'Gm': [67, 70, 74],     # G, A#, D
    'G#m': [68, 71, 75],    # G#, B, D#
    'Am': [69, 72, 76],     # A, C, E
    'A#m': [70, 73, 77],    # A#, C#, F
    'Bm': [71, 74, 78],     # B, D, F#
}


def detect_chords(audio_file: str) -> List[Tuple[float, float, str]]:
    """
    Detect chords in an audio file using autochord.
    
    Args:
        audio_file: Path to the audio file
        
    Returns:
        List of tuples (start_time, end_time, chord_name) representing the detected chords
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        Exception: If chord detection fails
    """
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    
    print(f"Analyzing audio file: {audio_file}")
    print("Detecting chords using autochord (this may take a moment)...")
    print("Note: First run will download the model, which may take some time.")
    
    try:
        # Use autochord to recognize chords
        # autochord.recognize() returns list of (start_time, end_time, chord_name) tuples
        chords_raw = autochord.recognize(audio_file)
        
        if not chords_raw:
            raise Exception("No chords detected in the audio file")
        
        # Convert to our format: (start_time, end_time, normalized_chord_name)
        # Filter out 'N' (no chord) and merge consecutive identical chords
        detected_chords = []
        prev_chord = None
        prev_start = None
        prev_end = None
        
        for start_time, end_time, chord_name in chords_raw:
            normalized_chord = normalize_chord_name(chord_name)
            
            # Only process real chords (not 'N')
            if normalized_chord != 'N':
                if normalized_chord == prev_chord:
                    # Extend the previous chord's end time
                    prev_end = end_time
                else:
                    # Save previous chord if it exists
                    if prev_chord is not None:
                        detected_chords.append((prev_start, prev_end, prev_chord))
                    # Start new chord
                    prev_chord = normalized_chord
                    prev_start = start_time
                    prev_end = end_time
            else:
                # Save previous chord before 'N'
                if prev_chord is not None:
                    detected_chords.append((prev_start, prev_end, prev_chord))
                    prev_chord = None
                    prev_start = None
                    prev_end = None
        
        # Don't forget the last chord
        if prev_chord is not None:
            detected_chords.append((prev_start, prev_end, prev_chord))
        
        print(f"Detected {len(detected_chords)} chord segments")
        
        if not detected_chords:
            print("Warning: No valid chords detected (only 'N' chords found)")
        
        return detected_chords
        
    except Exception as e:
        raise Exception(f"Failed to detect chords: {str(e)}")


def get_chord_notes(chord_name: str) -> List[int]:
    """
    Convert a chord name to MIDI note numbers.
    
    Args:
        chord_name: Chord name (e.g., 'C', 'Am', 'F#')
        
    Returns:
        List of MIDI note numbers (middle C = 60)
    """
    if chord_name == 'N':
        return []
    
    # Return the MIDI notes for this chord, or empty list if not found
    return CHORD_NOTES.get(chord_name, [])
