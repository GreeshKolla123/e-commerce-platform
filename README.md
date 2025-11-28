# e-commerce-platform

A comprehensive e-commerce platform with user authentication, product catalog, shopping cart, order management, and admin panel.

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: FastAPI + SQLAlchemy
- **Design**: Figma ([View Design](https://www.figma.com/design/dyF1kttLxX5lIepS4hs2bO/Business-Consulting-Website-UI-Template--Community-?node-id=0-1&t=qeSSKsS8obfvLt2g-1))

## Project Structure

```
e-commerce-platform/
├── frontend/          # Frontend application
├── backend/           # Backend API
├── README.md          # This file
└── docker-compose.yml # Docker configuration (if applicable)
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for Python backends)
- Docker (optional, for containerized setup)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
# Follow backend-specific setup instructions in backend/README.md
```

## Features

- User registration and login
- Product catalog and search
- Shopping cart and checkout
- Order management
- Admin panel
- User profile and order history

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Log in a user
- `GET /api/products` - Get a list of all products
- `GET /api/products/{product_id}` - Get a specific product
- `POST /api/cart` - Add a product to the cart
- `GET /api/cart` - Get the cart contents
- `POST /api/checkout` - Checkout and pay for the order
- `GET /api/orders` - Get a list of all orders
- `GET /api/orders/{order_id}` - Get a specific order

## License

MIT
