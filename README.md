# YouTube Chord Progression to MIDI Extractor

A Python command-line tool that downloads audio from YouTube, analyzes it to detect chord progressions using machine learning, and generates a MIDI file with the detected chords.

## Features

- **Automatic chord recognition** using [autochord](https://github.com/cjbayron/autochord), a Bi-LSTM-CRF deep learning model
- **YouTube integration** - Search and download audio directly from YouTube
- **MIDI generation** - Convert detected chords to MIDI files with accurate timing
- **High accuracy** - The autochord model achieves 67.33% accuracy on chord recognition
- **Lightweight** - Uses autochord for efficient chord detection without extensive computational resources
- **24 chord types** - Recognizes 12 major and 12 minor triads (C, C#, D, D#, E, F, F#, G, G#, A, A#, B and their minor variants)
- **Auto cleanup** - Temporary audio files are automatically removed after processing

## Requirements

This tool is **macOS only**. The following are required:

- **macOS** (Apple Silicon or Intel)
- **Python 3.8 or higher**
- **FFmpeg** (for audio processing)
- **Homebrew** (for installing dependencies)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kaiuu75/youtube-chord-midi-extractor.git
   cd youtube-chord-midi-extractor
   ```

2. Set up a virtual environment (recommended):
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the NNLS-Chroma VAMP plugin:
   ```bash
   # Install dependencies
   brew install boost vamp-plugin-sdk
   
   # Get installed versions (adjust paths if needed)
   VAMP_VERSION=$(ls /opt/homebrew/Cellar/vamp-plugin-sdk/ | head -1)
   BOOST_VERSION=$(ls /opt/homebrew/Cellar/boost/ | head -1)
   
   # Clone and build the plugin
   cd /tmp
   git clone https://github.com/c4dm/nnls-chroma
   cd nnls-chroma
   
   # Set up build environment
   ln -s /opt/homebrew/Cellar/vamp-plugin-sdk/$VAMP_VERSION vamp
   ln -s /opt/homebrew/Cellar/boost/$BOOST_VERSION boost
   cp vamp/lib/*.a vamp/include/ 2>/dev/null || true
   
   # Patch Makefile for macOS
   sed -i '' 's|VAMP_SDK_DIR = ../vamp-plugin-sdk|VAMP_SDK_DIR = vamp/include|' Makefile.osx
   sed -i '' 's|BOOST_ROOT = ../boost_1_48_0|BOOST_ROOT = boost/include|' Makefile.osx
   sed -i '' 's|-arch x86_64||' Makefile.osx
   
   # Build and install
   make -f Makefile.osx
   mkdir -p ~/Library/Audio/Plug-Ins/Vamp
   cp nnls-chroma.dylib ~/Library/Audio/Plug-Ins/Vamp/
   ```
   
   **Note:** If you have an Intel Mac (not Apple Silicon), use `/usr/local/Cellar` instead of `/opt/homebrew/Cellar` in the paths above.
   
   See [this issue](https://github.com/cjbayron/autochord/issues/2) for more details.

**Note:** On first run, autochord will download the pre-trained model (~50MB). This is a one-time download.

## Disclaimer

This tool is for educational and research purposes. Users are responsible for:
- Complying with YouTube's Terms of Service
- Respecting copyright laws and obtaining necessary permissions for any downloaded content
- Using downloaded content in accordance with applicable laws and regulations

The authors and contributors of this tool are not responsible for any misuse of this software.

## Usage

Make sure your virtual environment is activated (if you're using one):
```bash
source venv/bin/activate
```

Run the script:
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

**Note on chord detection:** While there are other chord detection libraries available (such as librosa's chord recognition, ChordRecognition, or more complex deep learning models), autochord was chosen for this project because it provides a good balance between accuracy and computational efficiency. It is more lightweight than many alternatives, making it suitable for quick chord extraction from YouTube audio without requiring extensive computational resources.

## Notes

- Chord detection accuracy is approximately 67.33% (as reported by autochord)
- Processing may take a few minutes depending on song length (especially on first run when the model is downloaded)
- Temporary audio files are automatically cleaned up after processing
- The model recognizes major and minor triads only (no extended chords like 7ths, sus, dim, aug, etc.)

