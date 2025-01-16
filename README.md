# Bookstore Microservices

A microservices-based bookstore application built using Flask and Docker.

## Features

- **Catalog Service**: Adds and manages books.
- **Order Service**: Allows customers to place orders by selecting books.
- **Frontend Service**: Displays books and allows customers to interact with the system.

## Technologies Used

- **Python (Flask)** A lightweight and flexible web framework used for building the microservices and their APIs.
- **SQLite (for storing books and orders)** A lightweight relational database used for storing book and order data. Each service manages its own data storage for simplicity.
- **Docker (for containerization)** Containerization platform used to package the microservices into isolated containers, ensuring consistent environments for development and deployment.
- **Docker Compose (for service orchestration)** A tool for defining and running multi-container Docker applications. It helps in orchestrating the Catalog, Order, and Frontend services.


## Recent Updates
 - Added the ability to add new books to the catalog directly from the UI.
 - Introduced the feature to update book information, such as stock, seamlessly.
 - Enhanced the frontend for better usability, including structured forms with improved visuals for adding and managing books and orders.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

**Clone the repository:**
```bash
git clone https://github.com/talhamahmood1/bookstore-microservices.git
```

```bash
cd bookstore-microservices
```
Build and start the services using Docker Compose:

```bash
docker compose up --build
```

Access the services:

**Frontend**: http://localhost:5000

**Catalog**: http://localhost:5001/add_book

**Order**: http://localhost:5002/add_order

### Stopping the Services

To stop the running containers, follow these steps:

1. **Stop the containers gracefully**:  
   Use `Ctrl+C` in the terminal where `docker compose up` is running.

2. **Bring down the services completely**:  
   Run the following command to stop and remove all containers started by Docker Compose:

   ```bash
   docker compose down
   ```
