---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
Date modified: 06/25/2025
Version: 3.5
---

```dataviewjs
// ============================
// SINGLE DEFINITION SECTION
// ============================

// Define hierarchy once
const hierarchy = {
  "[[🏛️ Institutions]]": [
    "[[👔 Customers]]",
    "[[🏇 Competitors]]", 
    "[[🎓 Universities]]",
    "[[🎓 Schools]]",
    "[[🤝 3rd Pty Partners]]",
    "[[🛍️ Shopping]]",
    "[[👩‍⚕️ Medical]]",
    "[[💰 Finances]]",
    "[[👩‍⚖️ Legal & Tax]]",
    "[[💼 Employment]]",
    "[[👮‍♂️ Government]]",
    "[[🧐 Analysts]]",
    "[[🛄 Travel]]"
  ],
  "[[👥 People]]": [
    "[[🧑‍🧑‍🧒‍🧒 Family]]",
    "[[👯 Friends]]",
    "[[💪 Work People]]",
    "[[🐶 Pets]]",
    "[[🧾 Providers]]",
    "[[👩‍🎓 Applicant Tracker]]",
    "[[🩺 Doctors]]"
  ],
  "[[👔 Work]]": [
	"[[🌴 Work Topics]]",
	"[[👐 1st Pty Partners]]"
  ],
  "[[🚴‍♀️ Teams]]": [
    "[[🚴‍♀️ Medical]]",
    "[[🚴‍♀️ Work Teams]]",
    "[[🚴‍♀️ Old Brompton Road (OBR)]]",
    "[[🚴‍♀️ Killarney Road]]",
    "[[🏡 Garden House]]",
    "[[🍸 Olive Grove]]",
    "[[🚴‍♀️ Santa Maura]]",
    "[[🚴‍♀️ champion]]",
    "[[🚴‍♀️ Pets]]"
  ],
  "[[🚵 Sanity]]": [
    "[[🐧 Linux]]",
    "[[🍱 Recipies]]",
    "[[🚴‍♀️ Sports]]",
    "[[✍️ Stories]]",
    "[[✈️ Travel Plans]]",
    "[[👩‍🏫 Training]]"
  ],
  "[[🔲 Frameworks]]": [
    "[[🧮 Templates]]",
    "[[📝 Transcripts]]",
    "[[🖇️ Attachments]]",
    "[[📎 Clippings]]",
    "[[🎗️ Reminders]]",
    "[[💜 Obsidian Tools]]",
    "[[🔒 Vault]]"
  ]
};

// Helper functions (defined once)
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

// ============================
// DATA COLLECTION (SINGLE PASS)
// ============================

// Collect all data in one pass for efficiency
const allPages = dv.pages('');
const currentPagePath = dv.current().file.path;

// Initialize data structures
const stats = {
  total: 0,
  categorized: 0,
  uncategorized: 0,
  noFrontmatter: 0,
  withSubcategories: 0,
  withTeams: 0,
  byCategory: {},
  byFolder: {},
  byFolderNoFrontmatter: {},
  validationIssues: [],
  recentActivity: [],
  teamAssignments: {},
  invalidTeamAssignments: [],
  missingSubcategories: [],
  teamPages: new Set() // Track valid team pages
};

// Initialize category counts
for (const cat of Object.keys(hierarchy)) {
  stats.byCategory[cat] = {
    count: 0,
    withSubcat: 0,
    bySubcat: {},
    pages: []
  };
  for (const subcat of hierarchy[cat]) {
    stats.byCategory[cat].bySubcat[subcat] = 0;
  }
}

// First pass to identify valid team pages
for (const page of allPages) {
  if (page.Category && matchesHierarchyValue(page.Category, "[[🚴‍♀️ Teams]]")) {
    stats.teamPages.add(getLinkName(page.file.name));
  }
}

// Helper function to detect if a page has frontmatter
function hasFrontmatter(page) {
  // Check if page has any properties beyond the default file properties
  const defaultProps = ['file', 'aliases', 'tags'];
  const pageKeys = Object.keys(page);
  
  // If the page has any non-default properties, it has frontmatter
  return pageKeys.some(key => !defaultProps.includes(key));
}

// Single pass through all pages
for (const page of allPages) {
  // Skip current dashboard page
  if (page.file.path === currentPagePath) continue;
  
  stats.total++;
  
  // Track recent activity (keep last 15)
  if (stats.recentActivity.length < 15 || page.file.mtime > stats.recentActivity[14].mtime) {
    stats.recentActivity.push({
      page: page,
      mtime: page.file.mtime
    });
    stats.recentActivity.sort((a, b) => b.mtime - a.mtime);
    if (stats.recentActivity.length > 15) {
      stats.recentActivity.pop();
    }
  }
  
  // Check if page has frontmatter
  if (!hasFrontmatter(page)) {
    stats.noFrontmatter++;
    // Track by folder for notes without frontmatter
    const folder = page.file.folder || "Root";
    if (!stats.byFolderNoFrontmatter[folder]) {
      stats.byFolderNoFrontmatter[folder] = 0;
    }
    stats.byFolderNoFrontmatter[folder]++;
  } else if (page.Category) {
    // Has frontmatter and Category
    stats.categorized++;
    
    // Count subcategories and teams
    if (page.Subcategory) stats.withSubcategories++;
    if (page.Team) {
      stats.withTeams++;
      // Track team assignments
      const teams = normalizeToArray(page.Team);
      for (const team of teams) {
        const teamName = getLinkName(team);
        
        // Check if team is valid
        if (!stats.teamPages.has(teamName)) {
          stats.invalidTeamAssignments.push({
            page: page,
            invalidTeam: teamName
          });
        }
        
        if (!stats.teamAssignments[teamName]) {
          stats.teamAssignments[teamName] = [];
        }
        stats.teamAssignments[teamName].push(page);
      }
    }
    
    // Track by category
    const catName = getLinkName(page.Category);
    let validCategory = null;
    
    for (const [hierCat, subcats] of Object.entries(hierarchy)) {
      if (matchesHierarchyValue(page.Category, hierCat)) {
        validCategory = hierCat;
        stats.byCategory[hierCat].count++;
        stats.byCategory[hierCat].pages.push(page);
        
        // Track subcategories
        if (page.Subcategory) {
          stats.byCategory[hierCat].withSubcat++;
          const subcatNames = getSubcategoryNames(page.Subcategory);
          for (const subcatName of subcatNames) {
            for (const validSubcat of subcats) {
              if (matchesHierarchyValue(subcatName, validSubcat)) {
                stats.byCategory[hierCat].bySubcat[validSubcat]++;
              }
            }
          }
        } else {
          stats.missingSubcategories.push(page);
        }
        break;
      }
    }
    
    // Validation
    if (!validCategory) {
      stats.validationIssues.push({
        page: page,
        issue: `Invalid category: "${catName}"`
      });
    } else if (page.Subcategory) {
      const subcatNames = getSubcategoryNames(page.Subcategory);
      const validSubcats = hierarchy[validCategory];
      for (const subcatName of subcatNames) {
        const isValid = validSubcats.some(validSubcat => 
          matchesHierarchyValue(subcatName, validSubcat)
        );
        if (!isValid) {
          stats.validationIssues.push({
            page: page,
            issue: `Invalid subcategory: "${subcatName}" for category "${getLinkName(validCategory)}"`
          });
        }
      }
    }
  } else {
    // Has frontmatter but no Category
    stats.uncategorized++;
    // Track by folder
    const folder = page.file.folder || "Root";
    if (!stats.byFolder[folder]) {
      stats.byFolder[folder] = 0;
    }
    stats.byFolder[folder]++;
    
    // Check for partial metadata
    if (page.Subcategory && !page.Category) {
      stats.validationIssues.push({
        page: page,
        issue: "Has subcategory but no category"
      });
    }
  }
}

// ============================
// DISPLAY SECTIONS
// ============================

// Quick Stats
dv.header(1, "1 - 📊 Summary Categorized and Uncategorized Notes");
const tableRows = [
  ["**Total Notes**", stats.total, "100%"],
  ["", "", ""],
  ["**Categorized Notes**", stats.categorized, `${Math.round(stats.categorized / stats.total * 100)}%`],
  ["  → With Subcategories", stats.withSubcategories, `${Math.round(stats.withSubcategories / stats.total * 100)}%`],
  ["  → With Team Assignments", stats.withTeams, `${Math.round(stats.withTeams / stats.total * 100)}%`],
  ["", "", ""],
  ["**Uncategorized Notes**", stats.uncategorized, `${Math.round(stats.uncategorized / stats.total * 100)}%`]
];

// Add top folders for uncategorized
const sortedFolders = Object.entries(stats.byFolder)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10);
  
let displayedCount = 0;
for (const [folder, count] of sortedFolders) {
  const displayName = folder.length > 40 ? folder.substring(0, 37) + "..." : folder;
  tableRows.push([`  → ${displayName}`, count, `${Math.round(count / stats.total * 100)}%`]);
  displayedCount += count;
}

// Add remaining folders count for uncategorized
const totalFolders = Object.keys(stats.byFolder).length;
if (totalFolders > 10) {
  const remainingCount = stats.uncategorized - displayedCount;
  tableRows.push([`  → ... ${totalFolders - 10} more folders`, remainingCount, `${Math.round(remainingCount / stats.total * 100)}%`]);
}

// Add section for notes with no frontmatter
tableRows.push(["", "", ""]);
tableRows.push(["**Notes with no frontmatter YAML**", stats.noFrontmatter, `${Math.round(stats.noFrontmatter / stats.total * 100)}%`]);

// Add top folders for notes without frontmatter
const sortedFoldersNoFrontmatter = Object.entries(stats.byFolderNoFrontmatter)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10);
  
let displayedCountNoFrontmatter = 0;
for (const [folder, count] of sortedFoldersNoFrontmatter) {
  const displayName = folder.length > 40 ? folder.substring(0, 37) + "..." : folder;
  tableRows.push([`  → ${displayName}`, count, `${Math.round(count / stats.total * 100)}%`]);
  displayedCountNoFrontmatter += count;
}

// Add remaining folders count for no frontmatter
const totalFoldersNoFrontmatter = Object.keys(stats.byFolderNoFrontmatter).length;
if (totalFoldersNoFrontmatter > 10) {
  const remainingCountNoFrontmatter = stats.noFrontmatter - displayedCountNoFrontmatter;
  tableRows.push([`  → ... ${totalFoldersNoFrontmatter - 10} more folders`, remainingCountNoFrontmatter, `${Math.round(remainingCountNoFrontmatter / stats.total * 100)}%`]);
}

dv.table(["Metric", "Count", "Percentage"], tableRows);

// Recent Activity
dv.header(1, "2 - 🕐 Recent Activity");
dv.table(
  ["Note", "Category", "Subcategory", "Team", "Modified"],
  stats.recentActivity.map(item => [
    item.page.file.link,
    getLinkName(item.page.Category) || "-",
    item.page.Subcategory ? getSubcategoryNames(item.page.Subcategory).join(", ") : "-",
    item.page.Team ? normalizeToArray(item.page.Team).map(t => getLinkName(t)).join(", ") : "-",
    item.mtime
  ])
);

// Category Distribution
dv.header(1, "3 - 📁 Category Distribution");
const categoryRows = [];
for (const [cat, data] of Object.entries(stats.byCategory)) {
  if (data.count > 0) {
    categoryRows.push([
      cat,
      data.count,
      `${Math.round(data.count / stats.categorized * 100)}%`,
      `${Math.round(data.withSubcat / data.count * 100)}%`
    ]);
  }
}
dv.table(
  ["Category", "Notes", "% of Categorized", "% with Subcategories"],
  categoryRows.sort((a, b) => b[1] - a[1])
);

// Subcategory Usage
dv.header(1, "4 - 📈 Subcategory Usage");
const usageData = [];
for (const [cat, subcats] of Object.entries(hierarchy)) {
  const catData = stats.byCategory[cat];
  if (catData.count > 0) {
    for (const [subcat, count] of Object.entries(catData.bySubcat)) {
      usageData.push({
        category: cat,
        subcategory: subcat,
        count: count,
        percentage: Math.round(count / catData.count * 100)
      });
    }
  }
}

// Most used subcategories
const topUsed = usageData
  .sort((a, b) => b.count - a.count)

if (topUsed.length > 0) {
  dv.header(2, "Most Used Subcategories");
  dv.table(
    ["Category", "Subcategory", "Count", "%"],
    topUsed.map(d => [d.category, d.subcategory, d.count, `${d.percentage}%`])
  );
}

// Unused subcategories
const unused = usageData.filter(d => d.count === 0);
if (unused.length > 0) {
  dv.header(2, "Unused Subcategories");
  dv.table(
    ["Category", "Subcategory"],
    unused.map(d => [d.category, d.subcategory])
  );
}

// Validation Issues Summary
if (stats.validationIssues.length > 0) {
  dv.header(1, "5 - ⚠️ Validation Issues");
  dv.paragraph(`Found ${stats.validationIssues.length} issues that need attention. The validation checks for: valid categories matching the hierarchy, valid subcategories for each category, and proper metadata structure.`);
  
  // Group by issue type
  const issueGroups = {};
  for (const item of stats.validationIssues) {
    if (!issueGroups[item.issue]) {
      issueGroups[item.issue] = [];
    }
    issueGroups[item.issue].push(item.page);
  }
  
  for (const [issue, pages] of Object.entries(issueGroups)) {
    dv.header(2, `${issue} (${pages.length} notes)`);
    dv.list(pages.slice(0, 5).map(p => p.file.link));
    if (pages.length > 5) {
      dv.paragraph(`*... and ${pages.length - 5} more*`);
    }
  }
  
  // Export for fixing
  dv.header(2, "📤 Export for Fixing");
  const exportList = stats.validationIssues.slice(0, 20).map(item => 
    `- [ ] ${item.page.file.path}: ${item.issue}`
  );
  dv.paragraph("```");
  dv.paragraph(exportList.join("\n"));
  if (stats.validationIssues.length > 20) {
    dv.paragraph(`... and ${stats.validationIssues.length - 20} more issues`);
  }
  dv.paragraph("```");
} else {
  dv.header(1, "✅ All Notes Valid");
  dv.paragraph("No validation issues found! All notes have valid categories from the hierarchy, subcategories match their parent categories, and metadata structure is correct.");
}

// Missing Subcategories
if (stats.missingSubcategories.length > 0) {
  dv.header(1, "6 - 📝 Notes Missing Subcategories");
  dv.paragraph(`${stats.missingSubcategories.length} categorized notes need subcategories:`);
  dv.table(
    ["Note", "Obsidian", "Category", "Subcategory", "Stakeholder", "Team"],
    stats.missingSubcategories.slice(0, 10).map(p => [
      p.file.link,
      p.Obsidian || "-",
      getLinkName(p.Category),
      p.Subcategory || "-",
      p.Stakeholder || "-",
      p.Team ? normalizeToArray(p.Team).map(t => getLinkName(t)).join(", ") : "-"
    ])
  );
  if (stats.missingSubcategories.length > 10) {
    dv.paragraph(`*... and ${stats.missingSubcategories.length - 10} more*`);
  }
}

// Team Overview
const teamData = [];
for (const [teamName, members] of Object.entries(stats.teamAssignments)) {
  const institutions = members.filter(m => 
    matchesHierarchyValue(m.Category, "[[🏛️ Institutions]]")
  ).length;
  const people = members.filter(m => 
    matchesHierarchyValue(m.Category, "[[👥 People]]")
  ).length;
  
  // Get team page to find its subcategory
  const teamPage = allPages.find(p => 
    getLinkName(p.file.name) === teamName && 
    matchesHierarchyValue(p.Category, "[[🚴‍♀️ Teams]]")
  );
  
  teamData.push({
    name: teamName,
    institutions: institutions,
    people: people,
    total: members.length,
    subcategory: teamPage && teamPage.Subcategory ? getSubcategoryNames(teamPage.Subcategory).join(", ") : "-"
  });
}

if (teamData.length > 0) {
  dv.header(1, "7 - 👥 Team Assignments");
  dv.table(
    ["Team", "Institutions", "People", "Total", "Subcategory"],
    teamData
      .sort((a, b) => b.total - a.total)
      .map(t => [t.name, t.institutions, t.people, t.total, t.subcategory])
  );
}

// Team Assignment Validation
if (stats.invalidTeamAssignments.length > 0) {
  dv.header(1, "8 - ❌ Team Assignment Validation");
  dv.paragraph(`Found ${stats.invalidTeamAssignments.length} notes with invalid team assignments (references to non-existent teams):`);
  
  const displayLimit = 15;
  dv.table(
    ["Note", "Category", "Subcategory", "Invalid Team Reference"],
    stats.invalidTeamAssignments.slice(0, displayLimit).map(item => {
      const subcategories = item.page.Subcategory ? getSubcategoryNames(item.page.Subcategory) : [];
      const subcategoryDisplay = subcategories.length > 0 
        ? subcategories.map(s => `• ${s}`).join("<br>") 
        : "-";
      
      return [
        item.page.file.link,
        getLinkName(item.page.Category),
        subcategoryDisplay,
        item.invalidTeam
      ];
    })
  );
  
  if (stats.invalidTeamAssignments.length > displayLimit) {
    dv.paragraph(`*... and ${stats.invalidTeamAssignments.length - displayLimit} more*`);
  }
}
```
---