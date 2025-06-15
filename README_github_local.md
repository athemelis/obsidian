# Local Development Branch Guide for Obsidian Project

This guide explains how to maintain a local `obsidian-dev` branch for testing and development, separate from the main branch that syncs with GitHub.

## Overview

**Branch Structure:**
- `main`: Stable branch that syncs with GitHub
- `obsidian-dev`: Local development branch for testing changes

**Workflow Benefits:**
- Test changes without affecting the main branch
- Validate code before pushing to GitHub
- Keep experimental work separate
- Maintain a stable main branch

---

## Initial Setup

### Step 1: Create the obsidian-dev Branch

1. **Open your Obsidian project in VSCode**

2. **Check current branch** (bottom-left status bar)
   - Should show "main"

3. **Create obsidian-dev branch**
   - Click on "main" in the status bar
   - Select "Create new branch..."
   - Type: `obsidian-dev`
   - Press Enter

**Alternative method:**
```bash
# In VSCode terminal (Ctrl + `)
git checkout -b obsidian-dev
```

### Step 2: Verify Branch Creation

- Status bar should now show "obsidian-dev"
- You're ready to start development!

---

## Daily Development Workflow

### 1. Start Your Work Session

**Always check which branch you're on:**
- Look at bottom-left status bar
- Should say "obsidian-dev"
- If it says "main", click and switch to "obsidian-dev"

### 2. Make Changes on obsidian-dev

1. **Edit your files** freely
   - Python backend changes
   - HTML/JavaScript frontend updates
   - Documentation improvements

2. **Test everything locally**
   - Run your Python server
   - Test frontend functionality
   - No risk to main branch!

3. **Commit to obsidian-dev**
   ```
   Cmd + Shift + G     # Open Source Control
   Click + on files    # Stage changes
   Write message       # Describe your changes
   Cmd + Enter         # Commit
   ```

**Note:** These commits stay local - they're not pushed to GitHub

### 3. Continue Development

- Make as many commits as needed
- Experiment freely
- Your main branch remains untouched

---

## Syncing Validated Changes to Main

When you're satisfied with your changes and ready to update GitHub:

### Method 1: Merge Everything (Recommended)

1. **Test thoroughly on obsidian-dev**
   - Ensure all features work
   - Fix any bugs

2. **Switch to main branch**
   - Click "obsidian-dev" in status bar
   - Select "main"

3. **Update main from GitHub**
   
   Use one of these methods:
   
   **Option A: Command Palette (Recommended)**
   - Press `Cmd + Shift + P`
   - Type: "Git: Pull"
   - Press Enter
   
   **Option B: Source Control Panel**
   - Open Source Control (`Cmd + Shift + G`)
   - Click the three dots menu (...) at the top
   - Select "Pull" or "Sync"
   
   **Option C: Status Bar**
   - Look at bottom-left status bar for sync arrows (⟲)
   - Click if present (may show numbers)
   
   **Option D: Terminal**
   - Open terminal: `` Ctrl + ` ``
   - Type: `git pull`
   - Press Enter
   
   This ensures you have the latest changes from GitHub

4. **Merge obsidian-dev into main**
   - Press `Cmd + Shift + P`
   - Type: "Git: Merge Branch"
   - Select "obsidian-dev"
   - Resolve any conflicts if they appear

5. **Push to GitHub**
   
   Use one of these methods:
   
   **Option A: Command Palette**
   - Press `Cmd + Shift + P`
   - Type: "Git: Push"
   - Press Enter
   
   **Option B: Source Control Panel**
   - Look for "Sync Changes" button
   - Or click ... menu → "Push"
   
   **Option C: Status Bar**
   - Click sync arrows if visible
   
   Your changes are now on GitHub!

6. **Switch back to obsidian-dev**
   - Continue development

### Method 2: Selective Changes (Advanced)

If you only want to move specific changes:

1. **Switch to main**
2. **View Git History**
   - `Cmd + Shift + P` → "Git: View History"
3. **Cherry-pick specific commits**
   - Find commits you want
   - Right-click → "Cherry Pick Commit"
4. **Push to GitHub**

---

## Keeping Branches Synchronized

### Update obsidian-dev with Latest from Main

After pushing changes to GitHub, update your dev branch:

1. **Stay on obsidian-dev branch**
2. **Merge main into obsidian-dev**
   ```
   Cmd + Shift + P
   Type: "Git: Merge Branch"
   Select: "main"
   ```

This keeps obsidian-dev up-to-date with production code.

### Understanding Sync Options

**What each Git action does:**
- **Pull**: Downloads changes from GitHub to your local branch
- **Push**: Uploads your local commits to GitHub
- **Sync**: Does both pull and push as needed
- **Fetch**: Downloads info about changes without applying them

---

## Visual Workflow

```
Day 1: Starting development
main:         A ← (synced with GitHub)
obsidian-dev: A ← (YOU ARE HERE)

Day 2: After local development
main:         A ← (unchanged)
obsidian-dev: A → B → C → D ← (your local commits)

Day 3: Ready to publish
Step 1 - Switch to main and merge:
main:         A → B → C → D ← (ready to push)
obsidian-dev: A → B → C → D

Step 2 - Push to GitHub:
main:         A → B → C → D ← (GitHub updated!)
obsidian-dev: A → B → C → D ← (still local)
```

---

## Common Scenarios and Solutions

### "I accidentally made changes on main"

1. **Create a backup branch from main**
   ```
   git checkout -b temp-backup
   ```

2. **Switch back to main**
   ```
   git checkout main
   ```

3. **Reset main to match GitHub**
   ```
   git reset --hard origin/main
   ```

4. **Merge your changes to obsidian-dev**
   ```
   git checkout obsidian-dev
   git merge temp-backup
   ```

### "I want to discard all changes on obsidian-dev"

1. **Switch to obsidian-dev**
2. **Reset to match main**
   ```
   git reset --hard main
   ```

### "I need to temporarily save work"

1. **On obsidian-dev, commit with WIP message**
   ```
   git commit -m "WIP: saving progress"
   ```

2. **Later, continue working or amend the commit**

---

## Best Practices

### 1. Commit Messages on obsidian-dev

Even though they're local, use clear messages:
- `feat: add user authentication`
- `fix: resolve database connection`
- `WIP: testing new API endpoint`
- `experiment: trying new UI layout`

### 2. When to Merge to Main

Merge when:
- ✅ Feature is complete
- ✅ All tests pass
- ✅ No known bugs
- ✅ Code is cleaned up
- ✅ You're ready for others to see it

### 3. Branch Hygiene

- Keep obsidian-dev as your primary local branch
- Create additional branches for major experiments
- Regularly sync with main to avoid conflicts

---

## Quick Command Reference

| Action | Method |
|--------|--------|
| Switch branches | Click branch name in status bar |
| Create branch | Click branch → "Create new branch" |
| Pull from GitHub | `Cmd+Shift+P` → "Git: Pull" |
| Push to GitHub | `Cmd+Shift+P` → "Git: Push" |
| Merge branches | `Cmd+Shift+P` → "Git: Merge Branch" |
| View history | `Cmd+Shift+P` → "Git: View History" |
| Discard changes | Source Control → "Discard Changes" |

---

## Troubleshooting

### "Merge conflicts when merging to main"

1. VSCode will highlight conflicts
2. Click on conflicted files
3. Choose "Accept Current" / "Accept Incoming" / "Accept Both"
4. Save files
5. Complete the merge

### "Can't switch branches - uncommitted changes"

Either:
- Commit your changes first
- Or stash them: `Cmd+Shift+P` → "Git: Stash"

### "Lost track of which branch I'm on"

- Always check bottom-left status bar
- Run `git branch` in terminal to see all branches
- Current branch has an asterisk (*)

---

## Summary

1. **Work on obsidian-dev** for all development
2. **Keep main clean** and synced with GitHub
3. **Merge to main** only when ready
4. **Push main** to share with others

This workflow gives you freedom to experiment while maintaining a stable, shareable codebase!