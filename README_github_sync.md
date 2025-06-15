# GitHub Sync Instructions for Obsidian Project

This guide explains how to save files to your project and sync them with GitHub using VSCode's built-in Git features.

## Summary
1. Save files to your project folder
2. Stage the files in VSCode
3. Commit with a message
4. Push to GitHub

---

## Step 1: Save Files to Your Project

**Method A: Copy from artifacts or other sources**
1. Copy the content you want to save
2. Open VSCode
3. In VSCode, create a new file:
   - Press `Cmd + N` (new file)
   - Paste the content (`Cmd + V`)
   - Save it: `Cmd + S`
   - Choose appropriate filename with extension (.md, .py, .html, .js, etc.)
   - Navigate to your Obsidian project folder and save

**Method B: Create directly in VSCode**
1. Open your Obsidian project folder in VSCode
2. Right-click in the Explorer panel (left sidebar)
3. Select "New File"
4. Name your file with appropriate extension
5. Add your content

---

## Step 2: Stage the Files

1. **Open Source Control**
   - Press `Cmd + Shift + G`
   - Or click the Source Control icon in the left sidebar (looks like a branch)

2. **Stage your changes**
   - You'll see your new/modified files under "Changes"
   - Hover over each file you want to include
   - Click the `+` button that appears
   - The files move to "Staged Changes"

**Tip**: To stage all changes at once, click the `+` next to "Changes" header

---

## Step 3: Commit the Files

1. **Write a commit message**
   - In the message box at the top, write a descriptive message
   - Follow conventional format:
     ```
     feat: add user authentication
     fix: resolve database connection issue
     docs: update API documentation
     style: format code with black
     test: add unit tests
     chore: update dependencies
     ```

2. **Commit**
   - Press `Cmd + Enter`
   - Or click the checkmark (✓) button

---

## Step 4: Push to GitHub

**Regular push:**
1. Click the "Sync Changes" button (🔄) in the Source Control panel
2. Your changes are now on GitHub!

**First time pushing to a new branch:**
1. Click "Sync Changes" or "Publish Branch"
2. If prompted about upstream branch, click "OK"
3. Enter your GitHub username when prompted
4. For password, use your Personal Access Token

**Alternative push methods:**
- Click the cloud icon with an up arrow in the bottom status bar
- Use Command Palette: `Cmd + Shift + P` → type "Git: Push"

---

## Verify Your Changes on GitHub

1. Go to https://github.com/athemelis/obsidian
2. Check that your files appear
3. Click on "commits" to see your commit history

---

## Common Workflows

### Quick Daily Workflow
After making changes:
1. `Cmd + Shift + G` (Source Control)
2. Click `+` on changed files (stage)
3. Type commit message
4. `Cmd + Enter` (commit)
5. Click sync button (push)

### Working with Multiple Files
1. Make all your changes
2. Stage files selectively or all at once
3. Write one commit message describing all changes
4. Commit and sync

### Pulling Latest Changes
Before starting work:
1. Open Source Control (`Cmd + Shift + G`)
2. Click the "..." menu
3. Select "Pull" or click sync button

---

## Troubleshooting

### "No remote repository" Error
```bash
# In VSCode terminal (Ctrl + `)
git remote add origin https://github.com/athemelis/obsidian.git
```

### Authentication Failed
1. Make sure you're using your Personal Access Token as the password
2. Your username should be your GitHub username (athemelis)
3. Regenerate token if needed: GitHub → Settings → Developer settings → Personal access tokens

### Merge Conflicts
1. Pull latest changes first
2. VSCode will show conflicting files in red
3. Click on each file to resolve conflicts
4. Stage resolved files
5. Commit and push

### Push Rejected
This means the remote has changes you don't have:
1. Click "Pull" first
2. Resolve any conflicts if they arise
3. Then push again

---

## VSCode Git Shortcuts

- `Cmd + Shift + G`: Open Source Control
- `Cmd + Enter`: Commit staged changes
- `Cmd + Shift + P`: Command Palette (search for Git commands)

## Status Bar Indicators

Bottom left of VSCode shows:
- Current branch name
- Sync status (pending changes)
- Click branch name to switch branches

---

## Best Practices

1. **Commit frequently**: Small, focused commits are better than large ones
2. **Write clear messages**: Future you will thank present you
3. **Pull before pushing**: Always sync before starting work
4. **Review changes**: Check what you're committing before pushing

---

## Getting Help

If you encounter errors:
1. Note the exact error message
2. Check which step you were on
3. Try the troubleshooting section
4. Search for the error message online

Remember: Git keeps a history of everything, so don't worry about making mistakes - you can always revert changes!