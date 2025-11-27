# BlackCobra Karate Club - UI Design System

Reference based on **landing.html** styling. Apply consistently across all pages.

---

## Color Palette

### Primary Colors
- **Red (Primary Action)**: `#ef4444` - Used for buttons, text highlights, alerts
- **Orange (Secondary)**: `#f97316` - Used for gradients, accents
- **Dark Background**: `#111827` (gray-900) - Main background
- **Secondary Background**: `#1f2937` (gray-800) - Card backgrounds, sections
- **Tertiary Background**: `#374151` (gray-700) - Hover states, borders

### Accent Colors (Feature Icons)
- Red: `bg-red-500 bg-opacity-20`
- Orange: `bg-orange-500 bg-opacity-20`
- Yellow: `bg-yellow-500 bg-opacity-20`
- Green: `bg-green-500 bg-opacity-20`
- Blue: `bg-blue-500 bg-opacity-20`
- Purple: `bg-purple-500 bg-opacity-20`

### Text Colors
- Primary: `text-white`
- Secondary: `text-gray-300`
- Tertiary: `text-gray-400`
- Muted: `text-gray-500`

---

## Typography

### Font Stack
- Family: Default system fonts (Tailwind default)
- Weights: 400 (regular), 600 (semibold), 700 (bold), 900 (extra-bold)

### Heading Sizes
- H1: `text-5xl md:text-7xl font-bold` - Hero titles
- H2: `text-4xl md:text-5xl font-bold` - Section titles
- H3: `text-2xl font-bold` - Card titles
- H4: `text-lg font-bold` - Subsections

### Body Text
- Large: `text-xl md:text-2xl text-gray-300`
- Regular: `text-base text-gray-300`
- Small: `text-sm text-gray-400`

### Gradient Text (Headings)
```css
.gradient-text {
    background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

---

## Components

### Buttons

#### Primary Button (Action CTA)
```html
<a href="" class="btn-primary px-8 py-3 rounded-lg font-semibold text-white inline-block">
    Login to Dashboard
</a>
```
- Background: Red → Orange gradient (`linear-gradient(135deg, #ef4444 0%, #f97316 100%)`)
- Padding: `px-8 py-3`
- Border Radius: `rounded-lg`
- Hover: `scale(1.05)` + shadow
- Animation: `transition: all 0.3s ease`

#### Secondary Button (Alternative Action)
```html
<button class="px-8 py-3 rounded-lg font-semibold border-2 border-red-400 hover:bg-red-400 hover:bg-opacity-10 transition">
    View Test Credentials
</button>
```
- Border: `border-2 border-red-400`
- Hover: `bg-red-400 bg-opacity-10`
- Font: Semibold, white text

### Cards

#### Feature Card
```html
<div class="feature-card p-8 rounded-2xl bg-gray-700 hover:bg-gray-650 border border-gray-600">
    <div class="feature-icon bg-red-500 bg-opacity-20">🎓</div>
    <h3 class="text-2xl font-bold mb-4">Expert Instructors</h3>
    <p class="text-gray-300">Description text here...</p>
</div>
```
- Padding: `p-8`
- Background: `bg-gray-700`
- Border: `border border-gray-600`
- Border Radius: `rounded-2xl`
- Hover: `transform: translateY(-10px)` + enhanced shadow
- Transition: `all 0.3s ease`

#### Stats Card
```html
<div class="p-8 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 bg-opacity-10 border border-red-500 border-opacity-30">
    <div class="text-4xl font-bold text-red-400 mb-2">20+</div>
    <p class="text-gray-300">Years of Excellence</p>
</div>
```
- Background Gradient: `bg-gradient-to-br from-{color}-500 to-{color}-500 bg-opacity-10`
- Border: Colored, `border-opacity-30`
- Padding: `p-8`
- Border Radius: `rounded-2xl`

#### Glass Effect Cards (Modals/Special)
```html
<div class="glass-effect rounded-2xl p-8 border border-gray-700">
```
- Background: `rgba(255, 255, 255, 0.1)` with `backdrop-filter: blur(10px)`
- Border: `1px solid rgba(255, 255, 255, 0.2)`

### Icons (Feature Icons)
```html
<div class="feature-icon bg-red-500 bg-opacity-20">🎓</div>
```
- Size: `width: 60px; height: 60px`
- Border Radius: `rounded-12`
- Display: Flex center
- Background: Colored semi-transparent (e.g., `bg-red-500 bg-opacity-20`)
- Font Size: `text-2xl` (for emoji)

---

## Layout Patterns

### Section Spacing
- Vertical: `py-20` (80px)
- Horizontal: `px-4` (responsive)
- Container: `max-w-6xl mx-auto`

### Grid Systems

#### 3-Column Grid (Features, Team)
```html
<div class="grid md:grid-cols-3 gap-8">
```
- Mobile: 1 column (default)
- Desktop: 3 columns
- Gap: `gap-8` (32px)

#### 4-Column Grid (Stats)
```html
<div class="grid md:grid-cols-4 gap-8 text-center">
```
- Mobile: 1 column
- Desktop: 4 columns
- Gap: `gap-8`

#### 2-Column Grid (Buttons, Form Fields)
```html
<div class="flex flex-col sm:flex-row gap-4">
```
- Mobile: Stacked (flex-col)
- Desktop: Side-by-side (flex-row)
- Gap: `gap-4`

---

## Animations & Effects

### Keyframe Animations

#### Float Animation
```css
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
.float-animation {
    animation: float 3s ease-in-out infinite;
}
```

#### Pulse Ring Animation
```css
@keyframes pulse-ring {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.pulse-ring {
    animation: pulse-ring 2s infinite;
}
```

#### Slide-In Animation
```css
@keyframes slide-in {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.slide-in {
    animation: slide-in 0.8s ease-out;
}
```

### Transition Effects
- Button hover: `transition: all 0.3s ease`
- Card hover: `transition: all 0.3s ease` with `transform: translateY(-10px)`
- Links: `hover:text-red-400 transition`

### Shadow Effects
- Subtle: `shadow-md`
- Medium: `shadow-lg`
- Button hover: `box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4)`
- Card hover: `box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3)`

---

## Navigation

### Header/Nav Style
- Fixed: `fixed top-0 left-0 right-0`
- Glass Effect: Blurred background with subtle border
- Z-index: `z-50`
- Spacing: `h-16` with centered flex layout
- Logo: `w-10 h-10 bg-red-500 rounded-lg` (emoji inside)
- Links: White text with `hover:text-red-400 transition`

---

## Forms & Input Fields

### Text Input
```html
<input type="text" class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-red-400 focus:ring-1 focus:ring-red-400">
```
- Background: `bg-gray-700`
- Border: `border border-gray-600`
- Focus: `border-red-400 ring-1 ring-red-400`
- Padding: `px-4 py-2`
- Text: `text-white`
- Placeholder: `placeholder-gray-400`

### Select Dropdown
```html
<select class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-red-400">
```
Same as text input

### Checkbox/Radio
```html
<input type="checkbox" class="w-4 h-4 accent-red-500 rounded">
```
- Accent: `accent-red-500`
- Size: `w-4 h-4`

---

## Dashboard Components

### Data Table
```html
<div class="overflow-x-auto">
    <table class="w-full">
        <thead class="bg-gray-700 border-b border-gray-600">
            <tr>
                <th class="px-6 py-3 text-left text-sm font-semibold text-gray-200">Header</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b border-gray-700 hover:bg-gray-750">
                <td class="px-6 py-4 text-sm text-gray-300">Data</td>
            </tr>
        </tbody>
    </table>
</div>
```
- Header: `bg-gray-700 border-b border-gray-600`
- Body Row: `border-b border-gray-700 hover:bg-gray-750`
- Padding: `px-6 py-3` (header), `px-6 py-4` (cells)

### Status Badge
```html
<span class="px-3 py-1 rounded-full text-sm font-medium bg-green-500 bg-opacity-20 text-green-400">Active</span>
```
- Padding: `px-3 py-1`
- Border Radius: `rounded-full`
- Background: `{color}-500 bg-opacity-20`
- Text Color: `{color}-400`
- Font: `text-sm font-medium`

### Alert Box
```html
<div class="p-4 bg-red-500 bg-opacity-20 border border-red-500 border-opacity-30 rounded-lg">
    <p class="text-sm text-red-200">Error message here</p>
</div>
```
- Padding: `p-4`
- Background: `{color}-500 bg-opacity-20`
- Border: `{color}-500 border-opacity-30`
- Border Radius: `rounded-lg`
- Text: `{color}-200`

### Info Box (Tip/Notice)
```html
<div class="mt-8 p-4 bg-orange-500 bg-opacity-20 border border-orange-500 border-opacity-30 rounded-lg">
    <p class="text-sm text-orange-200">💡 <strong>Tip:</strong> Use these credentials to test...</p>
</div>
```

---

## Modal/Dialog

### Modal Container
```html
<div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
    <div class="bg-gray-800 rounded-2xl max-w-2xl w-full p-8 border border-gray-700">
        <!-- Content -->
    </div>
</div>
```
- Background Overlay: `bg-black bg-opacity-50`
- Z-index: `z-50`
- Modal: `bg-gray-800 border border-gray-700 rounded-2xl`
- Padding: `p-8`

### Modal Header
```html
<div class="flex justify-between items-center mb-6">
    <h3 class="text-2xl font-bold gradient-text">Modal Title</h3>
    <button class="text-gray-400 hover:text-white">Close</button>
</div>
```

---

## Responsive Design

### Breakpoints
- Mobile: < 640px (default)
- Tablet: `sm:` (640px+), `md:` (768px+)
- Desktop: `lg:` (1024px+), `xl:` (1280px+)

### Mobile-First Classes
```html
<!-- Stacks on mobile, columns on tablet, wider on desktop -->
<div class="w-full md:w-1/2 lg:w-1/3">
```

### Responsive Text
```html
<h1 class="text-5xl md:text-7xl font-bold">
```

### Responsive Grid
```html
<div class="grid md:grid-cols-3 gap-8">
```
- Default: 1 column
- md (768px+): 3 columns

---

## Spacing System

### Padding
- `px-4` / `py-4` = 16px
- `px-6` / `py-6` = 24px
- `px-8` / `py-8` = 32px

### Margin
- `mb-4` = 16px bottom
- `mb-6` = 24px bottom
- `mb-8` = 32px bottom
- `mt-8` = 32px top

### Gap (Grid/Flex)
- `gap-4` = 16px
- `gap-6` = 24px
- `gap-8` = 32px

---

## Border Radius

- `rounded-lg` = 8px (buttons, inputs)
- `rounded-xl` = 12px (cards)
- `rounded-2xl` = 16px (larger cards, modals)
- `rounded-full` = badges, circles

---

## Implementation Checklist

When styling new pages (Trainee Management, Matchmaking, Dashboard, Payments):

- [ ] Use dark background (gray-900/gray-800)
- [ ] Apply gradient text to main headings
- [ ] Use red/orange for primary actions
- [ ] Feature cards: `p-8 rounded-2xl bg-gray-700 border border-gray-600`
- [ ] Apply hover effects: `transform translateY(-10px)`
- [ ] Use glass effect for special sections
- [ ] Implement badge system for status
- [ ] Responsive grid (md:grid-cols-3 or similar)
- [ ] Consistent padding (py-20 for sections)
- [ ] Smooth transitions (all 0.3s ease)
- [ ] Match color palette for icons/accents
- [ ] Add animations (float, slide-in) where appropriate
- [ ] Use consistent typography sizes
- [ ] Ensure form inputs match style guide
- [ ] Test on mobile, tablet, desktop

---

## Files Using This System

- ✅ landing.html (reference implementation)
- 📋 trainee_management.html (pending)
- 📋 matchmaking.html (pending)
- 📋 dashboard.html (pending)
- 📋 payments.html (pending)

---

## Notes

- All CSS leverages TailwindCSS utilities
- Three.js can be used for hero sections or special visual effects
- Alpine.js for interactive components
- Keep animations subtle (not distracting from content)
- Maintain accessibility (color contrast, semantic HTML)
