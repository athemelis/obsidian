# Hierarchy Validator

```dataviewjs
// Define valid hierarchy with wikilinks
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
    "[[🎗️ Reminders]]"
  ]
};

// Helper function to get the display name from a category/subcategory value
function getName(value) {
  if (typeof value === 'string') return value;
  if (value && value.path) {
    // Extract filename without extension from path
    const parts = value.path.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('.md', '');
  }
  return null;
}

// Helper function to normalize subcategory values
function getSubcategoryNames(subcats) {
  if (!subcats) return [];
  if (!Array.isArray(subcats)) subcats = [subcats];
  return subcats.map(s => getName(s)).filter(s => s);
}

// Collect all issues
const issues = [];

// Check all pages with categories
const pages = dv.pages().where(p => p.Category || p.Subcategory);

for (const page of pages) {
  const pageIssues = [];
  
  // Get the category name
  const categoryName = getName(page.Category);
  
  // Check if category exists but is invalid
  if (page.Category) {
    // Find matching hierarchy category
    let validCategory = null;
    for (const hierCat of Object.keys(validHierarchy)) {
      if (hierCat.replace(/[\[\]]/g, '') === categoryName) {
        validCategory = hierCat;
        break;
      }
    }
    
    if (!validCategory) {
      pageIssues.push(`Invalid category: "${categoryName}"`);
    } else {
      // Check subcategories
      if (page.Subcategory) {
        const subcatNames = getSubcategoryNames(page.Subcategory);
        const validSubcats = validHierarchy[validCategory];
        
        for (const subcatName of subcatNames) {
          // Check if subcategory is valid for this category
          let isValid = false;
          for (const validSubcat of validSubcats) {
            const validSubcatName = validSubcat.replace(/[\[\]]/g, '');
            if (subcatName === validSubcatName || subcatName === validSubcat) {
              isValid = true;
              break;
            }
          }
          
          if (!isValid) {
            pageIssues.push(`Invalid subcategory: "${subcatName}" for category "${categoryName}"`);
          }
        }
      }
    }
  } else if (page.Subcategory) {
    pageIssues.push("Has subcategories but no category");
  }
  
  if (pageIssues.length > 0) {
    issues.push({
      file: page.file.link,
      issues: pageIssues
    });
  }
}

// Display results
if (issues.length === 0) {
  dv.paragraph("✅ **All notes have valid hierarchy!**");
} else {
  dv.header(3, `⚠️ Found ${issues.length} notes with hierarchy issues`);
  
  for (const issue of issues) {
    dv.header(4, issue.file);
    dv.list(issue.issues);
  }
}

// Show orphaned subcategories (subcategories never used)
dv.header(3, "Subcategory Usage");
for (const [category, subcats] of Object.entries(validHierarchy)) {
  const categoryNameToMatch = category.replace(/[\[\]]/g, '');
  const usage = {};
  subcats.forEach(s => usage[s] = 0);
  
  const categoryPages = dv.pages().where(p => {
    const catName = getName(p.Category);
    return catName === categoryNameToMatch && p.Subcategory;
  });
  
  for (const page of categoryPages) {
    const subcatNames = getSubcategoryNames(page.Subcategory);
    for (const subcatName of subcatNames) {
      // Match against valid subcategories
      for (const validSubcat of subcats) {
        const validSubcatName = validSubcat.replace(/[\[\]]/g, '');
        if (subcatName === validSubcatName || subcatName === validSubcat) {
          usage[validSubcat]++;
          break;
        }
      }
    }
  }
  
  const unusedSubcats = subcats.filter(s => usage[s] === 0);
  if (unusedSubcats.length > 0) {
    dv.paragraph(`**${category}** - Unused subcategories: ${unusedSubcats.join(", ")}`);
  }
}

// Validate that category and subcategory pages exist
dv.header(3, "Missing Category/Subcategory Pages");
const allCategoryPages = [...Object.keys(validHierarchy)];
const allSubcategoryPages = Object.values(validHierarchy).flat().filter(s => s.startsWith("[["));

const missingPages = [];

// Check categories
for (const catLink of allCategoryPages) {
  const catName = catLink.replace(/[\[\]]/g, "");
  if (!dv.page(catName)) {
    missingPages.push(`Category page missing: ${catLink}`);
  }
}

// Check subcategories with wikilinks
for (const subcatLink of allSubcategoryPages) {
  const subcatName = subcatLink.replace(/[\[\]]/g, "");
  if (!dv.page(subcatName)) {
    missingPages.push(`Subcategory page missing: ${subcatLink}`);
  }
}

if (missingPages.length > 0) {
  dv.list(missingPages);
} else {
  dv.paragraph("✅ All category and subcategory pages exist!");
}

// Show categories not in hierarchy
dv.header(3, "Categories Not in Hierarchy");
const unknownCategories = new Set();
const allPages = dv.pages().where(p => p.Category);

for (const page of allPages) {
  const catName = getName(page.Category);
  if (!catName) continue;
  
  const matchesHierarchy = Object.keys(validHierarchy).some(h => 
    h.replace(/[\[\]]/g, '') === catName
  );
  
  if (!matchesHierarchy) {
    unknownCategories.add(catName);
  }
}

// Show team assignments
dv.header(3, "Team Assignment Validation");

// Get all team pages
const teamPages = dv.pages().where(p => p.Category === "[[🚴‍♀️ Teams]]").map(p => getName(p.file.link));

// Check for invalid team assignments
const invalidTeamAssignments = [];
const pagesWithTeams = dv.pages().where(p => p.Team && (p.Category === "[[🏛️ Institutions]]" || p.Category === "[[👥 People]]"));

for (const page of pagesWithTeams) {
  const teams = Array.isArray(page.Team) ? page.Team : [page.Team];
  const invalidTeams = [];
  
  for (const team of teams) {
    const teamName = getName(team);
    if (!teamPages.includes(teamName)) {
      invalidTeams.push(teamName);
    }
  }
  
  if (invalidTeams.length > 0) {
    invalidTeamAssignments.push({
      file: page.file.link,
      invalidTeams: invalidTeams
    });
  }
}

if (invalidTeamAssignments.length > 0) {
  dv.paragraph(`⚠️ **Found ${invalidTeamAssignments.length} notes with invalid team assignments**`);
  for (const assignment of invalidTeamAssignments) {
    dv.paragraph(`- ${assignment.file}: Invalid teams: ${assignment.invalidTeams.join(", ")}`);
  }
} else {
  dv.paragraph("✅ All team assignments are valid!");
}
```