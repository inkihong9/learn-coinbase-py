# Use official Python 3.13 image
FROM python:3.13

# Set environment variable
ENV KEY=value

# Set working directory inside container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your app
COPY . /app

# Default command to start bash
CMD ["bash"]
