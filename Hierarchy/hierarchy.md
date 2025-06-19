---
aliases: [Hierarchy, Categories]
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 06/18/2025
Version: 1.1
---

# Vault Hierarchy Definition

This file defines the valid categories and subcategories for the vault.

## Valid Hierarchies

```dataviewjs
// Define the hierarchy structure
const hierarchy = {
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
    "[[🏡 Garden House]]",
    "[[🚴‍♀️ Santa Maura]]"
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

// Display as a nice table
dv.header(3, "Category and Subcategory Structure");
for (const [category, subcategory] of Object.entries(hierarchy)) {
  dv.header(4, category);
  dv.list(subcategory);
}

// Export for use in other scripts (though this doesn't persist across queries)
window.vaultHierarchy = hierarchy;
```

## Statistics

```dataviewjs
// Helper function to extract name from link object
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

const pages = dv.pages().where(p => p.Category);
const categoryCount = {};

for (const page of pages) {
  const catName = getLinkName(page.Category);
  const catDisplay = page.Category.path ? `[[${catName}]]` : page.Category;
  
  if (!categoryCount[catDisplay]) categoryCount[catDisplay] = 0;
  categoryCount[catDisplay]++;
}

dv.header(3, "Category Distribution");
dv.table(["Category", "Count", "Percentage"], 
  Object.entries(categoryCount)
    .sort(([,a], [,b]) => b - a)
    .map(([cat, count]) => [cat, count, `${Math.round(count / pages.length * 100)}%`])
);
```

## Subcategory Usage

```dataviewjs
// Define hierarchy again (since it doesn't persist)
const hierarchy = {
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
    "[[🏡 Garden House]]",
    "[[🚴‍♀️ Santa Maura]]"
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

// Helper functions
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

function normalizeToArray(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

function matchesHierarchyValue(value, hierarchyValue) {
  const valueName = getLinkName(value);
  const hierarchyName = hierarchyValue.replace(/[\[\]]/g, '');
  return valueName === hierarchyName || valueName === hierarchyValue;
}

// Count subcategory usage
const subcategoryUsage = [];

for (const [category, subcategories] of Object.entries(hierarchy)) {
  const categoryPages = dv.pages().where(p => 
    p.Category && matchesHierarchyValue(p.Category, category)
  );
  
  for (const subcat of subcategories) {
    const count = categoryPages.where(p => {
      if (!p.Subcategory) return false;
      const subcats = normalizeToArray(p.Subcategory);
      return subcats.some(s => matchesHierarchyValue(s, subcat));
    }).length;
    
    subcategoryUsage.push([category, subcat, count]);
  }
}

dv.header(3, "Subcategory Usage Statistics");
dv.table(
  ["Category", "Subcategory", "Usage Count"],
  subcategoryUsage.sort((a, b) => b[2] - a[2])
);
```