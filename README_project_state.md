# Obsidian Tools Suite - Project State Document

## Project Overview

### Description
A powerful set of tools for managing and modifying Obsidian vault notes in bulk, with advanced query capabilities and search/replace functionality. The suite consists of two main tools served through a Flask web server:

1. **Note Query & Modifier Tool** - Build complex boolean queries to find notes by frontmatter properties and modify them in bulk
2. **Search & Replace Tool** - Search and replace text patterns across the entire vault with wildcard support

### Tech Stack
- **Backend**: Python 3.6+ with Flask
- **Frontend**: Vanilla HTML/JavaScript with inline CSS
- **Dependencies**: Flask, flask-cors, PyYAML
- **Platform**: macOS (tested on macOS with zsh)

### Current Status (2025-06-14)
- ✅ All major features implemented and working
- ✅ Both tools feature complete with folder/file scoping
- ✅ Table view for query results with property columns
- ✅ Progress indicators for all long-running operations
- ✅ Import/export functionality for saved queries
- ✅ Comprehensive keyboard shortcuts
- ✅ **NEW**: "exists" and "does not exist" operators for property queries

## Complete File Inventory

### Core Application Files
1. **obsidian_tools_server.py** (1,087 lines)
   - Main Flask server application
   - Handles all API endpoints for both tools
   - Manages configuration, backups, and file operations
   - Recent updates: Added scoped queries, property retrieval, exists/notExists operators

2. **index.html** (351 lines)
   - Main menu and configuration interface
   - Vault and backup path configuration
   - Navigation hub for both tools
   - Shows backup information and status

3. **query_tool.html** (1,462 lines)
   - Note Query & Modifier interface
   - Features: Visual query builder, saved queries, table results
   - Recent updates: Added folder/file scoping, Team column, progress indicators, exists/notExists operators

4. **search_replace_tool.html** (513 lines)
   - Search & Replace interface
   - Features: Wildcard support, wikilink protection, preview
   - Folder/file scoping with search functionality

5. **start_server.sh** (68 lines)
   - Server startup script
   - Handles virtual environment setup
   - Auto-detects available ports
   - Installs dependencies automatically

6. **README.md** (457 lines)
   - Comprehensive user documentation
   - Installation and usage instructions
   - Feature descriptions and examples
   - Troubleshooting guide

### Configuration Files (Auto-generated)
1. **vault_config.json**
   ```json
   {
     "vault_path": "/Users/tonythem/Obsidian/tonythem/",
     "backup_path": "/Users/tonythem/Obsidian/backups/"
   }
   ```

2. **server_config.json**
   ```json
   {
     "port": 5001,
     "host": "localhost"
   }
   ```

3. **saved_queries.json**
   - Stores user's saved queries with metadata
   - Supports import/export functionality
   - Format: Array of query objects with expression, displayText, createdAt

4. **modification_log.json**
   - Detailed audit trail of all modifications
   - Includes timestamps, actions, affected files, backup locations
   - Used for tracking changes and debugging

### Virtual Environment Files
- **venv/** (created by start_server.sh)
- Contains Flask, PyYAML, flask-cors installations

## Current Features Status

### Query Tool Features ✅
- [x] Visual query builder with AND/OR/NOT operators
- [x] Direct query editor for advanced users
- [x] Saved queries with search functionality
- [x] Import/export saved queries
- [x] Query validation with visual feedback
- [x] Undo/redo functionality (50 states)
- [x] Folder/file scoping (entire vault, specific folder, or single file)
- [x] Table view results with property columns
- [x] Property type selection for new properties
- [x] Bulk modification with preview
- [x] Progress indicators for modifications
- [x] Keyboard shortcuts for efficiency
- [x] Automatic backup before modifications
- [x] **NEW**: "exists" operator to find notes with non-empty property values
- [x] **NEW**: "does not exist" operator to find notes without property or with empty values

### Search & Replace Tool Features ✅
- [x] Wildcard pattern matching (* and ?)
- [x] Search in contents, filenames, or both
- [x] Wikilink protection option
- [x] Folder/file scoping with search
- [x] Real-time file filtering
- [x] Preview before replacement
- [x] Progress indicators
- [x] Automatic backup before modifications

### Shared Features ✅
- [x] Automatic backup system (keeps 3 most recent)
- [x] Configuration management
- [x] Health check endpoints
- [x] Error handling and logging
- [x] Cross-platform compatibility (tested on macOS)

## Recent Changes (2025-06-14)

### Morning Session
1. Fixed "addCondition is not defined" error
2. Implemented 5 suggested improvements:
   - Query validation with parentheses checking
   - Visual indicators for invalid queries
   - Undo/redo functionality
   - Import/export for saved queries
   - Enhanced keyboard shortcuts
3. Added table view for query results

### Afternoon Session
1. Added folder/file scoping to query tool (matching search/replace tool)
2. Made both scope and query optional for flexible searching
3. Fixed three bugs:
   - Clear button in folder search now works properly
   - Added Team column to results table
   - Added progress indicators to modifications
4. Updated server to handle scoped queries and empty expressions

### Evening Session (NEW)
1. **Added "exists" and "does not exist" operators**:
   - "exists" finds notes where property has a non-empty value
   - "does not exist" finds notes where property is missing, null, or empty
   - Operators work with all property types (text, list, etc.)
   - Value input field automatically disabled for these operators
2. **Fixed JavaScript scope issues**:
   - Moved critical functions to global scope in HTML head
   - Fixed button onclick handlers for AND/OR/NOT operators
   - Added undo/redo functionality
   - Cleaned up debugging code
3. **Query examples with new operators**:
   - `Stakeholder does not exist` - finds all notes without Stakeholder property
   - `Stakeholder exists` - finds all notes with non-empty Stakeholder property
   - `Stakeholder does not exist AND Team equals "Engineering"` - compound queries

## Current Issues
None identified - all known bugs have been resolved.

## Next Steps & Future Enhancements

### Short-term Improvements
1. **Export Results to CSV** - Add ability to export query results table
2. **Query Templates** - Pre-built queries for common operations
3. **Batch Operations** - Queue multiple modifications
4. **Property Auto-complete** - Suggest property names while typing
5. **Dark Mode** - Add theme toggle for better visibility

### Medium-term Enhancements
1. **Query History** - Track and replay past queries (beyond undo/redo)
2. **Scheduled Operations** - Run queries/modifications on schedule
3. **Dry Run Mode** - Test operations without making changes
4. **Property Analytics** - Show property usage statistics
5. **Regex Support** - Add regex patterns alongside wildcards

### Long-term Vision
1. **Plugin Integration** - Convert to Obsidian plugin
2. **Multi-vault Support** - Manage multiple vaults simultaneously
3. **Collaboration Features** - Share queries and modifications
4. **AI Integration** - Smart query suggestions based on vault content
5. **Performance Optimization** - Indexed searches for large vaults

## Important Discoveries & Decisions

### Technical Decisions
1. **Inline CSS** - Chose inline styles for portability and single-file distribution
2. **No External Dependencies** - Frontend uses only vanilla JavaScript
3. **Flask Server** - Simple, lightweight server perfect for local tools
4. **JSON Storage** - Simple file-based storage for configurations and queries
5. **Global Function Scope** - Critical functions defined in HTML head for reliable onclick handlers

### Design Decisions
1. **Table View Default** - Better information density than list view
2. **Optional Scoping** - Flexibility to search by scope, query, or both
3. **3-Backup Limit** - Balance between safety and disk space
4. **Property Columns** - Show key properties (Obsidian, Category, Subcategory, Team, Stakeholder)
5. **Dynamic Value Input** - Value field disabled for exists/notExists operators

### UX Decisions
1. **Progressive Disclosure** - File selection only shows after folder selection
2. **Confirmation Dialogs** - For potentially large operations
3. **Visual Feedback** - Loading spinners, progress text, validation errors
4. **Keyboard Shortcuts** - Power user efficiency without cluttering UI
5. **Contextual Help** - Operator-specific placeholder text and help messages

## Performance Considerations
- Large vaults (1000+ files) may experience slower initial loads
- Query execution scales linearly with vault size
- Property modifications are performed sequentially for safety
- Backup creation time depends on vault size

## Security & Safety
- All modifications create automatic backups
- Backups are timestamped and kept for 3 iterations
- Preview functionality for all destructive operations
- Modification logs provide complete audit trail
- No external network requests (fully local operation)

## Known Limitations
1. **Platform Testing** - Only tested on macOS, may need adjustments for Windows/Linux
2. **Vault Size** - Performance degrades with very large vaults (10,000+ files)
3. **Property Types** - Limited to predefined types (text, list, number, checkbox, date, datetime)
4. **Query Complexity** - No support for nested property queries
5. **Concurrent Use** - Not designed for multiple simultaneous users

## Maintenance Notes
- Virtual environment should be recreated if Python version changes
- Backup cleanup runs automatically after each modification
- Server finds available ports automatically (5001-5002 preferred)
- All configuration stored in script directory (not in vault)

## Testing Recommendations
1. Test with small vault subset before bulk operations
2. Verify backups are created successfully
3. Use "Modify First File" option for testing
4. Check modification_log.json for operation details
5. Monitor server console for error messages
6. Test exists/notExists operators with various property types

## Deployment Checklist
- [x] Server starts successfully
- [x] Vault path is correctly configured
- [x] Backup path has write permissions
- [x] All dependencies installed (Flask, PyYAML, flask-cors)
- [x] Port 5001 or alternative is available
- [x] Browser can access http://localhost:5001

## Support Resources
- Project documentation: README.md
- Error logs: Check terminal running start_server.sh
- Modification history: modification_log.json
- Configuration issues: vault_config.json
- Query examples: saved_queries.json

---

**Project Status**: Production Ready
**Last Updated**: 2025-06-14
**Version**: 2.2.0