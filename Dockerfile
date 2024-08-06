# Stage 1: Build the React frontend
FROM node:22 AS client_build

WORKDIR /code

COPY ./client /code
RUN npm install
RUN npm run build


# Stage 2: Build the Django backend and serve static files with Whitenoise
FROM python:3.12.3

WORKDIR /code

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY server/requirements.txt /code/requirements.txt
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Copy Django project
# COPY server/code_review_project ./

# # Copy built React files from the previous stage
# COPY --from=build /app/build /app/staticfiles

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Set environment variables for Django
# ENV DJANGO_SETTINGS_MODULE=code_review_project.settings
# ENV PYTHONUNBUFFERED=1

COPY --from=client_build /code/build/static/ /code/static/
COPY --from=client_build /code/build/ /code/static/
COPY ./server/code_review_project /code

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "code_review_project.wsgi:application"]
