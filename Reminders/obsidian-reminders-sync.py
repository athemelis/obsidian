#!/usr/bin/env python3
"""
Obsidian-Reminders Bidirectional Sync - Improved Version
Synchronizes tasks between Obsidian notes and macOS Reminders
"""

import os
import re
import json
import subprocess
import datetime
import time
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dateutil import parser
import hashlib
import pickle
from functools import wraps
import traceback

# Configuration - can be overridden by config.yaml
DEFAULT_CONFIG = {
    'vault_path': "/Users/tonythem/Obsidian/tonythem",
    'archive_path': "🔲 Framework/🎗️ Reminders/📚 Archive.md",
    'logs_directory': "/Users/tonythem/Github/obsidian/Reminders/Logs",
    'sync_interval_minutes': 3,
    'batch_size': 10,
    'enable_bidirectional': True,
    'obsidian_priority': True,
    'max_retries': 3,
    'retry_delay_seconds': 2,
    'enable_progress_logging': True,
    'progress_interval': 10
}

# Task regex patterns
TASK_PATTERN = re.compile(r'^(\s*)-\s+\[([ xX])\]\s+(.+)$', re.MULTILINE)
TAG_PATTERN = re.compile(r'#(\w+)')
DUE_DATE_PATTERN = re.compile(r'\^due\(([^)]+)\)')
PRIORITY_PATTERN = re.compile(r'!\[(high|medium|low)\]')
EMOJI_PATTERN = re.compile(r'^[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F680-\U0001F6FF\s]+')

def timing_decorator(func):
    """Decorator to time function execution"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        elapsed = time.time() - start_time
        if elapsed > 1.0:  # Only log if operation took more than 1 second
            self.log(f"{func.__name__} took {elapsed:.2f} seconds", level="DEBUG")
        return result
    return wrapper

def retry_on_error(max_retries=3, delay=2):
    """Decorator to retry operations on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        self.log(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. Retrying...", level="WARNING")
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                    else:
                        self.log(f"All attempts failed for {func.__name__}: {str(e)}", level="ERROR")
            raise last_error
        return wrapper
    return decorator

class Task:
    """Represents a task with all its metadata"""
    def __init__(self, content: str, completed: bool = False, 
                 due_date: Optional[datetime.datetime] = None,
                 priority: Optional[str] = None, tags: List[str] = None,
                 source_note: str = "", created_date: Optional[datetime.datetime] = None):
        self.content = content
        self.completed = completed
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.source_note = source_note
        self.created_date = created_date or datetime.datetime.now()
        self.completed_date = None if not completed else datetime.datetime.now()
    
    def to_obsidian_format(self) -> str:
        """Convert task to Obsidian format"""
        checkbox = "[x]" if self.completed else "[ ]"
        task_text = f"- {checkbox} {self.content}"
        
        # Add tags
        for tag in self.tags:
            if f"#{tag}" not in task_text:
                task_text += f" #{tag}"
        
        # Add priority
        if self.priority and f"![{self.priority}]" not in task_text:
            task_text += f" ![{self.priority}]"
        
        # Add due date
        if self.due_date and "^due(" not in task_text:
            task_text += f" ^due({self.due_date.strftime('%Y-%m-%d')})"
        
        return task_text
    
    def to_reminder_format(self) -> Dict:
        """Convert task to Reminders format"""
        return {
            'name': self.content,
            'completed': self.completed,
            'dueDate': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'priority': self.priority,
            'notes': ', '.join([f"#{tag}" for tag in self.tags]) if self.tags else None
        }
    
    def get_hash(self) -> str:
        """Get a unique hash for the task"""
        return hashlib.md5(f"{self.content}:{self.source_note}".encode()).hexdigest()
    
    def __eq__(self, other):
        """Compare tasks for equality"""
        if not isinstance(other, Task):
            return False
        return (self.content == other.content and 
                self.source_note == other.source_note)
    
    def __hash__(self):
        """Hash for using tasks in sets"""
        return hash((self.content, self.source_note))

class ObsidianRemindersSync:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self.load_config(config_path)
        self.vault_path = Path(self.config['vault_path'])
        self.archive_path = self.vault_path / self.config['archive_path']
        self.logs_dir = Path(self.config['logs_directory'])
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.sync_state_file = self.logs_dir / "obsidian_reminders_sync_state.pkl"
        self.log_file = self.logs_dir / "obsidian_reminders_sync.log"
        self.status_file = self.logs_dir / "sync_status.json"
        
        self.sync_state = self.load_sync_state()
        self.current_sync_stats = {
            'start_time': None,
            'end_time': None,
            'tasks_synced': 0,
            'errors': [],
            'status': 'idle'
        }
    
    def load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration from file or use defaults"""
        config = DEFAULT_CONFIG.copy()
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                config.update(user_config)
        elif Path("config.yaml").exists():
            with open("config.yaml", 'r') as f:
                user_config = yaml.safe_load(f)
                config.update(user_config)
        
        return config
    
    def load_sync_state(self) -> Dict:
        """Load the previous sync state"""
        if self.sync_state_file.exists():
            try:
                with open(self.sync_state_file, 'rb') as f:
                    return pickle.load(f)
            except:
                pass
        return {'obsidian': {}, 'reminders': {}, 'last_sync': None}
    
    def save_sync_state(self):
        """Save the current sync state"""
        self.sync_state['last_sync'] = datetime.datetime.now().isoformat()
        with open(self.sync_state_file, 'wb') as f:
            pickle.dump(self.sync_state, f)
    
    def update_status(self, status: str, extra_data: Dict = None):
        """Update the sync status file for web monitoring"""
        status_data = {
            'status': status,
            'last_updated': datetime.datetime.now().isoformat(),
            'current_stats': self.current_sync_stats
        }
        if extra_data:
            status_data.update(extra_data)
        
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages to file and console"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] [{level}] {message}"
        
        # Console output
        if level in ["ERROR", "WARNING"] or self.config.get('log_level') == 'DEBUG':
            print(log_message)
        
        # File output
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def strip_emoji(self, text: str) -> str:
        """Remove leading emojis from text"""
        return EMOJI_PATTERN.sub('', text).strip()
    
    def get_note_name_without_emoji(self, note_path: Path) -> str:
        """Get note name without emoji and extension"""
        name = note_path.stem
        return self.strip_emoji(name)
    
    def find_note_by_name(self, name: str) -> Optional[Path]:
        """Find a note by name, ignoring emojis"""
        clean_name = self.strip_emoji(name).lower()
        
        for note_path in self.vault_path.rglob('*.md'):
            if note_path == self.archive_path:
                continue
            note_clean_name = self.get_note_name_without_emoji(note_path).lower()
            if note_clean_name == clean_name:
                return note_path
        return None
    
    def parse_obsidian_task(self, task_line: str, source_note: str) -> Optional[Task]:
        """Parse an Obsidian task line into a Task object"""
        match = TASK_PATTERN.match(task_line.strip())
        if not match:
            return None
        
        indent, status, content = match.groups()
        completed = status.lower() == 'x'
        
        # Extract metadata
        tags = TAG_PATTERN.findall(content)
        
        due_match = DUE_DATE_PATTERN.search(content)
        due_date = None
        if due_match:
            try:
                due_date = parser.parse(due_match.group(1))
            except:
                pass
        
        priority_match = PRIORITY_PATTERN.search(content)
        priority = priority_match.group(1) if priority_match else None
        
        # Clean content
        clean_content = content
        clean_content = TAG_PATTERN.sub('', clean_content)
        clean_content = DUE_DATE_PATTERN.sub('', clean_content)
        clean_content = PRIORITY_PATTERN.sub('', clean_content)
        clean_content = clean_content.strip()
        
        return Task(
            content=clean_content,
            completed=completed,
            due_date=due_date,
            priority=priority,
            tags=tags,
            source_note=source_note
        )
    
    @timing_decorator
    def get_obsidian_tasks(self) -> Dict[str, List[Task]]:
        """Get all tasks from Obsidian vault"""
        tasks_by_note = {}
        excluded_folders = set(self.config.get('excluded_folders', []))
        
        for note_path in self.vault_path.rglob('*.md'):
            # Skip excluded folders
            if any(excluded in note_path.parts for excluded in excluded_folders):
                continue
            
            if note_path == self.archive_path:
                continue
            
            try:
                with open(note_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                note_name = note_path.stem
                tasks = []
                
                for match in TASK_PATTERN.finditer(content):
                    task = self.parse_obsidian_task(match.group(0), note_name)
                    if task:
                        tasks.append(task)
                
                if tasks:
                    tasks_by_note[note_name] = tasks
                    
            except Exception as e:
                self.log(f"Error reading {note_path}: {e}", level="ERROR")
        
        return tasks_by_note
    
    @retry_on_error(max_retries=3, delay=2)
    def get_reminders_lists(self) -> List[str]:
        """Get all Reminders list names"""
        script = '''
        tell application "Reminders"
            set listNames to {}
            repeat with reminderList in lists
                set end of listNames to name of reminderList
            end repeat
            return listNames
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                                capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            raise Exception(f"Error getting reminder lists: {result.stderr}")
        
        # Parse list names
        output = result.stdout.strip()
        if not output:
            return []
        
        # Handle different possible formats
        if ', ' in output:
            return [name.strip() for name in output.split(', ')]
        else:
            return [output]
    
    @retry_on_error(max_retries=3, delay=2)
    def get_reminders_for_list(self, list_name: str) -> List[Task]:
        """Get all reminders for a specific list"""
        # Escape single quotes in list name
        escaped_list_name = list_name.replace("'", "\\'")
        
        script = f'''
        tell application "Reminders"
            set output to ""
            repeat with reminderList in lists
                if name of reminderList is "{escaped_list_name}" then
                    repeat with reminderItem in reminders of reminderList
                        set taskName to name of reminderItem
                        set isCompleted to completed of reminderItem
                        set taskDueDate to due date of reminderItem
                        set taskPriority to priority of reminderItem
                        set taskNotes to body of reminderItem
                        
                        set output to output & "===TASK_START===" & return
                        set output to output & "name:" & taskName & return
                        set output to output & "completed:" & isCompleted & return
                        
                        if taskDueDate is not missing value then
                            set output to output & "dueDate:" & (taskDueDate as string) & return
                        end if
                        
                        set output to output & "priority:" & taskPriority & return
                        
                        if taskNotes is not missing value then
                            set output to output & "notes:" & taskNotes & return
                        end if
                        
                        set output to output & "===TASK_END===" & return
                    end repeat
                    exit repeat
                end if
            end repeat
            return output
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                                capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            raise Exception(f"Error getting reminders for list '{list_name}': {result.stderr}")
        
        tasks = []
        current_task = {}
        
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line == '===TASK_START===':
                current_task = {}
            elif line == '===TASK_END===':
                if current_task.get('name'):
                    # Parse task data
                    tags = []
                    if current_task.get('notes'):
                        tags = [tag.strip('#') for tag in current_task['notes'].split() 
                                if tag.startswith('#')]
                    
                    due_date = None
                    if current_task.get('dueDate'):
                        try:
                            due_date = parser.parse(current_task['dueDate'])
                        except:
                            pass
                    
                    priority = None
                    priority_val = current_task.get('priority', '0')
                    if priority_val and priority_val != '0':
                        priority_map = {'1': 'high', '5': 'medium', '9': 'low'}
                        priority = priority_map.get(priority_val, None)
                    
                    task = Task(
                        content=current_task['name'],
                        completed=current_task.get('completed', '').lower() == 'true',
                        due_date=due_date,
                        priority=priority,
                        tags=tags,
                        source_note=list_name
                    )
                    tasks.append(task)
            elif ':' in line:
                key, value = line.split(':', 1)
                current_task[key] = value
        
        return tasks
    
    @timing_decorator
    def get_reminders_tasks(self) -> Dict[str, List[Task]]:
        """Get all tasks from Reminders app"""
        try:
            # Get all list names first
            list_names = self.get_reminders_lists()
            if not list_names:
                return {}
            
            tasks_by_list = {}
            excluded_lists = set(self.config.get('excluded_lists', []))
            
            # Get reminders for each list
            for list_name in list_names:
                if list_name in excluded_lists:
                    continue
                
                try:
                    tasks = self.get_reminders_for_list(list_name)
                    if tasks:
                        tasks_by_list[list_name] = tasks
                except Exception as e:
                    self.log(f"Error getting reminders for list '{list_name}': {e}", level="ERROR")
            
            self.log(f"Successfully retrieved {len(tasks_by_list)} lists from Reminders")
            return tasks_by_list
            
        except Exception as e:
            self.log(f"Error in get_reminders_tasks: {e}", level="ERROR")
            self.log(traceback.format_exc(), level="DEBUG")
            return {}
    
    @timing_decorator
    def get_existing_reminders_batch(self, list_name: str) -> Set[str]:
        """Get all existing reminder names in a list at once"""
        escaped_list_name = list_name.replace("'", "\\'")
        script = f'''
        tell application "Reminders"
            set reminderNames to {{}}
            repeat with reminderList in lists
                if name of reminderList is "{escaped_list_name}" then
                    repeat with reminderItem in reminders of reminderList
                        set end of reminderNames to name of reminderItem
                    end repeat
                    exit repeat
                end if
            end repeat
            return reminderNames
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                                capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            names = result.stdout.strip()
            if names and names != '{}':
                return set(name.strip() for name in names.split(', ') if name.strip())
        return set()
    
    @retry_on_error(max_retries=2, delay=1)
    def create_reminders_batch(self, tasks: List[Task], list_name: str):
        """Create multiple reminders at once for better performance"""
        if not tasks:
            return
        
        # Get existing reminders
        existing_reminders = self.get_existing_reminders_batch(list_name)
        
        # Filter out tasks that already exist
        new_tasks = [task for task in tasks if task.content not in existing_reminders]
        
        if not new_tasks:
            self.log(f"All {len(tasks)} tasks already exist in {list_name}")
            return
        
        # Process in batches
        batch_size = self.config.get('batch_size', 10)
        for i in range(0, len(new_tasks), batch_size):
            batch = new_tasks[i:i + batch_size]
            self._create_reminder_batch(batch, list_name)
            self.current_sync_stats['tasks_synced'] += len(batch)
    
    def _create_reminder_batch(self, tasks: List[Task], list_name: str):
        """Create a batch of reminders"""
        escaped_list_name = list_name.replace("'", "\\'")
        
        script = f'''
        tell application "Reminders"
            set targetList to missing value
            
            repeat with reminderList in lists
                if name of reminderList is "{escaped_list_name}" then
                    set targetList to reminderList
                    exit repeat
                end if
            end repeat
            
            if targetList is missing value then
                set targetList to make new list with properties {{name:"{escaped_list_name}"}}
            end if
            '''
        
        for task in tasks:
            task_content = task.content.replace('"', '\\"').replace("'", "\\'")
            script += f'''
            set newReminder to make new reminder in targetList with properties {{name:"{task_content}"}}
            '''
            
            if task.completed:
                script += f'set completed of newReminder to true\n'
            
            if task.due_date:
                script += f'set due date of newReminder to date "{task.due_date.strftime("%m/%d/%Y")}"\n'
            
            if task.priority:
                priority_map = {'high': 1, 'medium': 5, 'low': 9}
                script += f'set priority of newReminder to {priority_map.get(task.priority, 0)}\n'
            
            if task.tags:
                notes = ' '.join([f"#{tag}" for tag in task.tags])
                script += f'set body of newReminder to "{notes}"\n'
        
        script += '''
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                                capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            self.log(f"Created {len(tasks)} new reminders in {list_name}")
        else:
            raise Exception(f"Error creating batch reminders: {result.stderr}")
    
    def create_or_update_obsidian_task(self, task: Task, note_name: str):
        """Create or update a task in an Obsidian note"""
        note_path = self.find_note_by_name(note_name)
        
        if not note_path:
            # Create new note
            note_path = self.vault_path / f"{note_name}.md"
            note_path.write_text(f"# {note_name}\n\n", encoding='utf-8')
        
        content = note_path.read_text(encoding='utf-8')
        
        # Check if task already exists
        task_found = False
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            existing_task = self.parse_obsidian_task(line, note_name)
            if existing_task and existing_task.content == task.content:
                # Update existing task
                lines[i] = task.to_obsidian_format()
                task_found = True
                break
        
        if not task_found:
            # Add new task after frontmatter
            frontmatter_end = 0
            if content.startswith('---'):
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        frontmatter_end = i + 1
                        break
            
            # Insert task after frontmatter
            lines.insert(frontmatter_end, task.to_obsidian_format())
        
        note_path.write_text('\n'.join(lines), encoding='utf-8')
        self.current_sync_stats['tasks_synced'] += 1
    
    def archive_completed_task(self, task: Task):
        """Archive a completed task"""
        # Ensure archive directory exists
        self.archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing archive or create new
        if self.archive_path.exists():
            content = self.archive_path.read_text(encoding='utf-8')
        else:
            content = "# 📚 Archive\n\n"
        
        # Find or create section for source note
        section_header = f"## [[{task.source_note}]]"
        
        if section_header not in content:
            content += f"\n{section_header}\n\n"
        
        # Create archive entry
        completed_date = task.completed_date or datetime.datetime.now()
        archive_entry = (
            f"- [x] {task.content} "
            f"(Created: {task.created_date.strftime('%Y-%m-%d')}, "
            f"Completed: {completed_date.strftime('%Y-%m-%d')})\n"
        )
        
        # Insert entry after section header
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line == section_header:
                # Insert after header, maintaining date order
                insert_pos = i + 1
                while insert_pos < len(lines) and lines[insert_pos].strip() != '' and not lines[insert_pos].startswith('##'):
                    insert_pos += 1
                lines.insert(insert_pos, archive_entry.strip())
                break
        
        self.archive_path.write_text('\n'.join(lines), encoding='utf-8')
    
    def delete_reminder(self, task_name: str, list_name: str):
        """Delete a reminder from the Reminders app"""
        escaped_list_name = list_name.replace("'", "\\'")
        escaped_task_name = task_name.replace('"', '\\"').replace("'", "\\'")
        
        script = f'''
        tell application "Reminders"
            repeat with reminderList in lists
                if name of reminderList is "{escaped_list_name}" then
                    repeat with reminder in reminders of reminderList
                        if name of reminder is "{escaped_task_name}" then
                            delete reminder
                            exit repeat
                        end if
                    end repeat
                    exit repeat
                end if
            end repeat
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=False)
    
    def sync(self):
        """Main sync method with improved performance and error handling"""
        self.log("=" * 50)
        self.log("Starting sync...")
        self.current_sync_stats = {
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': None,
            'tasks_synced': 0,
            'errors': [],
            'status': 'running'
        }
        self.update_status('running')
        
        start_time = time.time()
        
        try:
            # Get current states
            self.log("Reading Obsidian tasks...")
            obsidian_tasks = self.get_obsidian_tasks()
            total_obsidian_tasks = sum(len(tasks) for tasks in obsidian_tasks.values())
            
            self.log("Reading Reminders...")
            reminders_tasks = self.get_reminders_tasks()
            total_reminder_tasks = sum(len(tasks) for tasks in reminders_tasks.values())
            
            # Log summary
            self.log(f"Found {len(obsidian_tasks)} notes with {total_obsidian_tasks} tasks in Obsidian")
            self.log(f"Found {len(reminders_tasks)} lists with {total_reminder_tasks} reminders in Reminders app")
            
            if self.config.get('enable_bidirectional') and reminders_tasks:
                # Full bidirectional sync
                self.log("Performing bidirectional sync...")
                self._perform_bidirectional_sync(obsidian_tasks, reminders_tasks)
            else:
                # One-way sync (Obsidian to Reminders)
                self.log("Performing one-way sync (Obsidian → Reminders)...")
                self._perform_oneway_sync(obsidian_tasks)
            
            # Save sync state
            self.save_sync_state()
            
            # Final summary
            elapsed_time = time.time() - start_time
            self.log(f"Sync completed in {elapsed_time:.1f} seconds")
            self.log(f"Tasks synced: {self.current_sync_stats['tasks_synced']}")
            
            self.current_sync_stats['end_time'] = datetime.datetime.now().isoformat()
            self.current_sync_stats['status'] = 'completed'
            self.update_status('completed')
            
        except Exception as e:
            self.log(f"Sync failed with error: {str(e)}", level="ERROR")
            self.log(traceback.format_exc(), level="DEBUG")
            self.current_sync_stats['errors'].append(str(e))
            self.current_sync_stats['status'] = 'error'
            self.update_status('error')
            raise
    
    def _perform_bidirectional_sync(self, obsidian_tasks: Dict[str, List[Task]], 
                                    reminders_tasks: Dict[str, List[Task]]):
        """Perform bidirectional sync between Obsidian and Reminders"""
        all_notes_lists = set(obsidian_tasks.keys()) | set(reminders_tasks.keys())
        total_items = len(all_notes_lists)
        processed = 0
        
        for note_list_name in all_notes_lists:
            processed += 1
            if self.config.get('enable_progress_logging') and processed % self.config.get('progress_interval', 10) == 0:
                self.log(f"Progress: {processed}/{total_items} notes/lists processed...")
            
            obs_tasks = obsidian_tasks.get(note_list_name, [])
            rem_tasks = reminders_tasks.get(note_list_name, [])
            
            # Find matching list/note name
            reminder_list = self.strip_emoji(note_list_name)
            
            # Convert to dictionaries for efficient lookup
            obs_task_dict = {t.content: t for t in obs_tasks}
            rem_task_dict = {t.content: t for t in rem_tasks}
            
            # Tasks in Obsidian but not in Reminders
            obs_only = set(obs_task_dict.keys()) - set(rem_task_dict.keys())
            new_reminders = [obs_task_dict[content] for content in obs_only if not obs_task_dict[content].completed]
            if new_reminders:
                self.create_reminders_batch(new_reminders, reminder_list)
            
            # Tasks in Reminders but not in Obsidian
            rem_only = set(rem_task_dict.keys()) - set(obs_task_dict.keys())
            for content in rem_only:
                task = rem_task_dict[content]
                if not task.completed:
                    self.create_or_update_obsidian_task(task, note_list_name)
            
            # Handle conflicts (same task, different state)
            common_tasks = set(obs_task_dict.keys()) & set(rem_task_dict.keys())
            for content in common_tasks:
                obs_task = obs_task_dict[content]
                rem_task = rem_task_dict[content]
                
                if obs_task.completed != rem_task.completed:
                    if self.config.get('obsidian_priority'):
                        # Obsidian takes priority
                        if obs_task.completed:
                            self.archive_completed_task(obs_task)
                            self.delete_reminder(obs_task.content, reminder_list)
                        else:
                            # Update reminder to match Obsidian
                            self.delete_reminder(rem_task.content, reminder_list)
                            self.create_reminders_batch([obs_task], reminder_list)
                    else:
                        # Reminders takes priority
                        if rem_task.completed:
                            self.archive_completed_task(rem_task)
                            # Update Obsidian task
                            rem_task.completed = True
                            self.create_or_update_obsidian_task(rem_task, note_list_name)
    
    def _perform_oneway_sync(self, obsidian_tasks: Dict[str, List[Task]]):
        """Perform one-way sync from Obsidian to Reminders"""
        total_notes = len(obsidian_tasks)
        processed = 0
        
        for note_name, tasks in obsidian_tasks.items():
            processed += 1
            if self.config.get('enable_progress_logging') and processed % self.config.get('progress_interval', 10) == 0:
                self.log(f"Progress: {processed}/{total_notes} notes processed...")
            
            reminder_list = self.strip_emoji(note_name)
            uncompleted_tasks = [t for t in tasks if not t.completed]
            
            if uncompleted_tasks:
                self.create_reminders_batch(uncompleted_tasks, reminder_list)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Obsidian-Reminders Sync')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()
    
    sync = ObsidianRemindersSync(config_path=args.config)
    
    if args.once:
        sync.sync()
    else:
        # Continuous mode
        interval = sync.config.get('sync_interval_minutes', 3) * 60
        while True:
            try:
                sync.sync()
            except Exception as e:
                sync.log(f"Sync error: {e}", level="ERROR")
            
            sync.log(f"Waiting {interval} seconds until next sync...")
            time.sleep(interval)

if __name__ == "__main__":
    main()
