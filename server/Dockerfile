# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
ADD . /app
WORKDIR /app
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# Make port 5000 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
# CMD ["python", "index.py"]
ENTRYPOINT ["python","index.py"]
# docker-compose down
# docker-compose up --build
# docker-compose build