---
Category: "[[🔲 Frameworks]]"
Subcategory:
  - "[[💜 Obsidian Tools]]"
Date modified: 08/03/2025
Version: 1
---

# Overview

The Image Zoom plugin allows you to click on any image in your Obsidian notes to view it in a full-screen modal overlay. This is particularly useful for viewing screenshots, diagrams, and other detailed images without leaving your note.

## Features

- **Single-click activation** - Click any image to expand it
- **Multiple close options** - Close with ESC key, X button, or clicking outside
- **Universal compatibility** - Works in both Reading View and Live Preview mode
- **Theme compatibility** - Works with Minimal theme and default Obsidian theme
- **Smooth animations** - Fade-in effects for a polished experience
- **Smart image detection** - Automatically ignores icons and UI elements

# Installation

## Prerequisites

- Obsidian v0.15.0 or higher
- Community plugins must be enabled (turn off Safe Mode)

## Step-by-Step Installation

1. **Create the plugin folder structure**
   ```
   Navigate to: [YourVault]/.obsidian/plugins/image-zoom/
   ```
   Create the `image-zoom` folder if it doesn't exist.

2. **Create the plugin files**
   
   You'll need to create three files:
   - `manifest.json` - Plugin metadata
   - `main.js` - Plugin functionality
   - CSS snippet file (in a different location)

3. **Add the CSS snippet**
   ```
   Navigate to: [YourVault]/.obsidian/snippets/
   ```
   Create `image-zoom.css` in this folder.

# Code Files

## File Structure

The Image Zoom plugin requires exactly 3 files in specific locations within your Obsidian vault:

```
Your Vault/
├── .obsidian/
│   ├── plugins/
│   │   └── image-zoom/
│   │       ├── manifest.json   # Plugin metadata
│   │       └── main.js         # Plugin functionality
│   └── snippets/
│       └── image-zoom.css      # Styling for the modal and hover effects
```

**Important**: Make sure to create the folders if they don't exist. Do not place JavaScript files in the snippets folder - Obsidian only loads CSS from there.

## 1. Plugin Manifest (`manifest.json`)

Create this file in `[YourVault]/.obsidian/plugins/image-zoom/manifest.json`:

```json
{
  "id": "image-zoom",
  "name": "Image Zoom",
  "version": "1.0.0",
  "minAppVersion": "0.15.0",
  "description": "Click images to view them in full screen",
  "author": "Your Name",
  "authorUrl": "",
  "isDesktopOnly": false
}
```

## 2. Plugin Main File (`main.js`)

Create this file in `[YourVault]/.obsidian/plugins/image-zoom/main.js`:

```javascript
const { Plugin } = require('obsidian');

module.exports = class ImageZoomPlugin extends Plugin {
  async onload() {
    console.log('Image Zoom Plugin loading...');
    
    // Create modal immediately
    this.createModal();
    
    // Set up click handler immediately
    this.setupClickHandler();
    
    // Also set up a mutation observer for dynamically loaded content
    this.setupMutationObserver();
    
    console.log('Image Zoom Plugin loaded successfully');
  }

  createModal() {
    // Remove any existing modal
    const existing = document.querySelector('.image-zoom-modal');
    if (existing) existing.remove();
    
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'image-zoom-modal';
    modal.style.display = 'none'; // Hidden by default
    modal.innerHTML = `
      <img src="" alt="Zoomed image">
      <button class="image-zoom-close">&times;</button>
    `;
    
    document.body.appendChild(modal);
    
    // Store references
    this.modal = modal;
    this.modalImg = modal.querySelector('img');
    const closeBtn = modal.querySelector('.image-zoom-close');
    
    // Click outside to close
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.hideModal();
      }
    });
    
    // Close button
    closeBtn.addEventListener('click', () => {
      this.hideModal();
    });
    
    // ESC key to close
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.modal.style.display === 'block') {
        this.hideModal();
      }
    });
    
    console.log('Modal created');
  }

  setupClickHandler() {
    this.clickHandler = (e) => {
      // IMPORTANT: Don't process clicks on modal elements
      if (e.target.closest('.image-zoom-modal')) {
        return; // Let modal handle its own clicks
      }
      
      // Only process if we directly clicked on an image or image container
      const directImageClick = e.target.tagName === 'IMG';
      const directContainerClick = e.target.classList.contains('image-embed') || 
                                  e.target.classList.contains('media-embed');
      
      if (!directImageClick && !directContainerClick) {
        return; // Ignore clicks that aren't directly on images or their containers
      }
      
      let img = null;
      
      if (directImageClick) {
        img = e.target;
      } else if (directContainerClick) {
        img = e.target.querySelector('img');
      }
      
      if (img && img.src && 
          (img.src.startsWith('app://') || 
           img.src.includes('/Obsidian/') || 
           img.src.startsWith('http')) &&
          img.naturalWidth > 50) {
        
        console.log('Image found and clicking through:', img.src.substring(0, 50) + '...');
        
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        
        this.showModal(img.src);
      }
    };
    
    // Use capture phase with highest priority
    document.addEventListener('click', this.clickHandler, true);
    console.log('Click handler attached');
  }

  setupMutationObserver() {
    // Watch for changes in the editor
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Apply pointer-events fix to any new images
            if (node.tagName === 'IMG' || (node.querySelectorAll && node.querySelectorAll('img').length > 0)) {
              this.fixMinimalThemeImages();
            }
          }
        });
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    this.observer = observer;
    console.log('Mutation observer set up');
  }

  fixMinimalThemeImages() {
    // Force pointer-events on images in Minimal theme
    const images = document.querySelectorAll('.theme-minimal .workspace-leaf-content img');
    images.forEach(img => {
      if (img.src && (img.src.startsWith('app://') || img.src.includes('/Obsidian/') || img.src.startsWith('http'))) {
        img.style.pointerEvents = 'auto';
        img.style.cursor = 'zoom-in';
      }
    });
  }

  showModal(src) {
    if (!this.modal || !this.modalImg) {
      console.error('Modal not initialized!');
      return;
    }
    
    console.log('Setting modal image source...');
    this.modalImg.src = src;
    this.modal.style.display = 'block';
    document.body.classList.add('image-zoom-active');
    console.log('Modal shown');
  }

  hideModal() {
    if (!this.modal) return;
    
    this.modal.style.display = 'none';
    document.body.classList.remove('image-zoom-active');
    this.modalImg.src = '';
    console.log('Modal hidden');
  }

  onunload() {
    console.log('Image Zoom Plugin unloading...');
    
    // Remove click handler
    if (this.clickHandler) {
      document.removeEventListener('click', this.clickHandler, true);
    }
    
    // Stop mutation observer
    if (this.observer) {
      this.observer.disconnect();
    }
    
    // Remove modal
    if (this.modal) {
      this.modal.remove();
    }
    
    // Clean up body class
    document.body.classList.remove('image-zoom-active');
    
    console.log('Image Zoom Plugin unloaded');
  }
};
```

## 3. CSS Styles (`image-zoom.css`)

Create this file in `[YourVault]/.obsidian/snippets/image-zoom.css`:

```css
/* Image Zoom for Obsidian with Minimal Theme */

/* Make images clickable in reading view */
.markdown-reading-view .internal-embed.image-embed {
  cursor: zoom-in;
  transition: transform 0.2s ease;
}

.markdown-reading-view .internal-embed.image-embed:hover {
  transform: scale(1.02);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Make images clickable in live preview mode - target all images */
.workspace-leaf-content img[src*="/Obsidian/"],
.workspace-leaf-content img[src^="app://"],
.workspace-leaf-content img[src^="http"] {
  cursor: zoom-in !important;
  transition: transform 0.2s ease;
}

.workspace-leaf-content img[src*="/Obsidian/"]:hover,
.workspace-leaf-content img[src^="app://"]:hover,
.workspace-leaf-content img[src^="http"]:hover {
  transform: scale(1.02);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Modal container */
.image-zoom-modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  cursor: zoom-out;
  animation: fadeIn 0.3s ease;
}

/* Modal image */
.image-zoom-modal img {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
  cursor: default;
  animation: zoomIn 0.3s ease;
}

/* Close button */
.image-zoom-close {
  position: absolute;
  top: 20px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  cursor: pointer;
  z-index: 1001;
  background: none;
  border: none;
  padding: 0;
  line-height: 1;
  font-family: Arial, sans-serif;
  transition: color 0.2s ease;
}

.image-zoom-close:hover {
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes zoomIn {
  from {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
  }
  to {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

/* Prevent body scroll when modal is open */
body.image-zoom-active {
  overflow: hidden;
}

/* Override Minimal theme's image handling if present */
.theme-minimal .workspace-leaf-content img[src*="/Obsidian/"],
.theme-minimal .workspace-leaf-content img[src^="app://"],
.theme-minimal .workspace-leaf-content img[src^="http"] {
  cursor: zoom-in !important;
  pointer-events: auto !important;
}

.theme-minimal.theme-dark .image-zoom-close {
  color: var(--text-muted);
}

.theme-minimal.theme-dark .image-zoom-close:hover {
  color: var(--text-normal);
}
```

# Activation

## Enable the Plugin

1. Open Obsidian Settings (Cmd/Ctrl + ,)
2. Navigate to **Community plugins**
3. Ensure **Safe mode** is OFF
4. Click **Reload plugins**
5. Find **Image Zoom** in your installed plugins list
6. Toggle the switch to enable it

## Enable the CSS Snippet

1. In Settings, go to **Appearance**
2. Scroll down to **CSS snippets**
3. Click the reload button (circular arrow icon)
4. Find **image-zoom** in the list
5. Toggle it ON

# Usage

## Basic Usage

1. Open any note containing images
2. Switch to either:
   - **Reading View** (preview mode)
   - **Live Preview** mode (editing with source mode OFF)
3. Click on any image to expand it

## Closing the Modal

You can close the expanded image using any of these methods:
- Press the **ESC** key
- Click the **×** button in the top-right corner
- Click anywhere **outside** the image

## Supported Image Types

- Local images stored in your vault
- Web images (http/https URLs)
- Images embedded using wikilinks: `![[image.png]]`
- Images embedded using markdown: `![](image.png)`

# Customization

## Adjusting Modal Size

To change the maximum size of expanded images, modify these values in `image-zoom.css`:

```css
.image-zoom-modal img {
  max-width: 90vw;  /* Change to desired width (e.g., 95vw for larger) */
  max-height: 90vh; /* Change to desired height (e.g., 95vh for larger) */
}
```

## Changing Background Opacity

To make the background darker or lighter:

```css
.image-zoom-modal {
  background-color: rgba(0, 0, 0, 0.9); /* Last value is opacity (0-1) */
}
```

## Animation Speed

To make animations faster or slower:

```css
.image-zoom-modal {
  animation: fadeIn 0.3s ease; /* Change 0.3s to desired duration */
}

.image-zoom-modal img {
  animation: zoomIn 0.3s ease; /* Change 0.3s to desired duration */
}
```

# Troubleshooting

## Plugin Not Working

1. **Check plugin is enabled**: Settings → Community plugins → Image Zoom should be ON
2. **Check CSS is enabled**: Settings → Appearance → CSS snippets → image-zoom should be ON
3. **Restart Obsidian**: Cmd/Ctrl + Q, then reopen
4. **Check view mode**: Ensure you're in Reading View or Live Preview (not Source mode)

## Console Debugging

To see debug messages:
1. Open Developer Tools: Cmd/Ctrl + Option/Shift + I
2. Go to Console tab
3. Look for messages starting with "Image Zoom Plugin"

## Images Not Clickable

- Ensure images are larger than 50px width (smaller images are considered icons)
- Check that cursor changes to zoom-in pointer when hovering
- Try disabling other image-related plugins temporarily

# Compatibility

- **Obsidian**: v0.15.0 or higher
- **Themes**: Tested with Default and Minimal themes
- **Platforms**: Works on all desktop platforms (Windows, macOS, Linux)
- **Mobile**: Not tested on mobile devices

# Known Limitations

- Does not work in Source Mode (markdown view)
- Small images (<50px width) are ignored to avoid zooming icons
- May conflict with other image-handling plugins

# License

This plugin is provided as-is for personal use. Feel free to modify and adapt it to your needs.

# Credits

Created for the Obsidian community to enhance image viewing experience.