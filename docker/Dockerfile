FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 5000

ENV PORT=5000
ENV FLASK_APP=app.main
ENV FLASK_ENV=production

CMD ["python", "run.py"]
