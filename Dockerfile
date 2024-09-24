FROM python:3.11-slim-bookworm
# FROM python:3.11-bookworm
ENV PYTHONBUFFERED=1

WORKDIR /students

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]