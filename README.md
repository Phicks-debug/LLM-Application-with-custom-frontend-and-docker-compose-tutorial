# Docker Setup for LLM Chat Application

This README provides instructions on how to run the LLM Chat Application using Docker.

## Prerequisites

- Docker
- Docker Compose

## Running the Application

1. Clone this repository to your local machine.

2. Navigate to the root directory of the project.

3. Build and run the Docker containers:

   ```
   docker-compose up --build
   ```

   This command will build the Docker images for both the backend and frontend, and then start the containers.

4. Once the containers are running, you can access:
   - The frontend at: http://localhost:3000
   - The backend API at: http://localhost:8000

5. To stop the application, use:

   ```
   docker-compose down
   ```

## Notes

- The backend API is configured to run on port 8000.
- The frontend React application is configured to run on port 3000.
- The frontend is set up to communicate with the backend at http://localhost:8000.
- Both the frontend and backend directories are mounted as volumes, allowing for real-time code changes without rebuilding the containers.