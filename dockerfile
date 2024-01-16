# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9

# Kopieren Sie die Anwendungsdateien in den Container
COPY . /app

# Installieren Sie die Abhängigkeiten
RUN pip install fastapi pandas uvicorn openpyxl pyyaml pydantic

# Öffnen Sie den Port 80 für eingehende Verbindungen
EXPOSE 80

# Wechseln Sie in das Verzeichnis /app
WORKDIR /app

# Starten Sie die Anwendung mit Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
