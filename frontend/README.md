# Ecommerce App

This is an ecommerce app built with React, Vite, and Tailwind CSS.

## Getting Started

1. Clone the repository: `git clone https://github.com/username/ecommerce-app.git`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`
4. Open the app in your browser: `http://localhost:3000`

## Features

* User authentication (login, register)
* Product catalog
* Shopping cart
* Order management

## API Endpoints

* `/login`: Login a user
* `/register`: Register a new user
* `/cart`: Get the shopping cart
* `/orders`: Get all orders
* `/orders/{orderId}`: Get an order by ID

## Database Schema

* `users`: table for storing user data
* `products`: table for storing product data
* `cart`: table for storing cart data
* `orders`: table for storing order data

## Technical Requirements

* React + Vite for frontend
* FastAPI + SQLAlchemy for backend
* PostgreSQL for database