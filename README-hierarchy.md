---
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 06/18/2025
Version: 2.0
---

# Obsidian Vault Hierarchy and Organization - Complete Documentation

## Overview

This document provides comprehensive documentation for the hierarchical organization system in your Obsidian vault. The system uses frontmatter YAML properties, Dataview, and DataviewJS queries to organize and validate your notes.

## System Architecture

### Core Concepts
1. **Categories**: Top-level organization using wikilinks with emojis (e.g., `[[🏛️ Institutions]]`)
2. **Subcategories**: Second-level organization, can be single or multiple values per note
3. **Team Assignments**: Cross-linking between Institutions/People and Teams using the Team property
4. **Properties**: Standardized frontmatter fields (Category, Subcategory, Team, etc.)

### Property Schema
```yaml
---
Category: "[[🏛️ Institutions]]"  # Required, single value
Subcategory:                      # Optional, can be single or multiple
  - "[[👔 Customers]]"
  - "[[🤝 3rd Pty Partners]]"
Team:                             # Optional, for Institutions/People only
  - "[[🏡 Garden House]]"
Stakeholder:                      # Optional, your custom property
  - "[[⛔ Personal]]"
---
```

## File Inventory

### 1. **hierarchy.md** (`🔲 Framework/💜 Obsidian Tools/hierarchy.md`)
**Purpose**: Defines the valid categories and subcategories for your entire vault. This is the single source of truth for your hierarchy.

**What it shows**:
- Complete hierarchy structure with all valid categories and subcategories
- Category distribution statistics (how many notes in each category)
- Subcategory usage statistics

**How to read it**:
- The "Valid Hierarchies" section shows the complete structure
- The "Category Distribution" table shows note counts per category
- The "Subcategory Usage Statistics" shows which subcategories are most/least used

### 2. **dataview-helpers.md** (`🔲 Framework/💜 Obsidian Tools/dataview-helpers.md`)
**Purpose**: Contains reusable helper functions for all DataviewJS queries. Ensures consistency across all dashboards and validators.

**What it contains**:
- `getLinkName()`: Extracts display names from link objects
- `normalizeToArray()`: Handles single/array values consistently
- `getSubcategoryNames()`: Processes subcategory properties
- `matchesHierarchyValue()`: Compares values regardless of format
- `getValidHierarchy()`: Returns the complete hierarchy definition
- Complete documentation for each function

**How to use it**:
- Copy the functions you need into your DataviewJS blocks
- Reference the usage examples at the bottom of the file
- Use the function reference section to understand each function

### 3. **category-dashboard.md** 
**Purpose**: Main dashboard for viewing and analyzing your categorized notes.

**What it shows**:
- **Quick Stats**: Total notes, percentages with subcategories/teams
- **Browse by Category**: Detailed breakdown by category and subcategory
- **Teams Overview**: All teams with member counts
- **Recent Activity**: Latest modified notes
- **Missing Subcategories**: Notes that need subcategories added
- **Category Health Check**: Identifies formatting issues

**How to read it**:
- Check Quick Stats for overall vault health
- Use Browse by Category to navigate your hierarchy
- Teams Overview shows team composition at a glance
- Category Health Check identifies notes needing updates

### 4. **hierarchy-validator.md**
**Purpose**: Comprehensive validation tool to ensure all notes comply with the hierarchy.

**What it shows**:
- **Validation Summary**: Overview of all issues found
- **Subcategory Usage Report**: Which subcategories are unused
- **Team Assignment Validation**: Invalid team assignments
- **Missing Pages**: Category/subcategory pages that need creation

**How to read it**:
- Start with Validation Summary for issue counts
- Review detailed issues grouped by type
- Use the export list to create tasks for fixing issues
- Check Missing Pages to identify pages to create

### 5. **Team Note Template** (Enhanced)
**Purpose**: Template for creating team pages that automatically show team members.

**Features**:
- Auto-populates with institutions and people assigned to the team
- Shows member counts and statistics
- Displays recent team activity
- Lists members who belong to multiple teams

**How to use it**:
1. Create a new note for a team
2. Copy the template content
3. Replace `TEAM_TYPE` with the appropriate subcategory
4. The member lists will auto-populate

## Current Hierarchy Structure

```
[[🏛️ Institutions]]
├── [[👔 Customers]]
├── [[🏇 Competitors]]
├── [[🎓 Universities]]
├── [[🤝 3rd Pty Partners]]
├── [[🛍️ Shopping]]
├── [[👩‍⚕️ Medical]]
├── [[💰 Finances]]
├── [[👩‍⚖️ Legal & Tax]]
└── [[💼 Employment]]

[[👥 People]]
├── Family
├── Friends
├── Work
└── Pets

[[🚴‍♀️ Teams]]
├── [[👩‍⚕️ Medical]]
├── [[🚴‍♀️ Work]]
├── [[🚴‍♀️ Old Brompton Road (OBR)]]
├── [[🚴‍♀️ Killarney Road]]
└── [[🏡 Garden House]]

[[🚵 Sanity]]
├── [[🐧 Linux]]
├── [[🚴‍♀️ Sports]]
└── [[✈️ Travel Plans]]

[[🔲 Frameworks]]
├── [[🧮 Templates]]
├── [[📝 Transcripts]]
├── [[🖇️ Attachments]]
├── [[📎 Clippings]]
├── [[🎗️ Reminders]]
└── [[💜 Obsidian Tools]]
```

## How to Update the Hierarchy

### Automated Update Process (Recommended)

The hierarchy system involves multiple files that need to stay synchronized. To avoid manual errors, use this automated approach:

#### Quick Update with AI Assistant

**Copy this prompt when you need to update your hierarchy:**

```
I need to update my Obsidian hierarchy system. Here are my current files:

1. hierarchy.md (attached)
2. dataview-helpers.md (attached)
3. category-dashboard.md (attached)
4. hierarchy-validator.md (attached)

Changes needed:
- [Describe your changes here, e.g., "Add new category [[🎯 Projects]] with subcategories [[📅 Active]], [[✅ Completed]], [[🔄 On Hold]]"]
- [Or: "Rename [[🏢 Companies]] to [[🏛️ Institutions]]"]
- [Or: "Remove subcategory [[👐 1st Pty Partners]]"]

Please:
1. Update all files to reflect these changes
2. Ensure all helper functions stay synchronized
3. Maintain the current version numbers and increment if needed
4. Provide the complete updated files
5. List any notes that will need manual updates based on these changes
```

#### Using the Update Service

1. **Prepare your files**: Have all 4 core files ready to attach
2. **Describe changes clearly**: Be specific about what needs to change
3. **Review the updates**: Check all provided files before replacing
4. **Run the validator**: After updating, run hierarchy-validator.md to find affected notes
5. **Update affected notes**: Use the validator's export list to track progress

### Semi-Automated Bulk Updates

For updating many notes after hierarchy changes:

#### Create a Migration Helper Note

Create a temporary note called `migration-helper.md`:

```dataviewjs
// Find all notes that need updating
const oldValue = "[[🏢 Companies]]";  // Change this
const newValue = "[[🏛️ Institutions]]";  // Change this

const affectedNotes = dv.pages('')
  .where(p => p.Category === oldValue)
  .sort(p => p.file.name);

dv.header(3, `Found ${affectedNotes.length} notes to update`);

// Create task list for tracking
dv.header(4, "Migration Checklist");
const tasks = affectedNotes.map(p => 
  `- [ ] Update ${p.file.link}: Category from "${oldValue}" to "${newValue}"`
);

dv.paragraph("```");
dv.paragraph(tasks.join("\n"));
dv.paragraph("```");

// Show sample frontmatter for reference
dv.header(4, "Sample Updated Frontmatter");
dv.paragraph("```yaml");
dv.paragraph(`Category: "${newValue}"`);
dv.paragraph("```");
```

### Manual Update Process (If Needed)

### Adding a New Category

1. **Update hierarchy.md**:
   ```javascript
   const hierarchy = {
     // ... existing categories ...
     "[[🆕 New Category]]": [
       "Subcategory 1",
       "[[📊 Subcategory 2]]"
     ]
   };
   ```

2. **Update dataview-helpers.md** - Add the new category to the `getValidHierarchy()` function

3. **Create the category page**:
   ```yaml
   ---
   Category: "[[🆕 New Category]]"
   Subcategory: "[[🆕 New Category]]"  # Self-referential
   Date modified: 06/18/2025
   Version: 1.0
   ---
   # 🆕 New Category
   ```

4. **Update all affected files**:
   - category-dashboard.md (if you've customized it)
   - hierarchy-validator.md (if you've customized it)

### Adding a New Subcategory

1. **Update hierarchy.md** - Add to the appropriate category:
   ```javascript
   "[[🏛️ Institutions]]": [
     // ... existing subcategories ...
     "[[🆕 New Subcategory]]"
   ]
   ```

2. **Update dataview-helpers.md** - Ensure the hierarchy in `getValidHierarchy()` matches

3. **Create the subcategory page** (if using wikilinks):
   ```yaml
   ---
   Category: "[[🏛️ Institutions]]"
   Subcategory: "[[🆕 New Subcategory]]"
   ---
   ```

### Renaming Categories or Subcategories

**⚠️ Warning**: This is a major operation that affects many notes.

1. **Create a backup** of your vault first!

2. **Update these files in order**:
   - hierarchy.md
   - dataview-helpers.md
   - Any category/subcategory pages

3. **Use the validator** to find all affected notes:
   - Run hierarchy-validator.md
   - Export the issues list
   - Update each affected note

4. **Bulk update approach**:
   - Use Obsidian's Search & Replace (Ctrl/Cmd + Shift + F)
   - Search: `"[[🏢 Old Name]]"`
   - Replace: `"[[🆕 New Name]]"`
   - Review changes before applying

### Best Practices

1. **Always update hierarchy.md first** - It's your source of truth
2. **Run the validator** after making changes to find issues
3. **Use exact wikilink format** including emojis and brackets
4. **Keep backups** before bulk operations
5. **Test with a few notes** before bulk updates

### Common Tasks

#### Finding Notes Without Subcategories
1. Open category-dashboard.md
2. Check the "Missing Subcategories" section
3. Click on note links to add subcategories

#### Validating Team Assignments
1. Open hierarchy-validator.md
2. Check "Team Assignment Validation" section
3. Fix any invalid team assignments shown

#### Checking Unused Subcategories
1. Open hierarchy-validator.md
2. Review "Unused Subcategories" section
3. Consider if these subcategories should be removed or if notes should be added

#### Creating a New Team
1. Create a note with the team name
2. Add frontmatter:
   ```yaml
   Category: "[[🚴‍♀️ Teams]]"
   Subcategory: "[[Appropriate Team Type]]"
   ```
3. Assign members by adding `Team: - "[[Team Name]]"` to their notes

## Quick Reference Cards

### Adding a New Category - Prompt Template
```
Add a new category to my Obsidian hierarchy:
- Category name: [[emoji Name]]
- Subcategories: [list them]
- Should it allow Team assignments: [yes/no]

Attached are my current hierarchy files. Please update all necessary files.
```

### Adding a New Subcategory - Prompt Template
```
Add new subcategory "[name]" to category "[[category]]" in my Obsidian hierarchy.
Current files attached. Please update all necessary files.
```

### Renaming Category/Subcategory - Prompt Template
```
Rename in my Obsidian hierarchy:
- Old: [[old name]]
- New: [[new name]]

Current files attached. Please update all files and list affected notes.
```

### "Browse by Category" shows wrong counts
- Check if Category values match exactly (including spaces after emojis)
- Run validator to identify mismatched categories
- Ensure wikilinks are properly formatted

### Team members not showing up
- Verify Team property uses wikilinks: `Team: - "[[🏡 Garden House]]"`
- Check team note filename matches exactly
- Ensure Team is an array even for single values

### Validator shows many errors
- Usually means hierarchy was updated but notes weren't
- Create a checklist of affected notes using the export feature
- Use find-and-replace carefully to update in bulk

### DataviewJS errors
- Each code block needs all required helper functions
- Copy functions from dataview-helpers.md
- Ensure hierarchy definition is included where needed

## Maintenance Schedule

### Daily
- Check Recent Activity in dashboard for new uncategorized notes

### Weekly
- Run hierarchy-validator.md
- Fix any validation issues
- Review Missing Subcategories section

### Monthly
- Review unused subcategories
- Consider hierarchy adjustments
- Update team assignments as needed

### Quarterly
- Full hierarchy review
- Consider restructuring if needed
- Archive obsolete categories

## Version History

- **v2.0** (06/18/2025): Complete system overhaul with standardized functions and enhanced validation
  - Added dataview-helpers.md for consistent functions
  - Enhanced dashboard with health checks
  - Improved validator with export functionality
  - Added [[💜 Obsidian Tools]] subcategory
- **v1.0** (Initial): Basic hierarchy system with categories and subcategories

## File Version Tracking

When updating the hierarchy system, these files should be kept in sync:

| File | Current Version | Last Modified |
|------|----------------|---------------|
| hierarchy.md | 1.0 | 06/18/2025 |
| dataview-helpers.md | 1.0 | 06/18/2025 |
| category-dashboard.md | 1.0 | 06/18/2025 |
| hierarchy-validator.md | 1.0 | 06/18/2025 |

**Version Update Rules:**
- Minor changes (fix typos, adjust formatting): Keep same version
- Add/remove single subcategory: Increment by 0.1
- Add/remove category or major restructure: Increment by 1.0
- Always update Date modified to current date

---

For questions or issues, refer to the helper functions in dataview-helpers.md or create a new discussion note tagged with #hierarchy-help.