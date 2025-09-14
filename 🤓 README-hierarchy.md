---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
Date modified: 06/25/2025
Version: 3.5
---
> [!Success] README-hierarchy.md - Obsidian Vault Hierarchy Documentation

# Overview

> [!Note] Summary
> This readme describes a comprehensive framework for organizing notes in Obsidian using Categories, Subcategories, and Teams. This solution defines the structure and provides consistent usage, powerful query capabilities, and automated validation. 
> The solution uses frontmatter YAML properties, Dataview, and DataviewJS queries to organize and validate your notes.
> It should be used in conjunction with [[🤓 README-tools]] which is a set of tools designed to make bulk updates to the hierarchy.

# Table of Contents

1. [[#Overview]]
2. [[#Core Hierarchy and Properties]]
3. [[#Quick Start]]
4. [[#Using the System]]
5. [[#Common Issues]]
6. [[#File Inventory]]
7. [[#Version Control]]
8. [[#Maintenance Schedule]]

# Core Hierarchy and Properties

## Definitions and Schema

1. **Categories**: Top-level organization using wikilinks with emojis (e.g., `[[🏛️ Institutions]]`)
2. **Subcategories**: Second-level organization, can be single or multiple values per note
3. **Team Assignments**: Cross-linking between Institutions/People and Teams using the Team property
4. **Properties**: Standardized Frontmatter fields (Category, Subcategory, Team, etc.)

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

## Property Rules

1. **Always use wikilink format**: `"[[Name]]"` not just `"Name"`
2. **Categories are mutually exclusive**: Each note has exactly one category
3. **Subcategories must match hierarchy**: Only use valid subcategories for each category
4. **Teams are only for**: Institutions and People notes
5. **Multiple values**: Subcategory and Team can have multiple values as a list

## Example Frontmatter

```yaml
---
# Institution with team
Category: "[[🏛️ Institutions]]"
Subcategory: "[[👔 Customers]]"
Team: "[[🚴‍♀️ Work]]"
---

# Person with multiple teams
Category: "[[👥 People]]"
Subcategory: "[[🧑‍🧑‍🧒‍🧒 Family]]"
Team: 
  - "[[🚴‍♀️ Work]]"
  - "[[👩‍⚕️ Medical]]"
---

# Framework tool
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
---
```

## Reference Hierarchy

Top Level (L1) is categories.
Second Level (L2) is subcategories.

```
[[🏛️ Institutions]]
├── [[👔 Customers]]
├── [[🏇 Competitors]]
├── [[🎓 Universities]]
├── [[🎓 Schools]]
├── [[🤝 3rd Pty Partners]]
├── [[🛍️ Shopping]]
├── [[👩‍⚕️ Medical]]
├── [[💰 Finances]]
├── [[👩‍⚖️ Legal & Tax]]
├── [[💼 Employment]]
├── [[👮‍♂️ Government]]
├── [[🧐 Analysts]]
└── [[🛄 Travel]]

[[👥 People]]
├── [[🧑‍🧑‍🧒‍🧒 Family]]
├── [[👯 Friends]]
├── [[💪 Work People]]
├── [[🐶 Pets]]
├── [[🧾 Providers]]
├── [[👩‍🎓 Applicant Tracker]]
└── [[🩺 Doctors]]

[[👔 Work]]
├── [[🌴 Work Topics]]
└── [[👐 1st Pty Partners]]

[[🚴‍♀️ Teams]]
├── [[🚴‍♀️ Medical]]
├── [[🚴‍♀️ Work Teams]]
├── [[🚴‍♀️ Old Brompton Road (OBR)]]
├── [[🚴‍♀️ Killarney Road]]
├── [[🏡 Garden House]]
├── [[🍸 Olive Grove]]
├── [[🚴‍♀️ Santa Maura]]
├── [[🚴‍♀️ champion]]
└── [[🚴‍♀️ Pets]]

[[🚵 Sanity]]
├── [[🐧 Linux]]
├── [[🍱 Recipies]]
├── [[🚴‍♀️ Sports]]
├── [[✍️ Stories]]
├── [[✈️ Travel Plans]]
└── [[👩‍🏫 Training]]

[[🔲 Frameworks]]
├── [[🧮 Templates]]
├── [[📝 Transcripts]]
├── [[🖇️ Attachments]]
├── [[📎 Clippings]]
├── [[🎗️ Reminders]]
├── [[💜 Obsidian Tools]]
└── [[🔒 Vault]]
```

# Quick Start

## 1. Add to Your Notes

Add these properties to your note's frontmatter:

```yaml
---
Category: "[[🏛️ Institutions]]"
Subcategory: "[[👔 Customers]]"
Team: "[[🚴‍♀️ Work]]"
---
```

## 2. View Dashboard

Open `hierarchy-dashboard.md` to see:

1. 📊 Summary Categorized and Uncategorized Notes
2. 🕐 Recent Activity
3. 📁 Category Distribution
4. 📈 Subcategory Usage (with Most Used and Unused subsections)
5. ⚠️ Validation Issues (or ✅ All Notes Valid)
6. 📝 Notes Missing Subcategories
7. 👥 Team Assignments
8. ❌ Team Assignment Validation
9. Quick Queries


# Best Practices

1. **Always update the hierarchy first** - It's your source of truth
	- Update it in the [[🤓 README-hierarchy]] file
	- Update it in the [[🤓 hierarchy-dashboard]] file
2. **Check for Validation issues** after making changes to find issues
3. **Use exact wikilink format** including emojis and brackets
4. Use your [[🤓 README-tools]] Obisidian tool for bulk operations:
	- It **keeps backups** before bulk operations
	- **It allows you to test with a few notes** before bulk updates
5. Consistency
	- **Always use wikilinks**: `"[[Name]]"` format
	- **Match emoji exactly**: Copy from hierarchy definition
	- **Case sensitive**: Use exact capitalization
6. Organization
	- **One category per note**: Don't mix categories
	- **Subcategory matches category**: Only valid combinations
	- **Teams for people/institutions**: Not for other categories
7. Maintenance
	- **Run validator weekly**: Catch issues early
	- **Update bulk notes**: Use query tool for changes
	- **Check dashboard regularly**: Monitor vault health
8. Templates
	- Create templates for each category:

```yaml
---
# Institution Template
Category: "[[🏛️ Institutions]]"
Subcategory: "[[null]]"
Team: 
Status: Active
---

# Person Template  
Category: "[[👥 People]]"
Subcategory: "[[null]]"
Team:
---
```


# How to Update the Hierarchy

Here are prompts you can use for future updates to your hierarchy dashboard:

## 1. General Maintenance Prompt (for any updates)

```
I need to update my hierarchy-dashboard.md file. Please make the following changes while:
- Keeping the single definition section at the top with the hierarchy constant
- Maintaining all helper functions (getLinkName, normalizeToArray, getSubcategoryNames, matchesHierarchyValue) in their current location
- Preserving the single-pass data collection approach for performance
- Keeping all data structures and stats objects as they are
- Not duplicating any code or definitions

Changes needed: [describe your specific changes]
```

## 2. Maintaining Table Order Prompt

```
I need to update my hierarchy dashboard. Please keep the exact same order of sections and tables:
1. 📊 Summary Categorized and Uncategorized Notes
2. 🕐 Recent Activity
3. 📁 Category Distribution
4. 📈 Subcategory Usage (with Most Used and Unused subsections)
5. ⚠️ Validation Issues (or ✅ All Notes Valid)
6. 📝 Notes Missing Subcategories
7. 👥 Team Assignments
8. ❌ Team Assignment Validation

Changes needed: [describe your specific changes]
```

## 3. Version Update Prompt

```
I need to update my hierarchy dashboard version number. Current version is X.X.

Update rules:
- Minor changes (typos, formatting, small fixes): Keep same version
- Feature additions or structural changes: Increment by 0.1 (e.g., 2.1 → 2.2)
- Major overhaul or breaking changes: Increment by 1.0 (e.g., 2.1 → 3.0)

Changes I'm making: [describe changes]
Please update the version number accordingly and update the Date modified to today's date.
```

## 4. Adding/Removing Categories and Subcategories Prompt

- This can easily be done manually - just update the hierarchy in two places:
	- [[🤓 README-hierarchy]]
	- [[🤓 hierarchy-dashboard]]

```
I need to update the hierarchy in my dashboard. Please update ONLY the hierarchy constant at the top of the DataviewJS block.

Current hierarchy has these categories:
- [[🏛️ Institutions]]
- [[👥 People]]
- [[🚴‍♀️ Teams]]
- [[🚵 Sanity]]
- [[🔲 Frameworks]]

Changes needed:
[Option A] ADD new category: [[🎯 Projects]] with subcategories: [[📅 Active]], [[✅ Completed]], [[🔄 On Hold]]
[Option B] ADD new subcategory: [[🏠 Real Estate]] to [[🏛️ Institutions]]
[Option C] REMOVE category: [[🚵 Sanity]] and all its subcategories
[Option D] REMOVE subcategory: [[🐶 Pets]] from [[👥 People]]
[Option E] RENAME category: [[🚵 Sanity]] to [[🧘 Wellness]]

Please:
1. Update only the hierarchy constant
2. Increment version by 0.1 for subcategory changes, 1.0 for category changes
3. Update Date modified to today
4. Keep all other code exactly the same
```

## 5. Adding/Removing Teams Prompt

```
I need to update the valid teams in my hierarchy dashboard. Please modify ONLY the Teams section in the hierarchy constant.

Current teams under [[🚴‍♀️ Teams]]:
- [[👩‍⚕️ Medical]]
- [[🚴‍♀️ Work]]
- [[🚴‍♀️ Old Brompton Road (OBR)]]
- [[🚴‍♀️ Killarney Road]]
- [[🏡 Garden House]]
- [[🚴‍♀️ Santa Maura]]

Changes needed:
[Option A] ADD new team: [[🎨 Creative Team]]
[Option B] REMOVE team: [[🚴‍♀️ Killarney Road]]
[Option C] RENAME team: [[🚴‍♀️ Work]] to [[💼 Corporate Team]]

Please:
1. Update only the [[🚴‍♀️ Teams]] section in the hierarchy constant
2. Keep all other categories and subcategories unchanged
3. Increment version by 0.1
4. Update Date modified to today
```

## Combined Update Prompt Template

```
I need to update my hierarchy-dashboard-v2.md. Here's my current file: [attach file]

Updates needed:
1. Categories: [list any category additions/removals/renames]
2. Subcategories: [list any subcategory changes]
3. Teams: [list any team changes]
4. Other changes: [list any other modifications]

Please:
- Update ONLY the hierarchy constant for hierarchy changes
- Maintain all existing code structure and functions
- Keep the same table order
- Update version: +0.1 for minor changes, +1.0 for major changes
- Update Date modified to [today's date]
- Preserve the single-pass data collection approach
- Don't duplicate any definitions or functions

Return the complete updated file.
```

## Quick Reference for Changes

When making your updates, remember:

- **Hierarchy changes**: Only modify the `const hierarchy = {...}` at the top
- **Performance**: Keep the single-pass data collection intact
- **Functions**: Don't modify or duplicate the helper functions
- **Order**: Maintain the existing section order
- **Version**: Follow the increment rules (0.1 for minor, 1.0 for major)

These prompts will help ensure consistent, maintainable updates to your hierarchy dashboard while preserving its optimized structure.

# Migration Guide

Example: From old hierarchy to new hierarchy (e.g. from `"[[🏢 Companies]]"` do a bulk update to: `"[[🏛️ Institutions]]"`):
1. Use query tool ([[🤓 README-tools]]) to find: `Category equals "[[🏢 Companies]]"`
2. Bulk update to: `"[[🏛️ Institutions]]"`
3. Run validator to confirm
4. Update any saved queries


# File Inventory

## 1. **[[🤓 README-hierarchy]].md** (`🔲 Framework/💜 Obsidian Tools/README-hierarchy.md`)
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

## 4. **hierarchy-dashboard.md** (`🔲 Framework/💜 Obsidian Tools/hierarchy-dashboard.md`)
**Purpose**: Main dashboard for viewing and analyzing your categorized notes. Comprehensive validation tool to ensure all notes comply with the hierarchy.

**What it shows**:
- **Quick Stats**: Total notes, percentages with subcategories/teams
	- Total categorized notes
	- Total uncategorized notes
	- Percentage with subcategories
	- Distribution by category
	- Distribution by folder
- **Recent Activity**: Latest modified notes
	- Last modified notes
	- Shows all hierarchy properties
- **Browse by Category**: Detailed breakdown by category and subcategory
	- Expandable category sections
	- Subcategory counts
	- Uncategorized notes finder
- **Validation Summary**: Overview of all issues found
- **Category Health Check**: Identifies formatting issues
- **Subcategory Usage Report**: Which subcategories are unused
	- Missing Subcategories: Notes that need subcategories added
	- Unused Subcategories
	- Usage statistics
- **Team Assignment Validation**: Invalid team assignments
	- Invalid Team assignments: references to non-existent teams
	- Teams Overview: For valid teams only, shows member counts
	- Member counts by type
	- Team assignments summary
	- Missing team warnings
- **Missing Pages**: Category/subcategory pages that need creation

**How to read it**:
- Check Quick Stats for overall vault health
- Use Browse by Category to navigate your hierarchy
- Teams Overview shows team composition at a glance
- Category Health Check identifies notes needing updates
- Start with Validation Summary for issue counts
- Review detailed issues grouped by type
- Use the export list to create tasks for fixing issues
- Check Missing Pages to identify pages to create

# Version Control

## Version Update Rules

- Minor changes (fix typos, adjust formatting): Keep same version
- Add/remove single subcategory: Increment by 0.1
- Add/remove category or major restructure: Increment by 1.0
- Always update Date modified to current date

> [!Tip] Remember to update the [[🤓 hierarchy-dashboard]]

## Version History

### Version 3.5 (Current)
- Date: 07/26/2025
- Added Subcategory [[🍱 Recipies]] to [[🚵 Sanity]]
- Added Subcategory [[🛄 Travel]] to [[🏛️ Institutions]]

### Version 3.4
- Date: 07/25/2025
- Changed team [[🐶 Nellie]] to Team [[🚴‍♀️ Pets]]
- Moved [[🐶 Nellie]] from [[🚴‍♀️ Teams]] to Category [[👥 People]] and Subcategory [[🐶 Pets]]
- Renamed the team to [[🚴‍♀️ Medical]] for better discoverability

### Version 3.3
- Date: 07/24/2025
- Added Subcategory [[✍️ Stories]] to [[🚵 Sanity]]

### Version 3.2
- Date: 07/17/2025
- Added Subcategory [[👐 1st Pty Partners]] to [[👔 Work]]

### Version 3.1
- Date: 07/11/2025
- Added Subcategory [[🧐 Analysts]] to [[🏛️ Institutions]]
### Version 3.0
- Date: 07/10/2025
- Added Category [[👔 Work]]
- Added Subcategory [[🌴 Work Topics]] to new Category [[👔 Work]]
- Renamed Subcategory from 💪 Work to [[💪 Work People]]
- Renamed Subcategory from 🚴‍♀️ Work to [[🚴‍♀️ Work Teams]]
### Version 2.6
- Date: 07/09/2025
- Added Subcategory [[🔒 Vault]] to [[🔲 Frameworks]]
### Version 2.5
- Date: 07/06/2025
- Added Subcategory [[👮‍♂️ Government]] to [[🏛️ Institutions]]
- Added Subcategory [[🍸 Olive Grove]] to [[🚴‍♀️ Teams]]
- Added Subcategory [[🐶 Nellie]] to [[🚴‍♀️ Teams]]

### Version 2.4
- Date: 07/05/2025
- Added Subcategory [[🚴‍♀️ champion]] to [[🚴‍♀️ Teams]]
- Added Subcategory [[🎓 Schools]] to [[🏛️ Institutions]]

### Version 2.3 (Current)
- Date: 06/25/2025
- Added Subcategory [[🩺 Doctors]] to [[👥 People]]
- Added Subcategory [[👩‍🏫 Training]] to [[🚵 Sanity]]
### Version 2.2
- Date: 06/24/2025
- Added ability to check for notes with not frontmatter YAML at all
### Version 2.0
- Date: 06/24/2025
- Consolidated into a single hierarchy-dashboard.md file
- Simplified all common components for re-use and scalability/efficiency

### Version 1.5
- Date: 06/19/2025
- Added [[👩‍🎓 Applicant Tracker]] subcategory to People
- Updated all hierarchy definitions
- Synchronized helper functions
### Version 1.4
- 06/18/2025:
- Added [[🚴‍♀️ Santa Maura]] subcategory under Teams
- Updated all hierarchy definitions
- Synchronized helper functions
### Version 1.3
- 06/18/2025
- Added Teams functionality
- Improved validation logic
- Enhanced helper functions
### Version 1.2
- 06/18/2025
- Added Old Brompton Road team
- Fixed validation bugs
- Improved dashboard layout
### Version 1.1
- Date: 06/18/2025)
- Complete system overhaul with standardized functions and enhanced validation
- Added dataview-helpers.md for consistent functions
- Enhanced dashboard with health checks
- Improved validator with export functionality
- Added [[💜 Obsidian Tools]] subcategory
### Version 1.0
- Basic hierarchy system with categories and subcategories
- Basic dashboard and validator
- Core helper functions

# Maintenance Schedule

## Daily
- Check Recent Activity in dashboard for new uncategorized notes

## Weekly
- Run hierarchy-validator.md
- Fix any validation issues
- Review Missing Subcategories section

## Monthly
- Review unused subcategories
- Consider hierarchy adjustments
- Update team assignments as needed

## Quarterly
- Full hierarchy review
- Consider restructuring if needed
- Archive obsolete categories

# Future Enhancements

## Planned Features
- Auto-fix common issues
- Hierarchy visualization graph
- Custom hierarchy extensions
- Batch operations UI
- Historical tracking

## Under Consideration
- Multi-level subcategories
- Dynamic hierarchy loading
- Cross-vault synchronization
- API for external tools
- Automated backups

# Quick Queries

Use these simple DataView queries to find specific notes:

## Find Uncategorized Notes
```
TABLE file.folder as Folder, file.mtime as Modified
WHERE !Category
SORT file.mtime DESC
LIMIT 20
```

## Find Notes by Specific Category
```
TABLE Subcategory, Team, file.mtime as Modified
WHERE Category = "[[🏛️ Institutions]]"
SORT file.mtime DESC
```

## Find Notes Without Subcategories
```
TABLE Category, Team, file.mtime as Modified
WHERE Category AND !Subcategory
SORT file.name ASC
```

## Find Team Members
```
TABLE Category, Subcategory, file.mtime as Modified
WHERE contains(Team, "[[🚴‍♀️ Work]]")
SORT Category ASC
```

## Validate Team Assignments
1. Open hierarchy-validator.md
2. Check "Team Assignment Validation" section
3. Fix any invalid team assignments shown

```
TABLE Category, Subcategory, Stakeholder, Team
WHERE contains(Subcategory,[[🚴‍♀️ Work]])
```


## Example DataviewJS to list where Obsidian is [[🦋 Categories]] and Category is [[🏛️ Institutions]] and Stakeholder includes [[⛔ Personal]]

```
const pages = dv.pages()
  .where(p =>
    (
      Array.isArray(p["Obsidian"])
        ? p["Obsidian"].some(cat =>
            (typeof cat === "string" && cat.includes("Categories")) ||
            (cat?.path && cat.path.includes("Categories"))
          )
        : (
            (typeof p["Obsidian"] === "string" && p["Obsidian"].includes("Categories")) ||
            (p["Obsidian"]?.path && p["Obsidian"].path.includes("Categories"))
          )
    ) &&
    (
      Array.isArray(p["Category"])
        ? p["Category"].some(cat =>
            (typeof cat === "string" && cat.includes("Companies")) ||
            (cat?.path && cat.path.includes("Companies"))
          )
        : (
            (typeof p["Category"] === "string" && p["Category"].includes("Companies")) ||
            (p["Category"]?.path && p["Category"].path.includes("Companies"))
          )
    ) &&
	(
		Array.isArray(p["Stakeholder"])
		? p["Stakeholder"].some(cat =>
			(typeof cat === "string" && cat.includes("⛔ Personal.md")) ||
			(cat?.path && cat.path.includes("⛔ Personal.md"))
		  )
	: (
		(typeof p["Stakeholder"] === "string" && p["Stakeholder"].includes("⛔ Personal.md")) ||
		(p["Stakeholder"]?.path && p["Stakeholder"].path.includes("⛔ Personal.md"))
	  )
	)
  );

dv.table(
  ["Index", "Note", "Obsidian", "Category", "Stakeholder", "Team"],
  pages.map((page, index) => [
    index + 1,
    page.file.link,
    page["Obsidian"],
    page["Category"],
    page["Stakeholder"],
    page["Team"]
  ])
);
```

---
## Example DataviewJS list of prospects where Category is [[🏛️ Institutions]] and Subcategory includes [[💼 Employment]] - with Index column


```
const pages = dv.pages()
  .where(p =>
    // Check for Category = [[🏛️ Institutions]]
    (
      Array.isArray(p["Category"])
        ? p["Category"].some(cat =>
            (typeof cat === "string" && cat.includes("🏛️ Institutions")) ||
            (cat?.path && cat.path.includes("🏛️ Institutions"))
          )
        : (
            (typeof p["Category"] === "string" && p["Category"].includes("🏛️ Institutions")) ||
            (p["Category"]?.path && p["Category"].path.includes("🏛️ Institutions"))
          )
    ) &&
    // Check for Subcategory = [[💼 Employment]]
    (
      Array.isArray(p["Subcategory"])
        ? p["Subcategory"].some(cat =>
            (typeof cat === "string" && cat.includes("💼 Employment")) ||
            (cat?.path && cat.path.includes("💼 Employment"))
          )
        : (
            (typeof p["Subcategory"] === "string" && p["Subcategory"].includes("💼 Employment")) ||
            (p["Subcategory"]?.path && p["Subcategory"].path.includes("💼 Employment"))
          )
    )
  );

dv.table(
  ["Index", "Note", "Category", "Subcategory", "Team", "Stakeholder"],
  pages.map((page, index) => [
    index + 1,
    page.file.link,
    page["Category"],
    page["Subcategory"],
    page["Team"],
    page["Stakeholder"]
  ])
);
```

## Example dataviewjs indexed table that filters on Category and Subcategoty, with Category, Subcategory, Team, Stakeholder, Created, Modified columns

```javascript
const pages = dv.pages()
  .where(p =>
    // Check for Category = [[🏛️ Institutions]]
    (
      Array.isArray(p["Category"])
        ? p["Category"].some(cat =>
            (typeof cat === "string" && cat.includes("🏛️ Institutions")) ||
            (cat?.path && cat.path.includes("🏛️ Institutions"))
          )
        : (
            (typeof p["Category"] === "string" && p["Category"].includes("🏛️ Institutions")) ||
            (p["Category"]?.path && p["Category"].path.includes("🏛️ Institutions"))
          )
    ) &&
    // Check for Subcategory = [[👔 Customers]]
    (
      Array.isArray(p["Subcategory"])
        ? p["Subcategory"].some(cat =>
            (typeof cat === "string" && cat.includes("👔 Customers")) ||
            (cat?.path && cat.path.includes("👔 Customers"))
          )
        : (
            (typeof p["Subcategory"] === "string" && p["Subcategory"].includes("👔 Customers")) ||
            (p["Subcategory"]?.path && p["Subcategory"].path.includes("👔 Customers"))
          )
    )
  );

// Helper for formatting dates
function formatDateTimeCompact(dt) {
  return dt ? dt.toFormat("yyyy-MM-dd @ h:mma") : "";
}

dv.table(
  ["Index", "Note", "Category", "Subcategory", "Team", "Stakeholder", "Created", "Modified"],
  pages.map((page, index) => [
    index + 1,
    page.file.link,
    page["Category"],
    page["Subcategory"],
    page["Team"],
    page["Stakeholder"],
    formatDateTimeCompact(page.file.ctime),
    formatDateTimeCompact(page.file.mtime)
  ])
);
```
## DataviewJS snippet to handle wikilinks

This same pattern works well for any property that might contain wikilinks. You can save it as a snippet and reuse it whenever you need to filter by linked notes. 
- Replace `PropertyName` with the property you want to query.
- Replace `Search Term` with the value you are looking for.

```javascript
// Reusable pattern for checking if a property contains a specific link
(
  Array.isArray(p["PropertyName"])
    ? p["PropertyName"].some(item =>
        (typeof item === "string" && item.includes("Search Term")) ||
        (item?.path && item.path.includes("Search Term"))
      )
    : (
        (typeof p["PropertyName"] === "string" && p["PropertyName"].includes("Search Term")) ||
        (p["PropertyName"]?.path && p["PropertyName"].path.includes("Search Term"))
      )
)
```

## DataviewJS Generic snippets with Index column

```javascript
// Basic index pattern
dv.table(
  ["Index", /* ...other columns */],
  pages.map((page, index) => [
    index + 1,  // Start counting from 1 instead of 0
    /* ...other column values */
  ])
);
```

```javascript
// Pattern 1: Simple index
dv.table(
  ["#", "Note", "Created"],
  pages.map((page, idx) => [
    idx + 1,
    page.file.link,
    page.file.ctime
  ])
);
```

```javascript
// Pattern 2: With custom formatting
dv.table(
  ["No.", "Title", "Status"],
  pages.map((page, i) => [
    `${i + 1}.`,  // Adds period after number
    page.file.link,
    page.status
  ])
);
```

```javascript
// Pattern 3: Zero-padded for better alignment
dv.table(
  ["ID", "Document", "Modified"],
  pages.map((page, index) => [
    String(index + 1).padStart(3, '0'),  // Shows as 001, 002, etc.
    page.file.link,
    page.file.mtime
  ])
);
```

```javascript
// Pattern 4: With row highlighting for specific indices
dv.table(
  ["Rank", "Project", "Priority"],
  pages.map((page, idx) => {
    const rowNum = idx + 1;
    return [
      rowNum <= 3 ? `**${rowNum}**` : rowNum,  // Bold top 3
      page.file.link,
      page.priority
    ];
  })
);
```

## Date Formats

```javascript
// ISO format: "2025-07-13"
function formatDateISO(dt) {
  return dt ? dt.toFormat("yyyy-MM-dd") : "";
}
```

```javascript
// Ordinal format: "13th Feb 2025"
function formatDateOrdinal(dt) {
  if (!dt) return "";
  const day = dt.day;
  const suffix = day % 10 === 1 && day !== 11 ? "st"
    : day % 10 === 2 && day !== 12 ? "nd"
    : day % 10 === 3 && day !== 13 ? "rd"
    : "th";
  return dt.toFormat(`d'${suffix}' MMM yyyy`);
}
```

```javascript
// Time + Full date: "1:33 PM - August 17, 2023"
function formatDateTime(dt) {
  return dt ? dt.toFormat("h:mm a - MMMM dd, yyyy") : "";
}
```

```javascript
// ISO + Time: "2025-07-13 - 1:33PM"
function formatDateTimeCompact(dt) {
  return dt ? dt.toFormat("yyyy-MM-dd - h:mma") : "";
}
```

```javascript
// 9:08AM - June 21, 2025
function formatDate(dt) {
  return dt ? dt.toFormat("h:mm a - MMMM dd, yyyy") : "";
}
```

```javascript
// ====== DATE ONLY FORMATS ======

// US format: "07/13/2025"
function formatDateUS(dt) {
  return dt ? dt.toFormat("MM/dd/yyyy") : "";
}

// UK/EU format: "13/07/2025"
function formatDateEU(dt) {
  return dt ? dt.toFormat("dd/MM/yyyy") : "";
}

// Short format: "Jul 13, 2025"
function formatDateShort(dt) {
  return dt ? dt.toFormat("MMM dd, yyyy") : "";
}

// Long format: "July 13, 2025"
function formatDateLong(dt) {
  return dt ? dt.toFormat("MMMM dd, yyyy") : "";
}

// Compact: "13-Jul-25"
function formatDateCompact(dt) {
  return dt ? dt.toFormat("dd-MMM-yy") : "";
}

// Day of week: "Sunday, July 13, 2025"
function formatDateWithDay(dt) {
  return dt ? dt.toFormat("EEEE, MMMM dd, yyyy") : "";
}

// ====== TIME FORMATS ======

// Time only 12h: "1:33 PM"
function formatTime12(dt) {
  return dt ? dt.toFormat("h:mm a") : "";
}

// Time only 24h: "13:33"
function formatTime24(dt) {
  return dt ? dt.toFormat("HH:mm") : "";
}

// Time with seconds: "1:33:45 PM"
function formatTimeSeconds(dt) {
  return dt ? dt.toFormat("h:mm:ss a") : "";
}

// ====== DATETIME COMBINATIONS ======

// Full datetime: "2025-07-13 13:33:45"
function formatDateTimeFull(dt) {
  return dt ? dt.toFormat("yyyy-MM-dd HH:mm:ss") : "";
}

// Readable: "Jul 13 at 1:33 PM"
function formatDateTimeReadable(dt) {
  return dt ? dt.toFormat("MMM dd 'at' h:mm a") : "";
}

// Minimal: "7/13 1:33PM"
function formatDateTimeMinimal(dt) {
  return dt ? dt.toFormat("M/d h:mma") : "";
}

// ====== RELATIVE/SPECIAL FORMATS ======

// Week format: "2025-W28"
function formatWeek(dt) {
  return dt ? dt.toFormat("yyyy-'W'WW") : "";
}

// Quarter: "Q3 2025"
function formatQuarter(dt) {
  return dt ? dt.toFormat("'Q'q yyyy") : "";
}

// Relative days (requires moment plugin)
function formatRelative(dt) {
  if (!dt) return "";
  const now = dv.date('now');
  const days = Math.floor(dt.diff(now, 'days').days);
  
  if (days === 0) return "Today";
  if (days === 1) return "Tomorrow";
  if (days === -1) return "Yesterday";
  if (days > 0 && days <= 7) return `In ${days} days`;
  if (days < 0 && days >= -7) return `${Math.abs(days)} days ago`;
  return dt.toFormat("MMM dd, yyyy");
}
```