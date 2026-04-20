---
name: design-taste-frontend
description: Senior UI/UX Engineer skill. Architect digital interfaces overriding default LLM biases. Enforces metric-based rules, strict component architecture, CSS hardware acceleration, and balanced design engineering.
---

# High-Agency Frontend Skill

## 1. ACTIVE BASELINE CONFIGURATION
* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* VISUAL_DENSITY: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

**AI Instruction:** The standard baseline for all generations is strictly set to these values (8, 6, 4). Do not ask the user to edit this file. Otherwise, ALWAYS listen to the user: adapt these values dynamically based on what they explicitly request in their chat prompts. Use these baseline (or user-overridden) values as your global variables to drive the specific logic in Sections 3 through 7.

## 2. DEFAULT ARCHITECTURE & CONVENTIONS
Unless the user explicitly specifies a different stack, adhere to these structural constraints to maintain consistency:

* **DEPENDENCY VERIFICATION [MANDATORY]:** Before importing ANY 3rd party library (e.g. `framer-motion`, `lucide-react`, `zustand`), you MUST check `package.json`. If the package is missing, you MUST output the installation command (e.g. `npm install package-name`) before providing the code. **Never** assume a library exists.
* **Framework & Interactivity:** React or Next.js. Default to Server Components (`RSC`).
    * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
    * **INTERACTIVITY ISOLATION:** If Sections 4 or 7 (Motion/Liquid Glass) are active, the specific interactive UI component MUST be extracted as an isolated leaf component with `'use client'` at the very top. Server Components must exclusively render static layouts.
* **State Management:** Use local `useState`/`useReducer` for isolated UI. Use global state strictly for deep prop-drilling avoidance.
* **Styling Policy:** Use Tailwind CSS (v3/v4) for 90% of styling.
    * **TAILWIND VERSION LOCK:** Check `package.json` first. Do not use v4 syntax in v3 projects.
    * **T4 CONFIG GUARD:** For v4, do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **ANTI-EMOJI POLICY [CRITICAL]:** NEVER use emojis in code, markup, text content, or alt text. Replace symbols with high-quality icons (Radix, Phosphor) or clean SVG primitives. Emojis are BANNED.
* **Responsiveness & Spacing:**
  * Standardize breakpoints (`sm`, `md`, `lg`, `xl`).
  * Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
  * **Viewport Stability [CRITICAL]:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent catastrophic layout jumping on mobile browsers (iOS Safari).
  * **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for reliable structures.
* **Icons:** You MUST use exactly `@phosphor-icons/react` or `@radix-ui/react-icons` as the import paths (check installed version). Standardize `strokeWidth` globally (e.g., exclusively use `1.5` or `2.0`).

## 3. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

**Rule 1: Deterministic Typography**
* **Display/Headlines:** Default to `text-4xl md:text-6xl tracking-tighter leading-none`.
    * **ANTI-SLOP:** Discourage `Inter` for "Premium" or "Creative" vibes. Force unique character using `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
    * **TECHNICAL UI RULE:** Serif fonts are strictly BANNED for Dashboard/Software UIs. Use exclusively high-end Sans-Serif pairings (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`).
* **Body/Paragraphs:** Default to `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

**Rule 2: Color Calibration**
* **Constraint:** Max 1 Accent Color. Saturation < 80%.
* **THE LILA BAN:** The "AI Purple/Blue" aesthetic is strictly BANNED. Use absolute neutral bases (Zinc/Slate) with high-contrast, singular accents.
* **COLOR CONSISTENCY:** Stick to one palette for the entire output.

**Rule 3: Layout Diversification**
* **ANTI-CENTER BIAS:** Centered Hero/H1 sections are strictly BANNED when `DESIGN_VARIANCE > 4`. Force "Split Screen", "Left Aligned content/Right Aligned asset", or "Asymmetric White-space" structures.

**Rule 4: Anti-Card Overuse**
* **DASHBOARD HARDENING:** For `VISUAL_DENSITY > 7`, generic card containers are strictly BANNED. Use `border-t`, `divide-y`, or purely negative space.
* Use cards ONLY when elevation communicates hierarchy.

**Rule 5: Interactive UI States**
* **Loading:** Skeletal loaders matching layout sizes (avoid generic circular spinners).
* **Empty States:** Beautifully composed empty states.
* **Error States:** Clear, inline error reporting.
* **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]`.

## 4. CREATIVE PROACTIVITY (Anti-Slop)
* **"Liquid Glass" Refraction:** Beyond `backdrop-blur` — add `border-white/10` inner border + `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`.
* **Magnetic Micro-physics (MOTION_INTENSITY > 5):** Use EXCLUSIVELY Framer Motion's `useMotionValue` and `useTransform` — NEVER `useState` for hover animations.
* **Perpetual Micro-Interactions:** When `MOTION_INTENSITY > 5`, use Spring Physics (`type: "spring", stiffness: 100, damping: 20`) on all interactive elements.
* **Layout Transitions:** Always use Framer Motion's `layout` and `layoutId` props.
* **Staggered Orchestration:** Use `staggerChildren` — Parent and Children MUST be in the same Client Component tree.

## 5. PERFORMANCE GUARDRAILS
* **Hardware Acceleration:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`.
* **DOM Cost:** Apply grain/noise filters exclusively to fixed, `pointer-events-none` pseudo-elements.
* **Z-Index Restraint:** NEVER spam arbitrary z-index values.

## 6. DIAL DEFINITIONS

### DESIGN_VARIANCE
* **1-3:** Strict symmetrical grids, `justify-center`.
* **4-7:** Offset margins, varied aspect ratios, left-aligned headers.
* **8-10:** Masonry, fractional CSS Grid, massive empty zones. MOBILE OVERRIDE: always collapse to single column `< 768px`.

### MOTION_INTENSITY
* **1-3:** CSS `:hover` and `:active` only.
* **4-7:** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Transform + opacity only.
* **8-10:** Framer Motion hooks. NEVER `window.addEventListener('scroll')`.

### VISUAL_DENSITY
* **1-3:** Lots of white space, huge section gaps.
* **4-7:** Normal spacing for standard web apps.
* **8-10:** Tiny paddings, 1px dividers, `font-mono` for all numbers.

## 7. AI TELLS — FORBIDDEN PATTERNS

### Visual
* NO Neon/Outer Glows — use inner borders or subtle tinted shadows
* NO Pure Black (`#000000`) — use Off-Black or Zinc-950
* NO Oversaturated Accents
* NO Excessive Gradient Text on large headers
* NO Custom Mouse Cursors

### Typography
* NO Inter Font — use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
* NO Serif fonts on clean Dashboards

### Layout
* NO 3-Column Card Layouts — use 2-column Zig-Zag, asymmetric grid, or horizontal scrolling

### Content
* NO Generic Names (John Doe, Jane Smith) — use creative, realistic names
* NO Fake Round Numbers (99.99%, 50%) — use organic data (47.2%, +1 (312) 847-1928)
* NO Startup Slop Names (Acme, Nexus, SmartFlow)
* NO Filler Words (Elevate, Seamless, Unleash, Next-Gen)
* NO Broken Unsplash Links — use `https://picsum.photos/seed/{random}/800/600`

### Components
* shadcn/ui MUST be customized — never generic default state

## 8. CREATIVE ARSENAL

### Navigation
* Mac OS Dock Magnification, Magnetic Button, Dynamic Island, Floating Speed Dial

### Layouts
* Bento Grid, Masonry, Chroma Grid, Split Screen Scroll, Curtain Reveal

### Cards
* Parallax Tilt Card, Spotlight Border Card, Glassmorphism Panel, Morphing Modal

### Scroll
* Sticky Scroll Stack, Horizontal Scroll Hijack, Zoom Parallax, Scroll Progress Path

### Typography
* Kinetic Marquee, Text Mask Reveal, Text Scramble Effect, Gradient Stroke Animation

### Micro-Interactions
* Skeleton Shimmer, Directional Hover Aware Button, Ripple Click Effect, Mesh Gradient Background

## 9. BENTO 2.0 PARADIGM
* **Palette:** Background `#f9fafb`. Cards `#ffffff` with `border-slate-200/50`.
* **Surfaces:** `rounded-[2.5rem]`, diffusion shadow `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`.
* **Typography:** `Geist`, `Satoshi`, or `Cabinet Grotesk` with `tracking-tight`.
* **Spring Physics:** `type: "spring", stiffness: 100, damping: 20` — no linear easing.
* **Infinite Loops:** Every card has an Active State (Pulse, Typewriter, Float, or Carousel).
* **Performance:** Perpetual motion MUST be `React.memo` isolated in its own Client Component.

## 10. FINAL PRE-FLIGHT CHECK
- [ ] Mobile layout collapse guaranteed for high-variance designs?
- [ ] Full-height sections use `min-h-[100dvh]` not `h-screen`?
- [ ] `useEffect` animations have cleanup functions?
- [ ] Empty, loading, and error states provided?
- [ ] CPU-heavy perpetual animations isolated in their own Client Components?
- [ ] No banned patterns from Section 7?
