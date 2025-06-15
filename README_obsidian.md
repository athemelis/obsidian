# Obsidian Tools Suite

A powerful set of tools for managing and modifying Obsidian vault notes in bulk, with advanced query capabilities and search/replace functionality.

## 📚 Documentation Overview

This README covers:

1. **Quick Start** - Get running in 3 simple steps
2. **Features** - Overview of both tools and backup system
3. **File Structure** - Visual representation of all files
4. **File Descriptions** - Detailed explanation of each file's purpose
5. **Configuration Files** - Examples of auto-generated files
6. **Usage Guide** - Step-by-step instructions for both tools
7. **Requirements** - System and package requirements
8. **Safety Features** - Backup and preview capabilities
9. **Troubleshooting** - Common issues and solutions
10. **Tips** - Best practices for using the tools

### Notable Documentation Includes:
- **Query syntax examples** for complex boolean expressions
- **Property type formats** for adding new properties
- **Wildcard usage** in search and replace
- **File locations** and what each stores
- **Safety reminders** about backups
- **Keyboard shortcuts** for power users

---

## 🚀 Quick Start

1. **Start the server**:
   ```bash
   ./start_server.sh
   ```

2. **Open your browser** to the URL shown (typically `http://localhost:5001`)

3. **Configure your vault paths** in the web interface

## 📋 Features

### 1. **Note Query & Modifier Tool**
- Build complex boolean queries to find notes by frontmatter properties
- Supports AND/OR/NOT operators with parentheses for grouping
- **NEW: Property existence operators**:
  - **exists** - finds notes where property has a non-empty value
  - **does not exist** - finds notes where property is missing, null, or empty
- **Flexible Search Options**:
  - Search by query only (across entire vault)
  - Search by scope only (all files in selected folder/file)
  - Combine scope and query for targeted searches
- Modify properties across multiple notes simultaneously
- Add new properties with specific types (Text, List, Number, Checkbox, Date, DateTime)
- Save and reuse queries for repeated operations
- Preview changes before applying them
- **Enhanced Features (v2.2):**
  - **Property Existence Queries** - Find notes with or without specific properties
  - **Real-time Query Validation** - Visual feedback for syntax errors
  - **Undo/Redo Support** - Up to 50 history states
  - **Import/Export Queries** - Share queries between vaults
  - **Keyboard Shortcuts** - Faster workflow for power users
  - **Error Indicators** - Red highlighting for invalid queries
  - **Table View Results** - Query results display with property columns
  - **Folder/File Scoping** - Limit searches to specific locations
  - **Progress Indicators** - Visual feedback during modifications

### 2. **Search & Replace Tool**
- Search and replace text across your entire vault
- Support for wildcards (* and ?)
- Search in file contents, filenames, or both
- Exclude matches within wikilinks [[...]]
- Real-time search for folders and files
- Preview all changes before applying
- Case-sensitive matching

### 3. **Automatic Backup System**
- Creates automatic backups before any modifications
- Keeps the 3 most recent backups
- Backups stored in your configured backup directory

## 📁 File Structure

```
obsidian-tools/
├── obsidian_tools_server.py    # Main server application
├── index.html                  # Main menu interface
├── query_tool.html             # Query & Modifier interface
├── search_replace_tool.html    # Search & Replace interface
├── start_server.sh             # Server startup script
├── README.md                   # This documentation
│
├── vault_config.json           # Vault and backup paths (created on first run)
├── server_config.json          # Server port configuration (created on startup)
├── modification_log.json       # Log of all modifications (created after first change)
└── saved_queries.json          # Your saved queries (created when saving queries)
```

## 📄 File Descriptions

### **Core Files**

#### `obsidian_tools_server.py`
The main Python server that handles all operations.
- **Purpose**: Processes queries, performs modifications, handles search/replace
- **Note**: Don't run this directly - use `start_server.sh` instead

#### `start_server.sh`
Bash script that starts the server with proper environment setup.
- **Purpose**: Ensures Python virtual environment is set up and starts the server
- **Usage**: `./start_server.sh`
- **Features**: 
  - Automatically finds an available port
  - Creates virtual environment if needed
  - Installs required packages (Flask, PyYAML, flask-cors)

#### `index.html`
The main menu page.
- **Purpose**: Central hub for accessing tools and configuring paths
- **Features**:
  - Configure vault and backup paths
  - View backup information
  - Navigate to specific tools

#### `query_tool.html`
The Note Query & Modifier interface.
- **Purpose**: Find and modify notes based on frontmatter properties
- **Features**:
  - Visual query builder
  - Direct query editor for advanced users
  - Saved queries with search functionality
  - Property type selection for new properties
  - Bulk modification with preview
  - **New in v2.2:**
    - Property existence operators (exists/does not exist)
    - Dynamic value input field disabling
  - **New in v2.0:**
    - Query validation with error messages
    - Undo/redo functionality
    - Import/export saved queries
    - Enhanced keyboard shortcuts
    - **Table view for results with property columns**

#### `search_replace_tool.html`
The Search & Replace interface.
- **Purpose**: Find and replace text across your vault
- **Features**:
  - Folder/file search and selection
  - Wildcard support
  - Wikilink exclusion option
  - Preview before replacing

### **Configuration Files** (Auto-generated)

#### `vault_config.json`
Stores your vault and backup directory paths.
```json
{
  "vault_path": "/Users/tonythem/Obsidian/tonythem/",
  "backup_path": "/Users/tonythem/Obsidian/backups/"
}
```

#### `server_config.json`
Stores the current server configuration.
```json
{
  "port": 5001,
  "host": "localhost"
}
```

#### `modification_log.json`
Detailed log of all modifications made to your vault.
- Contains timestamps, actions, affected files, and backup locations
- Useful for auditing changes

#### `saved_queries.json`
Your saved queries for the Query Tool.
- Stores query expressions and metadata
- Persists across server restarts
- Can be exported and imported

## 🛠️ Usage Guide

### **Query Tool Usage**

1. **Building a Query**:
   - Use the visual builder to add conditions
   - Combine with AND/OR/NOT operators
   - Or switch to "Query Editor" tab to write directly
   - **New**: Watch for red highlighting if query is invalid

2. **Query Operators**:
   - **equals** - exact match
   - **contains** - substring match
   - **startsWith** - prefix match
   - **endsWith** - suffix match
   - **exists** - property has a non-empty value (NEW)
   - **does not exist** - property is missing or empty (NEW)

3. **Example Queries**:
   ```
   Obsidian equals "[[🦋 Categories]]"
   
   Category equals "[[🏢 Companies]]" AND Status equals "Active"
   
   (Type equals "Project" OR Type equals "Task") AND NOT Status equals "Completed"
   
   Stakeholder does not exist
   
   Stakeholder exists AND Team equals "Engineering"
   
   (Stakeholder does not exist OR Stakeholder equals "") AND Priority equals "High"
   ```

4. **Using Existence Operators** (NEW):
   - Select property name (e.g., "Stakeholder")
   - Choose "exists" or "does not exist" from operator dropdown
   - Value field automatically disables (no value needed)
   - Click "Add Condition"
   - Useful for finding notes missing required properties

5. **Adding New Properties**:
   - Leave "Original Value" empty
   - Choose property type from dropdown
   - Enter new value according to type format

6. **Property Types**:
   - **Text**: Single string value
   - **List**: Comma-separated values (becomes YAML list)
   - **Number**: Numeric value
   - **Checkbox**: true/false
   - **Date**: YYYY-MM-DD format
   - **DateTime**: YYYY-MM-DD HH:MM format

7. **Keyboard Shortcuts**:
   - **Enter** in property name → Focus value field
   - **Enter** in value field → Add condition
   - **Ctrl/Cmd + Z** → Undo last change
   - **Ctrl/Cmd + Y** or **Ctrl/Cmd + Shift + Z** → Redo
   - **Ctrl/Cmd + Enter** → Execute query
   - **Escape** → Clear current inputs

8. **Import/Export Queries**:
   - Click "Export All Queries" to save queries to JSON file
   - Click "Import Queries" to load queries from file
   - Choose to add to existing queries or replace all

### **Search & Replace Usage**

1. **Search Patterns**:
   - Use `*` for any number of characters
   - Use `?` for single character
   - Example: `TODO*` finds "TODO", "TODO:", "TODO list", etc.

2. **Wikilink Protection**:
   - Check "Exclude matches within wikilinks" to preserve [[links]]
   - Example: Won't replace "Project" in "[[Project Management]]"

3. **Workflow**:
   - Select target folder
   - Enter search pattern
   - Preview results
   - Enter replacement text
   - Preview changes
   - Apply changes

## ⚙️ Requirements

- **Python 3.6+**
- **macOS** (tested on macOS with zsh)
- **Packages** (auto-installed by start script):
  - Flask
  - flask-cors
  - PyYAML

## 🔒 Safety Features

1. **Automatic Backups**: Every modification creates a timestamped backup
2. **Preview Mode**: See exactly what will change before applying
3. **Backup Retention**: Keeps last 3 backups to prevent disk space issues
4. **Change Logging**: Complete audit trail of all modifications
5. **Query Validation**: Prevents execution of invalid queries (v2.0)
6. **Undo/Redo**: Revert query changes easily (v2.0)

## 🐛 Troubleshooting

### Server won't start
- Check if port 5001-5002 are in use
- Verify Python 3 is installed: `python3 --version`
- Check permissions on start script: `chmod +x start_server.sh`

### Can't see property type selector
- Click "Show/Hide Type" button next to Original Value field
- Ensure Original Value field is completely empty

### Saved queries disappeared
- Check if `saved_queries.json` exists in the script directory
- Queries are saved per-directory, not per-vault
- Use the export feature to backup queries

### Connection errors
- Ensure the server is running (check terminal)
- Try refreshing the browser
- Check browser console for errors (F12)

### Query validation errors (v2.0)
- Red highlighting indicates syntax errors
- Check for unmatched parentheses
- Ensure queries don't end with operators
- Validate operator sequences

### Button click errors (v2.2)
- If AND/OR/NOT buttons show "not defined" errors, hard refresh the page (Ctrl+F5)
- Check browser console for JavaScript errors
- Ensure no browser extensions are interfering

## 💡 Tips

1. **Query Reuse**: Save frequently used queries for quick access
2. **Test First**: Use "Modify First File" to test changes on one file
3. **Wildcards**: Use `*` liberally in searches, e.g., `*TODO*`
4. **Backup Location**: Configure backup path to a cloud-synced folder for extra safety
5. **Complex Queries**: Use parentheses to group conditions properly
6. **Keyboard Efficiency**: Learn the shortcuts for faster query building
7. **Query Sharing**: Export queries to share with team members
8. **Version Control**: Export queries before major vault changes
9. **Finding Missing Properties**: Use "does not exist" to audit your vault for missing metadata
10. **Property Cleanup**: Combine "exists" with other conditions to find and fix incomplete notes

## 🆕 What's New in v2.2

### Property Existence Operators
- **"exists" operator**: Finds notes where property has any non-empty value
- **"does not exist" operator**: Finds notes where property is missing, null, or empty
- Value field automatically disabled when these operators are selected
- Works with all property types (text, list, number, etc.)
- Perfect for finding notes missing required metadata

### Technical Improvements
- Fixed JavaScript scope issues with button handlers
- Moved critical functions to global scope for reliability
- Cleaned up debugging code for better performance
- Improved operator validation logic

### Example Use Cases
- Find all notes without a Stakeholder: `Stakeholder does not exist`
- Find incomplete projects: `Status does not exist AND Type equals "Project"`
- Find properly tagged notes: `Tags exists AND Category exists`
- Audit for missing dates: `created does not exist OR modified does not exist`

## 🆕 What's New in v2.1

### Flexible Search Options
- Search by scope only (folder/file)
- Search by query only (properties)
- Combine both for targeted searches
- Optional query building

### Enhanced Table View
- Added Team column to results
- Improved property formatting
- Better visual indicators

### Progress Indicators
- Visual feedback during modifications
- Loading spinners for all operations
- Clear progress messages

### Bug Fixes
- Fixed folder clear button functionality
- Improved scope selection behavior
- Better error handling

### Previous v2.0 Features

### Query Validation
- Real-time syntax checking
- Visual feedback with red highlighting
- Clear error messages for common mistakes
- Parentheses balance checking

### Undo/Redo System
- Up to 50 history states
- Keyboard shortcuts (Ctrl/Cmd + Z/Y)
- Works for all query modifications

### Import/Export
- Export all saved queries to JSON
- Import queries from other vaults
- Merge or replace existing queries
- Automatic duplicate removal

### Enhanced Keyboard Support
- Quick condition entry with Enter key
- Execute queries with Ctrl/Cmd + Enter
- Clear inputs with Escape
- Full undo/redo shortcuts

### Table View Results
- Query results in organized table format
- Columns for key properties
- Visual property type indicators
- Efficient file selection
- Export results to CSV (coming soon)

## 📝 License

This tool is provided as-is for personal use with Obsidian vaults. Always backup your data before bulk operations.

## 🤝 Contributing

To extend or modify these tools:
1. Core logic is in `obsidian_tools_server.py`
2. UI is in the respective HTML files
3. All styling is inline (no external CSS files)
4. Server uses Flask with simple REST endpoints

---

**Remember**: Always backup your vault before performing bulk operations!