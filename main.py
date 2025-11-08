#!/usr/bin/env python3
"""Main CLI interface for YouTube Chord to MIDI Extractor."""

import sys
import os
import argparse
import tempfile
import shutil
from pathlib import Path

from download import search_and_download
from analyze import detect_chords
from midi_generator import create_midi_file


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Extract chord progression from YouTube song and generate MIDI file'
    )
    parser.add_argument(
        'song_name',
        type=str,
        help='Name of the song to search for on YouTube'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output MIDI file path (default: based on song name)'
    )
    parser.add_argument(
        '--temp-dir',
        type=str,
        default=None,
        help='Temporary directory for audio files (default: system temp)'
    )
    parser.add_argument(
        '--keep-audio',
        action='store_true',
        help='Keep downloaded audio file after processing'
    )
    parser.add_argument(
        '--tempo',
        type=int,
        default=120,
        help='Tempo for MIDI file in BPM (default: 120)'
    )
    parser.add_argument(
        '--min-duration',
        type=float,
        default=0.5,
        help='Minimum duration for each chord in seconds (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    temp_dir = args.temp_dir
    audio_file = None
    
    try:
        # Step 1: Download audio from YouTube
        print("=" * 50)
        print("Step 1: Downloading audio from YouTube")
        print("=" * 50)
        audio_file = search_and_download(args.song_name, temp_dir)
        
        if not os.path.exists(audio_file):
            print(f"Error: Audio file not found: {audio_file}")
            return 1
        
        # Step 2: Analyze audio and detect chords
        print("\n" + "=" * 50)
        print("Step 2: Analyzing audio and detecting chords")
        print("=" * 50)
        chords = detect_chords(audio_file)
        
        if not chords:
            print("Warning: No chords detected in the audio")
            return 1
        
        # Display detected chords
        print("\nDetected chord progression:")
        for start_time, end_time, chord in chords[:20]:  # Show first 20 chords
            duration = end_time - start_time
            print(f"  {start_time:.2f}s - {end_time:.2f}s ({duration:.2f}s): {chord}")
        if len(chords) > 20:
            print(f"  ... and {len(chords) - 20} more chord segments")
        
        # Step 3: Generate MIDI file
        print("\n" + "=" * 50)
        print("Step 3: Generating MIDI file")
        print("=" * 50)
        
        # Determine output file name
        if args.output:
            output_file = args.output
        else:
            # Create filename from song name
            safe_name = "".join(c for c in args.song_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            output_file = f"{safe_name}_chords.mid"
        
        create_midi_file(chords, output_file, tempo=args.tempo, min_duration=args.min_duration)
        
        print(f"\nSuccess! MIDI file created: {output_file}")
        print(f"Total chords detected: {len(chords)}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup: Remove temporary audio file unless --keep-audio is specified
        if audio_file and os.path.exists(audio_file) and not args.keep_audio:
            try:
                # Remove the audio file
                os.remove(audio_file)
                print(f"Cleaned up temporary audio file: {audio_file}")
                
                # Also try to remove the temp directory if it's empty and we created it
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        # Only remove if directory is empty
                        if not os.listdir(temp_dir):
                            os.rmdir(temp_dir)
                            print(f"Cleaned up temporary directory: {temp_dir}")
                    except OSError:
                        pass  # Directory not empty or other error, that's okay
            except Exception as e:
                print(f"Warning: Could not clean up temporary files: {e}", file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())

