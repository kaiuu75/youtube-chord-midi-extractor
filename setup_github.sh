#!/bin/bash
# Script to create GitHub repository and push code

set -e

REPO_NAME="youtube-chord-midi-extractor"
REPO_DESCRIPTION="Extract chord progressions from YouTube songs and convert to MIDI using autochord"

echo "Setting up GitHub repository..."
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "GitHub CLI found. Creating repository..."
    gh repo create "$REPO_NAME" --public --description "$REPO_DESCRIPTION" --source=. --remote=origin --push
    echo ""
    echo "✅ Repository created and pushed to GitHub!"
    echo "Repository URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
else
    echo "GitHub CLI (gh) not found."
    echo ""
    echo "Option 1: Install GitHub CLI and run this script again"
    echo "  brew install gh"
    echo "  gh auth login"
    echo ""
    echo "Option 2: Create repository manually on GitHub:"
    echo "  1. Go to https://github.com/new"
    echo "  2. Repository name: $REPO_NAME"
    echo "  3. Description: $REPO_DESCRIPTION"
    echo "  4. Choose Public or Private"
    echo "  5. DO NOT initialize with README, .gitignore, or license"
    echo "  6. Click 'Create repository'"
    echo ""
    echo "Then run these commands:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

