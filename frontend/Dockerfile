# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose port 5000 to allow access to the app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

