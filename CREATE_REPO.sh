#!/bin/bash
# Quick script to create GitHub repository

set -e

REPO_NAME="youtube-chord-midi-extractor"
REPO_DESCRIPTION="Extract chord progressions from YouTube songs and convert to MIDI using autochord"

echo "🚀 Creating GitHub repository..."
echo ""

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "⚠️  Not authenticated with GitHub."
    echo ""
    echo "Please run: gh auth login"
    echo "Then run this script again."
    echo ""
    exit 1
fi

# Create repository
echo "Creating repository: $REPO_NAME"
gh repo create "$REPO_NAME" \
  --public \
  --description "$REPO_DESCRIPTION" \
  --source=. \
  --remote=origin \
  --push

echo ""
echo "✅ Repository created successfully!"
echo ""
echo "Repository URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo ""

