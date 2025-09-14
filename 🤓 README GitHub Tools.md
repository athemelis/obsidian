# File Comparison (Diff) Guide for VSCode

This guide explains how to compare (diff) files in your local branch using VSCode's built-in features.

## Overview

VSCode provides multiple ways to compare files:
- Compare any two files side-by-side
- Compare versions of the same file over time
- Compare changes before committing
- Compare files across branches

---

## Method 1: Compare Any Two Files Side-by-Side

Perfect for comparing similar files or checking differences between files.

### Steps:
1. **Right-click the first file** in the Explorer panel
2. Select **"Select for Compare"**
3. **Right-click the second file**
4. Select **"Compare with Selected"**

### Result:
- VSCode opens both files in a diff view
- Left side shows first file
- Right side shows second file
- Differences are highlighted

---

## Method 2: Compare Different Versions of Same File

### A. Compare with Last Commit (Most Common)

See what you've changed since your last commit:

1. **Open Source Control** (`Cmd + Shift + G`)
2. Find your modified file under "Changes"
3. **Click on the file**

This shows:
- Left side: Last committed version
- Right side: Your current changes

### B. Compare with Previous Versions Using Timeline

1. **Click on the file** in Explorer to open it
2. Look for **"Timeline"** at the bottom of the Explorer sidebar
3. Expand Timeline to see file history
4. **Click any previous version** to compare with current

### C. Using Command Palette

1. Press `Cmd + Shift + P`
2. Type: **"Git: Open Changes"**
3. Select the file you want to compare

---

## Method 3: Compare Files from Different Branches

### Using GitLens Extension (Recommended)

1. **Install GitLens** if not already installed:
   - Open Extensions (`Cmd + Shift + X`)
   - Search "GitLens"
   - Install

2. **Right-click file** in Explorer
3. Select **"Open Changes" → "Open Changes with Branch..."**
4. Choose which branch to compare against

### Using Command Palette

1. Switch to the branch you want to compare from
2. `Cmd + Shift + P`
3. Type: **"Git: Open Changes with..."**
4. Select the branch to compare against

---

## Method 4: Compare Using Terminal

For those who prefer command line:

```bash
# Compare two different files
diff file1.py file2.py

# Compare with more context
diff -u file1.py file2.py

# Using git diff for tracked files
git diff file1.py

# Compare file between branches
git diff main obsidian-dev -- filename.py

# Compare two specific files
git diff --no-index file1.py file2.py
```

---

## Understanding the Diff View

### Visual Indicators

- **Red background (-)**: Lines removed
- **Green background (+)**: Lines added
- **Blue/Yellow highlights**: Modified portions within lines
- **Gray text**: Unchanged context lines

### Navigation Controls

| Action | Shortcut |
|--------|----------|
| Next change | `F7` |
| Previous change | `Shift + F7` |
| Jump to specific change | Click in overview ruler (right side) |
| Close diff view | `Cmd + W` |

### Diff View Options

Click the **"..."** menu in diff view for:
- Toggle inline/side-by-side view
- Toggle whitespace differences
- Ignore trim whitespace

---

## Common Use Cases

### 1. Review Changes Before Committing

1. Open Source Control (`Cmd + Shift + G`)
2. Click each file to review changes
3. Stage only reviewed files
4. Commit with confidence

### 2. Compare Configuration Files

1. Select `config.dev.json` → "Select for Compare"
2. Select `config.prod.json` → "Compare with Selected"
3. Review differences between environments

### 3. Check What Changed in a Merge

After merging branches:
1. Open Source Control
2. Review each conflicted file
3. Use diff view to resolve conflicts

### 4. Compare Entire Folders

1. Right-click first folder → "Select for Compare"
2. Right-click second folder → "Compare with Selected"
3. See all file differences between folders

---

## Advanced Features

### Inline Diff View

Instead of side-by-side comparison:
1. In diff view, click **"..."** menu
2. Select **"Toggle Inline View"**
3. Shows changes in a single column

### Three-Way Merge Editor

For merge conflicts:
1. Click on conflicted file
2. Click **"Open Merge Editor"**
3. See three panels:
   - Incoming changes (theirs)
   - Current changes (yours)
   - Result (combined)

### Compare with Clipboard

1. Copy text to clipboard
2. Select file in Explorer
3. `Cmd + Shift + P`
4. Type: **"Compare Active File with Clipboard"**

---

## Tips and Best Practices

### 1. Efficient Change Review

- Use `F7`/`Shift + F7` to quickly jump between changes
- Click on the overview ruler for bird's-eye navigation
- Review changes before every commit

### 2. Diff Settings

Add to VSCode settings for better diffs:
```json
{
    "diffEditor.ignoreTrimWhitespace": false,
    "diffEditor.renderSideBySide": true,
    "diffEditor.maxComputationTime": 5000
}
```

### 3. When to Use Each Method

- **Quick change review**: Source Control panel
- **Historical comparison**: Timeline view
- **Cross-file comparison**: Select for Compare
- **Complex diffs**: GitLens extension

---

## Troubleshooting

### "Select for Compare" Not Showing

- Make sure you right-clicked in the Explorer panel
- Try refreshing Explorer: `Cmd + Shift + P` → "File: Refresh Explorer"

### Diff View Not Opening

- Ensure files are saved
- Check if files are in the same workspace
- Try using Command Palette method instead

### Changes Not Showing in Source Control

- Make sure Git is initialized
- Check if files are in `.gitignore`
- Refresh Source Control: Click refresh icon

---

## Keyboard Shortcuts Summary

| Action | Shortcut |
|--------|----------|
| Open Source Control | `Cmd + Shift + G` |
| Command Palette | `Cmd + Shift + P` |
| Next diff | `F7` |
| Previous diff | `Shift + F7` |
| Close tab | `Cmd + W` |
| Toggle inline view | (Use ... menu) |

---

## External Tools

If you need more advanced diff capabilities:
- **Kaleidoscope**: Professional Mac diff tool
- **Beyond Compare**: Cross-platform comparison
- **Meld**: Free, open-source option

Configure external diff tool:
```bash
git config --global diff.tool <tool-name>
git difftool file1.py file2.py
```

Remember: VSCode's built-in diff tools are sufficient for most development needs!