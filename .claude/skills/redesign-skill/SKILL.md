---
name: redesign-existing-projects
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality.
---

# Redesign Skill

## How This Works

When applied to an existing project, follow this sequence:

1. **Scan** — Read the codebase. Identify the framework, styling method, and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state you find.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.

## Design Audit

### Typography
- Browser default fonts or Inter → replace with `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
- Headlines lack presence → increase size, tighten letter-spacing, reduce line-height
- Body text too wide → limit to ~65ch, increase line-height
- Only Regular + Bold weights → introduce Medium (500) and SemiBold (600)
- Numbers in proportional font → use monospace or `font-variant-numeric: tabular-nums`
- All-caps subheaders → try lowercase italics or sentence case
- Orphaned words → fix with `text-wrap: balance` or `text-wrap: pretty`

### Color and Surfaces
- Pure `#000000` → replace with off-black (`#0a0a0a`, `#121212`)
- Oversaturated accents → keep saturation below 80%
- More than one accent color → pick one, remove the rest
- Mixing warm and cool grays → stick to one gray family
- Purple/blue "AI gradient" aesthetic → replace with neutral bases + single accent
- Generic `box-shadow` → tint shadows to match background hue
- Flat design with zero texture → add subtle noise, grain, or micro-patterns
- Empty flat sections → add background imagery, patterns, or ambient gradients (use `https://picsum.photos/seed/{name}/1920/1080`)
- Random dark section in light page (or vice versa) → commit to one mode throughout

### Layout
- Everything centered and symmetrical → break symmetry with offset margins
- Three equal card columns → replace with 2-column zig-zag, asymmetric grid, or horizontal scroll
- `height: 100vh` → replace with `min-height: 100dvh`
- Complex flexbox percentage math → use CSS Grid
- No max-width container → add ~1200-1440px constraint with auto margins
- No overlap or depth → use negative margins to create layering
- Missing whitespace → double the spacing on marketing pages
- Buttons not bottom-aligned in card groups → pin to bottom with flexbox column layout
- Inconsistent vertical rhythm in side-by-side elements → align shared elements across all items

### Interactivity and States
- No hover states on buttons → add background shift, slight scale, or translate
- No active/pressed feedback → add `scale(0.98)` or `translateY(1px)` on press
- Instant transitions → add 200-300ms smooth transitions
- Missing focus ring → required for keyboard navigation accessibility
- No loading states → skeleton loaders matching layout shape
- No empty states → design a composed "getting started" view
- No error states → clear inline error messages
- Animations using `top`, `left`, `width`, `height` → switch to `transform` and `opacity`

### Content
- Generic names (John Doe, Jane Smith) → diverse, realistic-sounding names
- Fake round numbers (99.99%, $100.00) → organic messy data (47.2%, $99.00)
- Placeholder company names (Acme, Nexus) → contextual, believable brand names
- AI copywriting clichés (Elevate, Seamless, Unleash, Next-Gen, Delve) → plain specific language
- Exclamation marks in success messages → remove, be confident not loud
- Lorem Ipsum → never, write real draft copy
- Title Case On Every Header → use sentence case

### Component Patterns
- Generic card look (border + shadow + white bg) → remove border, or use only bg color, or only spacing
- Pill-shaped "New" badges → try square badges or plain text labels
- 3-card carousel testimonials with dots → masonry wall, embedded social posts, or single rotating quote
- Modals for simple actions → inline editing, slide-over panels, or expandable sections
- Footer link farm with 4 columns → simplify, focus on main paths

### Iconography
- Lucide or Feather exclusively → use Phosphor, Heroicons, or custom set
- Inconsistent stroke widths → standardize to one stroke weight
- Missing favicon → always include branded favicon

### Code Quality
- Div soup → use semantic HTML (`nav`, `main`, `article`, `aside`, `section`)
- Inline styles mixed with CSS classes → move all styling to the project's styling system
- Arbitrary z-index values (9999) → establish a clean z-index scale
- Commented-out dead code → remove all debug artifacts
- Missing alt text on images → describe image content for screen readers

### Strategic Omissions
- No legal links → add privacy policy and terms in footer
- No custom 404 page → design a helpful branded experience
- No form validation → add client-side validation
- No "skip to content" link → essential for keyboard users

## Fix Priority

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliché patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Rules

- Work with the existing tech stack. Do not migrate frameworks or styling libraries.
- Do not break existing functionality. Test after every change.
- Before importing any new library, check the project's dependency file first.
- If the project uses Tailwind, check the version (v3 vs v4) before modifying config.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
