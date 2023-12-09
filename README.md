# E-commerce Project - README

This is a MERN (MongoDB, Express.js, React.js, Node.js) stack E-commerce project that I have developed.

## Project Description

The project is an E-commerce web application that allows users to browse products, add them to the cart, and proceed to checkout. It also includes features for user authentication, order management, and product administration.

## Project Features

### 1. User Authentication

- **API:** `/api/users`
- **Routes:** 
  - `/api/users/register` - Register a new user
  - `/api/users/login` - User login
  - `/api/users/profile` - Get user profile
  - `/api/users/update-profile` - Update user profile
  - `/api/users/update-password` - Update user password
  - `/api/users/logout` - Logout user

### 2. Product Listing and Details

- **API:** `/api/products`
- **Routes:** 
  - `/api/products` - Get all products
  - `/api/products/:id` - Get a specific product by ID

### 3. Shopping Cart

- **API:** `/api/cart`
- **Routes:** 
  - `/api/cart` - Get the current user's cart
  - `/api/cart/add-to-cart/:id` - Add a product to the cart
  - `/api/cart/remove-from-cart/:id` - Remove a product from the cart
  - `/api/cart/clear-cart` - Clear the entire cart

### 4. Checkout and Orders

- **API:** `/api/orders`
- **Routes:** 
  - `/api/orders` - Get all orders for the current user
  - `/api/orders/:id` - Get a specific order by ID
  - `/api/orders/create` - Create a new order

### 5. Admin Functionalities

- **API:** `/api/admin`
- **Routes:** 
  - `/api/admin/products` - Get all products (Admin)
  - `/api/admin/products/:id` - Get a specific product by ID (Admin)
  - `/api/admin/products/create` - Create a new product (Admin)
  - `/api/admin/products/:id/update` - Update a product (Admin)
  - `/api/admin/products/:id/delete` - Delete a product (Admin)
 
![EcommercePostman](https://github.com/yash-sahni54321/E-commerce/assets/67969545/76569f61-e14a-4c42-841e-a853118daa68)


## Installation

1. Clone the repository: `git clone https://github.com/yash-sahni54321/E-commerce.git`
2. Change directory to the project: `cd E-commerce`
3. Install server dependencies: `npm install`
4. Change directory to the client: `cd frontend`
5. Install client dependencies: `npm install`

## Usage

1. Start the server: `npm run dev`
2. Start the client: `cd frontend  npm start`

## Dependencies

- Node.js
- Express.js
- React.js
- MongoDB
  
## YouTube Link
https://www.youtube.com/watch?v=ULQCkPX5zV8
  
## Screenshots

Arrange these 6 screen shots in two columns and three rows:

| Profile          | Dashboard         | Details           |
| :--------------: | :--------------: | :---------------: |
| ![profile](https://github.com/yash-sahni54321/E-commerce/assets/67969545/faf0571b-0777-418b-b558-2a5349b75fe7) | ![dashboardE](https://github.com/yash-sahni54321/E-commerce/assets/67969545/ed0fcf33-fe80-4bbd-9ced-77f5041a7652) | ![details](https://github.com/yash-sahni54321/E-commerce/assets/67969545/ea64d453-84a8-44e9-8709-2eaf64e31905) |

| Create           | Cart              | Products          |
| :--------------: | :--------------: | :---------------: |
| ![Create](https://github.com/yash-sahni54321/E-commerce/assets/67969545/80849629-1149-4927-bbe7-33f1779d1a15) | ![cart](https://github.com/yash-sahni54321/E-commerce/assets/67969545/bc050e2b-69e7-4f94-8267-1985866d8e3a) | ![Products](https://github.com/yash-sahni54321/E-commerce/assets/67969545/bf244e50-05b1-4d0b-96ad-e913193a9930) |
