# Obsidian Vault Organization Project State

## Project Overview
You're building a hierarchical organization system for your Obsidian vault using frontmatter YAML properties, Dataview, and DataviewJS queries.

## Current Implementation

### Core Structure
- **Categories**: Top-level organization using wikilinks with emojis
- **Subcategories**: Second-level organization, can be multiple per note
- **Team Assignments**: Cross-linking between Institutions/People and Teams

### Property Schema
```yaml
---
Category: "[[🏛️ Institutions]]"  # Single value, required
Subcategory:                      # Can be single or multiple values
  - "[[👔 Customers]]"
Team:                             # Optional, for Institutions/People
  - "[[🏡 Garden House]]"
---
```

### Current Hierarchy
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
└── [[🎗️ Reminders]]
```

## Key Discoveries & Technical Details

### 1. Dataview Link Objects
- When using wikilinks in frontmatter (e.g., `Category: "[[🏛️ Institutions]]"`), Dataview converts them to link objects
- Structure: `{path: "🦋 Categories/🏛️ Institutions.md", embed: false, type: "file"}`
- Must use helper functions to extract display names

### 2. Helper Functions Created

**Why these functions are necessary:**
When you use wikilinks in frontmatter (like `Category: "[[🏛️ Institutions]]"`), Dataview doesn't store them as simple strings. Instead, it converts them into link objects with a complex structure. Without helper functions, you can't compare these values or extract the readable names.

```javascript
// Extract name from link object or string
function getCategoryName(cat) {
  if (typeof cat === 'string') return cat;
  if (cat && cat.path) {
    const parts = cat.path.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('.md', '');
  }
  return null;
}
```

**What it does:**
- Takes a category value that could be either a string ("Maintenance") or a link object
- If it's a link object, extracts just the page name from the path
- Example: `{path: "🦋 Categories/🏛️ Institutions.md"}` → `"🏛️ Institutions"`
- Returns null if the value is neither string nor valid link object

**Where it's used:**
- Dashboard: To match user's categories against the hierarchy
- Validator: To check if categories are valid
- Team queries: To compare team assignments

```javascript
// Handle subcategory arrays
function getSubcategoryNames(subcats) {
  if (!subcats) return [];
  if (!Array.isArray(subcats)) subcats = [subcats];
  return subcats.map(s => getCategoryName(s)).filter(s => s);
}
```

**What it does:**
- Handles the fact that Subcategory can be either a single value or an array
- Normalizes everything to an array format for consistent processing
- Applies getCategoryName to each item to handle link objects
- Filters out any null values

**Where it's used:**
- Dashboard: To count and group notes by subcategory
- Validator: To check if all subcategories are valid for their parent category
- Browse by Category: To display notes grouped by their subcategories

**Example of why we need these:**
```javascript
// Without helper functions - THIS DOESN'T WORK:
if (page.Category === "[[🏛️ Institutions]]") // Always false!

// With helper functions - THIS WORKS:
if (getCategoryName(page.Category) === "🏛️ Institutions") // True!
```

### 3. Mixed Property Types
- Some categories are strings, others are link objects
- Dashboard handles both types gracefully
- Validator checks for both formats

## Recent Changes

### Phase 1: Initial Setup
- Created hierarchy definition in `_hierarchy.md`
- Built Category Dashboard with Browse by Category section
- Created Hierarchy Validator

### Phase 2: Property Standardization
- Changed from lowercase to capitalized properties (category → Category)
- Changed from plural to singular (subcategories → Subcategory)
- Updated all queries to handle link objects

### Phase 3: Hierarchy Updates
1. Renamed "[[🏢 Companies]]" → "[[🏛️ Institutions]]"
2. Removed "[[👐 1st Pty Partners]]" subcategory
3. Updated Teams subcategories to use wikilinks
4. Updated Sanity subcategories to use wikilinks
5. Updated Frameworks subcategories to use wikilinks

### Phase 4: Team Integration
- Added Team property approach for cross-linking
- Created Team Note Template
- Updated Dashboard with Teams Overview section
- Added team validation to Hierarchy Validator

## Current Issues & Next Steps

### Immediate Tasks
1. **Update existing notes** to match new hierarchy:
   - Change old category values to new names
   - Convert plain text subcategories to wikilinks
   - Add Team properties where appropriate

2. **Create missing pages**:
   - Ensure all category/subcategory pages exist
   - Create team pages for new teams

3. **Test team queries**:
   - Verify team member counting works correctly
   - Test bidirectional querying

### Future Enhancements
1. **Automation**:
   - QuickAdd plugin for consistent note creation
   - Templater templates with dropdown selections
   - Buttons plugin for quick category assignment

2. **Additional Dashboards**:
   - People without team assignments
   - Institutions by subcategory and team
   - Team comparison dashboard

3. **Validation Enhancements**:
   - Check for circular team references
   - Validate stakeholder properties
   - Report on property completeness

## File Locations
- **Hierarchy Definition**: `/Users/tonythem/Obsidian/tonythem/_hierarchy.md`
- **Category Dashboard**: Create as new note in vault
- **Hierarchy Validator**: Create as new note in vault
- **Team Note Template**: Use for new team pages

## Important Notes
- Always use exact wikilink format including emojis
- Subcategory can contain multiple values (YAML array)
- Category must be single value
- Team property enables cross-category relationships
- Some notes have additional properties (Stakeholder, Topic, etc.)

## How to Use This System

### Connecting Teams to Institutions and People

#### Step 1: Create Team Pages
For each team, create a note with:
```yaml
---
Category: "[[🚴‍♀️ Teams]]"
Subcategory: "[[🏡 Garden House]]"  # Use the matching subcategory
---
```

#### Step 2: Add Team Property to Members
For Institutions and People that belong to teams, add the Team property:

**Institution Example:**
```yaml
---
Category: "[[🏛️ Institutions]]"
Subcategory:
  - "[[👔 Customers]]"
Team:
  - "[[🏡 Garden House]]"
  - "[[🚴‍♀️ Killarney Road]]"  # Can belong to multiple teams
---
```

**Person Example:**
```yaml
---
Category: "[[👥 People]]"
Subcategory:
  - "Work"
Team:
  - "[[🏡 Garden House]]"
---
```

#### Step 3: Team Pages Auto-populate
When you open a team page with the Team Note Template, it automatically shows:
- All institutions assigned to that team
- All people assigned to that team
- Total counts and statistics

### Maintaining the Hierarchy

#### 1. **Always Update _hierarchy.md First**
Before adding new categories or subcategories:
1. Open `_hierarchy.md`
2. Add the new item to the appropriate section
3. Save the file
4. THEN create notes using the new category/subcategory

#### 2. **Creating New Notes**
Follow this checklist:
- [ ] Set Category (required, single value)
- [ ] Set Subcategory (optional, can be multiple)
- [ ] Add Team if applicable (for Institutions/People)
- [ ] Ensure all values use exact wikilink format from hierarchy

#### 3. **Regular Validation**
Weekly maintenance routine:
1. Run the Hierarchy Validator
2. Fix any invalid categories/subcategories
3. Update notes with missing subcategories
4. Verify team assignments are valid

#### 4. **Naming Conventions**
- **Categories**: Always use emoji + space + name in wikilinks: `[[🏛️ Institutions]]`
- **Subcategories**: Follow the pattern defined in hierarchy (some have emojis, some don't)
- **Teams**: Should match their subcategory in the Teams category

### Best Practices

#### 1. **One Source of Truth**
- The `_hierarchy.md` file is the single source of truth
- Never create ad-hoc categories or subcategories
- If you need a new category/subcategory, update hierarchy first

#### 2. **Consistent Property Usage**
```yaml
# CORRECT
Category: "[[🏛️ Institutions]]"      # Single value with quotes
Subcategory:                          # Array format for multiple
  - "[[👔 Customers]]"
  - "[[🤝 3rd Pty Partners]]"
Team:                                 # Array format even for single
  - "[[🏡 Garden House]]"

# INCORRECT
Category: [[🏛️ Institutions]]        # Missing quotes
Subcategory: "[[👔 Customers]]"       # Should be array if might have multiple
category: "[[🏛️ Institutions]]"      # Wrong case
```

#### 3. **Team Management**
- Teams are a special category that bridges Institutions and People
- Team subcategories in [[🚴‍♀️ Teams]] should represent actual teams
- Use the Team property to create relationships, not subcategories

#### 4. **Evolution Strategy**
When the hierarchy needs to change:
1. Document the change in a note
2. Update `_hierarchy.md`
3. Update all three artifacts (dashboard, validator, team template)
4. Run validator to find affected notes
5. Bulk update affected notes

### Common Patterns

#### Pattern 1: Multi-Team Membership
```yaml
# A consultant working with multiple teams
Category: "[[👥 People]]"
Subcategory:
  - "Work"
Team:
  - "[[🏡 Garden House]]"
  - "[[🚴‍♀️ Killarney Road]]"
  - "[[🚴‍♀️ Old Brompton Road (OBR)]]"
```

#### Pattern 2: Vendor Relationships
```yaml
# A vendor that's both a customer and partner
Category: "[[🏛️ Institutions]]"
Subcategory:
  - "[[👔 Customers]]"
  - "[[🤝 3rd Pty Partners]]"
Team:
  - "[[🏡 Garden House]]"  # Working with this team
```

#### Pattern 3: Internal Teams
```yaml
# Your medical team
Category: "[[🚴‍♀️ Teams]]"
Subcategory: "[[👩‍⚕️ Medical]]"
# No Team property needed - this IS a team
```

### Troubleshooting

#### Issue: "Browse by Category" shows wrong counts
- Check if Category values match exactly (including spaces after emojis)
- Run validator to identify mismatched categories
- Use debug section to see actual values

#### Issue: Team members not showing up
- Verify Team property uses wikilinks: `Team: - "[[🏡 Garden House]]"`
- Check team note filename matches exactly
- Ensure Team is an array even for single values

#### Issue: Validator shows many errors
- Usually means hierarchy was updated but notes weren't
- Create a checklist of affected notes
- Use find-and-replace carefully to update in bulk

### Migration Guide

If migrating existing notes:
1. Start with Categories - ensure all use new names
2. Then Subcategories - convert to wikilink format where needed
3. Finally add Team properties where relationships exist
4. Run validator after each phase

## Query Examples for Common Tasks

### Show all team members (for use in any team page):
```dataview
TABLE 
  Category,
  Subcategory,
  Team as "Teams",
  file.mtime as "Modified"
FROM ""
WHERE (Category = "[[🏛️ Institutions]]" OR Category = "[[👥 People]]")
  AND contains(Team, this.file.link)
SORT Category ASC, file.name ASC
```

This query:
- Shows both Institutions and People in one table
- Uses `this.file.link` to automatically reference the current team page
- Displays all team assignments (in case members belong to multiple teams)
- Sorts by Category first, then by name

### Find all people in a specific team:
```dataview
LIST
WHERE Category = "[[👥 People]]" 
  AND contains(Team, "[[🏡 Garden House]]")
```

### Find institutions without teams:
```dataview
LIST
WHERE Category = "[[🏛️ Institutions]]" 
  AND !Team
```

### Show all medical-related items:
```dataview
LIST
WHERE contains(Subcategory, "[[👩‍⚕️ Medical]]")
  OR contains(Team, "[[👩‍⚕️ Medical]]")
```