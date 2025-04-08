# 🗄️ Storage

**Storage** is a Django-based inventory management system designed for retail and warehouse shops. It supports barcode generation, batch-level tracking, nutrition facts, pricing variations, location-aware storage, and label printing.

---

## 🚀 Features

- 📦 Product & Batch Management
- 🏷️ Barcode Generation & Label Printing
- 🧾 Per-batch Expiration Dates, Prices, and Sizes
- 🍽️ Nutrition Facts (Per Serving & Whole)
- 📊 Inventory Tracking (Incoming / Outgoing)
- 💸 Discounts and Accumulated Pricing
- 🌍 Hierarchical Location Finder System
- 📷 Product Image Gallery
- 🛠️ Admin Dashboard for CRUD

---

## 🧱 Tech Stack

- Python 3.10+
- Django 4.x
- PostgreSQL (recommended)
- Pillow (for image support)
- django-mptt (for hierarchical location handling)
- django-import-export (optional for data import/export)

---

## 📁 Project Structure

```text
Storage/                      # Root project folder
├── manage.py
├── Storage/                  # Project settings module
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── inventory/                # Main app for inventory and storage logic
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py             # Product, ProductBatch, LocationFinder, etc.
    ├── views.py
    ├── urls.py               # App-specific routes
    ├── forms.py              # Admin and user-facing forms (if needed)
    ├── serializers.py        # For REST API (optional)
    ├── templates/            # HTML templates (if needed)
    │   └── inventory/
    ├── static/               # CSS, JS, images
    │   └── inventory/
    ├── migrations/           # Auto-generated database migrations
    │   └── __init__.py
    └── utils/                # Helper functions (e.g., barcode generation, pricing logic)
        └── __init__.py

```

---

## 📌 Key Concepts

- **Product**: Represents a product with name, barcode, and images.
- **ProductBatch**: Represents a version of the product (e.g., different expiration, price, size).
- **LocationFinder**: Tree structure (Country → Region → City → Warehouse → Cabinet) to manage physical storage hierarchy.
- **NutritionData**: Optional nutrition facts per batch for edible products.
- **Label Printing**: Prints barcode + batch info for product identification.

---

## ✅ To-Do

- [ ] Set up project structure and virtual environment
- [ ] Create and migrate database models
- [ ] Implement admin interface
- [ ] Add label printing and barcode generation
- [ ] Add import/export features
- [ ] Write tests and docs

---

## 📦 License

MIT — feel free to fork and modify!
