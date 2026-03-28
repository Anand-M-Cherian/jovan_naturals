# Plan: Product Listing Page (Static)

## Context

The product listing page is the store homepage. Currently `product_list.html` is empty and `base.html` has placeholder stubs for header and footer. This task builds the full page UI — hero carousel, product grid, sticky topbar, and fixed bottom nav — using hardcoded placeholder content with no database. The goal is to establish the visual structure and component hierarchy so future iterations can swap in real data.

Branch: `claude/feature/product-listing-page`
Spec: `specs/product-listing-page.md`

---

## Files to Modify / Create

| #   | File                                      | Action                                                                           |
| --- | ----------------------------------------- | -------------------------------------------------------------------------------- |
| 1   | `store/urls.py`                           | Add `app_name = 'store'`                                                         |
| 2   | `templates/base.html`                     | Replace header/footer stubs with topbar, announce bar, bottom nav, scripts block |
| 3   | `store/views.py`                          | Add module + function docstrings (no logic change)                               |
| 4   | `store/templates/store/product_list.html` | Implement carousel + product grid                                                |
| 5   | `store/tests/test_views.py`               | Create with 5 view tests                                                         |

---

## Step-by-Step Implementation

### 1. `store/urls.py`

Add `app_name = 'store'` before `urlpatterns`. This enables `{% url 'store:product_list' %}` syntax in all templates, consistent with CLAUDE.md conventions.

### 2. `templates/base.html`

Replace the `<header>` and `<footer>` stubs. Structure from top to bottom:

**a. Announce bar** (inside `<header>`)

- Full-width strip: `bg-primary text-white text-center text-xs py-1.5 font-sans`
- Static text: "Free shipping on orders over ₹499"

**b. Sticky topbar** (inside `<header>`, below announce bar)

- Container: `sticky top-0 z-50 bg-white border-b border-gray-200`
- Inner: `max-w-mobile mx-auto px-4 flex items-center justify-between h-14`
- Left: circular logo placeholder `w-10 h-10 rounded-full bg-primary-mid flex-shrink-0` — reserves space for the real logo image. Wrap with brand name `font-serif text-primary text-lg ml-2` in a `flex items-center`.
- Right: cart icon with `bg-accent` badge showing "0"

**c. `<main>` content wrapper**

- `<main class="max-w-mobile mx-auto pb-20">` — `pb-20` prevents content from hiding behind the fixed bottom nav

**d. Fixed bottom nav** (replacing `<footer>`)

- `fixed bottom-0 inset-x-0 z-50` outer, `max-w-mobile mx-auto bg-white border-t border-gray-200 flex items-center justify-around h-16` inner
- Add `data-nav="bottom"` for test targeting
- Four items: Home, About, Cart, Orders — all as `<a>` tags
- Home: `{% url 'store:product_list' %}` — active state with `text-primary`
- About, Cart, Orders: use `{% url 'store:product_list' %}` temporarily (routes don't exist yet) with a `{# TODO #}` comment — avoids `NoReverseMatch`
- Inactive items: `text-gray-500`

**e. Scripts block** — `{% block scripts %}{% endblock %}` just before `</body>`

### 3. `store/views.py`

Add module docstring and function docstring per CLAUDE.md Python
conventions. Pass `active_nav='home'` in the render context:

    return render(request, 'store/product_list.html', {
        'active_nav': 'home',
    })

### 4. `store/templates/store/product_list.html`

Extends `base.html`. Fills `{% block content %}` and `{% block scripts %}`.

**a. Hero carousel** — `{% block content %}` opens with:

- Outer: `relative overflow-hidden` + `data-carousel`
- Slide track: `flex transition-transform duration-500` + `data-carousel-track`
- 2 slides, each `min-w-full`: placehold.co image (`w-full h-48 object-cover`) + optional headline overlay
- Prev button: `data-carousel-prev`, `absolute left-2 top-1/2 -translate-y-1/2 bg-white/70 text-primary rounded-full p-1`
- Next button: same with `data-carousel-next` on the right

**b. Section heading**
`font-serif text-xl text-primary px-4 mt-6 mb-3` — "Our Products"

**c. Product grid**

- Container: `grid grid-cols-2 gap-3 px-4`
- 4 hardcoded cards, each with `data-product-card` on the outermost element only
- Card: `bg-white rounded-lg border border-gray-200 overflow-hidden relative`
- Image: placehold.co with `w-full aspect-square object-cover bg-primary-mid`
- One card gets "Best Seller" badge: `absolute top-2 left-2 bg-accent text-primary text-xs rounded-full px-2 py-0.5`
- Card body `p-3`: name (`font-serif text-sm`), description (`font-sans text-xs text-gray-500 line-clamp-2`), price (`font-sans text-sm font-medium text-primary mt-1`), Add to Cart button (`w-full mt-2 bg-primary text-white text-xs py-2 rounded-lg`, `type="button"`, non-functional)

**d. Carousel JS** — in `{% block scripts %}`:

- Inline `<script>`, wrapped in `DOMContentLoaded`
- Query elements by `data-carousel`, `data-carousel-track`, `data-carousel-prev`, `data-carousel-next`
- `currentIndex = 0`, `SLIDE_COUNT = 2`
- `goToSlide(index)`: sets `track.style.transform = \`translateX(-${index \* 100}%)\``— must use`style.transform` directly (Tailwind cannot generate dynamic translate values from JS)
- `next()`: `currentIndex = (currentIndex + 1) % SLIDE_COUNT` → `goToSlide`
- `prev()`: `currentIndex = (currentIndex - 1 + SLIDE_COUNT) % SLIDE_COUNT` → `goToSlide`
- Attach click listeners to prev/next buttons
- `setInterval(next, 3000)` — no pause on interaction per spec

### 5. `store/tests/test_views.py` (new file)

Class `ProductListViewTests(TestCase)`, uses `self.client.get('/')`:

1. `test_product_list_returns_200` — `status_code == 200`
2. `test_product_list_uses_correct_template` — `assertTemplateUsed(response, 'store/product_list.html')`
3. `test_page_contains_hero_carousel` — `assertContains(response, 'data-carousel')`
4. `test_page_contains_four_product_cards` — `response.content.count(b'data-product-card') == 4`
5. `test_page_contains_bottom_nav` — `assertContains(response, 'data-nav="bottom"')`

---

## Key Gotchas

- `data-product-card` must appear **exactly once per card** — only on the outermost card `<div>`, not on inner elements. The count assertion will break otherwise.
- `{% load static %}` is not needed for this iteration (all images are placehold.co URLs), but add it if any `{% static %}` tags are used.
- `pb-20` on `<main>` is critical — without it, the bottom two product cards hide behind the fixed nav.

---

## Verification

```bash
# Run the dev server and open http://localhost:8000/
python manage.py runserver

# Run the view tests
python manage.py test store.tests.test_views --verbosity=2
```

Visually confirm:

- [ ] Topbar sticks on scroll
- [ ] Carousel auto-advances every 3s and loops
- [ ] Prev/Next buttons work
- [ ] 4 cards in 2-column grid
- [ ] Bottom nav stays fixed and does not overlap content
- [ ] "Best Seller" badge visible on one card
