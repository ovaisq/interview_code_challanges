# Use an official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY *.pem .
COPY . .

# Expose the port used by the application
EXPOSE 9090

# Run the command to start the application
CMD ["./service_run.sh"]