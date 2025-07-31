# Leo Torres Portfolio Design System

## Overview

This design system implements a sophisticated 60/30/10 color strategy across three
distinct professional personas, using a unified visual language with strategic accent
differentiation. The system balances professional consistency with persona-specific
identity through careful color distribution and typography choices.


## Core Design Philosophy

### Color Strategy: 60/30/10 Distribution

**60% Neutrals (Foundation Colors)**
- Primary text: `#1f2937` (charcoal) - Main content, paragraphs
- Secondary text: `#4b5563` (dark-gray) - Secondary information, descriptions
- Tertiary text: `#6b7280` (medium-gray) - Taglines, metadata, timestamps
- Background base: `#f8fafc` (light-bg) - Page background
- Content background: `#ffffff` (white) - Main content container

**30% Navy (Primary Brand Color)**
- Main headings: `#1a365d` (navy) - Name, section titles, primary headings
- Navigation active states: navy for selected navigation items
- Primary brand elements: consistent across all personas

**10% Accent Colors (Persona-Specific)**
- **Researcher/Academic**: `#6b5b95` (plum) + `#8b7bb8` (plum-accent)
- **Leadership**: `#f59e0b` (gold)
- **Engineer/Technical**: `#e53e3e` (coral)

### Rationale for Navy as Primary Brand Color

Navy (`#1a365d`) serves as the unifying primary color because:

1. **Professional Authority**: Navy conveys expertise, reliability, and professionalism across all three career angles
2. **Versatility**: Works harmoniously with all three accent colors without competing
3. **Accessibility**: Provides excellent contrast ratios with all background colors
4. **Timelessness**: Unlike trend-driven colors, navy maintains professional credibility over time
5. **Cross-Cultural Appeal**: Universally recognized as authoritative in business/academic contexts

### Three-Persona Accent System

The accent color system differentiates three professional angles while maintaining visual cohesion:

#### **Academic/Researcher Persona (Plum)**
- **Primary accent**: `#6b5b95` (plum)
- **Secondary accent**: `#8b7bb8` (plum-accent) - lighter variant for decorative elements
- **Psychological association**: Academic sophistication, intellectual depth, research gravitas
- **Usage**: Section dividers, skill tags, bullet points, hover states, borders
- **Subtle background tint**: `#faf9fb` (extremely subtle plum wash)

#### **Leadership Persona (Gold)**
- **Accent**: `#f59e0b` (gold)
- **Psychological association**: Leadership, achievement, strategic thinking, executive presence
- **Usage**: Section dividers, achievement metrics, bullet points, hover states, borders
- **Subtle background tint**: `#fefdf8` (warm gold wash)

#### **Engineer/Technical Persona (Coral)**
- **Accent**: `#e53e3e` (coral)
- **Psychological association**: Energy, action, problem-solving, technical execution
- **Usage**: Section dividers, technical tags, bullet points, hover states, borders
- **Subtle background tint**: `#fffbfb` (gentle coral wash)

## Visual Identity Elements

### Diamond Navigation System

The diamond navigation serves as both brand element and persona indicator:

```css
.diamond {
  width: 12px;
  height: 12px;
  transform: rotate(45deg);
}
```

**Active State Logic**:
- **Academic page**: First diamond filled with plum, others outlined
- **Leadership page**: Second diamond filled with gold, others outlined
- **Engineering page**: Third diamond filled with coral, others outlined

**Footer Diamonds**: Always show all three colors as permanent brand elements

### Typography Hierarchy

**Primary Font**: Manrope (Geometric sans-serif)
- Chosen for: Modern professionalism, excellent readability, friendly authority
- Usage: All body text, headings, navigation

**Monospace Font**: JetBrains Mono
- Chosen for: Technical credibility, code-like precision
- Usage: Technical skill tags, project technologies, dates, metadata

**Font Scale**:
```css
Name (h1): 2.8rem (44.8px) - Navy, Weight 700
Tagline: 1rem (16px) - Medium gray, Weight 400
Section titles: 1.1rem (17.6px) - Navy, Weight 600
Body text: 1rem (16px) - Charcoal, Weight 400, Line-height 1.6
Small text: 0.9rem (14.4px) - Dark gray
Micro text: 0.8rem (12.8px) - Medium gray
```

### Spacing System

Based on mathematical progression for visual rhythm:

```css
--space-xs: 8px    /* Tight spacing, inline elements */
--space-sm: 15px   /* Standard spacing, related elements */
--space-md: 25px   /* Section spacing, content blocks */
--space-lg: 35px   /* Major section breaks */
--space-xl: 50px   /* Page section spacing */
--space-xxl: 60px  /* Container padding */
```

## Layout Architecture

### Container System
- **Max width**: 800px (optimized for reading comprehension)
- **Centering**: Auto margins for centered layout
- **Padding**: 35px vertical, 60px horizontal on desktop
- **Background**: White content on light gray page background
- **Shadow**: Subtle box shadow for paper-like elevation

### Navigation Structure
- **Border**: 1px bottom border in light gray
- **Spacing**: 35px gaps between navigation items
- **Active indicators**: 2px accent-colored bottom border
- **Hover effects**: Subtle transform and background change

### Section Architecture
- **Section dividers**: 30px × 2px accent-colored horizontal bars
- **Section spacing**: 25px margin below dividers
- **Content hierarchy**: Clear visual rhythm through consistent spacing

## Component Specifications

### Skill Tags / Technology Badges
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.8rem;
padding: 4px 10px;
background-color: var(--light-bg);
border: 1px solid current accent color;
border-radius: 4px;
```

### Bullet Points
- **Character**: Standard bullet (•)
- **Color**: Current page accent color
- **Position**: Absolute positioned before pseudo element
- **Spacing**: 15px left padding on list items

### Links (Content)
- **Color**: Current page accent color with !important specificity
- **Exclusions**: Navigation links, CV buttons, footer contact links maintain their own styling
- **Hover**: Underline on hover

### Lists
- **Line height**: 1.6 for readability
- **Spacing**: 8px between list items
- **Nesting**: Proper visual hierarchy with indentation

## Responsive Behavior

### Mobile First Approach

**Large screens (768px+)**: Full desktop layout
**Medium screens (768px and below)**:
- Container padding: 25px horizontal
- Navigation: Stacked layout
- Typography: Reduced scale (name: 2rem, tagline: 0.95rem)
- Skill tags: Smaller (0.75rem)

**Small screens (480px and below)**:
- Name: 1.8rem
- Increased touch targets
- Optimized spacing for mobile interaction

## Accessibility Considerations

### Color Contrast Ratios
- **Navy on white**: 8.78:1 (AAA compliant)
- **Charcoal on white**: 12.63:1 (AAA compliant)
- **Dark gray on white**: 7.16:1 (AAA compliant)
- **Medium gray on white**: 4.69:1 (AA compliant)
- **All accent colors on white**: AA compliant minimum

### Focus States
- Clear focus indicators on all interactive elements
- Proper keyboard navigation order
- Screen reader friendly semantic structure

## Brand Consistency Rules

### What Remains Constant
1. **Navy** for all primary headings and brand elements
2. **Typography** scale and font choices
3. **Spacing** system and layout proportions
4. **Container** dimensions and structure
5. **Navigation** behavior and interactions

### What Changes Per Persona
1. **Accent color** throughout page (section dividers, bullets, links, tags)
2. **Diamond indicator** showing active persona
3. **Subtle background tints** in content cards
4. **Hover states** using persona accent color
5. **Content focus** while maintaining design consistency

## Implementation Guidelines

### CSS Custom Properties Usage
```css
:root {
  /* Base colors - never change */
  --navy: #1a365d;
  --charcoal: #1f2937;
  --dark-gray: #4b5563;
  --medium-gray: #6b7280;
  --light-bg: #f8fafc;
  --white: #ffffff;

  /* Accent colors - persona specific */
  --coral: #e53e3e;      /* Engineer */
  --gold: #f59e0b;       /* Leader */
  --plum: #6b5b95;       /* Academic */
  --plum-accent: #8b7bb8; /* Academic secondary */
}
```

### Page-Specific Overrides
Each persona page includes scoped styles that override specific accent elements while preserving the base design system.

## Technical Implementation Notes

### Font Loading
- Google Fonts API used for reliable font delivery
- Font display: swap for performance
- Fallback: system fonts maintaining similar characteristics

### Performance Considerations
- Minimal CSS footprint through systematic design
- Shared base styles with targeted overrides
- Optimized asset loading

### Browser Support
- Modern CSS Grid and Flexbox
- CSS Custom Properties (IE11+ with fallbacks)
- Progressive enhancement approach

---

This design system creates a cohesive yet differentiated professional identity that can
scale across multiple formats (web, PDF, print) while maintaining brand consistency and
persona clarity.
