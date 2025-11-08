# GitHub Repository Setup Guide

This guide will help you create a GitHub repository for this project.

## Option 1: Using GitHub CLI (Recommended)

### Step 1: Install GitHub CLI

If you don't have GitHub CLI installed:

```bash
brew install gh
```

### Step 2: Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate.

### Step 3: Create Repository

Run the setup script:

```bash
./setup_github.sh
```

Or manually create the repository:

```bash
gh repo create youtube-chord-midi-extractor \
  --public \
  --description "Extract chord progressions from YouTube songs and convert to MIDI using autochord" \
  --source=. \
  --remote=origin \
  --push
```

## Option 2: Manual Setup

### Step 1: Create Repository on GitHub

1. Go to [https://github.com/new](https://github.com/new)
2. Repository name: `youtube-chord-midi-extractor`
3. Description: `Extract chord progressions from YouTube songs and convert to MIDI using autochord`
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/youtube-chord-midi-extractor.git
git branch -M main
git push -u origin main
```

## Option 3: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/youtube-chord-midi-extractor.git
git branch -M main
git push -u origin main
```

## Verify Setup

After pushing, visit your repository:
```
https://github.com/YOUR_USERNAME/youtube-chord-midi-extractor
```

## Next Steps

- Add topics/tags to your repository (e.g., `python`, `music`, `chord-recognition`, `midi`, `youtube`)
- Consider adding a GitHub Actions workflow for CI/CD
- Update the LICENSE file if you want a different license
- Add more documentation or examples

