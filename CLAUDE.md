# CLAUDE.md — Jovan Naturals

Jovan Naturals is a mobile-first Django e-commerce website for natural
coconut oil products from Kerala. Built with Django Templates and
Tailwind CSS. No React, no heavy JS frameworks.

## Design Reference

Live prototype: https://jolly-gecko-a2c0a1.netlify.app/
Match this design closely for all pages. When in doubt, refer to the
prototype before making any UI decisions.

## Tech Stack

- **Backend:** Django 5.x, Python 3.13
- **Database:** SQLite (dev) → PostgreSQL (production)
- **Frontend:** Django Templates + Tailwind CSS via CDN
- **JS:** Vanilla JS only (carousel, cart badge, qty controls)
- **Payments:** Razorpay (future spec)
- **Shipping:** Shiprocket manual integration (future spec)
- **Fonts:** Playfair Display (headings), DM Sans (body) via Google Fonts

## Project Structure

```
jovan_naturals/
├── jovan_naturals/        # Project config
│   ├── settings.py
│   ├── urls.py            # Includes store.urls
│   ├── wsgi.py
│   └── asgi.py
├── store/                 # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/          # Business logic (payment, shipping etc.)
│   ├── templates/store/   # App templates
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_services.py
│   └── migrations/
├── templates/
│   └── base.html          # Project-level base template
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/                 # User uploads
├── .env                   # SECRET_KEY, DB credentials (never commit)
└── requirements.txt
```

## Design System

Tailwind config is defined in `templates/base.html` before the CDN
script. Use these token names in all templates — never hardcode hex
values.

### Colour Tokens

| Token           | Hex       | Usage                        |
| --------------- | --------- | ---------------------------- |
| `primary`       | `#1a5c3a` | Buttons, active nav, CTAs    |
| `primary-light` | `#e8f5ee` | Card backgrounds, highlights |
| `primary-mid`   | `#d4ecd9` | Image backgrounds            |
| `accent`        | `#FFD166` | Best seller badge, hero CTA  |
| `surface`       | `#f5f7f6` | Section backgrounds          |
| `danger`        | `#c0392b` | Error states, failure pages  |
| `danger-light`  | `#fdecea` | Error card backgrounds       |

### Typography

- `font-serif` → Playfair Display — headings, brand name, product titles
- `font-sans` → DM Sans — body, labels, buttons, nav

### Layout Rules

- Max content width: `max-w-mobile` (480px), centred with `mx-auto`
- Horizontal padding: `px-4` (16px) throughout
- Product grid: `grid grid-cols-2 gap-3`
- Topbar: `sticky top-0 z-50`
- Bottom nav: `fixed bottom-0` — width matches content container
- Border radius: `rounded-lg` (cards), `rounded-full` (pills/badges)
- Borders: `border border-gray-200` (0.5px equivalent)

## URL Structure

```
/                    → store:product_list
/product/<slug>/     → store:product_detail
/cart/               → store:cart
/checkout/           → store:checkout
/order/success/      → store:order_success
/order/failure/      → store:order_failure
/orders/             → store:order_history
/about/              → store:about
/admin/              → Django admin
```

## Engineering Standards

- Separate business logic from views — use `store/services/` for
  payment and shipping logic
- Keep views thin — views call services, services do the work
- Keep functions small and single-purpose
- Follow SOLID principles
- Use meaningful variable and function names
- Never put secrets or credentials in code — use `.env`

## Template Conventions

Always extend `base.html`:

```django
{% extends 'base.html' %}
{% block content %}
<!-- content here -->
{% endblock %}
```

- Use `{% url 'store:view_name' %}` — never hardcode URLs
- Use `{% static 'path/file' %}` after `{% load static %}`
- App templates live in `store/templates/store/`
- Project templates live in `templates/`

## Testing Convention

IMPORTANT: Never use the auto-generated `tests.py` file. Always use
the `tests/` package structure.

Every app follows this structure:

```
appname/
  tests/
    __init__.py
    test_models.py      ← created in the same spec as models.py
    test_views.py       ← created in the same spec as views.py
    test_services.py    ← created only if services.py exists
```

```bash
python manage.py test           # all tests
python manage.py test store     # single app
python manage.py test --verbosity=2
```

## Adding New Apps

When creating any new Django app:

1. `python manage.py startapp appname`
2. Delete the auto-generated `tests.py`
3. Create `tests/__init__.py` immediately
4. Add to `INSTALLED_APPS` in `settings.py`
5. Create `appname/urls.py` and wire into project `urls.py`
6. Follow the same tests/ structure above

## Common Commands

```bash
python manage.py runserver        # dev server
python manage.py test store       # run store app tests
python manage.py shell            # Django shell for debugging
```

## Git Commit Convention

Use conventional commits format:

```
feat: add product detail page
fix: correct cart quantity update logic
style: align product card heights in grid
test: add unit tests for Product model
refactor: move payment logic to services layer
chore: update requirements.txt
```

## Constraints

- NO React, NO Vue, NO heavy JS frameworks
- NO inline styles — use Tailwind classes only
- NO hardcoded URLs — always use `{% url %}` tag
- NO business logic in views — use services/
- NO secrets in code — use `.env`
- Keep JS minimal — only for carousel, cart badge, qty controls

## Service Layer Architecture

All third-party integrations use the Strategy pattern via an abstract
base class. This is the same pattern Django uses internally for email
backends, cache backends, and storage backends.

### Structure

```
store/services/
├── payment/
│   ├── __init__.py      # get_payment_service() factory
│   ├── base.py          # Abstract PaymentService (ABC)
│   └── razorpay.py      # RazorpayBackend(PaymentService)
└── shipping/
    ├── __init__.py      # get_shipping_service() factory
    ├── base.py          # Abstract ShippingService (ABC)
    └── shiprocket.py    # ShiprocketBackend(ShippingService)
```

### Pattern to follow for every integration

**base.py** — defines the interface, no implementation:

```python
from abc import ABC, abstractmethod

class PaymentService(ABC):
    @abstractmethod
    def create_order(self, amount: int, currency: str) -> dict:
        pass

    @abstractmethod
    def verify_payment(self, payment_data: dict) -> bool:
        pass
```

**razorpay.py** — concrete implementation:

```python
from .base import PaymentService

class RazorpayBackend(PaymentService):
    def create_order(self, amount: int, currency: str) -> dict:
        # Razorpay-specific implementation
        pass

    def verify_payment(self, payment_data: dict) -> bool:
        # Razorpay-specific verification
        pass
```

`__init__.py` — settings-driven factory:

```python
from django.conf import settings
from django.utils.module_loading import import_string

def get_payment_service():
    backend_class = import_string(settings.PAYMENT_BACKEND)
    return backend_class()
```

**settings.py** — one line to swap providers:

```python
PAYMENT_BACKEND = 'store.services.payment.razorpay.RazorpayBackend'
SHIPPING_BACKEND = 'store.services.shipping.shiprocket.ShiprocketBackend'
```

**views.py** — never imports Razorpay or Shiprocket directly:

```python
from store.services.payment import get_payment_service

def checkout(request):
    payment = get_payment_service()
    order = payment.create_order(amount=849, currency='INR')
```

### Rules

- NEVER import `razorpay` or `shiprocket` directly in views
- NEVER hardcode provider names anywhere except `settings.py`
- Adding a new provider = new file only, zero changes to existing code
- Every new third-party integration follows this same pattern

## Python Conventions (PEP 8)

- snake_case for variables, functions, methods, modules
- PascalCase for classes
- UPPER_SNAKE_CASE for constants
- Prefix private methods/attributes with single underscore `_method`
- Max line length: 88 characters (Black formatter standard)
- Two blank lines between top-level functions/classes
- One blank line between methods inside a class
- Docstrings on all public functions, classes, and modules

## Naming Conventions

### Python

- Models: singular noun — `Product`, `Order`, `CartItem`
- Views: action + noun — `product_list`, `product_detail`, `cart_add`
- URLs: kebab-case — `product-detail`, `order-history`
- URL names: snake_case — `store:product_detail`, `store:order_history`
- Services: noun + Service — `PaymentService`, `ShippingService`
- Templates: match URL name — `product_detail.html`, `order_history.html`

### Templates

- Block names: snake_case — `{% block page_title %}`
- Template variables: snake_case — `{{ product_list }}`, `{{ cart_total }}`
- CSS classes: Tailwind utilities only — no custom class names unless
  absolutely necessary
