# taste-skill — PlotLot Design System Rules

## Dial Settings (Real Estate Dashboard Context)

```
DESIGN_VARIANCE: 6        # Meaningful variety — asymmetric layouts OK, not chaotic
MOTION_INTENSITY: 5       # Professional, data-focused — no Disney bounce
VISUAL_DENSITY: 7         # Information-rich — dense tables/grids are intentional
```

## Core Principle

PlotLot is a **cinematic, data-rich** real estate intelligence tool. Premium but functional.
Motion serves data. Every animation communicates state, not decoration.

---

## Spring Physics (Always)

**Never** use CSS `transition-all duration-X` for interactive or reveal animations.
Use framer-motion with spring physics from `@/lib/motion`.

```ts
import { spring, springGentle, fadeUp, stagger, cardHover } from "@/lib/motion"

// Card hover — professional lift, no bounce
<motion.div whileHover={{ y: -2, transition: spring }} whileTap={{ scale: 0.98 }}>

// Metric reveal — staggered entrance
<motion.div {...fadeUp} transition={{ ...springGentle, delay: i * 0.05 }}>

// Bar animation — spring expand from left
<motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ type: "spring", stiffness: 120, damping: 20 }}>
```

---

## Stagger Orchestration

Use `staggerChildren` for sibling element entrances. Never animate all at once.

```tsx
const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.07 } },
}
const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 25 } },
}

<motion.div variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item, i) => (
    <motion.div key={i} variants={itemVariants}>
      <MetricBox {...item} />
    </motion.div>
  ))}
</motion.div>
```

---

## AnimatePresence — Required for Conditional Renders

Wrap any conditionally-rendered element in `<AnimatePresence>` so exit animations fire.

```tsx
<AnimatePresence mode="wait">
  {isLoading ? (
    <motion.div key="loading" {...fadeUp} transition={springGentle}>
      <SkeletonShimmer />
    </motion.div>
  ) : (
    <motion.div key="content" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

---

## Loading States — Shimmer Skeletons

Use the `.animate-shimmer` CSS class (defined in globals.css) for loading placeholders.
Shimmer communicates "AI is generating" — do not use spinning indicators for image gen.

```tsx
// Image loading skeleton
<div className="aspect-[16/9] w-full rounded-xl animate-shimmer" />

// Metric box skeleton
<div className="h-12 w-full rounded-xl animate-shimmer" />
```

---

## Hover Physics — Cards and Buttons

```tsx
// Standard card hover — lift and border brighten
whileHover={{ y: -2 }}
whileTap={{ scale: 0.97 }}
transition={spring}  // stiffness: 400, damping: 30

// Subtle button hover — no translate, just scale
whileHover={{ scale: 1.01 }}
whileTap={{ scale: 0.98 }}
```

Remove Tailwind `hover:-translate-y-0.5` when using framer-motion hover — they conflict.

---

## Typography Entrances

Display headings (font-display, text-4xl+) enter from y:24 with springGentle.
Body copy and labels enter from y:12 with spring.

```tsx
<motion.h1
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={springGentle}
  className="font-display text-4xl"
>
```

---

## Progress Bars

Replace CSS `transition-all duration-500` with framer-motion spring:

```tsx
<motion.div
  className="h-full rounded-full bg-amber-500"
  animate={{ width: `${pct}%` }}
  transition={{ type: "spring", stiffness: 60, damping: 15 }}
/>
```

---

## Anti-Patterns to Avoid

- ❌ `animate-bounce` — too playful, this is financial software
- ❌ `transition-all duration-700` on interactive elements — use spring instead
- ❌ Animating every element on the page simultaneously — always stagger
- ❌ Scale > 1.05 on hover — subtle is professional
- ❌ `framer-motion` in Server Components — always check for `"use client"`
- ❌ `motion.div` wrapping layout containers — wrap leaf nodes or groups only

---

## PlotLot-Specific Motion Context

| Component | Motion Pattern |
|-----------|---------------|
| DensityBreakdown bars | Spring expand from 0 → `pct%`, governing bar first |
| DealHeroCard metrics | staggerChildren 0.05s, fadeUp from y:12 |
| ToolCards | whileHover y:-2, whileTap scale:0.97, spring transition |
| AnalysisStream progress | Spring bar, AnimatePresence on narrative messages |
| Welcome heading | springGentle from y:24 |
| DevelopmentConceptCard | AnimatePresence between states: CTA → skeleton → image |
| PropertyFlyoverVideo | AnimatePresence: CTA → progress → video |

---

## Accent Color

Brand amber: `#b45309` light / `#f59e0b` dark. Use for governing constraints, CTAs, icons.
Stone/neutral palette for non-governing elements.
One accent only — no rainbow.
