# Admin Sidebar Navigation - Collapsible Dropdown Groups

## Overview
Converted the admin sidebar navigation into collapsible dropdown groups for better organization and cleaner UI.

## Changes Made

### Navigation Groups (Collapsible)
The following sections now feature collapsible dropdown menus:

1. **Judge Management** (Dropdown)
   - Active Judges
   - Archived Judges

2. **Trainee Management** (Dropdown)
   - Active Trainees
   - Archived Trainees

3. **Event Management** (Dropdown)
   - Active Events
   - Archived Events

4. **Matchmaking** (Dropdown)
   - Active Matchmaking
   - Archived Matchmaking

### Non-Grouped Items
These remain as standard navigation links:
- Dashboard
- User Management
- Payments
- Reports
- Belt Promotion
- Evaluations

## Features

### Dropdown Functionality
- **Click to Toggle**: Click the group header to expand/collapse
- **Chevron Animation**: Arrow rotates 180° when opened/closed
- **Auto-Open**: Parent dropdown automatically opens when a child item is active
- **Single Open**: Only one dropdown can be open at a time

### Styling
- **Hover Effects**: Blue background with border accent
- **Active States**: Highlighted when group or item is active
- **Icons**: Each item includes appropriate SVG icons
- **Nested Padding**: Child items are indented for visual hierarchy
- **Smooth Animations**: CSS transitions for expand/collapse

### HTML Structure
```
.nav-dropdown-group
├── .nav-dropdown-toggle (button)
│   ├── Icon & Title
│   └── Chevron (rotates)
└── .nav-dropdown-menu
    ├── .nav-dropdown-item (link)
    └── .nav-dropdown-item (link)
```

### JavaScript Behavior
```javascript
- Handles click events on toggle buttons
- Closes other open dropdowns
- Toggles current dropdown open/close
- On page load: Opens parent if child is active
```

## CSS Classes

### Toggle Button
- `.nav-dropdown-toggle` - Main group header button
- `.nav-dropdown-toggle.open` - When expanded
- `.nav-dropdown-toggle.active` - When current page matches group

### Menu Container
- `.nav-dropdown-menu` - Container for dropdown items
- `.nav-dropdown-menu.open` - When expanded

### Menu Items
- `.nav-dropdown-item` - Individual menu link
- `.nav-dropdown-item.active` - When current page

### Icons
- `.nav-dropdown-icon` - Group header icon
- `.nav-dropdown-chevron` - Toggle arrow
- `.nav-dropdown-item-icon` - Item icon

## Visual Effects

### Hover States
- Background color change to light blue
- Left border accent appears
- Text color changes to lighter blue
- Icon shifts slightly right

### Active States
- Blue background gradient
- Blue text color
- Blue left border
- Blue icon shadow

### Animations
- Max-height transition for smooth expand/collapse (0.3s)
- Chevron rotation (0.3s)
- Hover effects (0.3s)

## Browser Compatibility
- Modern browsers with CSS transitions
- ES6 JavaScript support
- Flexbox layout

## Files Modified
- `/templates/components/sidebar_admin.html`
  - Added dropdown group structure
  - Added CSS styles
  - Added JavaScript functionality
  - Updated navigation markup
