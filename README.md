# Animal Image Microservice

This microservice fetches and stores random images of animals (duck, dog, bear) and provides REST APIs to extract them and a simple UI to view them. It is built with FastAPI, uses SQLAlchemy for database interactions, and includes automated tests using Pytest.

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your system. You can download Docker from [docker.com](https://www.docker.com/get-started).

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/keithyuen/animal_image_microservice.git
cd animal_image_microservice
```

### 2. Build and Run the Docker
To simplify the setup, this project uses Docker to handle all dependencies and to run the application. The following commands will build the Docker image and start the container.

#### 2.1 Build the Docker Image
Run the following command to build the Docker image:
```bash
docker build -t animal_image_microservice .
```
#### 2.2 Run the Docker Container
After building the image, start the container with this command:
```bash
docker run -p 80:80 animal_image_microservice
```

#### 2.3 Start the UI
The application will be accessible at http://localhost/ in your browser.

From the UI, you can:
Select an animal type and the number of images to save.
View the last saved image or all images by type.

### 3. Automated Tests
After executing step 2.1 build the Docker image, you can run the automated tests directly inside the container:
```bash
docker run --rm animal_image_microservice pytest tests/
```
This command will execute all tests in the tests/ directory. If all tests pass, you should see a summary indicating that all tests were successful.
