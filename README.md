# Social Network App

This is a small insurance rate app that allows users to upload insurance rates for specific dates and cargo types. Users can also retrieve the insurance price based on a given date and cargo type. The app is built using the FastAPI framework and utilizes the Tortoise ORM for database operations.

## Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/NickFlabel/insurance_rates_app.git

2. Start the app using the following command:
    ```bash
    docker-compose up --build

3. The API will be accessable at http://0.0.0.0:8000

4. To run the tests, use the following command:
    ```bash
    docker-compose exec rates_app pytest main/ -v

5. Swagger documentation for the API endpoints is available at http://localhost:8000/docs when the project is started.
