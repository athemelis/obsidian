# Category Dashboard

## Quick Stats

```dataviewjs
const pages = dv.pages().where(p => p.Category);
const total = pages.length;
const withSubcats = pages.where(p => p.Subcategory).length;
const withTeams = pages.where(p => p.Team).length;

dv.paragraph(`**Total Categorized Notes:** ${total}`);
dv.paragraph(`**Notes with Subcategories:** ${withSubcats}`);
dv.paragraph(`**Notes with Team Assignments:** ${withTeams}`);
```

## Browse by Category

```dataviewjs
// Load hierarchy from the definition file
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

// Helper function to get the display name from a category value
function getCategoryName(cat) {
  if (typeof cat === 'string') return cat;
  if (cat && cat.path) {
    // Extract filename without extension from path
    const parts = cat.path.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('.md', '');
  }
  return null;
}

// Helper function to normalize subcategory values
function getSubcategoryNames(subcats) {
  if (!subcats) return [];
  if (!Array.isArray(subcats)) subcats = [subcats];
  return subcats.map(s => getCategoryName(s)).filter(s => s);
}

// Get all pages with categories
const allCategorizedPages = dv.pages().where(p => p.Category);

// Build summary data
const summaryData = [];

// Process each category in hierarchy
for (const [hierarchyCategory, hierarchySubcategories] of Object.entries(hierarchy)) {
  const categoryNameToMatch = hierarchyCategory.replace(/[\[\]]/g, '');
  
  // Find all pages that match this category
  const categoryPages = allCategorizedPages.where(p => {
    const catName = getCategoryName(p.Category);
    return catName === categoryNameToMatch;
  });
  
  if (categoryPages.length > 0) {
    // Count by subcategory
    const subcategoryCounts = {};
    let noSubcategoryCount = 0;
    
    for (const page of categoryPages) {
      const subcatNames = getSubcategoryNames(page.Subcategory);
      
      if (subcatNames.length > 0) {
        for (const subcatName of subcatNames) {
          // Try to match against hierarchy subcategories
          for (const hierSubcat of hierarchySubcategories) {
            const hierSubcatName = hierSubcat.replace(/[\[\]]/g, '');
            if (subcatName === hierSubcatName || hierSubcat === subcatName) {
              subcategoryCounts[hierSubcat] = (subcategoryCounts[hierSubcat] || 0) + 1;
              break;
            }
          }
        }
      } else {
        noSubcategoryCount++;
      }
    }
    
    // Add category total row
    summaryData.push([hierarchyCategory, "**Total**", `**${categoryPages.length}**`]);
    
    // Add subcategory rows
    for (const subcat of hierarchySubcategories) {
      if (subcategoryCounts[subcat]) {
        summaryData.push([hierarchyCategory, subcat, subcategoryCounts[subcat]]);
      }
    }
    
    // Add no subcategory row if any
    if (noSubcategoryCount > 0) {
      summaryData.push([hierarchyCategory, "*No Subcategory*", noSubcategoryCount]);
    }
  }
}

// Display summary table
dv.header(3, "Summary by Category and Subcategory");
dv.table(["Category", "Subcategory", "Count"], summaryData);

// Show categories not in hierarchy
const unknownCategories = new Set();
for (const page of allCategorizedPages) {
  const catName = getCategoryName(page.Category);
  const matchesHierarchy = Object.keys(hierarchy).some(h => 
    h.replace(/[\[\]]/g, '') === catName
  );
  if (!matchesHierarchy && catName) {
    unknownCategories.add(catName);
  }
}

if (unknownCategories.size > 0) {
  dv.header(3, "Other Categories");
  dv.list([...unknownCategories]);
}
```

## Recent Updates

```dataview
TABLE Category, Subcategory, file.mtime as "Modified"
WHERE Category
SORT file.mtime DESC
LIMIT 10
```

## Missing Subcategories

```dataviewjs
const pages = dv.pages()
  .where(p => p.Category && !p.Subcategory);

if (pages.length > 0) {
  dv.header(3, "Notes Missing Subcategories");
  dv.table(["Note", "Obsidian", "Category", "Subcategory", "Stakeholder", "Team"],
    pages.map(p => [p.file.link, p.Obsidian, p.Category, p.Subcategory, p.Stakeholder, p.Team])
  );
}
```

## Teams Overview

```dataviewjs
// Get all team pages
const teamPages = dv.pages().where(p => p.Category === "[[🚴‍♀️ Teams]]");

const teamData = [];

for (const team of teamPages) {
  const teamLink = team.file.link;
  
  // Count institutions and people in this team
  const institutions = dv.pages()
    .where(p => p.Team && p.Category === "[[🏛️ Institutions]]")
    .where(p => {
      const teams = Array.isArray(p.Team) ? p.Team : [p.Team];
      return teams.some(t => {
        const tName = getCategoryName(t);
        const teamName = getCategoryName(teamLink);
        return tName === teamName;
      });
    });
    
  const people = dv.pages()
    .where(p => p.Team && p.Category === "[[👥 People]]")
    .where(p => {
      const teams = Array.isArray(p.Team) ? p.Team : [p.Team];
      return teams.some(t => {
        const tName = getCategoryName(t);
        const teamName = getCategoryName(teamLink);
        return tName === teamName;
      });
    });
    
  teamData.push([
    teamLink,
    institutions.length,
    people.length,
    institutions.length + people.length
  ]);
}

if (teamData.length > 0) {
  dv.header(3, "Team Composition");
  dv.table(["Team", "Institutions", "People", "Total"], teamData);
} else {
  dv.header(3, "No Teams Found");
}
```

## Category Links

```dataviewjs
// Show all category pages
const hierarchy = {
  "[[🏢 Companies]]": true,
  "[[👥 People]]": true,
  "[[🚴‍♀️ Teams]]": true,
  "[[🚵 Sanity]]": true,
  "[[🔲 Frameworks]]": true
};

dv.header(3, "Category Pages");
const categoryLinks = Object.keys(hierarchy);
dv.list(categoryLinks);
```