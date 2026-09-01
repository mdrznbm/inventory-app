# Base image — matches the Python version used in local development (3.13.5)
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency list first (better layer caching — if requirements.txt
# hasn't changed, Docker reuses the cached install step on rebuilds instead of
# reinstalling everything from scratch every time)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application files actually needed to run the app.
# Explicit, not a blanket "COPY . .", so migration scripts, utility scripts,
# and .before-* backups never end up in the image regardless of .dockerignore.
COPY app.py .
COPY models.py .
COPY templates/ templates/
COPY static/ static/

# The app listens on port 5001 (matches app.run(port=5001) in app.py)
EXPOSE 5001

# Run with gunicorn (production WSGI server), not the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
