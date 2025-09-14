#!/bin/bash
# Manual trigger for Obsidian-Reminders sync

# Use the correct path and filename
SCRIPT_DIR="/Users/tonythem/Github/obsidian/Reminders"
LOG_DIR="$SCRIPT_DIR/Logs"
LOG_FILE="$LOG_DIR/obsidian_reminders_sync.log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo "🔄 Starting Obsidian-Reminders sync..."
python3 "$SCRIPT_DIR/obsidian-reminders-sync.py"

# Check if sync was successful
if [ $? -eq 0 ]; then
    echo "✅ Sync completed successfully!"
    echo "📋 Check the log at: $LOG_FILE"
else
    echo "❌ Sync failed! Check the log for details."
    if [ -f "$LOG_FILE" ]; then
        tail -n 20 "$LOG_FILE"
    else
        echo "Log file not found yet."
    fi
fi
