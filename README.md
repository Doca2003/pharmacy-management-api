# Pharmacy Management API

Pharmacy management REST API built with FastAPI and SQLAlchemy, featuring medication inventory control and order management.

## Features

- Medication registration
- Inventory management
- Order creation
- Add and remove items from orders
- Automatic stock update
- Order status control

## Technologies

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## Installation

Clone the repository:

git clone https://github.com/Doca2003/pharmacy-management-api.git

Enter the project folder:

cd pharmasys

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn app.main:app --reload

## API Documentation

After running the server, access:

http://127.0.0.1:8000/docs

FastAPI automatically generates interactive documentation using Swagger UI.

## Project Structure

pharmasys
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── app
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── main.py
│   │
│   └── routers
│       ├── medicamentos.py
│       └── pedidos.py

## Roadmap

### Completed
- [x] Medication CRUD
- [x] Order creation
- [x] Add items to order
- [x] Remove items from order
- [x] Automatic inventory update

### In Progress
- [ ] Order total price calculation
- [ ] Order finalization
- [ ] Validation for expired medications

### Future Improvements
- [ ] Authentication (JWT)
- [ ] Automated tests
- [ ] Docker support
- [ ] Cloud deployment

## Status

🚧 Work in Progress

This project is being developed as a backend portfolio project.
