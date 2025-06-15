# Obsidian

A web development project with Python backend and HTML/JavaScript frontend.

**GitHub Repository:** https://github.com/athemelis/obsidian

## Project Setup Guide

This guide covers setting up Git for source code management with GitHub integration on macOS using VSCode.

### Prerequisites
- macOS
- VSCode installed
- GitHub account

## Setup Instructions

### 1. Install Git on macOS

Choose one of the following methods:

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

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

**Verify installation:**
```bash
git --version
```

### 2. Configure Git Identity

Open Terminal and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Set up GitHub Authentication

**Create Personal Access Token (PAT):**
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name
4. Select scopes: `repo`, `workflow`, `write:packages`, `delete:packages`
5. Generate and **save the token securely**

**Configure Git to store credentials:**
```bash
git config --global credential.helper osxkeychain
```

### 4. Clone This Repository

**In VSCode:**
1. Open VSCode
2. Open Command Palette (`Cmd+Shift+P`)
3. Type "Git: Clone"
4. Enter: `https://github.com/athemelis/obsidian`
5. Choose local folder location

**Alternative - Using Terminal:**
```bash
git clone https://github.com/athemelis/obsidian.git
cd obsidian
```

### 5. Configure VSCode for Git

#### Method 1: Using VSCode Settings UI (Easier)

1. **Open VSCode Settings**
   - Press `Cmd + ,` (Command + Comma)
   - Or: Code menu → Preferences → Settings

2. **Configure each Git setting:**
   
   Search for and configure these settings:

   - **"git autofetch"** → Check the box for `Git: Autofetch`
   - **"git confirm sync"** → Uncheck the box for `Git: Confirm Sync`
   - **"git smart commit"** → Check the box for `Git: Enable Smart Commit`
   - **"git post commit"** → Set `Git: Post Commit Command` dropdown to `sync`
   - **"git prune"** → Check the box for `Git: Prune On Fetch`
   - **"git pull tags"** → Check the box for `Git: Pull Tags`

#### Method 2: Using settings.json (Advanced)

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

#### Install Recommended Extensions

1. Open Extensions panel (`Cmd + Shift + X`)
2. Search and install:
   - **GitLens** — Git supercharged by GitKraken
   - **Git Graph** by mhutchie

### 6. Project Structure

This project uses:
- Python for backend development
- HTML/CSS/JavaScript for frontend
- Git for version control

### 7. Git Ignore Configuration

The project includes a `.gitignore` file configured for Python and JavaScript development:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.env
*.log
.pytest_cache/
.coverage
*.db
*.sqlite3

# JavaScript/Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache

# IDE
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build/Distribution
dist/
build/
*.egg-info/
```

## VSCode Git Workflow

### Daily Workflow

1. **Source Control panel** (`Ctrl+Shift+G`)
   - View changes
   - Stage files (+ button)
   - Write commit message
   - Commit (✓ button)
   - Sync changes (🔄 button)

2. **Status bar** (bottom left)
   - Shows current branch
   - Click to switch branches
   - Sync indicator shows pending changes

### Key Shortcuts

- `Cmd+Shift+G`: Open Source Control
- `Cmd+Enter`: Commit staged changes
- `Cmd+Shift+P` → "Git: Sync": Push/pull changes

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
```

### Branch Strategy
- `main`: production-ready code
- `develop`: integration branch
- `feature/*`: new features
- `bugfix/*`: bug fixes
- `hotfix/*`: urgent fixes for production

### VSCode Git Features
- **Timeline view**: See file history
- **Inline blame**: See who changed what
- **Merge editor**: Visual merge conflict resolution

## Troubleshooting

### Git not recognized in VSCode
1. Restart VSCode (`Cmd + Q` then reopen)
2. Check Git output: `Cmd + Shift + P` → "Git: Show Git Output"
3. Manually set Git path in settings if needed

### Authentication Issues
1. Ensure your Personal Access Token is valid
2. Clear credentials: `git config --global --unset credential.helper`
3. Re-run: `git config --global credential.helper osxkeychain`

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'feat: add new feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create a Pull Request on GitHub

## License

[Add your license information here]

## Contact

[Add contact information if needed]