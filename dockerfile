FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Copy application files
COPY app.py /app/

# Install dependencies
RUN pip install flask requests gunicorn

# Expose port
EXPOSE 5000

# Start the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]