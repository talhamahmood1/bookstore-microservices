# Bookstore Microservices

A microservices-based bookstore application built using Flask and Docker.

## Features

- **Catalog Service**: Adds and manages books.
- **Order Service**: Allows customers to place orders by selecting books.
- **Frontend Service**: Displays books and allows customers to interact with the system.

## Technologies Used

- Python (Flask)
- SQLite (for storing books and orders)
- Docker (for containerization)
- Docker Compose (for service orchestration)


## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

Clone the repository:
   
   git clone https://github.com/talhamahmood1/bookstore-microservices.git
   
   cd bookstore-microservices

Build and start the services using Docker Compose:


**docker compose up --build**

Access the services:

Frontend: http://localhost:5000
Catalog: http://localhost:5001/add_book
Order: http://localhost:5002/add_order
