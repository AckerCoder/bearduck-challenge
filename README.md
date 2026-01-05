# E-commerce Full Stack Challenge

This is a technical challenge for mid-level full-stack developers. Build features for an e-commerce application using React and FastAPI.

> **Quick Start**: Run `docker-compose up --build` to start the app, then read the challenges below. See [QUICK_START.md](QUICK_START.md) for troubleshooting.

## 📋 Challenge Overview

### Current Implementation

The application currently includes:

- **Backend (FastAPI)**:
  - Product management API with SQLAlchemy ORM
  - Shopping cart management with session handling
  - Order creation and tracking
  - PostgreSQL database with persistent storage
  - RESTful API endpoints
  - Automatic database initialization with sample products

- **Frontend (React + Vite)**:
  - Product listing with images and details
  - Shopping cart functionality
  - Order creation
  - Order history view
  - Responsive design

### Tech Stack

- **Backend**: FastAPI 0.128.0, Python 3.10+, SQLAlchemy 2.0, PostgreSQL 16
- **Frontend**: React 19.0, Vite 6.0
- **Database**: PostgreSQL 16 (with Docker volume for persistence)
- **Containerization**: Docker & Docker Compose

## 🎯 Your Mission

Complete **one or more challenges** from the 7 tasks below. You can choose based on your time, interests, and expertise.

### Available Challenges

**Frontend (with Mockups in `/mockups` folder):**
- **Challenge 01**: Add to Cart Animation (Easy) - 30 min
- **Challenge 02**: Order Confirmation Modal (Medium) - 1 hour
- **Challenge 02b**: Order Detail View (Medium) - 1-1.5 hours
- **Challenge 03**: Authentication System (Hard, Full Stack) - 3-4 hours

**Backend + Frontend:**
- **Challenge 04**: Pagination (Easy) - 45 min - 1 hour
- **Challenge 05**: Order Status Management (Easy) - 1 hour
- **Challenge 06**: Search & Filtering (Medium) - 2-3 hours
- **Challenge 07**: Shopping Cart Persistence (Medium) - 1.5-2 hours

### How to Approach

1. **Start the app**: `docker-compose up --build`
2. **Choose your challenges**: Based on time available (see time estimates above)
3. **View mockups** (Challenges 01-03): Open HTML files in `mockups/` folder to see expected behavior
4. **Read requirements below**: Scroll down for detailed requirements of each challenge
5. **Implement & test**: Build features, test thoroughly, commit your work

### Recommended Combinations

**By Time:**
- **Quick (1-2 hours):** Pick 1-2 easy challenges
- **Standard (3-4 hours):** Pick 2-3 challenges of varying difficulty
- **Comprehensive (5+ hours):** Complete 4+ challenges including at least one hard

**By Specialty:**
- **Frontend Developers:** Challenges 01, 02, 02b (animations, modals, views)
- **Backend Developers:** Challenges 04, 05, 06 (pagination, status, filtering)
- **Full Stack Developers:** Challenges 02, 03, 05 OR 04, 06, 07

---

## 📋 Challenge Details

### Challenge 01: Add to Cart Animation (Easy)

**Type:** Frontend
**Time:** 30 minutes
**Mockup:** [`mockups/01-add-to-cart-animation.html`](mockups/01-add-to-cart-animation.html)

Add a smooth animation to the "Add to Cart" button when clicked.

**Requirements:**
- Button scale animation (0.95x shrink)
- Color transition from blue to green
- Checkmark icon animation
- Auto-reset after animation completes (~600ms)

**Acceptance Criteria:**
- ✓ Button animates smoothly when clicked
- ✓ Shows visual feedback to user
- ✓ Returns to normal state automatically
- ✓ Works on multiple rapid clicks

---

### Challenge 02: Order Confirmation Modal (Medium)

**Type:** Frontend
**Time:** 1 hour
**Mockup:** [`mockups/02-order-confirmation-modal.html`](mockups/02-order-confirmation-modal.html)

Replace the browser `alert()` with a custom modal component.

**Requirements:**
- Custom modal component with fade-in animation
- Semi-transparent overlay
- Display order ID and success message
- "View Order" and "Continue Shopping" buttons
- Close on overlay click or Escape key
- Responsive design

**Acceptance Criteria:**
- ✓ Modal appears with smooth animation
- ✓ Can close modal multiple ways
- ✓ Works on mobile devices
- ✓ No browser alerts used

---

### Challenge 02b: Order Detail View (Medium)

**Type:** Frontend
**Time:** 1-1.5 hours
**Mockup:** [`mockups/02b-order-detail-view.html`](mockups/02b-order-detail-view.html)

Create a detailed order view page showing complete order information.

**Requirements:**
- Order header with ID and status badge
- Order info grid (date, items count, payment status, delivery status)
- Items list with images, quantities, and prices
- Order summary with subtotal, shipping, tax, total
- Action buttons (Download Invoice, Track Order)
- Back navigation
- Color-coded status badges

**Status Colors:**
- Pending: Yellow (#fef3c7 / #92400e)
- Processing: Blue (#dbeafe / #1e40af)
- Successful: Green (#d1fae5 / #065f46)
- Cancelled: Gray (#f3f4f6 / #4b5563)
- Failed: Red (#fee2e2 / #991b1b)

**Acceptance Criteria:**
- ✓ All order information displayed correctly
- ✓ Status badge shows correct color
- ✓ Responsive on mobile
- ✓ Can navigate back to orders list

---

### Challenge 03: Authentication System (Hard, Full Stack)

**Type:** Full Stack
**Time:** 3-4 hours
**Mockup:** [`mockups/03-authentication-system.html`](mockups/03-authentication-system.html)

Implement a complete user authentication system.

**Backend Requirements:**
- Add `users` table to database schema
- Implement password hashing (bcrypt/argon2)
- Create auth endpoints: POST /api/register, POST /api/login, POST /api/logout
- Implement JWT tokens OR session-based auth
- Protect cart and order endpoints (require authentication)
- Associate orders with authenticated users (add user_id foreign key)

**Frontend Requirements:**
- Login/Register forms with tab switching
- Form validation
- Auth state management
- Store and use auth tokens
- Protected routes/components
- Show logged-in user in header
- Logout functionality
- Persistent login (localStorage/cookies)

**Database Changes:**
- Create `users` table with id, email, password_hash, created_at
- Add `user_id` foreign key to `orders` table
- Handle migration of existing anonymous orders

**Acceptance Criteria:**
- ✓ Users can register and login
- ✓ Passwords are hashed (never plain text)
- ✓ Auth is required for cart/orders
- ✓ Orders are linked to users
- ✓ Login persists across page refreshes
- ✓ Proper error messages for invalid credentials

---

### Challenge 04: Pagination (Easy)

**Type:** Backend + Frontend
**Time:** 45 minutes - 1 hour

Add pagination to product and order listing endpoints.

**Backend Requirements:**

Modify `GET /api/products`:
- Add query params: `page` (default: 1), `limit` (default: 10)
- Response format:
```json
{
  "items": [...products...],
  "total": 156,
  "page": 1,
  "limit": 10,
  "pages": 16
}
```

Modify `GET /api/orders` with same pagination structure.

**Implementation Hints:**
- Use SQLAlchemy: `.offset((page - 1) * limit).limit(limit)`
- Calculate pages: `math.ceil(total / limit)`
- Validate page doesn't exceed total pages
- Return empty array if out of bounds

**Frontend Requirements:**
- Pagination controls (Previous, Next, page numbers)
- Display "Showing X-Y of Z products"
- Update API calls with pagination params
- Items per page selector (bonus)

**Acceptance Criteria:**
- ✓ Products paginated correctly
- ✓ Orders paginated correctly
- ✓ Metadata returned (total, pages, etc.)
- ✓ Frontend shows pagination controls
- ✓ Navigation between pages works

---

### Challenge 05: Order Status Management (Easy)

**Type:** Full Stack
**Time:** 1 hour

Implement order status workflow with proper transitions.

**Backend Requirements:**

1. **Order Status Enum:**
   - Statuses: `pending`, `processing`, `successful`, `cancelled`, `failed`

2. **New Endpoint:** `PATCH /api/orders/{order_id}/status`
   - Body: `{"status": "processing"}`
   - Validate status transitions
   - Return updated order

3. **Business Rules:**
   - New orders start as `pending`
   - Valid transitions:
     - `pending` → `processing`, `cancelled`
     - `processing` → `successful`, `failed`, `cancelled`
     - `successful` → cannot change (terminal)
     - `cancelled` → cannot change (terminal)
     - `failed` → cannot change (terminal)

**Frontend Requirements:**
- Show status with color-coded badges (see Challenge 02b for colors)
- Add status update buttons (for testing/admin)
- Filter orders by status (bonus)
- Display status history (bonus)

**Acceptance Criteria:**
- ✓ Orders created with `pending` status
- ✓ Status can be updated via API
- ✓ Invalid transitions rejected with error
- ✓ Frontend shows correct status colors
- ✓ Users can filter by status (bonus)

---

### Challenge 06: Search & Filtering (Medium)

**Type:** Full Stack
**Time:** 2-3 hours

Add comprehensive search and filtering to product listing.

**Backend Requirements:**

Modify `GET /api/products` to accept:
- `search`: Search in name and description (case-insensitive)
- `min_price`, `max_price`: Price range filter
- `sort_by`: Sort by `price`, `name`, or `stock`
- `order`: Sort order `asc` or `desc`

Example: `GET /api/products?search=wireless&min_price=20&max_price=150&sort_by=price&order=asc&page=1&limit=10`

All filters work together with pagination from Challenge 04.

**Frontend Requirements:**

1. **Search Bar:**
   - Real-time search (debounced 300ms)
   - Clear search button
   - "No results" message

2. **Filter Panel:**
   - Price range slider or inputs
   - Sort dropdown (Price Low-High, High-Low, Name A-Z, etc.)
   - Clear all filters button

3. **Results:**
   - Show active filters
   - Display result count
   - Update URL with filter params (bonus)

**Acceptance Criteria:**
- ✓ Search works in name and description
- ✓ Price range filtering works
- ✓ Sorting works correctly
- ✓ All filters can be combined
- ✓ Search is debounced
- ✓ Active filters displayed
- ✓ Clear filters works

---

### Challenge 07: Shopping Cart Persistence (Medium)

**Type:** Full Stack
**Time:** 1.5-2 hours

Improve cart persistence with auto-expiry and cleanup.

**Current Issue:**
- Cart tied to session_id (browser-based)
- Lost if cookies cleared
- Doesn't sync across devices

**Backend Requirements:**

1. **Improvements:**
   - Cart already in database ✓
   - Add `created_at` and `updated_at` timestamps to Cart model
   - Auto-expire carts after 30 days of inactivity
   - Merge carts when user logs in (if using Challenge 03)

2. **Cleanup Endpoint:** `DELETE /api/carts/cleanup`
   - Remove carts older than 30 days
   - Can be scheduled with cron or called manually

**Frontend Requirements:**
- Load cart on app start
- Sync cart when items change
- Show last updated time
- Warning if cart is old (>7 days)
- Allow user to refresh cart

**Acceptance Criteria:**
- ✓ Cart persists across browser sessions
- ✓ Old carts automatically cleaned
- ✓ Cart shows last updated time
- ✓ Cart merges on login (if using auth)

---

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Node.js 22+ (if running locally)
- Python 3.10+ (if running locally)

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd challenge
```

2. Start the application:
```bash
docker-compose up --build
```

This will start three services:
- **PostgreSQL database** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 3000

The database will be automatically initialized with sample products on first run.

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432 (credentials in docker-compose.yml)

4. Stop the application:
```bash
docker-compose down
```

To remove the database volume (reset all data):
```bash
docker-compose down -v
```

### Running Locally (Development)

**Note**: For local development, you'll need PostgreSQL installed or use SQLite.

#### Option 1: Use Docker for Database Only

```bash
# Start only PostgreSQL
docker-compose up db

# In another terminal, run backend
cd backend
pip install -r requirements.txt
export DATABASE_URL="postgresql://ecommerce:ecommerce123@localhost:5432/ecommerce"
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, run frontend
cd frontend
npm install
npm run dev
```

#### Option 2: Use SQLite (No PostgreSQL Required)

```bash
# Backend
cd backend
pip install -r requirements.txt
export DATABASE_URL="sqlite:///./ecommerce.db"
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Key Endpoints

**Products**
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product by ID

**Cart**
- `GET /api/cart/{session_id}` - Get cart
- `POST /api/cart/{session_id}/items` - Add item to cart
- `PUT /api/cart/{session_id}/items/{product_id}` - Update cart item
- `DELETE /api/cart/{session_id}/items/{product_id}` - Remove item
- `DELETE /api/cart/{session_id}` - Clear cart

**Orders**
- `POST /api/orders` - Create order
- `GET /api/orders` - List all orders
- `GET /api/orders/{id}` - Get order by ID

## 🏗️ Project Structure

```
challenge/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── database.py          # Database configuration & session
│   ├── controllers/         # Business logic
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   ├── routes/              # API routes
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   ├── App.css
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .dockerignore
├── mockups/                 # Interactive HTML mockups for challenges 01-03
│   ├── 01-add-to-cart-animation.html
│   ├── 02-order-confirmation-modal.html
│   ├── 02b-order-detail-view.html
│   └── 03-authentication-system.html
├── docker-compose.yml       # Multi-container orchestration
├── docker-compose.sqlite.yml # SQLite alternative (backup)
├── .gitignore
├── README.md               # ⭐ This file - Complete challenge guide
├── DATABASE.md             # Database schema documentation
├── QUICK_START.md          # Docker commands & troubleshooting
└── TROUBLESHOOTING.md      # Common issues & solutions
```

## 📝 Submission Guidelines

1. **Complete Challenges**
   - Test each challenge thoroughly before moving to the next
   - Follow the requirements and acceptance criteria listed above

2. **Code Quality**
   - Write clean, readable code
   - Follow Python PEP 8 and JavaScript/React best practices
   - Add comments for complex logic
   - Use meaningful variable and function names
   - Apply SOLID principles and reusable components

3. **Documentation**
   - Update this README with:
     - **List of challenges you completed** (most important!)
     - Any assumptions made
     - Setup instructions for new features
     - Known limitations or future improvements
   - Document new API endpoints in code or README
   - Add comments explaining complex business logic

4. **Git Workflow**
   - Create a new branch for your work
   - Make atomic commits with clear messages
   - Keep your commit history clean

5. **Testing**
   - Test all new features thoroughly
   - Ensure Docker setup works correctly
   - Verify the application works end-to-end
   - Test across different browsers (for frontend challenges)

6. **Deliverables**
   - Source code with your implementations
   - Updated README.md with a **"Completed Challenges"** section listing what you built
   - (Optional) Screen recording or screenshots demonstrating features

## 🎓 Evaluation Criteria

Your submission will be evaluated based on:

1. **Functionality** (40%)
   - Features work as expected and meet acceptance criteria
   - No critical bugs or errors
   - Proper error handling and edge case management
   - Good user experience

2. **Code Quality** (30%)
   - **Clean Code**: Readable, self-documenting code with meaningful names
   - **SOLID Principles**: Proper application of SRP, DRY, and other principles
   - **Reusability**: Components and functions are modular and reusable
   - **Boy Scout Rule**: Code improvements and refactoring where touched
   - **Consistency**: Following Python PEP 8 and JavaScript best practices

3. **Architecture** (15%)
   - **Separation of Concerns**: Clear separation between routes, controllers, and models
   - **Database Design**: Normalized schemas with proper relationships
   - **Component Structure**: Logical organization of React components
   - **Scalability**: Design decisions that support future growth
   - **Patterns**: Appropriate use of design patterns

4. **Documentation** (10%)
   - Clear and updated README with completed challenges listed
   - Code comments explaining complex logic
   - API documentation for new endpoints
   - Assumptions and design decisions documented

5. **Testing** (5%)
   - Test coverage for critical functionality
   - Edge cases and error scenarios tested
   - Manual testing performed (all features work in Docker)

## 📐 Best Practices & Recommendations

We encourage you to follow industry best practices and demonstrate your understanding of software engineering principles:

### Code Quality Principles

**Clean Code:**
- Write self-documenting code with meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Avoid deep nesting and complex conditionals
- Use consistent naming conventions (PEP 8 for Python, Airbnb/Standard for JavaScript)
- Remove commented-out code and debug statements before submission

**Boy Scout Rule:**
- *"Leave the code cleaner than you found it"*
- If you modify existing code, improve it (refactor, add comments, fix naming)
- Don't just add to messy code - clean it up as you go
- This demonstrates ownership and care for code quality

### Frontend Development

**Reusable Components:**
- Extract common UI patterns into reusable React components
- Example: `<Button>`, `<Card>`, `<Modal>`, `<Badge>`, `<Input>` components
- Use props to make components flexible and configurable
- Avoid duplicating JSX - if you copy-paste, it should probably be a component
- Keep components focused - a component should do one thing well

**Component Best Practices:**
- Separate presentational components from container components
- Use PropTypes or TypeScript for type safety (bonus)
- Keep component files organized (one component per file)
- Use hooks properly (useState, useEffect, custom hooks)

### Backend Development

**SOLID Principles:**

1. **Single Responsibility Principle (SRP)**
   - Each function/class should have one reason to change
   - Example: Separate business logic (controllers) from routing (routes)
   - Don't mix database operations with business logic

2. **Open/Closed Principle**
   - Code should be open for extension, closed for modification
   - Use inheritance and composition to extend functionality

3. **Liskov Substitution Principle**
   - Subtypes should be substitutable for their base types
   - Ensure proper inheritance hierarchies

4. **Interface Segregation Principle**
   - Clients shouldn't depend on interfaces they don't use
   - Create specific interfaces rather than one general-purpose interface

5. **Dependency Inversion Principle**
   - Depend on abstractions, not concretions
   - Use dependency injection where appropriate

**Clean Architecture:**
- Keep business logic separate from framework code
- Controllers handle business logic, routes handle HTTP
- Models define data structure, schemas handle validation
- Use service layers for complex operations

### Database Design

**Normalization:**
- Design normalized database schemas (at least 3NF)
- Avoid data duplication across tables
- Use foreign keys to maintain referential integrity
- Think about relationships: One-to-Many, Many-to-Many

**Good Practices:**
- Use meaningful table and column names
- Add indexes for frequently queried columns
- Consider data types carefully (don't use VARCHAR for numbers)
- Use constraints (NOT NULL, UNIQUE, CHECK) to enforce data integrity
- Document schema changes if you modify the database

### General Engineering

**Error Handling:**
- Handle errors gracefully with try-catch blocks
- Return meaningful error messages
- Use appropriate HTTP status codes
- Log errors for debugging

**Security:**
- Validate all user inputs
- Sanitize data to prevent SQL injection and XSS
- Don't expose sensitive information in error messages
- Use environment variables for secrets

**Performance:**
- Avoid N+1 query problems
- Use database indexes wisely
- Implement pagination for large datasets (Challenge 04)
- Minimize unnecessary re-renders in React

**Testing:**
- Write tests for critical business logic
- Test edge cases and error scenarios
- Use meaningful test descriptions
- Aim for high coverage on important code paths

## 💡 Tips

- **Read this README thoroughly**: All requirements, hints, and acceptance criteria are documented here
- **Choose wisely**: Pick challenges that showcase your strengths (you don't need to complete all 7)
- **Quality over quantity**: A few well-implemented challenges are better than many rushed ones
- **Open the mockups**: For Challenges 01-03, open the HTML files in `/mockups` to see expected behavior
- **Test thoroughly**: Make sure Docker setup works and all features function correctly
- **Follow mockup designs**: Match the animations, colors, and interactions shown in mockups
- **Handle errors**: Consider edge cases, validate inputs, use appropriate HTTP status codes
- **Document well**: Update README with what you built, assumptions made, and how to test your work
- **Check acceptance criteria**: Each challenge lists specific criteria - make sure you meet them before moving on
- **Apply best practices**: Use clean code, SOLID principles, reusable components (see Best Practices section)

## ❓ Questions?

If you have questions about the challenge requirements, please document your assumptions in the README.

## 📄 License

This challenge is for evaluation purposes only.

---

**Good luck! We're excited to see what you build! 🚀**
