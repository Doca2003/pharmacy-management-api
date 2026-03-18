# Pharmacy Management API

REST API for pharmacy inventory and order management built with FastAPI and SQLAlchemy.

The system manages medication stock, order creation, and automatic inventory updates while enforcing business rules such as expired medication validation and order lifecycle control.

---

## Features

### Pharmacy System
* Full medication CRUD operations
* Inventory management
* Order creation and management
* Add and remove items from orders
* Automatic stock updates on item operations
* Order status control (OPEN / FINALIZED)
* Order total price calculation
* Order finalization
* Validation for expired medications
* List expired medications

---

### Query & Data Features
* Filtering orders by status and date
* Filtering medications by name and stock
* Sorting results (price, name, date)
* Pagination support for large datasets

---

### Authentication & Security
* User registration
* JWT authentication
* JWT-protected endpoints
* Role-based access control (RBAC)
* Current authenticated user endpoint (`/users/me`)
---

## Technologies

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* JWT (JSON Web Tokens)
* Passlib (bcrypt hashing)
---

## Installation

Clone the repository:

```
git clone https://github.com/Doca2003/pharmacy-management-api.git
```

Enter the project folder:

```
cd pharmasys
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the API:

```
uvicorn app.main:app --reload
```

---

## API Documentation

After running the server, access:

```
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive documentation using Swagger UI.

---

---
## API Endpoints

---

## Medications

| Method | Endpoint                 | Description                          |
|--------|--------------------------|--------------------------------------|
| POST   | `/medicamentos`          | Create a new medication              |
| GET    | `/medicamentos`          | List medications (with filters/sort) |
| PUT    | `/medicamentos/{id}`     | Update medication stock              |
| DELETE | `/medicamentos/{id}`     | Delete a medication                  |
| GET    | `/medicamentos/vencidos` | List expired medications             |

---

## Orders

| Method | Endpoint                        | Description                                |
|--------|-------------------------------- |--------------------------------------------|
| POST   | `/pedidos`                      | Create a new order                         |
| GET    | `/pedidos`                      | List orders (filters, sorting, pagination) |
| GET    | `/pedidos/{id}`                 | Get order details                          |
| POST   | `/pedidos/{id}/itens`           | Add item to order                          |
| DELETE | `/pedidos/{id}/itens/{item_id}` | Remove item from order                     |
| POST   | `/pedidos/{id}/finalizar`       | Finalize order                             |

---

## Users

| Method | Endpoint                   | Description                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/users/me`                | Get current authenticated user       |
| PATCH  | `/users/{user_id}/role`    | Update user role (admin only)        |

---

##  Authentication

| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| POST   | `/auth/register` | Register a new user              |
| POST   | `/auth/login`    | Authenticate and receive JWT     |

---
## Example Response

Example Request:

```
GET /pedidos/1
```

Response:

```
{
"id": 1,
"pedido_id": "7c52f7f5-7d52-4f4a-9c4a-9c89a5e4e8e0",
"status": "FINALIZADO",
"data_criacao": "2026-03-17T14:30:00",
"data_fechamento": "2026-03-17T15:10:00",
"valor_total": 40.0,
"itens": [
{
"id": 2,
"medicamento_id": 1,
"quantidade": 2,
"preco_unitario": 20.0
}
]
}
---
## Project Structure

```
pharmasys
│
├── create_admin.py
├── .gitignore
├── requirements.txt
│
├── app
│ ├── init.py
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│ ├── main.py
│ │
│ ├── auth
│ │ ├── auth_router.py
│ │ ├── security.py
│ │ └── roles.py
│ │
│ └── routers
│ ├── medicamentos.py
│ ├── pedidos.py
│ └── users_router.py
```

---

## Roadmap

### Completed

* [x] Medication CRUD
* [x] Order creation
* [x] Add items to order
* [x] Remove items from order
* [x] Automatic inventory update
* [x] Order total price calculation
* [x] Order finalization
* [x] Validation for expired medications
* [x] List expired medications
* [x] Filter orders by status
* [x] JWT Authentication
* [x] User registration
* [x] Protected endpoints
* [x] Role-based access control (RBAC)
* [x] Pagination for medication and order listing
* [x] Filtering medications by name and stock level
* [x] Admin-only endpoints for medication deletion
* [x] Admin and pharmacist only for medication creation
* [x] Filtering orders by date
* [x] Sorting results (price, date, name)

### In Progress

- [ ] Low stock alert
- [ ] Add created_at field to orders
- [ ] Persist total order value in database

### Future Improvements

* [ ] Automated tests with Pytest
* [ ] Docker containerization
* [ ] PostgreSQL support
* [ ] CI/CD pipeline with GitHub Actions
* [ ] API rate limiting
* [ ] Logging and monitoring
---

## Status

🚧 Work in Progress

This project is being developed as a backend portfolio project focused on:

* REST API architecture

* inventory management systems

* backend best practices using FastAPI

---

# Author
Developed as a portfolio project by Dominique G.
