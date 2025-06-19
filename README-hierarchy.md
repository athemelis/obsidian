---
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 06/18/2025
Version: 2.1
---

# README-hierarchy.md - Obsidian Vault Hierarchy Documentation

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

### 1. **README-hierarchy.md** (`🔲 Framework/💜 Obsidian Tools/README-hierarchy.md`)
**Purpose**: Complete documentation for the hierarchy system. This file you're reading now serves as the operations manual for the entire system.

**What it contains**:
- System overview and architecture
- Complete file inventory and descriptions
- Current hierarchy structure
- Update instructions (manual and automated)
- Troubleshooting guide
- Maintenance schedule

**How to use it**:
- Reference for understanding the system
- Copy prompt templates for automated updates
- Follow maintenance schedules
- Use troubleshooting section when issues arise

### 2. **hierarchy.md** (`🔲 Framework/💜 Obsidian Tools/hierarchy.md`)
**Purpose**: Defines the valid categories and subcategories for your entire vault. This is the single source of truth for your hierarchy.

**What it shows**:
- Complete hierarchy structure with all valid categories and subcategories
- Category distribution statistics (how many notes in each category)
- Subcategory usage statistics

**How to read it**:
- The "Valid Hierarchies" section shows the complete structure
- The "Category Distribution" table shows note counts per category
- The "Subcategory Usage Statistics" shows which subcategories are most/least used

### 3. **dataview-helpers.md** (`🔲 Framework/💜 Obsidian Tools/dataview-helpers.md`)
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

### 4. **category-dashboard.md** (`🔲 Framework/💜 Obsidian Tools/category-dashboard.md`)
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

### 5. **hierarchy-validator.md** (`🔲 Framework/💜 Obsidian Tools/hierarchy-validator.md`)
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

### Note: Team Template
The **Enhanced Team Note Template** is provided in the artifacts during the setup process but is not a separate file in the vault. You can find the template content in the setup artifacts or create your own template using the structure provided. The template includes:
- Auto-populating member lists
- Team statistics
- Recent activity tracking
- Multi-team membership display

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
├── [[🏡 Garden House]]
└── [[🚴‍♀️ Santa Maura]]

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

1. README-hierarchy.md (attached) - The main documentation
2. hierarchy.md (attached) - The hierarchy definition
3. dataview-helpers.md (attached) - Helper functions
4. category-dashboard.md (attached) - Main dashboard
5. hierarchy-validator.md (attached) - Validation tool

Changes needed:
- [Describe your changes here, e.g., "Add new category [[🎯 Projects]] with subcategories [[📅 Active]], [[✅ Completed]], [[🔄 On Hold]]"]
- [Or: "Rename