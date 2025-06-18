---
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 06/18/2025
Version: 1.0
---

# Hierarchy Validator

This validator checks all notes in your vault for compliance with the defined hierarchy structure.

## Validation Summary

```dataviewjs
// Helper functions (from dataview-helpers.md)
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

function getSubcategoryNames(subcats) {
  return normalizeToArray(subcats)
    .map(s => getLinkName(s))
    .filter(s => s);
}

function matchesHierarchyValue(value, hierarchyValue) {
  const valueName = getLinkName(value);
  const hierarchyName = hierarchyValue.replace(/[\[\]]/g, '');
  return valueName === hierarchyName || valueName === hierarchyValue;
}

// Define valid hierarchy
const validHierarchy = {
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

// Validation function
function validatePage(page) {
  const issues = [];
  
  if (!page.Category && page.Subcategory) {
    issues.push("Has subcategory but no category");
    return issues;
  }
  
  if (!page.Category) return issues;
  
  const categoryName = getLinkName(page.Category);
  let validCategory = null;
  
  // Find matching category in hierarchy
  for (const [hierCat, subcats] of Object.entries(validHierarchy)) {
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
    const validSubcats = validHierarchy[validCategory];
    
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

// Get all pages and validate
const allPages = dv.pages('').where(p => p.Category || p.Subcategory);
const validationResults = [];
let totalIssues = 0;

for (const page of allPages) {
  const issues = validatePage(page);
  if (issues.length > 0) {
    validationResults.push({
      file: page.file.link,
      category: page.Category || "None",
      subcategory: page.Subcategory || "None",
      issues: issues
    });
    totalIssues += issues.length;
  }
}

// Display summary
if (validationResults.length === 0) {
  dv.paragraph("✅ **All notes have valid hierarchy!**");
  dv.paragraph(`Total validated: ${allPages.length} notes`);
} else {
  dv.paragraph(`⚠️ **Found ${totalIssues} issues in ${validationResults.length} notes**`);
  dv.paragraph(`Total validated: ${allPages.length} notes`);
  
  // Group by issue type
  const issueTypes = {};
  
  for (const result of validationResults) {
    for (const issue of result.issues) {
      if (!issueTypes[issue]) {
        issueTypes[issue] = [];
      }
      issueTypes[issue].push(result);
    }
  }
  
  // Display by issue type
  for (const [issueType, pages] of Object.entries(issueTypes)) {
    dv.header(3, `${issueType} (${pages.length} notes)`);
    
    dv.table(
      ["Note", "Category", "Subcategory"],
      pages.slice(0, 10).map(p => [
        p.file,
        getLinkName(p.category),
        Array.isArray(p.subcategory) 
          ? p.subcategory.map(s => getLinkName(s)).join(", ")
          : getLinkName(p.subcategory) || "-"
      ])
    );
    
    if (pages.length > 10) {
      dv.paragraph(`*... and ${pages.length - 10} more*`);
    }
  }
  
  // Export section
  dv.header(3, "📤 Export Issues");
  dv.paragraph("Copy the list below to work on fixing issues:");
  
  const exportList = validationResults.slice(0, 50).map(r => 
    `- [ ] ${r.file.path || r.file}: ${r.issues.join("; ")}`
  );
  
  dv.paragraph("```");
  dv.paragraph(exportList.join("\n"));
  if (validationResults.length > 50) {
    dv.paragraph(`... and ${validationResults.length - 50} more issues`);
  }
  dv.paragraph("```");
}
```

## Subcategory Usage Report

```dataviewjs
// Redefine helper functions and hierarchy for this section
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

function getSubcategoryNames(subcats) {
  return normalizeToArray(subcats)
    .map(s => getLinkName(s))
    .filter(s => s);
}

function matchesHierarchyValue(value, hierarchyValue) {
  const valueName = getLinkName(value);
  const hierarchyName = hierarchyValue.replace(/[\[\]]/g, '');
  return valueName === hierarchyName || valueName === hierarchyValue;
}

const validHierarchy = {
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

// Get all pages
const allPages = dv.pages('').where(p => p.Category || p.Subcategory);

// Analyze subcategory usage
const usageData = [];

for (const [category, subcats] of Object.entries(validHierarchy)) {
  const categoryPages = allPages.where(p => 
    p.Category && matchesHierarchyValue(p.Category, category)
  );
  
  if (categoryPages.length === 0) continue;
  
  for (const subcat of subcats) {
    const count = categoryPages.where(p => {
      if (!p.Subcategory) return false;
      const subcatNames = getSubcategoryNames(p.Subcategory);
      return subcatNames.some(s => matchesHierarchyValue(s, subcat));
    }).length;
    
    const percentage = categoryPages.length > 0 
      ? Math.round(count / categoryPages.length * 100) 
      : 0;
    
    usageData.push({
      category: category,
      subcategory: subcat,
      count: count,
      percentage: percentage,
      unused: count === 0
    });
  }
}

// Show unused subcategories
const unusedSubcats = usageData.filter(d => d.unused);
if (unusedSubcats.length > 0) {
  dv.header(3, "🔍 Unused Subcategories");
  dv.table(
    ["Category", "Subcategory"],
    unusedSubcats.map(d => [d.category, d.subcategory])
  );
}

// Show usage statistics
dv.header(3, "📊 Usage Statistics");
dv.table(
  ["Category", "Subcategory", "Usage", "Percentage"],
  usageData
    .filter(d => !d.unused)
    .sort((a, b) => b.count - a.count)
    .slice(0, 20)
    .map(d => [
      d.category,
      d.subcategory,
      d.count,
      `${d.percentage}%`
    ])
);
```

## Team Assignment Validation

```dataviewjs
// Redefine helper functions for this section
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

// Get all valid team names
const validTeams = dv.pages('').where(p => 
  p.Category && matchesHierarchyValue(p.Category, "[[🚴‍♀️ Teams]]")
).map(p => p.file.name);

// Find pages with team assignments
const pagesWithTeams = dv.pages('').where(p => 
  p.Team && 
  (matchesHierarchyValue(p.Category, "[[🏛️ Institutions]]") || 
   matchesHierarchyValue(p.Category, "[[👥 People]]"))
);

// Check for invalid team assignments
const invalidTeamAssignments = [];

for (const page of pagesWithTeams) {
  const teams = normalizeToArray(page.Team);
  const invalidTeams = [];
  
  for (const team of teams) {
    const teamName = getLinkName(team);
    if (!validTeams.includes(teamName)) {
      invalidTeams.push(teamName);
    }
  }
  
  if (invalidTeams.length > 0) {
    invalidTeamAssignments.push({
      file: page.file.link,
      category: getLinkName(page.Category),
      invalidTeams: invalidTeams
    });
  }
}

// Display results
if (invalidTeamAssignments.length === 0) {
  dv.paragraph("✅ All team assignments are valid!");
  dv.paragraph(`Total notes with teams: ${pagesWithTeams.length}`);
} else {
  dv.paragraph(`⚠️ **Found ${invalidTeamAssignments.length} notes with invalid team assignments**`);
  
  dv.table(
    ["Note", "Category", "Invalid Teams"],
    invalidTeamAssignments.slice(0, 10).map(a => [
      a.file,
      a.category,
      a.invalidTeams.join(", ")
    ])
  );
  
  if (invalidTeamAssignments.length > 10) {
    dv.paragraph(`*... and ${invalidTeamAssignments.length - 10} more*`);
  }
}

// Show team distribution
const teamDistribution = {};
for (const page of pagesWithTeams) {
  const teams = normalizeToArray(page.Team);
  for (const team of teams) {
    const teamName = getLinkName(team);
    if (!teamDistribution[teamName]) {
      teamDistribution[teamName] = { institutions: 0, people: 0 };
    }
    if (matchesHierarchyValue(page.Category, "[[🏛️ Institutions]]")) {
      teamDistribution[teamName].institutions++;
    } else if (matchesHierarchyValue(page.Category, "[[👥 People]]")) {
      teamDistribution[teamName].people++;
    }
  }
}

dv.header(4, "📊 Team Distribution");
dv.table(
  ["Team", "Institutions", "People", "Total"],
  Object.entries(teamDistribution)
    .map(([team, counts]) => [
      team,
      counts.institutions,
      counts.people,
      counts.institutions + counts.people
    ])
    .sort((a, b) => b[3] - a[3])
);
```

## Missing Category/Subcategory Pages

```dataviewjs
// Redefine hierarchy for this section
const validHierarchy = {
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

const allCategoryPages = [...Object.keys(validHierarchy)];
const allSubcategoryPages = Object.values(validHierarchy)
  .flat()
  .filter(s => s.startsWith("[["));

const missingPages = [];

// Check categories
for (const catLink of allCategoryPages) {
  const catName = catLink.replace(/[\[\]]/g, "");
  const page = dv.page(catName);
  if (!page) {
    missingPages.push({
      type: "Category",
      link: catLink,
      status: "Missing"
    });
  }
}

// Check subcategories with wikilinks
for (const subcatLink of allSubcategoryPages) {
  const subcatName = subcatLink.replace(/[\[\]]/g, "");
  const page = dv.page(subcatName);
  if (!page) {
    missingPages.push({
      type: "Subcategory",
      link: subcatLink,
      status: "Missing"
    });
  }
}

if (missingPages.length > 0) {
  dv.table(
    ["Type", "Page", "Status"],
    missingPages.map(p => [p.type, p.link, p.status])
  );
  
  dv.paragraph("");
  dv.paragraph("💡 **Tip:** Create these missing pages to complete your hierarchy structure.");
} else {
  dv.paragraph("✅ All category and subcategory pages exist!");
}
```