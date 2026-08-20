FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY models.py .
COPY static/ static/
COPY templates/ templates/
COPY instance/ instance/

EXPOSE 5001

#CMD ["python", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
