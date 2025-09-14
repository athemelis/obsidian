---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
---
**OpenIn Browser Profiles Configuration Guide**

This guide explains how to configure OpenIn (by Loshadki) to support profiles in Chromium-based browsers that aren't officially supported.

# Prerequisites

- OpenIn app installed on macOS
- OpenIn Helper app installed
- A Chromium-based browser with profile support (e.g., Brave, Vivaldi, Opera, Arc, Dia, Comet)
- Basic familiarity with Terminal and SQLite

## ⚠️ Important: Common Issues and Solutions

## Critical: NULL vs Empty String Fields
**OpenIn will NOT display browsers that have NULL values in text fields.** Always use empty strings (`''`) instead of `NULL` for:
- `ZREWRITEURLSCRIPTTEXT`
- `ZREWRITEURLREGEX`
- `ZREWRITEURLREGEXSUBSTITUTION`
- `ZREWRITEURLSCRIPTEXAMPLE`
- `ZICONOVERLAY`

## SQL Quote Types Matter
Always use straight single quotes (`'`) not curly quotes (`'` or `'`) in SQL commands. Curly quotes will cause parse errors.

# Understanding OpenIn's Architecture

OpenIn stores browser configurations in a SQLite database, not in plist files. The database location is:
```bash
~/Library/Group\ Containers/4QE86VV38D.app.loshadki.OpenIn/Library/Application\ Support/OpenIn
```

# Step-by-Step Configuration Process

## Step 1: Locate the Configuration Database

First, go to the database:
```bash
cd ~/Library/Group\ Containers/4QE86VV38D.app.loshadki.OpenIn/Library/Application\ Support/OpenIn/
ls -la ~/Library/Group\ Containers/4QE86VV38D.app.loshadki.OpenIn/Library/Application\ Support/OpenIn/
```

If you don't see the database at this location, you can find it using:
```bash
# Monitor file access while opening OpenIn preferences
sudo fs_usage -w -f filesys | grep -i openin
# Then open OpenIn preferences and look for .sqlite file paths
```

## Step 2: Back Up the Database

Always create a backup before making changes:

```bash
cp local.sqlite ~/Downloads/local.sqlite.backup
```

## Step 3: Explore the Database Structure

Open the database and examine its structure:

```bash
sqlite3 local.sqlite
```

```bash
sqlite3 ~/Library/Group\ Containers/4QE86VV38D.app.loshadki.OpenIn/Library/Application\ Support/OpenIn/local.sqlite
```

Inside SQLite, run:
```sql
-- View all tables
.tables

-- View the schema of the browser configurations table
.schema ZOPENINHANDLERAPP

-- See all configured browsers
SELECT Z_PK, ZNAME, ZBUNDLEIDENTIFIER, ZBROWSERUSEPROFILES, ZBROWSERPROFILENAME, ZPATH 
FROM ZOPENINHANDLERAPP;

-- See how browsers with profile support are configured (e.g., Edge)
SELECT * FROM ZOPENINHANDLERAPP 
WHERE ZBROWSERUSEPROFILES = 1;
```

## Step 4: Gather Browser Information

### 4.1 Get Bundle Identifier
```bash
# Method 1: Using mdls
mdls -name kMDItemCFBundleIdentifier /Applications/YourBrowser.app
```

```bash
# Method 2: Using osascript
osascript -e 'id of app "YourBrowser"'
```

```bash
# Method 3: Check Info.plist
cat /Applications/YourBrowser.app/Contents/Info.plist | grep -A1 CFBundleIdentifier
```

### 4.2 Find Profile Directories
```bash
# Check the browser's Application Support directory
ls -la ~/Library/Application\ Support/YourBrowser/

# Look for directories like:
# - Default
# - Profile 1
# - Profile 2
# - etc.

# For Comet:
ls -al ~/Library/Application\ Support/Comet/

# For Dia:
ls -al ~/Library/Application\ Support/Dia/User\ Data
```

## Step 5: Configure Browser Profiles

### 5.1 Quit OpenIn

```bash
sudo killall "OpenIn Helper"
```

```bash
sudo killall OpenIn
```

### 5.2 Update Existing Browser Entry

If your Chromium-based browser is already in OpenIn but without profile support:
```sql
-- Enable profile support for existing browser
-- CRITICAL: Use empty strings ('') not NULL for text fields
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Default',
    ZNAME = 'BrowserName | ProfileLabel',
    ZREWRITEURLSCRIPTTEXT = '',  -- Must be empty string, not NULL
    ZREWRITEURLREGEX = '',        -- Must be empty string, not NULL
    ZREWRITEURLREGEXSUBSTITUTION = '',  -- Must be empty string, not NULL
    ZREWRITEURLSCRIPTEXAMPLE = ''  -- Must be empty string, not NULL
WHERE ZBUNDLEIDENTIFIER = 'your.browser.bundleid';
```

For Orion browser

```sql
-- Update existing Orion entry for athemelis profile (uses Defaults directory)
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Defaults',
    ZNAME = 'Orion | athemelis',
    ZREWRITEURLSCRIPTTEXT = '',
    ZREWRITEURLREGEX = '',
    ZREWRITEURLREGEXSUBSTITUTION = '',
    ZREWRITEURLSCRIPTEXAMPLE = '',
    ZICONOVERLAY = ''
WHERE ZBUNDLEIDENTIFIER = 'com.kagi.kagimacOS';

-- Add ᵉShare profile (uses the UUID directory)
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 5, NULL,
    '97BB28F8-A126-47D3-AF18-910D2679EBD8',
    'com.kagi.kagimacOS',
    '', 'Orion | ᵉShare',
    '', '', '', 'Script',
    'file:///Applications/Orion.app/',
    ''
);
```


Updates 2025-08-21

```sql
-- Enable profile support for existing browser
-- CRITICAL: Use empty strings ('') not NULL for text fields
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Default',
    ZNAME = 'Dia | athemelis',
    ZREWRITEURLSCRIPTTEXT = '',  -- Must be empty string, not NULL
    ZREWRITEURLREGEX = '',        -- Must be empty string, not NULL
    ZREWRITEURLREGEXSUBSTITUTION = '',  -- Must be empty string, not NULL
    ZREWRITEURLSCRIPTEXAMPLE = ''  -- Must be empty string, not NULL
WHERE ZBUNDLEIDENTIFIER = 'company.thebrowser.dia';
```

```sql
-- Enable profile support for existing browser
-- CRITICAL: Use empty strings ('') not NULL for text fields
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Profile 1',
    ZNAME = 'Dia | ᵉShare',
    ZREWRITEURLSCRIPTTEXT = '',  -- Must be empty string, not NULL
    ZREWRITEURLREGEX = '',        -- Must be empty string, not NULL
    ZREWRITEURLREGEXSUBSTITUTION = '',  -- Must be empty string, not NULL
    ZREWRITEURLSCRIPTEXAMPLE = ''  -- Must be empty string, not NULL
WHERE ZBUNDLEIDENTIFIER = 'company.thebrowser.dia';
```


Updates: 2025-08-13

```bash
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Default',
    ZNAME = 'Comet | athemelis',
    ZREWRITEURLSCRIPTTEXT = '',  -- Must be empty string, not NULL
    ZREWRITEURLREGEX = '',        -- Must be empty string, not NULL
    ZREWRITEURLREGEXSUBSTITUTION = '',  -- Must be empty string, not NULL
    ZREWRITEURLSCRIPTEXAMPLE = ''  -- Must be empty string, not NULL
WHERE ZBUNDLEIDENTIFIER = 'ai.perplexity.comet';
```

```bash
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Profile 1',
    ZNAME = 'Comet | ᵉShare',
    ZREWRITEURLSCRIPTTEXT = '',  -- Must be empty string, not NULL
    ZREWRITEURLREGEX = '',        -- Must be empty string, not NULL
    ZREWRITEURLREGEXSUBSTITUTION = '',  -- Must be empty string, not NULL
    ZREWRITEURLSCRIPTEXAMPLE = ''  -- Must be empty string, not NULL
WHERE ZBUNDLEIDENTIFIER = 'ai.perplexity.comet';
```
### 5.3 Add Additional Profile Entries

For each additional profile, create a new entry:
```sql
-- CRITICAL: Use empty strings ('') not NULL for optional text fields
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0,                    -- Standard values (ZAPPORDER=4 controls display order)
    0, 1,                           -- ZBROWSERUSEPROFILES = 1 enables profiles
    1, 1,                           -- Launch settings
    0, 0,                           -- Application behavior
    0, 0, 0,                        -- URL rewrite settings
    1, 5, NULL,                     -- Handler settings (NULL is OK here)
    'Profile 1',                    -- Actual profile directory name
    'your.browser.bundleid',        -- Bundle identifier
    '',                             -- Icon overlay - use empty string, not NULL
    'BrowserName | CustomLabel',    -- Display name in OpenIn
    '',                             -- Regex - use empty string, not NULL
    '',                             -- Regex substitution - use empty string, not NULL
    '',                             -- Script text - use empty string, not NULL
    'Script',                       -- Script type
    'file:///Applications/YourBrowser.app/',  -- Application path
    ''                              -- Script example - use empty string, not NULL
);
```

Log of changes:
2025-08-21 Add Dia profiles

```sql
-- CRITICAL: Use empty strings ('') not NULL for optional text fields
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0,                    -- Standard values (ZAPPORDER=4 controls display order)
    0, 1,                           -- ZBROWSERUSEPROFILES = 1 enables profiles
    1, 1,                           -- Launch settings
    0, 0,                           -- Application behavior
    0, 0, 0,                        -- URL rewrite settings
    1, 5, NULL,                     -- Handler settings (NULL is OK here)
    'Default',                    -- Actual profile directory name
    'company.thebrowser.dia',        -- Bundle identifier
    '',                             -- Icon overlay - use empty string, not NULL
    'Dia | athemelis',    -- Display name in OpenIn
    '',                             -- Regex - use empty string, not NULL
    '',                             -- Regex substitution - use empty string, not NULL
    '',                             -- Script text - use empty string, not NULL
    'Script',                       -- Script type
    'file:///Applications/Dia.app/',  -- Application path
    ''                              -- Script example - use empty string, not NULL
);
```

```sql
-- CRITICAL: Use empty strings ('') not NULL for optional text fields
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0,                    -- Standard values (ZAPPORDER=4 controls display order)
    0, 1,                           -- ZBROWSERUSEPROFILES = 1 enables profiles
    1, 1,                           -- Launch settings
    0, 0,                           -- Application behavior
    0, 0, 0,                        -- URL rewrite settings
    1, 5, NULL,                     -- Handler settings (NULL is OK here)
    'Profile 1',                    -- Actual profile directory name
    'company.thebrowser.dia',        -- Bundle identifier
    '',                             -- Icon overlay - use empty string, not NULL
    'Dia | ᵉShare',    -- Display name in OpenIn
    '',                             -- Regex - use empty string, not NULL
    '',                             -- Regex substitution - use empty string, not NULL
    '',                             -- Script text - use empty string, not NULL
    'Script',                       -- Script type
    'file:///Applications/Dia.app/',  -- Application path
    ''                              -- Script example - use empty string, not NULL
);
```


2025-08-13

```sql
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0,                    -- Standard values (ZAPPORDER=4 controls display order)
    0, 1,                           -- ZBROWSERUSEPROFILES = 1 enables profiles
    1, 1,                           -- Launch settings
    0, 0,                           -- Application behavior
    0, 0, 0,                        -- URL rewrite settings
    1, 5, NULL,                     -- Handler settings (NULL is OK here)
    'Default',                    -- Actual profile directory name
    'ai.perplexity.comet',        -- Bundle identifier
    '',                             -- Icon overlay - use empty string, not NULL
    'Comet | athemelis',    -- Display name in OpenIn
    '',                             -- Regex - use empty string, not NULL
    '',                             -- Regex substitution - use empty string, not NULL
    '',                             -- Script text - use empty string, not NULL
    'Script',                       -- Script type
    'file:///Applications/Comet.app/',  -- Application path
    ''                              -- Script example - use empty string, not NULL
);
```

Logs of changes: 2025-08-12

```sql
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0,                    -- Standard values (ZAPPORDER=4 controls display order)
    0, 1,                           -- ZBROWSERUSEPROFILES = 1 enables profiles
    1, 1,                           -- Launch settings
    0, 0,                           -- Application behavior
    0, 0, 0,                        -- URL rewrite settings
    1, 5, NULL,                     -- Handler settings (NULL is OK here)
    'Profile 2',                    -- Actual profile directory name
    'ai.perplexity.comet',        -- Bundle identifier
    '',                             -- Icon overlay - use empty string, not NULL
    'Comet | Bank2Trust (tt-b2tadmin)',    -- Display name in OpenIn
    '',                             -- Regex - use empty string, not NULL
    '',                             -- Regex substitution - use empty string, not NULL
    '',                             -- Script text - use empty string, not NULL
    'Script',                       -- Script type
    'file:///Applications/Comet.app/',  -- Application path
    ''                              -- Script example - use empty string, not NULL
);
```

## Step 6: Verify Configuration

```sql
-- Check your entries
SELECT Z_PK, ZNAME, ZBUNDLEIDENTIFIER, ZBROWSERUSEPROFILES, ZBROWSERPROFILENAME 
FROM ZOPENINHANDLERAPP 
WHERE ZBUNDLEIDENTIFIER = 'your.browser.bundleid'
ORDER BY Z_PK;

-- Exit SQLite
.quit
```

Log of changes 2025-08-26

```sql
-- Verify the configuration
SELECT Z_PK, ZNAME, ZBROWSERPROFILENAME 
FROM ZOPENINHANDLERAPP 
WHERE ZBUNDLEIDENTIFIER = 'com.kagi.kagimacOS'
ORDER BY Z_PK;
```

Log of changes 2025-08-21

```sql
-- Check your entries
SELECT Z_PK, ZNAME, ZBUNDLEIDENTIFIER, ZBROWSERUSEPROFILES, ZBROWSERPROFILENAME 
FROM ZOPENINHANDLERAPP 
WHERE ZBUNDLEIDENTIFIER = 'company.thebrowser.dia'
ORDER BY Z_PK;

-- Exit SQLite
.quit
```

Logs of changes 2025-08-12

```sql
SELECT Z_PK, ZNAME, ZBUNDLEIDENTIFIER, ZBROWSERUSEPROFILES, ZBROWSERPROFILENAME 
FROM ZOPENINHANDLERAPP 
WHERE ZBUNDLEIDENTIFIER = 'ai.perplexity.comet'
ORDER BY Z_PK;
```

## Step 7: Customize Display Order

The `ZAPPORDER` field controls the display order in OpenIn's browser list. Lower values appear first.

```sql
-- Set custom order for your browsers
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 1 WHERE ZNAME = 'FirstBrowser | Profile';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 2 WHERE ZNAME = 'SecondBrowser | Profile';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 3 WHERE ZNAME = 'ThirdBrowser | Profile';

-- Verify the order
SELECT ZAPPORDER, ZNAME 
FROM ZOPENINHANDLERAPP 
WHERE ZBROWSERUSEPROFILES = 1
ORDER BY ZAPPORDER;
```

Update 2025-08-12
```sql
-- Set custom order for your browsers
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 1 WHERE ZNAME = 'Comet | athemelis';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 1 WHERE ZNAME = 'Comet | ᵉShare';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 1 WHERE ZNAME = 'Comet | Bank2Trust (tt-b2tadmin)';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 2 WHERE ZNAME = 'Microsoft Edge | Copilot';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 2 WHERE ZNAME = 'Microsoft Edge | ᵉShare';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 3 WHERE ZNAME = 'Safari | athemelis';
UPDATE ZOPENINHANDLERAPP SET ZAPPORDER = 3 WHERE ZNAME = 'Safari | ᵉShare';
```

**Tip:** Group browsers together by assigning sequential ZAPPORDER values to profiles of the same browser.

## Step 8: Restart OpenIn

```bash
open -a "OpenIn Helper"
```

```bash
open -a OpenIn
```

1. Quit OpenIn completely
2. Quit OpenIn Helper if running
3. Relaunch OpenIn
4. Check that your browser profiles appear in the browser list

# Special Case: Orion Browser (WebKit-based)

Orion is a WebKit-based browser that handles profiles differently than Chromium browsers. Instead of using profile directories with command-line arguments, Orion creates separate app bundles for each profile.

## Prerequisites for Orion

- Orion browser installed in `/Applications/`
- Profile apps created in `~/Applications/Orion/Orion Profiles/`

## Understanding Orion's Profile System

Unlike Chromium browsers that use `--profile-directory`, Orion:
1. Uses the main app (`/Applications/Orion.app`) for the default profile
2. Creates separate app bundles for additional profiles in `~/Applications/Orion/Orion Profiles/[UUID]/`
3. Each profile app has a unique bundle identifier: `com.kagi.kagimacOS.[UUID]`

## Step-by-Step Orion Configuration

### Step 1: Identify Your Orion Profiles

Check your Orion profiles configuration

```bash
plutil -p ~/Library/Application\ Support/Orion/profiles
```

List profile apps (if any exist)

```bash
ls -la ~/Applications/Orion/Orion\ Profiles/
```

### Step 2: Get Bundle Identifiers

bash

```bash
# Main Orion app (default profile)
mdls -name kMDItemCFBundleIdentifier /Applications/Orion.app

# Profile apps (if they exist)
mdls -name kMDItemCFBundleIdentifier ~/Applications/Orion/Orion\ Profiles/*/*.app
```

### Step 3: Add Orion Profiles to OpenIn

Since Orion profiles are separate apps, add each as an individual "browser" entry:

sql

```sql
-- Example: Add default profile (main Orion app)
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 5, NULL,
    NULL, 'com.kagi.kagimacOS',
    '', 'Orion | ProfileName',
    '', '', '', 'Script',
    'file:///Applications/Orion.app/',
    ''
);

-- Example: Add additional profile (profile-specific app)
-- Replace [UUID] with actual UUID from profile directory
-- Replace [ProfileName] with your profile name
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 5, NULL,
    NULL, 'com.kagi.kagimacOS.[UUID]',
    '', 'Orion | ProfileName',
    '', '', '', 'Script',
    'file:///Users/[username]/Applications/Orion/Orion Profiles/[UUID]/Orion - [ProfileName].app/',
    ''
);
```

### Important Notes for Orion

1. **DO NOT enable `ZBROWSERUSEPROFILES`** - Keep it as `0` since Orion profiles are separate apps
2. **Use exact paths** - Don't URL-encode spaces or special characters in the path
3. **Each profile needs its own entry** - Unlike Chromium browsers, you can't use profile switching
4. **Profile apps must exist** - The profile app must be created in Orion first

### Troubleshooting Orion

If profiles don't appear or don't open correctly:

- Verify the profile app exists at the specified path
- Check that the bundle identifier matches exactly
- Ensure the path in `ZPATH` doesn't have URL encoding (%20 for spaces)
- Confirm the profile app launches correctly when opened directly

### Known Limitations

- Orion's `--profile` command-line argument doesn't work properly
- URL schemes like `orion://profile/[name]` don't switch profiles
- Must treat each profile as a separate browser in OpenIn



# Important Field Explanations

| Field | Purpose | Typical Value | Critical Notes |
|-------|---------|---------------|----------------|
| `ZBROWSERUSEPROFILES` | Enables profile support | `1` for enabled, `0` for disabled | Must be `1` for profiles |
| `ZBROWSERPROFILENAME` | Actual profile directory name | `'Default'`, `'Profile 1'`, etc. | Must match actual directory |
| `ZNAME` | Display name in OpenIn | `'Browser \| Label'` | Customize as needed |
| `ZBUNDLEIDENTIFIER` | macOS bundle ID | `'com.example.browser'` | Must be exact |
| `ZPATH` | Application path | `'file:///Applications/Browser.app/'` | Include trailing slash |
| `ZAPPORDER` | Display order | `1`, `2`, `3`, etc. | Lower numbers appear first |
| `ZREWRITEURLSCRIPTTEXT` | Script text | `''` | **Must be empty string, NOT NULL** |
| `ZREWRITEURLREGEX` | URL regex | `''` | **Must be empty string, NOT NULL** |
| `ZREWRITEURLREGEXSUBSTITUTION` | Regex substitution | `''` | **Must be empty string, NOT NULL** |
| `ZREWRITEURLSCRIPTEXAMPLE` | Script example | `''` | **Must be empty string, NOT NULL** |
| `ZICONOVERLAY` | Icon overlay | `''` | **Must be empty string, NOT NULL** |

# Example: Complete Configuration for Comet Browser

```sql
-- Update existing entry for Default profile (if it exists)
UPDATE ZOPENINHANDLERAPP 
SET ZBROWSERUSEPROFILES = 1, 
    ZBROWSERPROFILENAME = 'Default',
    ZNAME = 'Comet | Personal',
    ZAPPORDER = 1,  -- First in list
    ZREWRITEURLSCRIPTTEXT = '',
    ZREWRITEURLREGEX = '',
    ZREWRITEURLREGEXSUBSTITUTION = '',
    ZREWRITEURLSCRIPTEXAMPLE = '',
    ZICONOVERLAY = ''
WHERE ZBUNDLEIDENTIFIER = 'ai.perplexity.comet' AND ZBROWSERUSEPROFILES = 0;

-- Add Work profile
INSERT INTO ZOPENINHANDLERAPP (
    Z_ENT, Z_OPT, ZAPPORDER, ZBROWSERPROFILENUMBER, 
    ZBROWSERPROFILEPRIVATE, ZBROWSERUSEPROFILES, 
    ZLAUNCHACTIVATES, ZLAUNCHADDSTORECENTITEMS, 
    ZLAUNCHCREATESNEWAPPLICATIONINSTANCE, ZLAUNCHHIDES, 
    ZLAUNCHHIDESOTHERS, ZREWRITEURL, ZREWRITEURLUSEPARENTFOLDER, 
    ZHANDLER, Z2_HANDLER, ZLASTUSED, 
    ZBROWSERPROFILENAME, ZBUNDLEIDENTIFIER, 
    ZICONOVERLAY, ZNAME, 
    ZREWRITEURLREGEX, ZREWRITEURLREGEXSUBSTITUTION, 
    ZREWRITEURLSCRIPTTEXT, ZREWRITEURLTYPE, ZPATH, ZREWRITEURLSCRIPTEXAMPLE
) VALUES (
    6, 3, 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 5, NULL, 
    'Profile 1', 'ai.perplexity.comet', 
    '', 'Comet | Work', 
    '', '',  -- Use empty strings, not NULL
    '', 'Script',  -- Use empty string for script text
    'file:///Applications/Comet.app/', ''  -- Use empty string for example
);
```

# Troubleshooting

## Browsers Don't Appear in OpenIn
**Most common cause: NULL values in text fields**
```sql
-- Fix NULL values that prevent browsers from appearing
UPDATE ZOPENINHANDLERAPP 
SET ZREWRITEURLSCRIPTTEXT = '',
    ZREWRITEURLREGEX = '',
    ZREWRITEURLREGEXSUBSTITUTION = '',
    ZREWRITEURLSCRIPTEXAMPLE = '',
    ZICONOVERLAY = ''
WHERE ZBUNDLEIDENTIFIER = 'your.browser.bundleid' 
  AND (ZREWRITEURLSCRIPTTEXT IS NULL 
       OR ZREWRITEURLREGEX IS NULL 
       OR ZREWRITEURLREGEXSUBSTITUTION IS NULL);

-- Verify no NULL values remain
SELECT Z_PK, ZNAME,
       CASE WHEN ZREWRITEURLSCRIPTTEXT IS NULL THEN 'NULL' ELSE 'OK' END as SCRIPT_STATUS
FROM ZOPENINHANDLERAPP 
WHERE ZBUNDLEIDENTIFIER = 'your.browser.bundleid';
```

## SQL Parse Errors
- **Error: "no such column"** - You're using curly quotes. Replace `'` and `'` with straight quotes `'`
- Copy SQL into a plain text editor first to avoid smart quotes

## Profiles Don't Appear
- Ensure OpenIn and Helper are fully restarted
- Verify profile directory names match exactly
- Check bundle identifier is correct
- Try logging out and back in to macOS

## Browser Doesn't Open with Correct Profile
- Verify the browser supports `--profile-directory` argument
- Test manually in Terminal:
  ```bash
  /Applications/YourBrowser.app/Contents/MacOS/YourBrowser --profile-directory="Profile 1"
  ```

## Database Changes Don't Persist
- Make sure OpenIn is closed before editing
- Check file permissions on the database
- Verify you're editing the correct database file

# Alternative Approach: Script Wrappers

If direct database modification doesn't work, create launcher scripts:

```bash
#!/bin/bash
# Save as ~/Library/Scripts/open-browser-profile.sh
PROFILE="${1:-Default}"
shift
/Applications/YourBrowser.app/Contents/MacOS/YourBrowser --profile-directory="$PROFILE" "$@"
```

Then create an Automator application that OpenIn can recognize as a "browser."

# Notes

- Profile names in `ZBROWSERPROFILENAME` must match actual directory names in `~/Library/Application Support/BrowserName/`
- Custom display names in `ZNAME` can be anything you want
- Most Chromium-based browsers support the `--profile-directory` command-line argument
- Always backup before making changes
- Changes require OpenIn restart to take effect