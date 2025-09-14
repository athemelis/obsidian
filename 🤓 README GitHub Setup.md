---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
---
Obsidian Project - Complete Git & GitHub Guide

A web development project with Python backend and HTML/JavaScript frontend, using Git for version control with a dual-branch workflow.

**GitHub Repository:** https://github.com/athemelis/obsidian

---

## 🚀 Quick Start Guide

Get up and running with the dual-branch workflow in 10 minutes:

### 1. Install Git
```bash
# Using Homebrew (recommended)
brew install git

# Verify installation
git --version
```

### 2. Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global credential.helper osxkeychain
```

### 3. Get GitHub Token
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. **Save the token securely** (you'll need it for authentication)

### 4. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/athemelis/obsidian.git
cd obsidian

# Create development branch
git checkout -b obsidian-dev
```

### 5. Configure VSCode
Press `Cmd + ,` and enable:
- ✅ Git: Autofetch
- ✅ Git: Enable Smart Commit
- ✅ Git: Post Commit Command → set to "sync"
- ❌ Git: Confirm Sync (uncheck this)

### 6. Daily Workflow
```
1. Work on obsidian-dev branch (check bottom-left of VSCode)
2. Make changes and test locally
3. Commit: Cmd+Shift+G → Stage (+) → Message → Cmd+Enter
4. When ready for GitHub:
   - Switch to main branch
   - Pull latest: Cmd+Shift+P → "Git: Pull"
   - Merge: Cmd+Shift+P → "Git: Merge Branch" → select "obsidian-dev"
   - Push: Click sync button
   - Switch back to obsidian-dev
```

---

## 📚 Full Reference Guide

## Table of Contents
1. [Complete Setup Instructions](#complete-setup-instructions)
2. [Project Structure](#project-structure)
3. [Branch Workflow Guide](#branch-workflow-guide)
4. [Git Operations Reference](#git-operations-reference)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## Complete Setup Instructions

### Prerequisites
- macOS
- VSCode installed
- GitHub account

### 1. Install Git on macOS

Multiple Git installations can coexist:
1. macOS includes Apple’s Git at `/usr/bin/git` via the Xcode Command Line Tools.
2. Homebrew would install its own Git under `/opt/homebrew/Cellar/git/...` with a symlink at `/opt/homebrew/bin/git` (Apple Silicon) or `/usr/local/bin/git` (Intel).

Homebrew will install a newer version of git than what's included in macOS:

1. macOS version can be found like this:
```shell
git --version
git version 2.39.5 (Apple Git-154)
```

2. Homebrew available version can be found like this:
```bash
brew info git              
==> git: stable 2.50.1 (bottled), HEAD
Distributed revision control system
https://git-scm.com
Not installed
```
	Notice above it says "Not installed"

Recommendation is Option A below:

**Option A: Using Homebrew (Recommended)**
```bash
# Check if brew is installed
which brew
brew --version

# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update brew
brew update
brew upgrade
brew cleanup

# Install Git
brew install git
```

**Option B: Using Xcode Command Line Tools**
```bash
xcode-select --install
```

**Option C: Download from Git website**
- Visit [git-scm.com](https://git-scm.com/download/mac)
- Download and run the installer

**Switch to using the brew version of git**

For Intel mac (you’re using /usr/local), add to ~/.zshrc (or ~/.bash_profile if using bash):

```shell
export PATH="/usr/local/bin:/usr/local/sbin:$PATH"
```

For Apple Silicon mac:

```shell
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
```

If the file name doesn't exist, create it.

**Verify installation:**
```bash
git --version
```

### 2. Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Set up GitHub Authentication (I never used this...)

**Create Personal Access Token (PAT):**
1. Go to GitHub.com → Your Profile Picture (top right) → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name
4. Select scopes: `repo`, `workflow`, `write:packages`, `delete:packages`
5. Generate and **save the token securely**

**Configure Git to store credentials:**
```bash
git config --global credential.helper osxkeychain
```

### 4. Clone Repository

**Using VSCode:**
1. Open Command Palette (`Cmd+Shift+P`)
2. Type "Git: Clone"
3. Enter: `https://github.com/athemelis/obsidian`
4. Choose local folder location

**Using Terminal:**
```bash
git clone https://github.com/athemelis/obsidian.git
cd obsidian
```

### 5. Configure VSCode for Git

#### Method 1: Using Settings UI (Easier)
1. Open Settings: `Cmd + ,`
2. Configure these settings:
   - **"git autofetch"** → Check the box
   - **"git confirm sync"** → Uncheck the box
   - **"git smart commit"** → Check the box
   - **"git post commit"** → Set dropdown to `sync`
   - **"git prune"** → Check the box
   - **"git pull tags"** → Check the box

#### Method 2: Using settings.json
1. Press `Cmd + Shift + P`
2. Type: "Preferences: Open User Settings (JSON)"
3. Add these settings:
```json
{
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    "git.postCommitCommand": "sync",
    "git.pruneOnFetch": true,
    "git.pullTags": true
}
```

### 6. Install Recommended Extensions
1. Open Extensions: `Cmd + Shift + X`
2. Search and install:
   - **GitLens** — Git supercharged by GitKraken
   - **Git Graph** by mhutchie

---

## Project Structure

```
obsidian/
├── backend/          # Python backend code
├── frontend/         # HTML/CSS/JavaScript
├── docs/            # Documentation
├── tests/           # Test files
├── .gitignore       # Git ignore configuration
└── README.md        # This file
```

### Git Ignore Configuration

The project includes a `.gitignore` for Python and JavaScript:

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env
*.log
*.db

# JavaScript/Node
node_modules/
npm-debug.log*
.eslintcache

# IDE
.vscode/*
!.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Build/Distribution
dist/
build/
```

---

## Branch Workflow Guide

### Understanding the Dual-Branch System

**Branch Structure:**
- `main`: Stable branch that syncs with GitHub
- `obsidian-dev`: Local development branch for testing

**Visual Workflow:**
```
obsidian-dev: A → B → C → D (local development)
                    ↓ merge when ready
main:         A =============> D → push to GitHub
```

### Creating the Development Branch

**First-time setup:**
```bash
# Create and switch to obsidian-dev
git checkout -b obsidian-dev
```

**Verify current branch:**
- Check bottom-left status bar in VSCode
- Should show "obsidian-dev"

### Daily Development Process

#### 1. Start Work Session
- **Check branch**: Look at bottom-left status bar
- **Switch if needed**: Click branch name → select "obsidian-dev"

#### 2. Develop on obsidian-dev
- Make changes freely
- Test everything locally
- Commit regularly (stays local)

#### 3. Commit Changes
```
Cmd + Shift + G     # Open Source Control
Click + on files    # Stage changes
Write message       # feat: add new feature
Cmd + Enter         # Commit
```

### Publishing to GitHub

When your changes are tested and ready:

#### 1. Switch to main
- Click "obsidian-dev" in status bar
- Select "main"

#### 2. Update main from GitHub
Choose any method:
- **Command Palette**: `Cmd+Shift+P` → "Git: Pull"
- **Source Control**: Click ... menu → "Pull"
- **Status Bar**: Click sync arrows (⟲)
- **Terminal**: `git pull`

#### 3. Merge obsidian-dev
- `Cmd+Shift+P` → "Git: Merge Branch"
- Select "obsidian-dev"
- Resolve conflicts if any appear

#### 4. Push to GitHub
Choose any method:
- **Command Palette**: `Cmd+Shift+P` → "Git: Push"
- **Source Control**: Click "Sync Changes"
- **Status Bar**: Click sync arrows
- **Terminal**: `git push`

#### 5. Return to Development
- Switch back to "obsidian-dev"
- Continue working

### Keeping Branches Synchronized

After pushing to GitHub, update obsidian-dev:
1. Stay on obsidian-dev
2. `Cmd+Shift+P` → "Git: Merge Branch"
3. Select "main"

---

## Git Operations Reference

### Saving Files

**Method A: From Artifacts/External Sources**
1. Copy content
2. VSCode: `Cmd + N` (new file)
3. Paste: `Cmd + V`
4. Save: `Cmd + S`
5. Navigate to project folder

**Method B: Create in VSCode**
1. Right-click Explorer panel
2. Select "New File"
3. Name with extension (.py, .html, .js, .md)

### Staging Files

**All methods to stage:**
1. **Individual files**: Hover → click `+`
2. **All files**: Click `+` next to "Changes"
3. **Keyboard**: Select file → `Cmd+Shift+G` → `+`

### Committing

**All methods to commit:**
1. **Keyboard**: `Cmd + Enter`
2. **UI**: Click checkmark (✓)
3. **Command Palette**: `Cmd+Shift+P` → "Git: Commit"

### Pushing/Pulling

**All methods to push:**
1. **Sync Button**: Click 🔄 in Source Control
2. **Command Palette**: `Cmd+Shift+P` → "Git: Push"
3. **Status Bar**: Click cloud/arrows icon
4. **Terminal**: `git push`

**All methods to pull:**
1. **Command Palette**: `Cmd+Shift+P` → "Git: Pull"
2. **Source Control**: ... menu → "Pull"
3. **Sync Button**: Click 🔄 (does pull + push)
4. **Terminal**: `git pull`

### Switching Branches

**All methods:**
1. **Status Bar**: Click branch name → select branch
2. **Command Palette**: `Cmd+Shift+P` → "Git: Checkout to..."
3. **Source Control**: ... menu → "Checkout to..."
4. **Terminal**: `git checkout branch-name`

---

## Troubleshooting

### Common Issues and Solutions

#### "Git not recognized in VSCode"
1. Restart VSCode: `Cmd + Q` then reopen
2. Check Git output: `Cmd+Shift+P` → "Git: Show Git Output"
3. Manually set Git path in settings if needed

#### "Authentication Failed"
1. Ensure you're using Personal Access Token as password
2. Username should be your GitHub username
3. Regenerate token if needed: GitHub → Settings → Developer settings

#### "No remote repository"
```bash
# In VSCode terminal (Ctrl + `)
git remote add origin https://github.com/athemelis/obsidian.git
```

#### "I accidentally made changes on main"
1. Create backup: `git checkout -b temp-backup`
2. Switch to main: `git checkout main`
3. Reset main: `git reset --hard origin/main`
4. Merge to dev: `git checkout obsidian-dev && git merge temp-backup`

#### "Merge conflicts"
1. VSCode highlights conflicts in red
2. Click conflicted files
3. Choose "Accept Current" / "Accept Incoming" / "Accept Both"
4. Save files
5. Complete merge

#### "Can't switch branches - uncommitted changes"
Either:
- Commit changes first
- Stash them: `Cmd+Shift+P` → "Git: Stash"

#### "Push rejected"
1. Pull first to get remote changes
2. Resolve any conflicts
3. Push again

#### "Lost track of which branch I'm on"
- Check bottom-left status bar
- Terminal: `git branch` (current has *)

---

## Best Practices

### Commit Messages
Use conventional format:
```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
style: format code with black
test: add unit tests for user model
chore: update dependencies
WIP: experimental feature (for obsidian-dev)
```

### When to Merge to Main
Merge when:
- ✅ Feature is complete
- ✅ All tests pass
- ✅ No known bugs
- ✅ Code is cleaned up
- ✅ Ready for GitHub

### Development Tips
1. **Commit frequently** on obsidian-dev
2. **Pull before pushing** to avoid conflicts
3. **Test thoroughly** before merging to main
4. **Keep obsidian-dev** as primary work branch
5. **Review changes** before committing

### VSCode Shortcuts
- `Cmd + Shift + G`: Open Source Control
- `Cmd + Enter`: Commit staged changes
- `Cmd + Shift + P`: Command Palette
- `` Ctrl + ` ``: Open terminal

### Status Bar Indicators
Bottom-left shows:
- Current branch name
- Sync status (↑↓ with numbers)
- Click to switch branches

---

## Getting Help

If you encounter errors:
1. Note the exact error message
2. Check which step you were on
3. Try the troubleshooting section
4. Remember: Git keeps history, mistakes can be reverted!

---

## License
[Add your license information here]

## Contact
[Add contact information if needed]