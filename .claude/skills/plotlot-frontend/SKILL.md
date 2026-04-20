---
name: plotlot-frontend
description: PlotLot React components, SSE events, Tailwind conventions
user-invocable: false
---

# PlotLot Frontend

## Stack
- Next.js 16 + App Router (`src/app/`)
- React 19 (server components + client components)
- Tailwind CSS 4 (no CSS modules, no styled-components)
- TypeScript strict mode

## Key Components (16)
| Component | Purpose |
|-----------|---------|
| AnalysisStream | Main SSE streaming UI, progressive disclosure |
| ZoningReport | Full report card with collapsible sections |
| DensityBreakdown | 4-constraint visual breakdown |
| ArcGISParcelMap | Leaflet + esri-leaflet interactive map |
| ParcelViewer | Street View + Parcel Map tabs |
| SatelliteMap | Google Maps satellite view |
| EnvelopeViewer | 3D buildable envelope (Three.js) |
| FloorPlanViewer | Generated floor plan display |
| PropertyCard | Property summary with metrics |
| AddressAutocomplete | Google Places autocomplete input |
| QuickLookup | Streamlined address -> results (no chat) |
| ErrorBoundary | React error boundary with Sentry |

## SSE Event Types
`geocode`, `property`, `zoning`, `analysis`, `calculator`, `comps`, `proforma`, `contract`, `heartbeat`, `error`, `done`

## API Client (`src/lib/api.ts`)
- All backend calls through centralized client
- SSE streaming via EventSource pattern
- Backend URL from `NEXT_PUBLIC_API_URL`

## Tailwind Conventions
- Mobile-first: `sm:`, `md:`, `lg:` breakpoints
- Dark mode: `dark:` variant
- Cards: `rounded-xl border bg-white shadow-sm dark:bg-gray-900`
- Consistent spacing scale: `p-4`, `gap-6`, `mt-8`
