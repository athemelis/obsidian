---
Category: "[[🔲 Frameworks]]"
Subcategory: "[[💜 Obsidian Tools]]"
Date modified: 06/18/2025
Version: 1.0
---

# Category Dashboard

## Quick Stats

```dataviewjs
// Helper functions (copy from _dataview-helpers.md)
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

// Stats calculation
const pages = dv.pages().where(p => p.Category);
const stats = {
  total: pages.length,
  withSubcategories: pages.where(p => p.Subcategory).length,
  withTeams: pages.where(p => p.Team).length,
  institutions: pages.where(p => p.Category === "[[🏛️ Institutions]]").length,
  people: pages.where(p => p.Category === "[[👥 People]]").length,
  teams: pages.where(p => p.Category === "[[🚴‍♀️ Teams]]").length
};

// Display as a nice grid
dv.table(
  ["Metric", "Count", "Percentage"],
  [
    ["**Total Categorized Notes**", stats.total, "100%"],
    ["Notes with Subcategories", stats.withSubcategories, `${Math.round(stats.withSubcategories / stats.total * 100)}%`],
    ["Notes with Team Assignments", stats.withTeams, `${Math.round(stats.withTeams / stats.total * 100)}%`],
    ["", "", ""],
    ["Institutions", stats.institutions, `${Math.round(stats.institutions / stats.total * 100)}%`],
    ["People", stats.people, `${Math.round(stats.people / stats.total * 100)}%`],
    ["Teams", stats.teams, `${Math.round(stats.teams / stats.total * 100)}%`]
  ]
);
```

## Browse by Category

```dataviewjs
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

function getSubcategoryNames(subcats) {
  if (!subcats) return [];
  if (!Array.isArray(subcats)) subcats = [subcats];
  return subcats.map(s => getLinkName(s)).filter(s => s);
}

function matchesHierarchyValue(value, hierarchyValue) {
  const valueName = getLinkName(value);
  const hierarchyName = hierarchyValue.replace(/[\[\]]/g, '');
  return valueName === hierarchyName || valueName === hierarchyValue;
}

// Define hierarchy
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

// Process each category
for (const [category, subcategories] of Object.entries(hierarchy)) {
  const categoryPages = dv.pages().where(p => 
    p.Category && matchesHierarchyValue(p.Category, category)
  );
  
  if (categoryPages.length === 0) continue;
  
  // Count by subcategory
  const subcatCounts = {};
  let noSubcatCount = 0;
  
  for (const page of categoryPages) {
    const subcatNames = getSubcategoryNames(page.Subcategory);
    
    if (subcatNames.length === 0) {
      noSubcatCount++;
    } else {
      for (const subcatName of subcatNames) {
        for (const validSubcat of subcategories) {
          if (matchesHierarchyValue(subcatName, validSubcat)) {
            subcatCounts[validSubcat] = (subcatCounts[validSubcat] || 0) + 1;
          }
        }
      }
    }
  }
  
  // Display category section
  dv.header(3, `${category} (${categoryPages.length} notes)`);
  
  const rows = [];
  for (const subcat of subcategories) {
    if (subcatCounts[subcat]) {
      rows.push([subcat, subcatCounts[subcat]]);
    }
  }
  
  if (noSubcatCount > 0) {
    rows.push(["*No subcategory*", noSubcatCount]);
  }
  
  if (rows.length > 0) {
    dv.table(["Subcategory", "Count"], rows);
  }
}

// Show uncategorized notes
const uncategorized = dv.pages('').where(p => !p.Category && p.file.path !== dv.current().file.path);
if (uncategorized.length > 0) {
  dv.header(3, `Uncategorized Notes (${uncategorized.length})`);
  dv.paragraph("Consider adding categories to these notes:");
  dv.list(uncategorized.limit(10).map(p => p.file.link));
  if (uncategorized.length > 10) {
    dv.paragraph(`*... and ${uncategorized.length - 10} more*`);
  }
}
```

## Teams Overview

```dataviewjs
// Redefine helper for this block
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

// Get all team pages
const teamPages = dv.pages('').where(p => {
  const catName = getLinkName(p.Category);
  return catName === "🚴‍♀️ Teams";
});

// Debug: Check what we're finding
if (teamPages.length === 0) {
  // Try to find any pages that might be teams
  const possibleTeams = dv.pages('').where(p => 
    p.file.name.includes("Team") || 
    p.file.path.includes("Teams") ||
    (p.Category && p.Category.toString().includes("Teams"))
  );
  
  if (possibleTeams.length > 0) {
    dv.paragraph("⚠️ Found possible team pages but they don't have the correct Category:");
    dv.list(possibleTeams.limit(5).map(p => 
      `${p.file.link} - Category: ${p.Category || "none"}`
    ));
    dv.paragraph("Make sure team pages have `Category: \"[[🚴‍♀️ Teams]]\"` in their frontmatter.");
  } else {
    dv.paragraph("No team pages found. Create team pages with `Category: \"[[🚴‍♀️ Teams]]\"` to see them here.");
  }
} else {
  const teamData = [];
  
  for (const team of teamPages) {
    const teamName = team.file.name; // Use file name for comparison
    
    // Find all members of this team
    const members = dv.pages('').where(p => {
      if (!p.Team) return false;
      const isMemberType = p.Category === "[[🏛️ Institutions]]" || p.Category === "[[👥 People]]" ||
                          getLinkName(p.Category) === "🏛️ Institutions" || getLinkName(p.Category) === "👥 People";
      if (!isMemberType) return false;
      
      // Check if this page is assigned to the current team
      const teams = normalizeToArray(p.Team);
      return teams.some(t => {
        const tName = getLinkName(t);
        // Match by name, handling "Team Name" vs "[[Team Name]]" vs full paths
        return tName === teamName || 
               tName === team.file.name ||
               (t.path && t.path.includes(team.file.name));
      });
    });
    
    const institutions = members.where(m => 
      m.Category === "[[🏛️ Institutions]]" || getLinkName(m.Category) === "🏛️ Institutions"
    );
    const people = members.where(m => 
      m.Category === "[[👥 People]]" || getLinkName(m.Category) === "👥 People"
    );
    
    teamData.push([
      team.file.link,
      institutions.length,
      people.length,
      members.length,
      team.Subcategory ? getLinkName(team.Subcategory) : "-"
    ]);
  }
  
  dv.table(
    ["Team", "Institutions", "People", "Total", "Type"],
    teamData.sort((a, b) => b[3] - a[3]) // Sort by total members
  );
  
  // Show summary
  const totalInstitutions = teamData.reduce((sum, row) => sum + row[1], 0);
  const totalPeople = teamData.reduce((sum, row) => sum + row[2], 0);
  dv.paragraph(`**Summary:** ${teamPages.length} teams, ${totalInstitutions} institution assignments, ${totalPeople} people assignments`);
}
```

## Recent Activity

```dataview
TABLE 
  Category, 
  Subcategory,
  Team,
  file.mtime as "Modified"
WHERE Category
SORT file.mtime DESC
LIMIT 10
```

## Missing Subcategories

```dataviewjs
const pages = dv.pages('')
  .where(p => p.Category && !p.Subcategory)
  .sort(p => p.file.name);

if (pages.length > 0) {
  dv.header(3, `Notes Missing Subcategories (${pages.length})`);
  dv.table(
    ["Note", "Obsidian", "Category", "Subcategory", "Stakeholder", "Team"],
    pages.limit(20).map(p => [
      p.file.link,
      p.Obsidian || "-",
      p.Category || "-",
      p.Subcategory || "-",
      p.Stakeholder || "-",
      p.Team || "-"
    ])
  );
  if (pages.length > 20) {
    dv.paragraph(`*... and ${pages.length - 20} more*`);
  }
} else {
  dv.paragraph("✅ All categorized notes have subcategories!");
}
```

## Category Health Check

```dataviewjs
// Helper function for this section
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

// Quick health metrics
const allPages = dv.pages('').where(p => p.Category);
const issues = [];

// Check for old category names
const oldCategories = allPages.where(p => 
  getLinkName(p.Category) === "🏢 Companies"
);
if (oldCategories.length > 0) {
  issues.push({
    issue: `${oldCategories.length} notes still using old "[[🏢 Companies]]" category`,
    action: "Update these notes to use [[🏛️ Institutions]] instead",
    notes: oldCategories.limit(5).map(p => p.file.link)
  });
}

// Check for non-standard category formats
const nonWikilinks = allPages.where(p => 
  typeof p.Category === 'string' && !p.Category.startsWith("[[")
);
if (nonWikilinks.length > 0) {
  issues.push({
    issue: `${nonWikilinks.length} notes with non-wikilink categories`,
    action: "These notes have plain text categories. They should use [[wikilink]] format",
    notes: nonWikilinks.limit(5).map(p => p.file.link)
  });
}

// Note about case-sensitivity
dv.paragraph("*Note: Dataview properties are case-insensitive, so detecting lowercase property names requires manual inspection or a different tool.*");

// Display results
if (issues.length === 0) {
  dv.paragraph("✅ **All automated category health checks passed!**");
  dv.paragraph("");
  dv.paragraph("💡 **Tip:** To check for lowercase property names, use Obsidian's search:");
  dv.paragraph("- Search for `category:` (lowercase) in Search (Ctrl/Cmd + Shift + F)");
  dv.paragraph("- Search for `subcategory:` (lowercase)");
  dv.paragraph("- Search for `team:` (lowercase)");
} else {
  dv.header(3, "⚠️ Category Health Issues");
  
  for (const issue of issues) {
    dv.paragraph(`**${issue.issue}**`);
    dv.paragraph(`*Action: ${issue.action}*`);
    if (issue.notes.length > 0) {
      dv.paragraph("Sample affected notes:");
      dv.list(issue.notes);
    }
    dv.paragraph("");
  }
}
```

## Category Pages

Quick links to all category pages:

- [[🏛️ Institutions]]
- [[👥 People]]
- [[🚴‍♀️ Teams]]
- [[🚵 Sanity]]
- [[🔲 Frameworks]]