# Pull official base Python Docker image
FROM python:3.11.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /code/
RUN cp /code/views.py /usr/local/lib/python3.11/site-packages/django/contrib/auth/views.py
