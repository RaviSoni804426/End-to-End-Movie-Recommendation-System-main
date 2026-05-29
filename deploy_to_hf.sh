#!/usr/bin/env bash
# Simple script to push this repo to a Hugging Face Space (Docker)
# Usage: HF_SPACE_GIT="https://huggingface.co/spaces/<user>/<space>.git" ./deploy_to_hf.sh

set -e

if [ -z "$HF_SPACE_GIT" ]; then
  echo "Set HF_SPACE_GIT environment variable to your Space's Git URL."
  echo "Example: export HF_SPACE_GIT=https://huggingface.co/spaces/yourname/cinematch.git"
  exit 1
fi

branch=${1:-main}

git init 2>/dev/null || true
git add -A
git commit -m "Deploy to Hugging Face Space" || true

if git remote | grep hf >/dev/null 2>&1; then
  git remote remove hf
fi
git remote add hf "$HF_SPACE_GIT"
git push -f hf HEAD:$branch

echo "Pushed to $HF_SPACE_GIT on branch $branch. Build will start on Hugging Face." 
