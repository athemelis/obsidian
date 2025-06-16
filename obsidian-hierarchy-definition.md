---
aliases: [Hierarchy, Categories]
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
    "[[💼 Employment]]",
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
    "[[🎗️ Reminders]]"
  ]
};

// Display as a nice table
dv.header(3, "Category and subcategory structure");
for (const [category, subcategory] of Object.entries(hierarchy)) {
  dv.header(4, category);
  dv.list(subcategory);
}

// Export for use in other scripts
window.vaultHierarchy = hierarchy;
```

## Statistics

```dataviewjs
const pages = dv.pages().where(p => p.Category);
const categoryCount = {};

for (const page of pages) {
  const cat = page.Category;
  if (!categoryCount[cat]) categoryCount[cat] = 0;
  categoryCount[cat]++;
}

dv.header(3, "Category Distribution");
dv.table(["Category", "Count"], 
  Object.entries(categoryCount)
    .sort(([,a], [,b]) => b - a)
    .map(([cat, count]) => [cat, count])
);
```