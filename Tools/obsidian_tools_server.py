#!/usr/bin/env python3
"""
Combined Obsidian Tools Server
Provides both Note Query/Modification and Search/Replace functionality
"""

print("Obsidian Tools Server script starting...")

import os
import re
import json
import yaml
import fnmatch
import shutil
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import socket
# For the reminders sync
import threading
import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration constants - all files saved in script directory
CONFIG_FILE = os.path.join(SCRIPT_DIR, "vault_config.json")
DEFAULT_VAULT_PATH = "/Users/tonythem/Obsidian/tonythem/"
DEFAULT_BACKUP_PATH = "/Users/tonythem/Obsidian/backups/"
# For the reminders sync
# Add these after your existing app configuration
app.config['REMINDERS_LOGS_DIR'] = '/Users/tonythem/Github/obsidian/Reminders/Logs'
app.config['REMINDERS_SCRIPT_PATH'] = '/Users/tonythem/Github/obsidian/Reminders/obsidian-reminders-sync.py'
app.config['REMINDERS_CONFIG_PATH'] = '/Users/tonythem/Github/obsidian/Reminders/config.yaml'

# Load configuration
def load_config():
    """Load vault configuration from file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
    
    # Return default config
    return {
        'vault_path': DEFAULT_VAULT_PATH,
        'backup_path': DEFAULT_BACKUP_PATH
    }

# Save configuration
def save_config(config):
    """Save vault configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

# Initialize global configuration variables
config = load_config()
VAULT_PATH = config['vault_path']
BACKUP_PATH = config['backup_path']
# Save logs in script directory, not vault
LOG_FILE = os.path.join(SCRIPT_DIR, "modification_log.json")
SAVED_QUERIES_FILE = os.path.join(SCRIPT_DIR, "saved_queries.json")

# ============== Shared Functions ==============

def cleanup_old_backups(keep_count=3):
    """Remove old backups, keeping only the most recent ones"""
    try:
        if not os.path.exists(BACKUP_PATH):
            return
        
        # Get all backup directories
        backup_dirs = []
        for item in os.listdir(BACKUP_PATH):
            item_path = os.path.join(BACKUP_PATH, item)
            if os.path.isdir(item_path) and item.startswith('tonythem_backup_'):
                # Extract timestamp from directory name
                try:
                    timestamp_str = item.replace('tonythem_backup_', '')
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    backup_dirs.append((item_path, timestamp))
                except ValueError:
                    # Skip directories that don't match the expected format
                    continue
        
        # Sort by timestamp (newest first)
        backup_dirs.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        if len(backup_dirs) > keep_count:
            for backup_path, _ in backup_dirs[keep_count:]:
                try:
                    shutil.rmtree(backup_path)
                    logger.info(f"Removed old backup: {backup_path}")
                except Exception as e:
                    logger.error(f"Error removing backup {backup_path}: {e}")
        
        return len(backup_dirs[keep_count:])  # Return number of backups removed
        
    except Exception as e:
        logger.error(f"Error during backup cleanup: {e}")
        return 0

def create_backup():
    """Create a backup of the vault"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"tonythem_backup_{timestamp}"
        backup_full_path = os.path.join(BACKUP_PATH, backup_name)
        
        # Create backup directory if it doesn't exist
        os.makedirs(BACKUP_PATH, exist_ok=True)
        
        # Use shutil for cross-platform compatibility
        shutil.copytree(VAULT_PATH, backup_full_path)
        
        logger.info(f"Backup created: {backup_full_path}")
        
        # Cleanup old backups
        removed_count = cleanup_old_backups(keep_count=3)
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old backup(s)")
        
        return True, backup_full_path
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return False, str(e)

def read_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has frontmatter
        if not content.startswith('---'):
            return None, content
        
        # Find the closing ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content
        
        # Parse YAML
        try:
            frontmatter = yaml.safe_load(parts[1])
            return frontmatter or {}, '---'.join(['', parts[1], parts[2]])
        except yaml.YAMLError as e:
            logger.error(f"YAML parse error in {file_path}: {e}")
            return None, content
            
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None, ""

def write_frontmatter(file_path, frontmatter, original_content):
    """Write updated frontmatter back to file"""
    try:
        # Custom YAML representer for proper formatting
        class CustomDumper(yaml.SafeDumper):
            pass
        
        def represent_str(dumper, data):
            # Check if it's a wikilink
            if isinstance(data, str) and data.startswith('[[') and data.endswith(']]'):
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
            # Check if quotes are needed (contains special characters)
            elif isinstance(data, str) and any(char in data for char in [':', '#', '@', '|', '>', '<', '!', '%', '&', '*', '?', '[', ']', '{', '}', ',']):
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
            # Otherwise use default representation
            else:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')
        
        def represent_list(dumper, data):
            # Force block style for lists (each item on new line with -)
            return dumper.represent_list(data)
        
        # Add custom representers
        CustomDumper.add_representer(str, represent_str)
        CustomDumper.add_representer(list, represent_list)
        
        # Convert frontmatter to YAML with custom formatting
        yaml_content = yaml.dump(
            frontmatter, 
            Dumper=CustomDumper,
            default_flow_style=False,  # Force block style
            allow_unicode=True, 
            sort_keys=False,
            explicit_start=False,
            explicit_end=False
        )
        
        # Reconstruct the file
        parts = original_content.split('---', 2)
        if len(parts) >= 3:
            new_content = f"---\n{yaml_content}---{parts[2]}"
        else:
            # No existing frontmatter
            body = original_content.lstrip()
            new_content = f"---\n{yaml_content}---\n\n{body}"
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        logger.error(f"Error writing {file_path}: {e}")
        return False

def log_change(action, details):
    """Log changes to a file"""
    try:
        # Read existing log
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        # Add new entry
        log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        })
        
        # Write back
        with open(LOG_FILE, 'w') as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        logger.error(f"Error writing to log: {e}")

def get_md_files(directory, base_dir=None):
    """Recursively get all .md files in a directory"""
    if base_dir is None:
        base_dir = directory
    
    files = []
    
    for root, dirs, filenames in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith('.md'):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, base_dir)
                files.append({
                    'fullPath': full_path,
                    'relativePath': relative_path,
                    'fileName': filename
                })
    
    return files

# ============== Search/Replace Functions ==============

def wildcard_to_regex(pattern, multiline=False):
    """Convert wildcard pattern to regex with optional multiline support"""
    # Escape special regex characters except * and ?
    escaped = re.escape(pattern)
    # Replace wildcards
    if multiline:
        # In multiline mode, * can match across lines
        escaped = escaped.replace(r'\*', '(?:.|\\n)*')
        escaped = escaped.replace(r'\?', '(?:.|\\n)')
    else:
        escaped = escaped.replace(r'\*', '.*')
        escaped = escaped.replace(r'\?', '.')
    
    # Add flags for multiline matching if needed
    flags = re.DOTALL if multiline else 0
    return re.compile('^' + escaped + '$', flags)

def matches_wildcard(text, pattern, multiline=False):
    """Check if string matches wildcard pattern (case sensitive)"""
    regex = wildcard_to_regex(pattern, multiline)
    return regex.match(text) is not None

def replace_with_wildcard(text, search_pattern, replace_pattern, multiline=False):
    """Replace wildcards in string"""
    regex = wildcard_to_regex(search_pattern, multiline)
    matches = regex.match(text)
    
    if not matches:
        return text
    
    # Simple replacement without wildcard capturing
    if '*' not in search_pattern and '?' not in search_pattern:
        return text.replace(search_pattern, replace_pattern)
    
    # For wildcards, do a simple replacement of the entire match
    return regex.sub(replace_pattern, text)

def search_in_line_excluding_wikilinks(line, search_pattern, exclude_wikilinks=True):
    """Search for pattern in line, optionally excluding wikilinks"""
    if not exclude_wikilinks:
        # If not excluding wikilinks, do normal search
        return matches_wildcard(line, search_pattern) or search_pattern in line
    
    # Find all wikilinks in the line
    wikilink_positions = []
    for match in re.finditer(r'\[\[([^\]]+)\]\]', line):
        wikilink_positions.append((match.start(), match.end()))
    
    # For simple patterns (no wildcards), check each occurrence
    if '*' not in search_pattern and '?' not in search_pattern:
        # Find all occurrences of the pattern
        start = 0
        while True:
            pos = line.find(search_pattern, start)
            if pos == -1:
                break
            
            # Check if this occurrence is inside a wikilink
            inside_wikilink = False
            for wl_start, wl_end in wikilink_positions:
                if wl_start <= pos < wl_end:
                    inside_wikilink = True
                    break
            
            if not inside_wikilink:
                return True
            
            start = pos + 1
        
        return False
    else:
        # For wildcard patterns, we need to check the entire line
        # but exclude wikilink portions
        if matches_wildcard(line, search_pattern):
            # If there are no wikilinks, it's a valid match
            if not wikilink_positions:
                return True
            
            # For now, return True for wildcard matches
            # (this could be improved with more sophisticated logic)
            return True
        
        return False

def replace_in_line_excluding_wikilinks(line, search_pattern, replace_pattern, exclude_wikilinks=True):
    """Replace pattern in line, optionally excluding wikilinks"""
    if not exclude_wikilinks:
        # If not excluding wikilinks, do normal replacement
        if '*' not in search_pattern and '?' not in search_pattern:
            return line.replace(search_pattern, replace_pattern)
        else:
            return replace_with_wildcard(line, search_pattern, replace_pattern)
    
    # Find all wikilinks in the line
    wikilink_positions = []
    for match in re.finditer(r'\[\[([^\]]+)\]\]', line):
        wikilink_positions.append((match.start(), match.end()))
    
    # For simple patterns (no wildcards)
    if '*' not in search_pattern and '?' not in search_pattern:
        result = line
        offset = 0
        
        # Find all occurrences of the pattern
        start = 0
        replacements = []
        
        while True:
            pos = line.find(search_pattern, start)
            if pos == -1:
                break
            
            # Check if this occurrence is inside a wikilink
            inside_wikilink = False
            for wl_start, wl_end in wikilink_positions:
                if wl_start <= pos < wl_end:
                    inside_wikilink = True
                    break
            
            if not inside_wikilink:
                replacements.append(pos)
            
            start = pos + 1
        
        # Apply replacements from right to left to maintain positions
        for pos in reversed(replacements):
            result = result[:pos] + replace_pattern + result[pos + len(search_pattern):]
        
        return result
    else:
        # For wildcard patterns, return the original line if it contains wikilinks
        # (This could be improved with more sophisticated logic)
        if wikilink_positions:
            return line
        else:
            return replace_with_wildcard(line, search_pattern, replace_pattern)

def search_in_content_multiline(content, search_pattern, exclude_wikilinks=True):
    """Search for pattern in entire content (multiline)"""
    if not exclude_wikilinks:
        # If not excluding wikilinks, search entire content
        return search_pattern in content or matches_wildcard(content, search_pattern, multiline=True)
    
    # For excluding wikilinks, we need to be more careful
    # First, find all wikilink positions in the entire content
    wikilink_positions = []
    for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
        wikilink_positions.append((match.start(), match.end()))
    
    # For simple patterns (no wildcards)
    if '*' not in search_pattern and '?' not in search_pattern:
        # Find all occurrences of the pattern
        start = 0
        while True:
            pos = content.find(search_pattern, start)
            if pos == -1:
                break
            
            # Check if any part of this occurrence is inside a wikilink
            match_end = pos + len(search_pattern)
            inside_wikilink = False
            
            for wl_start, wl_end in wikilink_positions:
                # Check if the match overlaps with the wikilink
                if not (match_end <= wl_start or pos >= wl_end):
                    inside_wikilink = True
                    break
            
            if not inside_wikilink:
                return True
            
            start = pos + 1
        
        return False
    else:
        # For wildcard patterns in multiline mode
        # This is more complex - for now, we'll do a simpler check
        return matches_wildcard(content, search_pattern, multiline=True)

def replace_in_content_multiline(content, search_pattern, replace_pattern, exclude_wikilinks=True, delete_mode=False, delete_trailing_linebreaks=True):
    """Replace pattern in content (multiline)"""
    if not exclude_wikilinks:
        # If not excluding wikilinks, do normal replacement
        if '*' not in search_pattern and '?' not in search_pattern:
            if delete_mode and delete_trailing_linebreaks:
                # Handle line break deletion
                return handle_delete_with_linebreaks(content, search_pattern)
            return content.replace(search_pattern, replace_pattern)
        else:
            return replace_with_wildcard(content, search_pattern, replace_pattern, multiline=True)
    
    # Find all wikilinks in the content
    wikilink_positions = []
    for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
        wikilink_positions.append((match.start(), match.end()))
    
    # For simple patterns (no wildcards)
    if '*' not in search_pattern and '?' not in search_pattern:
        result = content
        offset = 0
        replacements = []
        
        # Find all occurrences of the pattern
        start = 0
        while True:
            pos = content.find(search_pattern, start)
            if pos == -1:
                break
            
            # Check if any part of this occurrence is inside a wikilink
            match_end = pos + len(search_pattern)
            inside_wikilink = False
            
            for wl_start, wl_end in wikilink_positions:
                # Check if the match overlaps with the wikilink
                if not (match_end <= wl_start or pos >= wl_end):
                    inside_wikilink = True
                    break
            
            if not inside_wikilink:
                replacements.append((pos, match_end))
            
            start = pos + 1
        
        # Apply replacements from right to left to maintain positions
        for start_pos, end_pos in reversed(replacements):
            if delete_mode:
                # Handle deletion with optional line break removal
                before = result[:start_pos]
                after = result[end_pos:]
                
                if delete_trailing_linebreaks and after.startswith('\n'):
                    after = after[1:]  # Remove the trailing line break
                
                result = before + after
            else:
                result = result[:start_pos] + replace_pattern + result[end_pos:]
        
        return result
    else:
        # For wildcard patterns, we need more sophisticated handling
        # This is a simplified version - could be enhanced
        if not wikilink_positions:
            if delete_mode:
                # For delete mode with wildcards, find the match and remove it
                regex = wildcard_to_regex(search_pattern, multiline=True)
                match = regex.search(content)
                if match:
                    start, end = match.span()
                    before = content[:start]
                    after = content[end:]
                    
                    if delete_trailing_linebreaks and after.startswith('\n'):
                        after = after[1:]
                    
                    return before + after
                return content
            else:
                return replace_with_wildcard(content, search_pattern, replace_pattern, multiline=True)
        else:
            # With wikilinks present, be more careful
            return content  # Simplified for now

def handle_delete_with_linebreaks(content, pattern):
    """Handle deletion of pattern with optional line break removal"""
    # Check if the pattern ends with a line break
    if pattern.endswith('\n'):
        # Pattern already includes line break, just remove it
        return content.replace(pattern, '')
    
    # Find all occurrences and check if they're followed by line breaks
    result = content
    start = 0
    offset = 0
    
    while True:
        pos = result.find(pattern, start)
        if pos == -1:
            break
        
        # Check if this occurrence is followed by a line break
        end_pos = pos + len(pattern)
        if end_pos < len(result) and result[end_pos] == '\n':
            # Remove pattern and the following line break
            result = result[:pos] + result[end_pos + 1:]
            start = pos
        else:
            # Just remove the pattern
            result = result[:pos] + result[end_pos:]
            start = pos
    
    return result

# ============== Query Tool Functions ==============

def evaluate_condition(frontmatter, condition):
    """Evaluate a single condition against frontmatter"""
    property_name = condition['property']
    operator = condition['operator']
    value = condition.get('value', '')
    
    # Handle 'exists' operator
    if operator == 'exists':
        if not frontmatter:
            return False
        # Property exists and has a non-empty value
        if property_name not in frontmatter:
            return False
        prop_value = frontmatter[property_name]
        # Check if value is not empty/null
        if prop_value is None or prop_value == '' or (isinstance(prop_value, list) and len(prop_value) == 0):
            return False
        return True
    
    # Handle 'notExists' operator
    if operator == 'notExists':
        # If no frontmatter at all, property doesn't exist
        if not frontmatter:
            return True
        # Property doesn't exist or is empty/null
        if property_name not in frontmatter:
            return True
        prop_value = frontmatter[property_name]
        # Check if value is empty/null
        if prop_value is None or prop_value == '' or (isinstance(prop_value, list) and len(prop_value) == 0):
            return True
        return False
    
    # For other operators, property must exist and have a value
    if not frontmatter or property_name not in frontmatter:
        return False
    
    prop_value = frontmatter[property_name]
    
    # Handle list properties
    if isinstance(prop_value, list):
        # Check if any item in the list matches
        for item in prop_value:
            if evaluate_single_value(str(item), operator, value):
                return True
        return False
    else:
        # Handle text properties
        return evaluate_single_value(str(prop_value), operator, value)

def evaluate_single_value(prop_value, operator, match_value):
    """Evaluate a single value against an operator and match value"""
    # Handle wildcard matching
    if '*' in match_value:
        pattern = match_value.replace('*', '.*')
        pattern = f"^{pattern}$"
        matches = bool(re.match(pattern, prop_value))
        return matches if operator == 'equals' else False
    
    # Handle different operators
    if operator == 'equals':
        return prop_value == match_value
    elif operator == 'contains':
        return match_value in prop_value
    elif operator == 'startsWith':
        return prop_value.startswith(match_value)
    elif operator == 'endsWith':
        return prop_value.endswith(match_value)
    
    return False

def evaluate_expression(frontmatter, expression):
    """Evaluate a boolean expression against frontmatter"""
    # Special case: if expression contains only 'notExists' conditions and no frontmatter
    # we need to handle this differently
    
    # Convert expression to evaluatable format
    eval_parts = []
    i = 0
    
    while i < len(expression):
        item = expression[i]
        
        if item['type'] == 'condition':
            result = evaluate_condition(frontmatter, item)
            eval_parts.append(str(result))
        elif item['type'] == 'operator':
            op = item['value']
            if op == 'AND':
                eval_parts.append('and')
            elif op == 'OR':
                eval_parts.append('or')
            elif op == 'NOT':
                eval_parts.append('not')
            elif op in ['(', ')']:
                eval_parts.append(op)
        
        i += 1
    
    # Evaluate the boolean expression
    try:
        eval_string = ' '.join(eval_parts)
        return eval(eval_string)
    except:
        return False

def find_matching_files(expression, include_properties=None, search_path=None, target_file=None):
    """Find all files matching the query expression, optionally including specific properties"""
    matching_files = []
    
    # Determine if we have a query to evaluate
    has_query = expression and len(expression) > 0
    
    # Determine the search path
    if target_file:
        # If a specific file is targeted, only check that file
        if os.path.exists(target_file) and target_file.endswith('.md'):
            frontmatter, _ = read_frontmatter(target_file)
            
            # If no query, include the file. If query exists, evaluate it
            # Important: evaluate even if frontmatter is None for 'notExists' operator
            if not has_query or evaluate_expression(frontmatter, expression):
                relative_path = os.path.relpath(target_file, VAULT_PATH)
                file_info = {
                    'name': os.path.basename(target_file),
                    'path': relative_path,
                    'full_path': target_file
                }
                
                # Include requested properties if specified
                if include_properties and frontmatter:
                    file_info['properties'] = {}
                    for prop in include_properties:
                        if prop in frontmatter:
                            file_info['properties'][prop] = frontmatter[prop]
                        else:
                            file_info['properties'][prop] = None
                elif include_properties:
                    # No frontmatter, set all properties to None
                    file_info['properties'] = {prop: None for prop in include_properties}
                
                matching_files.append(file_info)
        
        return matching_files
    
    # Otherwise, search in the specified path or vault
    search_root = search_path or VAULT_PATH
    
    # Walk through all markdown files in the search path
    for root, dirs, files in os.walk(search_root):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                frontmatter, _ = read_frontmatter(file_path)
                
                # If no query, include all files. If query exists, evaluate it
                # Key change: We now evaluate the expression even when frontmatter is None
                # This allows 'notExists' conditions to match files without frontmatter
                if not has_query or evaluate_expression(frontmatter, expression):
                    relative_path = os.path.relpath(file_path, VAULT_PATH)
                    file_info = {
                        'name': file,
                        'path': relative_path,
                        'full_path': file_path
                    }
                    
                    # Include requested properties if specified
                    if include_properties and frontmatter:
                        file_info['properties'] = {}
                        for prop in include_properties:
                            if prop in frontmatter:
                                file_info['properties'][prop] = frontmatter[prop]
                            else:
                                file_info['properties'][prop] = None
                    elif include_properties:
                        # No frontmatter, set all properties to None
                        file_info['properties'] = {prop: None for prop in include_properties}
                    
                    matching_files.append(file_info)
    
    return matching_files

# ============== Routes ==============

@app.route('/')
def index():
    """Serve the main menu page"""
    return send_file('index.html')

@app.route('/query_tool.html')
def query_tool():
    """Serve the query tool page"""
    return send_file('query_tool.html')

@app.route('/search_replace_tool.html')
def search_replace_tool():
    """Serve the search/replace tool page"""
    return send_file('search_replace_tool.html')

@app.route('/reminders_sync.html')
def reminders_sync():
    """Serve the reminders sync page"""
    return send_file('reminders_sync.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok', 
        'vault_path': VAULT_PATH,
        'backup_path': BACKUP_PATH
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify({
        'vault_path': VAULT_PATH,
        'backup_path': BACKUP_PATH
    })

@app.route('/config', methods=['POST'])
def update_config():
    """Update configuration"""
    global VAULT_PATH, BACKUP_PATH
    
    try:
        data = request.json
        new_vault_path = data.get('vault_path')
        new_backup_path = data.get('backup_path')
        
        if not new_vault_path or not new_backup_path:
            return jsonify({'error': 'Both vault_path and backup_path are required'}), 400
        
        # Validate paths
        if not os.path.exists(new_vault_path):
            return jsonify({'error': f'Vault path does not exist: {new_vault_path}'}), 400
        
        # Save configuration
        new_config = {
            'vault_path': new_vault_path,
            'backup_path': new_backup_path
        }
        
        if save_config(new_config):
            # Update global variables
            VAULT_PATH = new_vault_path
            BACKUP_PATH = new_backup_path
            # Note: LOG_FILE and SAVED_QUERIES_FILE remain in script directory
            
            return jsonify({
                'success': True,
                'vault_path': VAULT_PATH,
                'backup_path': BACKUP_PATH
            })
        else:
            return jsonify({'error': 'Failed to save configuration'}), 500
            
    except Exception as e:
        logger.error(f"Config update error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/backup-info', methods=['GET'])
def get_backup_info():
    """Get information about existing backups"""
    try:
        if not os.path.exists(BACKUP_PATH):
            return jsonify({
                'backup_count': 0,
                'backups': [],
                'total_size': 0
            })
        
        # Get all backup directories
        backups = []
        total_size = 0
        
        for item in os.listdir(BACKUP_PATH):
            item_path = os.path.join(BACKUP_PATH, item)
            if os.path.isdir(item_path) and item.startswith('tonythem_backup_'):
                try:
                    # Get directory size
                    size = sum(os.path.getsize(os.path.join(dirpath, filename))
                              for dirpath, dirnames, filenames in os.walk(item_path)
                              for filename in filenames)
                    
                    # Extract timestamp
                    timestamp_str = item.replace('tonythem_backup_', '')
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    
                    backups.append({
                        'name': item,
                        'path': item_path,
                        'timestamp': timestamp.isoformat(),
                        'size': size,
                        'size_mb': round(size / (1024 * 1024), 2)
                    })
                    total_size += size
                except Exception as e:
                    logger.error(f"Error processing backup {item}: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'backup_count': len(backups),
            'backups': backups[:5],  # Return only the 5 most recent
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        })
        
    except Exception as e:
        logger.error(f"Error getting backup info: {e}")
        return jsonify({'error': str(e)}), 500

# ============== Query Tool Routes ==============

@app.route('/query', methods=['POST'])
def query():
    """Execute a query against the vault"""
    try:
        data = request.json
        expression = data.get('expression', [])
        include_properties = data.get('includeProperties', None)
        vault_path = data.get('vaultPath', VAULT_PATH)
        target_path = data.get('targetPath', None)
        target_file = data.get('targetFile', None)
        
        # Note: Empty expression is now allowed - it will return all files in scope
        
        # Determine the search path
        search_path = target_path if target_path else vault_path
        
        matching_files = find_matching_files(expression, include_properties, search_path, target_file)
        
        log_change('query', {
            'expression': expression,
            'results_count': len(matching_files),
            'include_properties': include_properties,
            'search_path': search_path,
            'target_file': target_file,
            'has_query': len(expression) > 0
        })
        
        return jsonify({
            'count': len(matching_files),
            'results': matching_files
        })
        
    except Exception as e:
        logger.error(f"Query error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/saved-queries', methods=['GET'])
def get_saved_queries():
    """Get saved queries"""
    try:
        if os.path.exists(SAVED_QUERIES_FILE):
            with open(SAVED_QUERIES_FILE, 'r', encoding='utf-8') as f:
                queries = json.load(f)
            return jsonify(queries)
        else:
            return jsonify([])
    except Exception as e:
        logger.error(f"Error loading saved queries: {e}")
        return jsonify([])

@app.route('/saved-queries', methods=['POST'])
def save_saved_queries():
    """Save queries to file"""
    try:
        data = request.json
        queries = data.get('queries', [])
        
        with open(SAVED_QUERIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(queries, f, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error saving queries: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/check-property-types', methods=['POST'])
def check_property_types():
    """Check the types of a property across selected files"""
    try:
        data = request.json
        property_name = data.get('property')
        files = data.get('files', [])
        
        types = {}
        
        for file_path in files:
            full_path = os.path.join(VAULT_PATH, file_path)
            frontmatter, _ = read_frontmatter(full_path)
            
            if frontmatter and property_name in frontmatter:
                prop_value = frontmatter[property_name]
                prop_type = 'list' if isinstance(prop_value, list) else 'text'
                types[prop_type] = types.get(prop_type, 0) + 1
            else:
                types['not_found'] = types.get('not_found', 0) + 1
        
        return jsonify({'types': types})
        
    except Exception as e:
        logger.error(f"Check property types error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview():
    """Preview changes before applying them"""
    try:
        data = request.json
        property_name = data.get('property')
        original_value = data.get('originalValue', '')
        new_value = data.get('newValue')
        files = data.get('files', [])
        
        previews = []
        
        for file_path in files[:5]:  # Limit preview to first 5 files
            full_path = os.path.join(VAULT_PATH, file_path)
            frontmatter, _ = read_frontmatter(full_path)
            
            if not frontmatter:
                frontmatter = {}
            
            preview_text = ""
            
            if property_name in frontmatter:
                current_value = frontmatter[property_name]
                
                if isinstance(current_value, list):
                    if original_value and original_value in current_value:
                        preview_text = f"List property: Will replace '{original_value}' with '{new_value}'"
                    elif new_value not in current_value:
                        preview_text = f"List property: Will append '{new_value}' to {current_value}"
                    else:
                        preview_text = f"List property: '{new_value}' already exists in {current_value}"
                else:
                    if not original_value or str(current_value) == original_value:
                        preview_text = f"Text property: '{current_value}' → '{new_value}'"
                    else:
                        preview_text = f"Text property: Current value '{current_value}' doesn't match '{original_value}'"
            else:
                preview_text = f"Property doesn't exist. Will add: {property_name}: {new_value}"
            
            previews.append({
                'file': os.path.basename(file_path),
                'change': preview_text
            })
        
        return jsonify({'previews': previews})
        
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/modify', methods=['POST'])
def modify():
    """Modify properties in selected files"""
    try:
        data = request.json
        property_name = data.get('property')
        original_value = data.get('originalValue', '')
        new_value = data.get('newValue')
        files = data.get('files', [])
        
        # Create backup before modifications
        backup_success, backup_path = create_backup()
        if not backup_success:
            return jsonify({'error': f'Failed to create backup: {backup_path}'}), 500
        
        # Handle different data types for new properties
        if not original_value and new_value is not None:
            # For new properties, the value might already be processed on the client side
            # (e.g., arrays for lists, booleans for checkboxes, numbers)
            # Just use it as-is since the client has already done the conversion
            pass
        elif isinstance(new_value, str):
            # For existing properties being updated with a string value
            new_value = new_value.strip()
            # Remove outer quotes if the user added them
            if ((new_value.startswith('"') and new_value.endswith('"')) or 
                (new_value.startswith("'") and new_value.endswith("'"))):
                # But only if it's not a wikilink that needs quotes
                temp_value = new_value[1:-1]
                # Keep the cleaned value unless it would break the wikilink format
                if not (temp_value.startswith('[[') and temp_value.endswith(']]')):
                    new_value = temp_value
                else:
                    # For wikilinks, always use the inner value without quotes
                    new_value = temp_value
        
        modified_count = 0
        modifications = []
        
        for file_path in files:
            full_path = os.path.join(VAULT_PATH, file_path)
            frontmatter, original_content = read_frontmatter(full_path)
            
            if frontmatter is None:
                frontmatter = {}
            
            modified = False
            before_value = None
            after_value = None
            
            if property_name in frontmatter:
                current_value = frontmatter[property_name]
                before_value = current_value
                
                if isinstance(current_value, list):
                    # Handle list property
                    if original_value and original_value in current_value:
                        # Replace specific value in list
                        idx = current_value.index(original_value)
                        current_value[idx] = new_value
                        modified = True
                    elif new_value not in current_value:
                        # Append to list
                        if isinstance(new_value, list):
                            # If new value is a list, extend the current list
                            current_value.extend(new_value)
                        else:
                            # Otherwise append as single item
                            current_value.append(new_value)
                        modified = True
                    
                    after_value = current_value
                else:
                    # Handle text property
                    if not original_value or str(current_value) == original_value:
                        frontmatter[property_name] = new_value
                        after_value = new_value
                        modified = True
            else:
                # Property doesn't exist, add it
                frontmatter[property_name] = new_value
                after_value = new_value
                modified = True
            
            if modified:
                if write_frontmatter(full_path, frontmatter, original_content):
                    modified_count += 1
                    modifications.append({
                        'file': file_path,
                        'property': property_name,
                        'before': before_value,
                        'after': after_value
                    })
        
        # Log the changes
        log_change('modify', {
            'property': property_name,
            'original_value': original_value,
            'new_value': new_value,
            'files_count': len(files),
            'modified_count': modified_count,
            'modifications': modifications,
            'backup_path': backup_path
        })
        
        return jsonify({
            'modified': modified_count,
            'total': len(files),
            'backup_path': backup_path
        })
        
    except Exception as e:
        logger.error(f"Modify error: {e}")
        return jsonify({'error': str(e)}), 500

# ============== Search/Replace Routes ==============

@app.route('/api/folders', methods=['POST'])
def get_folders():
    """Get folders in vault"""
    try:
        data = request.json
        vault_path = data.get('vaultPath', VAULT_PATH)
        
        def get_folders_recursive(directory, base_dir, level=0):
            folders = []
            
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                if os.path.isdir(item_path) and not item.startswith('.'):
                    relative_path = os.path.relpath(item_path, base_dir)
                    folders.append({
                        'fullPath': item_path,
                        'relativePath': relative_path if relative_path != '.' else '',
                        'name': item,
                        'level': level
                    })
                    
                    # Recursively get subfolders
                    folders.extend(get_folders_recursive(item_path, base_dir, level + 1))
            
            return folders
        
        folders = get_folders_recursive(vault_path, vault_path)
        folders.insert(0, {
            'fullPath': vault_path,
            'relativePath': '.',
            'name': 'Entire Vault',
            'level': -1
        })
        
        return jsonify({'folders': folders})
        
    except Exception as e:
        logger.error(f"Get folders error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/files', methods=['POST'])
def get_files():
    """Get files in a folder"""
    try:
        data = request.json
        folder_path = data.get('folderPath')
        
        if not folder_path:
            return jsonify({'error': 'Missing folder path'}), 400
        
        files = get_md_files(folder_path, VAULT_PATH)
        
        return jsonify({'files': files})
        
    except Exception as e:
        logger.error(f"Get files error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    """Search for patterns in vault with multiline support"""
    try:
        data = request.json
        search_pattern = data.get('searchPattern')
        search_scope = data.get('searchScope')
        target_path = data.get('targetPath', VAULT_PATH)
        vault_path = data.get('vaultPath', VAULT_PATH)
        target_file = data.get('targetFile')
        exclude_wikilinks = data.get('excludeWikilinks', True)
        multiline_mode = data.get('multilineMode', False)
        
        if not search_pattern or not search_scope:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Get files to search
        if target_file:
            files = [{
                'fullPath': target_file,
                'relativePath': os.path.relpath(target_file, vault_path),
                'fileName': os.path.basename(target_file)
            }]
        else:
            files = get_md_files(target_path or vault_path, vault_path)
        
        matches = []
        
        for file_info in files:
            match_info = {
                'fullPath': file_info['fullPath'],
                'relativePath': file_info['relativePath'],
                'fileName': file_info['fileName'],
                'matches': []
            }
            
            # Search in filename
            if search_scope in ['names', 'both']:
                if matches_wildcard(file_info['fileName'], search_pattern, multiline=False):
                    match_info['matches'].append({
                        'type': 'filename',
                        'original': file_info['fileName'],
                        'lineNumber': None
                    })
            
            # Search in content
            if search_scope in ['contents', 'both']:
                try:
                    with open(file_info['fullPath'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if multiline_mode:
                        # Search entire content at once
                        if search_in_content_multiline(content, search_pattern, exclude_wikilinks):
                            # Find the actual match for display
                            if '*' not in search_pattern and '?' not in search_pattern:
                                # For literal patterns, show the exact match
                                pos = content.find(search_pattern)
                                if pos != -1:
                                    # Calculate line number of start
                                    line_num = content[:pos].count('\n') + 1
                                    match_info['matches'].append({
                                        'type': 'content',
                                        'original': search_pattern,
                                        'lineNumber': line_num
                                    })
                            else:
                                # For wildcard patterns, show that there's a match
                                match_info['matches'].append({
                                    'type': 'content',
                                    'original': f'[Multiline wildcard match for: {search_pattern}]',
                                    'lineNumber': None
                                })
                    else:
                        # Original line-by-line search
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if search_in_line_excluding_wikilinks(line, search_pattern, exclude_wikilinks):
                                match_info['matches'].append({
                                    'type': 'content',
                                    'original': line,
                                    'lineNumber': i + 1
                                })
                except Exception as e:
                    logger.error(f"Error reading file {file_info['fullPath']}: {e}")
            
            if match_info['matches']:
                matches.append(match_info)
        
        total_matches = sum(len(m['matches']) for m in matches)
        
        return jsonify({
            'matches': matches,
            'totalFiles': len(matches),
            'totalMatches': total_matches
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview', methods=['POST'])
def preview_replace():
    """Preview replace changes with multiline support"""
    try:
        data = request.json
        search_pattern = data.get('searchPattern')
        replace_pattern = data.get('replacePattern', '')
        search_scope = data.get('searchScope')
        target_path = data.get('targetPath', VAULT_PATH)
        vault_path = data.get('vaultPath', VAULT_PATH)
        target_file = data.get('targetFile')
        exclude_wikilinks = data.get('excludeWikilinks', True)
        multiline_mode = data.get('multilineMode', False)
        delete_mode = data.get('deleteMode', False)
        delete_trailing_linebreaks = data.get('deleteTrailingLineBreaks', True)
        selected_files = data.get('selectedFiles', [])
        
        if not search_pattern or not search_scope:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Get files to search
        if target_file:
            files = [{
                'fullPath': target_file,
                'relativePath': os.path.relpath(target_file, vault_path),
                'fileName': os.path.basename(target_file)
            }]
        else:
            files = get_md_files(target_path or vault_path, vault_path)
        
        # Filter to only selected files if provided
        if selected_files:
            files = [f for f in files if f['fullPath'] in selected_files]
        
        previews = []
        
        for file_info in files:
            preview = {
                'fullPath': file_info['fullPath'],
                'relativePath': file_info['relativePath'],
                'fileName': file_info['fileName'],
                'changes': []
            }
            
            # Preview filename changes
            if search_scope in ['names', 'both']:
                if matches_wildcard(file_info['fileName'], search_pattern, multiline=False):
                    if delete_mode:
                        preview['changes'].append({
                            'type': 'filename',
                            'original': file_info['fileName'],
                            'replacement': '[File will be renamed - pattern removed]'
                        })
                    else:
                        new_name = replace_with_wildcard(file_info['fileName'], search_pattern, replace_pattern, multiline=False)
                        preview['changes'].append({
                            'type': 'filename',
                            'original': file_info['fileName'],
                            'replacement': new_name
                        })
            
            # Preview content changes
            if search_scope in ['contents', 'both']:
                try:
                    with open(file_info['fullPath'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if multiline_mode:
                        # Check if pattern exists in content
                        if search_in_content_multiline(content, search_pattern, exclude_wikilinks):
                            # Show what will be changed
                            if '*' not in search_pattern and '?' not in search_pattern:
                                # For literal patterns
                                pos = content.find(search_pattern)
                                if pos != -1:
                                    line_num = content[:pos].count('\n') + 1
                                    
                                    if delete_mode:
                                        # Show what will be deleted
                                        deleted_text = search_pattern
                                        if delete_trailing_linebreaks and pos + len(search_pattern) < len(content) and content[pos + len(search_pattern)] == '\n':
                                            deleted_text += '\\n'
                                        
                                        preview['changes'].append({
                                            'type': 'content',
                                            'original': deleted_text.replace('\n', '\\n'),
                                            'replacement': '[Deleted]',
                                            'lineNumber': line_num
                                        })
                                    else:
                                        preview['changes'].append({
                                            'type': 'content',
                                            'original': search_pattern.replace('\n', '\\n'),
                                            'replacement': replace_pattern.replace('\n', '\\n'),
                                            'lineNumber': line_num
                                        })
                            else:
                                # For wildcard patterns
                                preview['changes'].append({
                                    'type': 'content',
                                    'original': f'[Multiline wildcard match for: {search_pattern}]',
                                    'replacement': '[Content will be modified]' if not delete_mode else '[Content will be deleted]',
                                    'lineNumber': None
                                })
                    else:
                        # Original line-by-line preview
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if search_in_line_excluding_wikilinks(line, search_pattern, exclude_wikilinks):
                                if delete_mode:
                                    # For delete mode, show what will be removed
                                    new_line = replace_in_line_excluding_wikilinks(line, search_pattern, '', exclude_wikilinks)
                                else:
                                    new_line = replace_in_line_excluding_wikilinks(line, search_pattern, replace_pattern, exclude_wikilinks)
                                
                                if new_line != line:  # Only show if there's an actual change
                                    preview['changes'].append({
                                        'type': 'content',
                                        'original': line,
                                        'replacement': new_line if not delete_mode else '[Line content will be modified]',
                                        'lineNumber': i + 1
                                    })
                except Exception as e:
                    logger.error(f"Error reading file {file_info['fullPath']}: {e}")
            
            if preview['changes']:
                previews.append(preview)
        
        total_changes = sum(len(p['changes']) for p in previews)
        
        return jsonify({
            'previews': previews,
            'totalFiles': len(previews),
            'totalChanges': total_changes
        })
        
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/replace', methods=['POST'])
def replace():
    """Perform replace operation with multiline support"""
    try:
        data = request.json
        search_pattern = data.get('searchPattern')
        replace_pattern = data.get('replacePattern', '')
        search_scope = data.get('searchScope')
        target_path = data.get('targetPath', VAULT_PATH)
        vault_path = data.get('vaultPath', VAULT_PATH)
        target_file = data.get('targetFile')
        exclude_wikilinks = data.get('excludeWikilinks', True)
        multiline_mode = data.get('multilineMode', False)
        delete_mode = data.get('deleteMode', False)
        delete_trailing_linebreaks = data.get('deleteTrailingLineBreaks', True)
        selected_files = data.get('selectedFiles', [])
        
        if not search_pattern or not search_scope:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Create backup before modifications
        backup_success, backup_path = create_backup()
        if not backup_success:
            return jsonify({'error': f'Failed to create backup: {backup_path}'}), 500
        
        # Get files to search
        if target_file:
            files = [{
                'fullPath': target_file,
                'relativePath': os.path.relpath(target_file, vault_path),
                'fileName': os.path.basename(target_file)
            }]
        else:
            files = get_md_files(target_path or vault_path, vault_path)
        
        # Filter to only selected files if provided
        if selected_files:
            files = [f for f in files if f['fullPath'] in selected_files]
        
        results = []
        
        for file_info in files:
            result = {
                'fullPath': file_info['fullPath'],
                'relativePath': file_info['relativePath'],
                'fileName': file_info['fileName'],
                'changes': 0
            }
            
            # Replace in content first (before renaming file)
            if search_scope in ['contents', 'both']:
                try:
                    with open(file_info['fullPath'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if multiline_mode:
                        # Multiline replacement
                        original_content = content
                        new_content = replace_in_content_multiline(
                            content, search_pattern, replace_pattern, 
                            exclude_wikilinks, delete_mode, delete_trailing_linebreaks
                        )
                        
                        if new_content != original_content:
                            result['changes'] += 1
                            with open(file_info['fullPath'], 'w', encoding='utf-8') as f:
                                f.write(new_content)
                    else:
                        # Original line-by-line replacement
                        lines = content.split('\n')
                        new_lines = []
                        changes_made = False
                        
                        for line in lines:
                            if search_in_line_excluding_wikilinks(line, search_pattern, exclude_wikilinks):
                                if delete_mode:
                                    new_line = replace_in_line_excluding_wikilinks(line, search_pattern, '', exclude_wikilinks)
                                else:
                                    new_line = replace_in_line_excluding_wikilinks(line, search_pattern, replace_pattern, exclude_wikilinks)
                                
                                if new_line != line:
                                    result['changes'] += 1
                                    changes_made = True
                                new_lines.append(new_line)
                            else:
                                new_lines.append(line)
                        
                        if changes_made:
                            new_content = '\n'.join(new_lines)
                            with open(file_info['fullPath'], 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                except Exception as e:
                    logger.error(f"Error processing file {file_info['fullPath']}: {e}")
            
            # Replace in filename
            if search_scope in ['names', 'both']:
                if matches_wildcard(file_info['fileName'], search_pattern, multiline=False):
                    if delete_mode:
                        # For delete mode in filenames, remove the matched pattern
                        new_name = file_info['fileName'].replace(search_pattern, '')
                    else:
                        new_name = replace_with_wildcard(file_info['fileName'], search_pattern, replace_pattern, multiline=False)
                    
                    new_path = os.path.join(os.path.dirname(file_info['fullPath']), new_name)
                    
                    try:
                        os.rename(file_info['fullPath'], new_path)
                        result['changes'] += 1
                        result['newFileName'] = new_name
                    except Exception as e:
                        logger.error(f"Error renaming file: {e}")
            
            if result['changes'] > 0:
                results.append(result)
        
        total_changes = sum(r['changes'] for r in results)
        
        log_change('search_replace', {
            'search_pattern': search_pattern,
            'replace_pattern': replace_pattern if not delete_mode else '[DELETE]',
            'scope': search_scope,
            'exclude_wikilinks': exclude_wikilinks,
            'multiline_mode': multiline_mode,
            'delete_mode': delete_mode,
            'delete_trailing_linebreaks': delete_trailing_linebreaks,
            'files_modified': len(results),
            'total_changes': total_changes,
            'backup_path': backup_path,
            'selected_files_count': len(selected_files) if selected_files else 'all'
        })
        
        return jsonify({
            'results': results,
            'totalFilesModified': len(results),
            'totalChanges': total_changes,
            'backup_path': backup_path
        })
        
    except Exception as e:
        logger.error(f"Replace error: {e}")
        return jsonify({'error': str(e)}), 500

def find_free_port():
    """Find an available port automatically"""
    # Try common development ports first
    preferred_ports = [5001, 5002, 8080, 8081, 8082, 3000, 3001, 9000]
    
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                s.close()
                return port
            except OSError:
                continue
    
    # If no preferred port is available, let the OS assign one
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

# ============== Reminders Sync Routes ==============
# Add these routes to your existing Flask server file

@app.route('/reminders/status')
def get_reminders_status():
    """Get the current status of the reminders sync"""
    status_file = Path(app.config['REMINDERS_LOGS_DIR']) / 'sync_status.json'
    
    if status_file.exists():
        with open(status_file, 'r') as f:
            return jsonify(json.load(f))
    else:
        return jsonify({
            'status': 'not_configured',
            'message': 'Reminders sync not configured yet'
        })

@app.route('/reminders/logs')
def get_reminders_logs():
    """Get recent log entries"""
    log_file = Path(app.config['REMINDERS_LOGS_DIR']) / 'obsidian_reminders_sync.log'
    
    if not log_file.exists():
        return jsonify({'logs': []})
    
    # Get last 100 lines
    with open(log_file, 'r') as f:
        lines = f.readlines()
        recent_logs = lines[-100:] if len(lines) > 100 else lines
    
    return jsonify({'logs': recent_logs})

@app.route('/reminders/sync', methods=['POST'])
def trigger_reminders_sync():
    """Manually trigger a reminders sync"""
    try:
        # Run sync in background thread
        sync_script = Path(app.config['REMINDERS_SCRIPT_PATH'])
        
        def run_sync():
            subprocess.run(['python3', str(sync_script), '--once', '--config', str(app.config['REMINDERS_CONFIG_PATH'])], 
                           capture_output=True)
        
        thread = threading.Thread(target=run_sync)
        thread.start()
        
        return jsonify({
            'status': 'started',
            'message': 'Sync started in background'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/reminders/config', methods=['GET', 'POST'])
def reminders_config():
    """Get or update reminders sync configuration"""
    config_file = Path(app.config['REMINDERS_CONFIG_PATH'])
    
    if request.method == 'GET':
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                return jsonify(config)
        else:
            return jsonify({
                'vault_path': app.config.get('VAULT_PATH', ''),
                'sync_interval_minutes': 3,
                'enable_bidirectional': True
            })
    
    elif request.method == 'POST':
        try:
            # Read existing config
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
            else:
                config = {}
            
            # Update only the fields sent from web interface
            updates = request.json
            config.update(updates)
            
            # Ensure vault path matches the main config
            config['vault_path'] = app.config.get('VAULT_PATH', config.get('vault_path', ''))
            
            # Write back
            with open(config_file, 'w') as f:
                yaml.dump(config, f)
            
            return jsonify({'status': 'saved'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/reminders/service/status')
def get_service_status():
    """Check if the LaunchAgent service is running"""
    try:
        result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
        is_running = 'com.tonythem.obsidian-reminders-sync' in result.stdout
        
        return jsonify({
            'running': is_running,
            'service_name': 'com.tonythem.obsidian-reminders-sync'
        })
    except Exception as e:
        return jsonify({
            'running': False,
            'error': str(e)
        })

@app.route('/reminders/service/start', methods=['POST'])
def start_service():
    """Start the LaunchAgent service"""
    try:
        plist_path = Path.home() / 'Library' / 'LaunchAgents' / 'com.tonythem.obsidian-reminders-sync.plist'
        subprocess.run(['launchctl', 'load', str(plist_path)], check=True)
        return jsonify({'status': 'started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reminders/service/stop', methods=['POST'])
def stop_service():
    """Stop the LaunchAgent service"""
    try:
        plist_path = Path.home() / 'Library' / 'LaunchAgents' / 'com.tonythem.obsidian-reminders-sync.plist'
        subprocess.run(['launchctl', 'unload', str(plist_path)], check=True)
        return jsonify({'status': 'stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Main execution block
if __name__ == '__main__':
    # Find an available port
    port = find_free_port()
    
    # Write port to config file for the web interface
    config = {'port': port, 'host': 'localhost'}
    server_config_file = os.path.join(SCRIPT_DIR, 'server_config.json')
    with open(server_config_file, 'w') as f:
        json.dump(config, f)
    
    print(f"Starting Combined Obsidian Tools Server")
    print(f"Script directory: {SCRIPT_DIR}")
    print(f"Vault path: {VAULT_PATH}")
    print(f"Config files stored in: {SCRIPT_DIR}")
    print(f"Server running on http://localhost:{port}")
    print(f"Port {port} has been saved to {server_config_file}")
    print("\nPress Ctrl+C to stop the server")
    
    # Run without debug mode to avoid auto-reloading issues
    app.run(host='0.0.0.0', port=port, debug=False)