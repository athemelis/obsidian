# Obsidian Tools Suite

A powerful set of tools for managing and modifying Obsidian vault notes in bulk, with advanced query capabilities and search/replace functionality.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Features Overview](#features-overview)
3. [Installation & Setup](#installation--setup)
4. [User Guide](#user-guide)
   - [Query Tool Usage](#query-tool-usage)
   - [Search & Replace Usage](#search--replace-usage)
5. [Technical Reference](#technical-reference)
   - [Architecture](#architecture)
   - [File Structure](#file-structure)
   - [API Endpoints](#api-endpoints)
6. [Configuration](#configuration)
7. [Safety & Backups](#safety--backups)
8. [Troubleshooting](#troubleshooting)
9. [Development Notes](#development-notes)
10. [Roadmap](#roadmap)

---

## Quick Start

1. **Start the server**:
   ```bash
   ./start_server.sh
   ```

2. **Open your browser** to the URL shown (typically `http://localhost:5001`)

3. **Configure your vault paths** in the web interface

That's it! You're ready to use the tools.

## Features Overview

### 1. **Note Query & Modifier Tool**
- Build complex boolean queries to find notes by frontmatter properties
- Supports AND/OR/NOT operators with parentheses for grouping
- Property existence operators (`exists` and `does not exist`)
- Bulk modify properties across multiple notes
- Save and reuse queries
- Import/export queries between vaults
- Table view with sortable columns
- Undo/redo support (up to 50 states)
- Keyboard shortcuts for power users

### 2. **Search & Replace Tool**
- Search and replace text across your entire vault
- Wildcard support (* and ?)
- Search in file contents, filenames, or both
- Protect wikilinks from replacement
- Real-time folder/file filtering
- Preview all changes before applying

### 3. **Automatic Backup System**
- Creates automatic backups before any modifications
- Keeps the 3 most recent backups
- Complete modification logging with timestamps

## Installation & Setup

### Requirements
- **Python 3.6+**
- **macOS** (tested on macOS with zsh, may work on other platforms)
- **Modern web browser** (Chrome, Firefox, Safari)

### Initial Setup
The `start_server.sh` script handles everything automatically:
- Creates Python virtual environment
- Installs required packages (Flask, flask-cors, PyYAML)
- Finds available port (5001-5002)
- Starts the server

### Manual Installation (if needed)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install flask flask-cors pyyaml

# Run server
python obsidian_tools_server.py
```

## User Guide

### Query Tool Usage

#### Building Queries

**Visual Query Builder** (Recommended for beginners):
1. Select a property from the dropdown
2. Choose an operator (equals, contains, exists, etc.)
3. Enter a value (if needed)
4. Click "Add Condition"
5. Combine conditions with AND/OR/NOT buttons

**Direct Query Editor** (For advanced users):
Write queries directly using this syntax:
```
PropertyName operator "value"
```

#### Query Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `equals` | Exact match | `Status equals "Active"` |
| `contains` | Substring match | `Title contains "Project"` |
| `startsWith` | Begins with | `Name startsWith "TODO"` |
| `endsWith` | Ends with | `File endsWith ".md"` |
| `exists` | Property has non-empty value | `Stakeholder exists` |
| `does not exist` | Property missing or empty | `DueDate does not exist` |

#### Example Queries

**Simple Queries:**
```
Status equals "Active"
Priority exists
Assignee does not exist
```

**Complex Queries:**
```
(Type equals "Project" OR Type equals "Task") AND NOT Status equals "Completed"

Stakeholder does not exist AND Priority equals "High"

(Category equals "[[🏢 Companies]]" AND Status equals "Active") OR Archived equals false
```

#### Modifying Properties

1. **Change existing values**: 
   - Original Value: `Old Status`
   - New Value: `New Status`

2. **Add new properties**:
   - Leave Original Value empty
   - Select property type
   - Enter new value

#### Property Types

| Type | Format | Example |
|------|--------|---------|
| Text | Plain string | `"Active Project"` |
| List | Comma-separated | `"tag1, tag2, tag3"` |
| Number | Numeric | `42` |
| Checkbox | Boolean | `true` or `false` |
| Date | YYYY-MM-DD | `2024-06-14` |
| DateTime | YYYY-MM-DD HH:MM | `2024-06-14 15:30` |

#### Keyboard Shortcuts

- **Enter** in property field → Jump to value field
- **Enter** in value field → Add condition
- **Ctrl/Cmd + Enter** → Execute query
- **Ctrl/Cmd + Z** → Undo
- **Ctrl/Cmd + Y** → Redo
- **Escape** → Clear current inputs

### Search & Replace Usage

#### Search Patterns

Use wildcards for flexible matching:
- `*` - Any number of characters
- `?` - Single character

**Examples:**
- `TODO*` matches "TODO", "TODO:", "TODO list"
- `Project?` matches "Project1", "ProjectA"
- `*meeting*` matches any text containing "meeting"

#### Replacement Options

1. **Search scope**:
   - Entire vault
   - Specific folder
   - Single file

2. **Search in**:
   - File contents only
   - Filenames only
   - Both

3. **Wikilink protection**:
   - Check "Exclude matches within wikilinks"
   - Preserves `[[Internal Links]]`

#### Workflow Example

1. Select target folder: `Projects/Active/`
2. Enter search pattern: `TODO*`
3. Preview matches (shows affected files)
4. Enter replacement: `DONE`
5. Preview changes (shows before/after)
6. Click "Apply Changes"

## Technical Reference

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│   Flask Server  │────▶│  Obsidian Vault │
│  (HTML/JS UI)   │◀────│    (Python)     │◀────│   (Markdown)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │ Config & Logs   │
                        │  (JSON files)   │
                        └─────────────────┘
```

### File Structure

```
obsidian-tools/
├── Core Files
│   ├── obsidian_tools_server.py    # Flask server (1,087 lines)
│   ├── index.html                  # Main menu (351 lines)
│   ├── query_tool.html             # Query interface (1,462 lines)
│   ├── search_replace_tool.html    # Search interface (513 lines)
│   └── start_server.sh             # Startup script (68 lines)
│
├── Configuration (auto-generated)
│   ├── vault_config.json           # Vault paths
│   ├── server_config.json          # Server settings
│   ├── saved_queries.json          # User's saved queries
│   └── modification_log.json       # Change history
│
├── Documentation
│   └── README.md                   # This file
│
└── Virtual Environment
    └── venv/                       # Python packages
```

### API Endpoints

#### Core Endpoints
- `GET /` - Serve main menu
- `GET /health` - Health check
- `GET /api/config` - Get configuration
- `POST /api/config` - Update configuration

#### Query Tool Endpoints
- `POST /api/query` - Execute query
- `GET /api/saved_queries` - Get saved queries
- `POST /api/saved_queries` - Save new query
- `DELETE /api/saved_queries/<id>` - Delete query
- `POST /api/modify` - Apply modifications
- `GET /api/folders` - List vault folders
- `GET /api/files/<path>` - List files in folder

#### Search & Replace Endpoints
- `POST /api/search` - Search for pattern
- `POST /api/replace_preview` - Preview replacements
- `POST /api/replace` - Apply replacements

## Configuration

### vault_config.json
```json
{
  "vault_path": "/Users/username/Obsidian/vault/",
  "backup_path": "/Users/username/Obsidian/backups/"
}
```

### server_config.json
```json
{
  "port": 5001,
  "host": "localhost"
}
```

### saved_queries.json
```json
[
  {
    "id": "uuid-here",
    "expression": "Status equals \"Active\"",
    "displayText": "Status equals \"Active\"",
    "createdAt": "2024-06-14T10:30:00Z"
  }
]
```

## Safety & Backups

### Automatic Backup System
- **Before every modification**: Full backup created
- **Backup naming**: `backup_YYYYMMDD_HHMMSS/`
- **Retention policy**: Keeps 3 most recent backups
- **Location**: Configured backup directory

### Modification Logging
Every change is logged with:
- Timestamp
- Action performed
- Files affected
- Original and new values
- Backup location

### Best Practices
1. **Test first**: Use "Modify First File" option
2. **Preview always**: Review changes before applying
3. **Regular backups**: Set backup path to cloud-synced folder
4. **Check logs**: Review `modification_log.json` after bulk operations

## Troubleshooting

### Common Issues

**Server won't start**
- Check Python version: `python3 --version` (need 3.6+)
- Verify port availability (5001-5002)
- Check script permissions: `chmod +x start_server.sh`

**Can't find property type selector**
- Click "Show/Hide Type" button
- Ensure "Original Value" field is empty

**Query validation errors**
- Red highlighting indicates syntax errors
- Check for unmatched parentheses
- Verify operator placement

**Button click errors ("not defined")**
- Hard refresh page (Ctrl/Cmd + F5)
- Check browser console for JavaScript errors
- Disable interfering browser extensions

### Performance Issues

**Slow query execution**
- Large vaults (1000+ files) take longer
- Consider using folder scoping
- Close other applications to free memory

**Backup creation slow**
- Normal for large vaults
- Ensure sufficient disk space
- Check backup path permissions

## Development Notes

### Tech Stack Details
- **Backend**: Python 3.6+ with Flask
- **Frontend**: Vanilla HTML/JavaScript (no frameworks)
- **Styling**: Inline CSS for portability
- **Storage**: JSON files for configuration and state

### Key Design Decisions

1. **Why Flask?** Lightweight, easy to deploy, perfect for local tools
2. **Why inline CSS?** Single-file distribution, no build process
3. **Why JSON storage?** Simple, human-readable, no database needed
4. **Global function scope**: Ensures reliable button onclick handlers

### Recent Changes (v2.2.0 - 2024-06-14)

**New Features:**
- Property existence operators (`exists`/`does not exist`)
- Flexible search options (scope-only, query-only, or both)
- Enhanced table view with Team column
- Progress indicators for all operations

**Bug Fixes:**
- Fixed JavaScript scope issues with button handlers
- Resolved folder clear button functionality
- Improved operator validation logic

### Code Organization

**obsidian_tools_server.py**
```python
# Main sections:
# 1. Configuration management (lines 1-150)
# 2. File operations (lines 151-400)
# 3. Query processing (lines 401-700)
# 4. API endpoints (lines 701-1087)
```

**Frontend Structure**
- Each HTML file is self-contained
- JavaScript in `<script>` tags at bottom
- CSS in `<style>` tags in head
- No external dependencies

## Roadmap

### Short-term (Next Release)
- [ ] Export query results to CSV
- [ ] Query templates for common operations
- [ ] Property name auto-completion
- [ ] Dark mode theme toggle
- [ ] Batch operation queuing

### Medium-term (3-6 months)
- [ ] Query history beyond undo/redo
- [ ] Scheduled operations (cron-like)
- [ ] Dry run mode for testing
- [ ] Property usage analytics
- [ ] Regular expression support

### Long-term Vision
- [ ] Obsidian plugin version
- [ ] Multi-vault management
- [ ] Collaboration features
- [ ] AI-powered query suggestions
- [ ] Performance optimizations for huge vaults

### Known Limitations
1. Platform testing limited to macOS
2. Performance degrades with 10,000+ files
3. No concurrent user support
4. Property types are predefined
5. No nested property queries

### Contributing
To extend the tools:
1. Core logic: Modify `obsidian_tools_server.py`
2. UI changes: Edit respective HTML files
3. New endpoints: Add to Flask routes
4. Test thoroughly with sample vault

---

**Version**: 2.2.0  
**Last Updated**: 2024-06-14  
**Status**: Production Ready  
**License**: Provided as-is for personal use with Obsidian vaults