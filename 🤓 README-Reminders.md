---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
Date modified: 07/07/2025
Version: 0.2
---

# Obsidian-Reminders Bidirectional Sync

A Python-based synchronization system that keeps your Obsidian tasks and macOS Reminders in perfect harmony.

## Overview

This tool provides bidirectional synchronization between:
- **Obsidian tasks** (using the `- [ ]` format) in your vault
- **macOS Reminders** app lists

### Key Features

- 🔄 **Bidirectional sync** - Changes in either app sync to the other
- 🏷️ **Metadata preservation** - Syncs due dates, priorities, and tags
- 📚 **Smart archiving** - Completed tasks are archived with full history
- 😊 **Emoji support** - Handles emojis in note/list names gracefully
- ⚡ **Flexible triggers** - Run manually or automatically every 3 minutes
- 🔧 **Conflict resolution** - Obsidian changes take priority in conflicts

## Requirements

- macOS (for Reminders app integration)
- Python 3.x
- Homebrew (for package management)
- Obsidian vault at `/Users/tonythem/Obsidian/tonythem/`

## Installation

### 1. Install Python Dependencies

```bash
pip3 install watchdog pyyaml python-dateutil
```

### 2. Clone or Download the Scripts

Place all scripts in `/Users/tonythem/Github/obsidian/Reminders/`

### 3. Set Up the Logs Directory

```bash
cd /Users/tonythem/Github/obsidian/Reminders
chmod +x setup-logs-directory.sh
./setup-logs-directory.sh
```

### 4. Make Scripts Executable

```bash
chmod +x sync-trigger-script.sh
chmod +x test-reminders-applescript.sh
```

### 5. Configure the LaunchAgent (for automatic sync)

```bash
# Copy the plist file to LaunchAgents
cp com.tonythem.obsidian-reminders-sync.plist ~/Library/LaunchAgents/

# Load the agent
launchctl load ~/Library/LaunchAgents/com.tonythem.obsidian-reminders-sync.plist
```

### 6. Add Convenient Aliases (Optional)

Add to your `~/.zshrc`:

```bash
# Obsidian Reminders Sync helpers
alias sync-reminders="/Users/tonythem/Github/obsidian/Reminders/sync-trigger-script.sh"
alias sync-logs="tail -f /Users/tonythem/Github/obsidian/Reminders/Logs/obsidian_reminders_sync.log"
alias sync-logs-all="ls -la /Users/tonythem/Github/obsidian/Reminders/Logs/"
```

Then reload:
```bash
source ~/.zshrc
```

## How to Use

### Manual Sync

Run the sync manually at any time:

```bash
# Using the full path
/Users/tonythem/Github/obsidian/Reminders/sync-trigger-script.sh

# Or if you set up the alias
sync-reminders
```

### Automatic Sync

The LaunchAgent runs the sync automatically every 3 minutes when loaded.

**To manage automatic sync:**

```bash
# Stop automatic sync
launchctl unload ~/Library/LaunchAgents/com.tonythem.obsidian-reminders-sync.plist

# Start automatic sync
launchctl load ~/Library/LaunchAgents/com.tonythem.obsidian-reminders-sync.plist

# Check if it's running
launchctl list | grep obsidian-reminders
```

### Task Format Support

The sync supports tasks with the following metadata:

```markdown
- [ ] Basic task
- [ ] Task with #tag1 #tag2
- [ ] Task with priority ![high]
- [ ] Task with due date ^due(2024-12-25)
- [ ] Complete task #urgent ![high] ^due(2024-12-25)
```

### How Sync Works

1. **Obsidian → Reminders**:
   - Creates a Reminders list matching the Obsidian note name
   - Syncs all tasks with their metadata
   - Handles emojis in note names (e.g., "📚 Reading List" → "Reading List")

2. **Reminders → Obsidian**:
   - Creates notes for new Reminders lists
   - Adds tasks to the top of notes (after frontmatter)
   - Preserves all task metadata

3. **Completed Tasks**:
   - Archived to `🔲 Framework/🎗️ Reminders/📚 Archive.md`
   - Grouped by source note with completion dates
   - Removed from both Obsidian and Reminders

4. **Conflict Resolution**:
   - If a task exists in both places with different states
   - Obsidian version takes priority

## Viewing Logs

### Log Locations

All logs are stored in `/Users/tonythem/Github/obsidian/Reminders/Logs/`

### Real-time Log Monitoring

```bash
# Watch the main sync log
tail -f /Users/tonythem/Github/obsidian/Reminders/Logs/obsidian_reminders_sync.log

# Watch for errors
tail -f /Users/tonythem/Github/obsidian/Reminders/Logs/obsidian_reminders_sync_stderr.log

# Or use the alias
sync-logs
```

### View All Logs

```bash
ls -la /Users/tonythem/Github/obsidian/Reminders/Logs/

# Or use the alias
sync-logs-all
```

## File Inventory

### Core Scripts

| File | Location | Purpose |
|------|----------|---------|
| `obsidian-reminders-sync.py` | `/Users/tonythem/Github/obsidian/Reminders/` | Main sync engine - handles all sync logic |
| `sync-trigger-script.sh` | `/Users/tonythem/Github/obsidian/Reminders/` | Manual trigger wrapper script |
| `test-reminders-applescript.sh` | `/Users/tonythem/Github/obsidian/Reminders/` | Debug tool for testing Reminders access |
| `setup-logs-directory.sh` | `/Users/tonythem/Github/obsidian/Reminders/` | Initial setup script for logs directory |

### Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| `com.tonythem.obsidian-reminders-sync.plist` | `~/Library/LaunchAgents/` | LaunchAgent config for automatic sync |

### Log Files

| File | Location | Purpose |
|------|----------|---------|
| `obsidian_reminders_sync.log` | `/Users/tonythem/Github/obsidian/Reminders/Logs/` | Main activity log |
| `obsidian_reminders_sync_stdout.log` | `/Users/tonythem/Github/obsidian/Reminders/Logs/` | Standard output from background runs |
| `obsidian_reminders_sync_stderr.log` | `/Users/tonythem/Github/obsidian/Reminders/Logs/` | Error output from background runs |
| `obsidian_reminders_sync_state.pkl` | `/Users/tonythem/Github/obsidian/Reminders/Logs/` | Persistent state between sync runs |

### Obsidian Files

| File | Location | Purpose |
|------|----------|---------|
| Task notes | `/Users/tonythem/Obsidian/tonythem/**/*.md` | Your Obsidian notes containing tasks |
| Archive | `/Users/tonythem/Obsidian/tonythem/🔲 Framework/🎗️ Reminders/📚 Archive.md` | Completed tasks archive |

## Troubleshooting

### Common Issues

1. **"No such file or directory" error**
   - Ensure all paths in the scripts match your actual file locations
   - Run `pwd` to check your current directory

2. **AppleScript errors with Reminders**
   - Grant Terminal/Python permission to access Reminders in System Preferences
   - Run the test script: `./test-reminders-applescript.sh`

3. **Tasks not syncing**
   - Check the log file for specific errors
   - Ensure task format is correct (`- [ ] Task text`)
   - Verify Reminders app permissions

4. **Duplicate tasks appearing**
   - This should be prevented, but if it happens, check logs for errors
   - The sync state file may need to be reset

### Permissions

On first run, macOS will ask for permission to:
- Access Reminders app
- Access your Obsidian vault files

Grant these permissions for the sync to work properly.

### Debug Mode

To see more detailed output, run the Python script directly:

```bash
cd /Users/tonythem/Github/obsidian/Reminders
python3 obsidian-reminders-sync.py
```

## Customization

### Change Sync Frequency

Edit the LaunchAgent plist file and modify the `StartInterval` value (in seconds):

```xml
<key>StartInterval</key>
<integer>180</integer> <!-- 3 minutes -->
```

Then reload the LaunchAgent.

### Change Vault Location

Edit `obsidian-reminders-sync.py` and update:

```python
VAULT_PATH = "/Users/tonythem/Obsidian/tonythem"
```

### Change Archive Location

Edit `obsidian-reminders-sync.py` and update:

```python
ARCHIVE_PATH = "🔲 Framework/🎗️ Reminders/📚 Archive.md"
```

## Support

For issues or questions:
1. Check the logs first - they usually contain helpful error messages
2. Run the test script to verify Reminders access
3. Ensure all file paths are correct for your system

## License

This tool is provided as-is for personal use.

---

*Built with ❤️ for better task management between Obsidian and macOS Reminders*