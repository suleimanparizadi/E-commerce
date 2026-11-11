# E-Commerce API

A complete e-commerce backend for a laptop store, built with Django REST Framework. Includes user authentication, product catalog with search and filtering, shopping cart, reviews, order checkout, an AI-powered Farsi chat assistant, and a custom React admin panel.

The frontend is a separate React app that consumes this API.

---

## Features

### Authentication
- Phone-number-based registration with OTP verification
- Login with either password or OTP
- JWT access and refresh tokens
- Password change for authenticated users
- Phone numbers validated for Iranian format (`09xxxxxxxxx`)

### Products
- Product catalog with categories, CPUs, specifications, and multiple gallery images
- Full-text search in Farsi using PostgreSQL `SearchVector`
- 12+ filters: brand, category, RAM, storage, GPU, CPU manufacturer, price range, display size, touchscreen, in-stock
- Pagination on all listing endpoints
- Average rating calculated from reviews

### Cart
- Supports guest carts (session-based) and authenticated carts
- Guest cart merges into the user cart on login
- Stock validation when adding or updating items
- Max 5 units per product per cart

### Reviews
- One review per user per product (enforced at the database level)
- Rating from 1 to 5 plus optional comment
- Only users with a completed purchase can review (verified-purchase check)
- Admin moderation via custom permission class

### Orders
- Checkout creates an order from the current cart
- Product price is snapshotted at purchase time so price changes don't alter history
- Stock is deducted atomically with the order creation
- Cart is cleared after successful checkout
- Order status flow: Pending → Confirmed → Shipped → Delivered → Canceled
- Address is stored on the order (not on the user), so past orders remain accurate

### AI Assistant
- Farsi chat assistant for the laptop store
- Answers FAQ questions using stored FAQ data
- Converts natural language requests into product filters ("لپ‌تاپ گیمینگ زیر ۵۰ میلیون" → `category: gaming, max_price: 50000000`)
- Returns product results as structured JSON so the frontend can render cards
- System prompt restricts the assistant to store-related topics only

### Admin Panel
- Custom React dashboard (not Django admin)
- Manage products, orders, users, reviews, and FAQs
- Change order status
- Activate/deactivate users

### Notifications
- Telegram notifications for new orders
- Low stock alerts sent to connected admins

### Cloud Storage
- Product images stored on S3-compatible storage (ParsPack)
- Custom storage class handles a bucket permission quirk

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL (with full-text search) |
| Cache / Sessions | Redis |
| Auth | Simple JWT |
| AI | OpenAI-compatible API (GapGPT) with Qwen models |
| Storage | S3-compatible (ParsPack) |
| Frontend | React + Axios |
| Container | Docker |
| Docs | Swagger (drf-yasg) |

---

## Project Structure
