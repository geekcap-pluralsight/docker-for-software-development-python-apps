# Start from the official Python Docker Image
FROM python

# Set environment variable for the virtual environment path
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create the virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Activate the virtual environment
RUN . /opt/venv/bin/activate

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# Command to run on container start: start our Flask application
CMD [ "python", "./app.py" ]
