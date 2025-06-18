---
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 01/23/2025
Version: 1.0
---

# Dataview Helper Functions

This note contains reusable helper functions for the hierarchy system. Copy these functions into your DataviewJS queries where needed.

## Core Helper Functions

```javascript
// Extract display name from link object or string
function getLinkName(value) {
  if (!value) return null;
  if (typeof value === 'string') return value;
  if (value && value.path) {
    const parts = value.path.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('.md', '');
  }
  return null;
}

// Handle single or array subcategory values
function normalizeToArray(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

// Get all subcategory names as array
function getSubcategoryNames(subcats) {
  return normalizeToArray(subcats)
    .map(s => getLinkName(s))
    .filter(s => s);
}

// Check if a value matches a hierarchy entry (handles with/without brackets)
function matchesHierarchyValue(value, hierarchyValue) {
  const valueName = getLinkName(value);
  const hierarchyName = hierarchyValue.replace(/[\[\]]/g, '');
  return valueName === hierarchyName || valueName === hierarchyValue;
}

// Get valid hierarchy definition
function getValidHierarchy() {
  return {
    "[[🏛️ Institutions]]": [
      "[[👔 Customers]]",
      "[[🏇 Competitors]]", 
      "[[🎓 Universities]]",
      "[[🤝 3rd Pty Partners]]",
      "[[🛍️ Shopping]]",
      "[[👩‍⚕️ Medical]]",
      "[[💰 Finances]]",
      "[[👩‍⚖️ Legal & Tax]]",
      "[[💼 Employment]]"
    ],
    "[[👥 People]]": [
      "Family",
      "Friends",
      "Work",
      "Pets"
    ],
    "[[🚴‍♀️ Teams]]": [
      "[[👩‍⚕️ Medical]]",
      "[[🚴‍♀️ Work]]",
      "[[🚴‍♀️ Old Brompton Road (OBR)]]",
      "[[🚴‍♀️ Killarney Road]]",
      "[[🏡 Garden House]]"
    ],
    "[[🚵 Sanity]]": [
      "[[🐧 Linux]]",
      "[[🚴‍♀️ Sports]]",
      "[[✈️ Travel Plans]]"
    ],
    "[[🔲 Frameworks]]": [
      "[[🧮 Templates]]",
      "[[📝 Transcripts]]",
      "[[🖇️ Attachments]]",
      "[[📎 Clippings]]",
      "[[🎗️ Reminders]]",
      "[[💜 Obsidian Tools]]"
    ]
  };
}

// Validate a page against hierarchy
function validatePage(page, hierarchy) {
  const issues = [];
  
  if (!page.Category && page.Subcategory) {
    issues.push("Has subcategory but no category");
    return issues;
  }
  
  if (!page.Category) return issues;
  
  const categoryName = getLinkName(page.Category);
  let validCategory = null;
  
  // Find matching category in hierarchy
  for (const [hierCat, subcats] of Object.entries(hierarchy)) {
    if (matchesHierarchyValue(page.Category, hierCat)) {
      validCategory = hierCat;
      break;
    }
  }
  
  if (!validCategory) {
    issues.push(`Invalid category: "${categoryName}"`);
    return issues;
  }
  
  // Validate subcategories
  if (page.Subcategory) {
    const subcatNames = getSubcategoryNames(page.Subcategory);
    const validSubcats = hierarchy[validCategory];
    
    for (const subcatName of subcatNames) {
      const isValid = validSubcats.some(validSubcat => 
        matchesHierarchyValue(subcatName, validSubcat)
      );
      
      if (!isValid) {
        issues.push(`Invalid subcategory: "${subcatName}" for category "${categoryName}"`);
      }
    }
  }
  
  return issues;
}

// Count pages by category and subcategory
function countByHierarchy(pages, hierarchy) {
  const counts = {};
  
  for (const [category, subcategories] of Object.entries(hierarchy)) {
    counts[category] = {
      total: 0,
      subcategories: {},
      noSubcategory: 0
    };
    
    // Initialize subcategory counts
    subcategories.forEach(subcat => {
      counts[category].subcategories[subcat] = 0;
    });
  }
  
  // Count pages
  for (const page of pages) {
    const categoryName = getLinkName(page.Category);
    
    // Find matching category
    for (const [hierCat, data] of Object.entries(counts)) {
      if (matchesHierarchyValue(page.Category, hierCat)) {
        data.total++;
        
        if (page.Subcategory) {
          const subcatNames = getSubcategoryNames(page.Subcategory);
          let hasValidSubcat = false;
          
          for (const subcatName of subcatNames) {
            for (const validSubcat of Object.keys(data.subcategories)) {
              if (matchesHierarchyValue(subcatName, validSubcat)) {
                data.subcategories[validSubcat]++;
                hasValidSubcat = true;
              }
            }
          }
          
          if (!hasValidSubcat) {
            data.noSubcategory++;
          }
        } else {
          data.noSubcategory++;
        }
        break;
      }
    }
  }
  
  return counts;
}

// Find team members (for use in team pages)
function findTeamMembers(pages, teamLink) {
  const teamName = getLinkName(teamLink);
  
  return pages.where(p => 
    (p.Category === "[[🏛️ Institutions]]" || p.Category === "[[👥 People]]") &&
    p.Team &&
    normalizeToArray(p.Team).some(t => matchesHierarchyValue(t, teamName))
  );
}
```

## Usage Examples

### In Dashboard:
```javascript
// At the start of your DataviewJS block
const hierarchy = getValidHierarchy();
const pages = dv.pages().where(p => p.Category);
const counts = countByHierarchy(pages, hierarchy);

// Display results
for (const [category, data] of Object.entries(counts)) {
  if (data.total > 0) {
    dv.header(4, `${category} (${data.total})`);
    // ... display subcategories
  }
}
```

### In Validator:
```javascript
const hierarchy = getValidHierarchy();
const pages = dv.pages().where(p => p.Category || p.Subcategory);

const issues = pages
  .map(page => ({
    file: page.file.link,
    issues: validatePage(page, hierarchy)
  }))
  .filter(result => result.issues.length > 0);
```

### In Team Pages:
```javascript
const members = findTeamMembers(dv.pages(), this.file.link);
dv.table(
  ["Name", "Category", "Type"],
  members.map(m => [
    m.file.link,
    getLinkName(m.Category),
    m.Subcategory ? getSubcategoryNames(m.Subcategory).join(", ") : "-"
  ])
);
```

## Function Reference

### `getLinkName(value)`
Extracts the display name from a link object or string value.
- **Input**: Link object or string
- **Output**: String name or null
- **Example**: `getLinkName("[[🏛️ Institutions]]")` → `"🏛️ Institutions"`

### `normalizeToArray(value)`
Ensures a value is always an array, handling single values and nulls.
- **Input**: Any value
- **Output**: Array
- **Example**: `normalizeToArray("test")` → `["test"]`

### `getSubcategoryNames(subcats)`
Extracts all subcategory names from a property that might be single or multiple values.
- **Input**: Single value, array, or null
- **Output**: Array of strings
- **Example**: `getSubcategoryNames(["[[👔 Customers]]", "Family"])` → `["👔 Customers", "Family"]`

### `matchesHierarchyValue(value, hierarchyValue)`
Checks if a value matches a hierarchy entry, handling different formats.
- **Input**: Two values to compare
- **Output**: Boolean
- **Example**: `matchesHierarchyValue("🏛️ Institutions", "[[🏛️ Institutions]]")` → `true`

### `getValidHierarchy()`
Returns the complete valid hierarchy structure.
- **Input**: None
- **Output**: Object with categories and subcategories
- **Usage**: Call at the start of any query needing hierarchy validation

### `validatePage(page, hierarchy)`
Validates a page's category and subcategory properties against the hierarchy.
- **Input**: Page object and hierarchy definition
- **Output**: Array of issue strings (empty if valid)
- **Example**: Returns `["Invalid category: \"Companies\""]` for old category names

### `countByHierarchy(pages, hierarchy)`
Counts pages organized by the hierarchy structure.
- **Input**: Collection of pages and hierarchy definition
- **Output**: Nested object with counts per category and subcategory
- **Usage**: For dashboard statistics and summaries

### `findTeamMembers(pages, teamLink)`
Finds all institutions and people assigned to a specific team.
- **Input**: Collection of pages and team link/name
- **Output**: Filtered collection of team members
- **Usage**: In team note templates to show members