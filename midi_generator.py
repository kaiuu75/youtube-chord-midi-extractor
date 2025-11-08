"""MIDI file generation module."""

import mido
from typing import List, Tuple


def create_midi_file(chords: List[Tuple[float, float, str]], output_file: str, tempo: int = 120, min_duration: float = 0.5):
    """
    Create a MIDI file from detected chords.
    
    Args:
        chords: List of tuples (start_time, end_time, chord_name) from chord detection
        output_file: Path to output MIDI file
        tempo: Tempo in BPM (default 120)
        min_duration: Minimum duration for each chord in seconds (default 0.5)
    """
    from analyze import get_chord_notes
    
    # Create a new MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo
    ticks_per_beat = mid.ticks_per_beat
    microseconds_per_beat = mido.bpm2tempo(tempo)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))
    
    # Convert time to MIDI ticks
    def time_to_ticks(seconds: float) -> int:
        beats = (seconds * tempo) / 60.0
        return int(beats * ticks_per_beat)
    
    # Track absolute time position in MIDI ticks (for calculating relative deltas)
    absolute_time_ticks = 0
    
    for start_time, end_time, chord_name in chords:
        if chord_name == 'N':
            continue
        
        # Get MIDI notes for this chord
        notes = get_chord_notes(chord_name)
        if not notes:
            continue
        
        # Calculate absolute start time for this chord in ticks
        chord_start_ticks = time_to_ticks(start_time)
        
        # Calculate relative time delta from current position
        # This is the time we need to wait before starting this chord
        delta_ticks = max(0, chord_start_ticks - absolute_time_ticks)
        
        # Calculate duration for this chord (use actual duration from autochord)
        chord_duration = max(end_time - start_time, min_duration)
        chord_duration_ticks = max(1, time_to_ticks(chord_duration))  # Ensure at least 1 tick
        
        # Add note on messages (relative timing)
        # First note: wait delta_ticks before starting
        track.append(mido.Message('note_on', channel=0, note=notes[0], velocity=64, time=delta_ticks))
        # Remaining notes: play simultaneously (time=0)
        for note in notes[1:]:
            track.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        
        # Update absolute time to when chord starts
        absolute_time_ticks = chord_start_ticks
        
        # Add note off messages after chord duration (relative timing)
        track.append(mido.Message('note_off', channel=0, note=notes[0], velocity=64, time=chord_duration_ticks))
        # Remaining notes: stop simultaneously (time=0)
        for note in notes[1:]:
            track.append(mido.Message('note_off', channel=0, note=note, velocity=64, time=0))
        
        # Update absolute time to when chord ends
        absolute_time_ticks += chord_duration_ticks
    
    # Save the MIDI file
    mid.save(output_file)
    print(f"MIDI file saved: {output_file}")

