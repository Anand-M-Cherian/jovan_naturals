# Spec for Product Listing Page

branch: claude/feature/product-listing-page
figma_component (if used): n/a

## Summary

Build the main product listing page as the homepage of the e-commerce store. The page will display a hero carousel showcasing featured products, followed by a 2-column grid of product cards with static placeholder content. Navigation includes a sticky top bar and fixed bottom navigation. All content is hardcoded (no database queries) to establish the UI structure and visual hierarchy.

## Functional Requirements

- **Hero Carousel**
    - Displays 2 static slides
    - Auto-rotates on a timer (e.g., 3-second interval)
    - Previous/Next navigation buttons
    - Responsive images that scale with viewport

- **Product Grid**
    - Display exactly 4 product cards in a 2-column grid layout
    - Grid uses `grid grid-cols-2 gap-3` (per design system)
    - Each card includes:
        - Product image (placeholder or static image)
        - Product name
        - Price
        - Brief description (1-2 lines max)
        - "Add to Cart" button (non-functional for now)
        - Optional badge (e.g., "Best Seller")

- **Sticky Top Bar**
    - Fixed at top with `sticky top-0 z-50`
    - Contains: logo/brand name, search placeholder, cart badge
    - Remains visible while scrolling
    - Uses primary color (`#1a5c3a`)

- **Fixed Bottom Navigation**
    - Fixed at bottom of viewport with `fixed bottom-0`
    - Width matches content container (max-w-mobile, 480px, centred)
    - Navigation items: Home, About, Cart, Orders
    - Home is active/highlighted on this page
    - Uses primary color for active state

- **Layout**
    - Mobile-first design, max content width 480px (`max-w-mobile`)
    - Horizontal padding: `px-4` (16px) throughout
    - Proper spacing between hero, grid, and footer sections
    - Safe area below for fixed bottom nav (add padding-bottom to body)

## Figma Design Reference (only if referenced)

- File: Live prototype at https://jolly-gecko-a2c0a1.netlify.app/
- Key visual constraints:
    - Playfair Display (serif) for headings
    - DM Sans (sans-serif) for body text
    - Primary color: `#1a5c3a`
    - Accent color: `#FFD166` (for badges, highlights)
    - Surface background: `#f5f7f6`

## Possible Edge Cases

- Carousel with only 1-2 images (should still be functional)
- Product cards with very long names or prices
- Different image aspect ratios (should maintain consistent card height)
- Small viewport widths near/below 480px
- Screen readers and keyboard navigation for carousel controls

## Acceptance Criteria

- [ ] Hero carousel displays, auto-rotates, and responds to next/previous buttons
- [ ] Product grid shows 4 cards in 2-column layout, responsive and properly spaced
- [ ] Sticky top bar remains visible while scrolling, matches design tokens
- [ ] Fixed bottom nav is properly positioned and does not overlap content
- [ ] All text is placeholder but matches the design system typography
- [ ] Page renders properly on mobile viewports (320px–480px)
- [ ] No console errors or warnings
- [ ] Uses only Tailwind utilities (no custom CSS classes)
- [ ] Extends `base.html` and uses proper template structure
- [ ] All hardcoded content is in the template (no database calls)

## Open Questions

- Should the carousel loop infinitely or stop at the end? Carousel loops infinitely, no pause on interaction
- What should happen if carousel timer is paused (e.g., on user interaction)? Carousel loops infinitely, no pause on interaction
- Should product cards link to detail pages, or are they static for now? Product cards are static, no links to detail pages
- Should the bottom nav be part of this template or a shared component in `base.html`? Announce bar, topbar, and bottom nav live in base.html

## Testing Guidelines

Add the following test to store/tests/test_views.py:

- GET / returns HTTP 200
- Response uses template store/product_list.html
- Template renders without errors and contains expected elements (hero, grid, nav)
- All 4 product cards are present in the template
- Sticky top bar and bottom nav are properly styled/classed
- Carousel markup is valid and JavaScript-ready (e.g., data attributes for JS)
- Mobile breakpoints work correctly with 2-column grid

## Files to Create / Modify

- `templates/base.html` — announce bar, topbar, bottom nav
- `store/views.py` — product_list view
- `store/urls.py` — wire / route
- `store/templates/store/product_list.html` — carousel and product grid
- `store/tests/test_views.py` — view tests
