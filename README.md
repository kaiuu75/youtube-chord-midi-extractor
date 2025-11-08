# YouTube Chord Progression to MIDI Extractor

A Python command-line tool that downloads audio from YouTube, analyzes it to detect chord progressions using machine learning, and generates a MIDI file with the detected chords.

## Features

- **Automatic chord recognition** using [autochord](https://github.com/cjbayron/autochord), a Bi-LSTM-CRF deep learning model
- **YouTube integration** - Search and download audio directly from YouTube
- **MIDI generation** - Convert detected chords to MIDI files with accurate timing
- **High accuracy** - The autochord model achieves 67.33% accuracy on chord recognition

## Installation

1. Install Python 3.8 or higher
2. Install FFmpeg (required for audio processing):
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Note:** On first run, autochord will download the pre-trained model (~50MB). This is a one-time download.

## Usage

```bash
python main.py "Song Name"
```

Example:
```bash
python main.py "Imagine by John Lennon"
```

The program will:
1. Search for the song on YouTube
2. Download the audio
3. Analyze the audio using autochord's deep learning model to detect chord progressions
4. Generate a MIDI file with the detected chords (named based on the song name)

### Command-line Options

- `-o, --output`: Specify output MIDI file path (default: based on song name)
- `--tempo`: Set tempo for MIDI file in BPM (default: 120)
- `--min-duration`: Minimum duration for each chord in seconds (default: 0.5)
- `--keep-audio`: Keep downloaded audio file after processing
- `--temp-dir`: Specify temporary directory for audio files

Example with options:
```bash
python main.py "Song Name" -o output.mid --tempo 140 --min-duration 1.0
```

## Output

The generated MIDI file will contain the detected chord progression with accurate timing. Each chord is represented as MIDI notes played simultaneously. The model recognizes 24 chord types:
- 12 major chords (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
- 12 minor chords (Cm, C#m, Dm, D#m, Em, Fm, F#m, Gm, G#m, Am, A#m, Bm)

## Technical Details

This tool uses:
- **[autochord](https://github.com/cjbayron/autochord)** - Automatic chord recognition using a Bi-LSTM-CRF neural network model
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube audio download
- **[mido](https://github.com/mido/mido)** - MIDI file generation

The autochord library uses TensorFlow and the NNLS-Chroma VAMP plugin for feature extraction.

## Notes

- Chord detection accuracy is approximately 67.33% (as reported by autochord)
- Processing may take a few minutes depending on song length (especially on first run when the model is downloaded)
- Temporary audio files are automatically cleaned up after processing
- macOS is supported (Windows is not supported by autochord, but the tool may work with some tweaks)
- The model recognizes major and minor triads only (no extended chords like 7ths, sus, dim, aug, etc.)

