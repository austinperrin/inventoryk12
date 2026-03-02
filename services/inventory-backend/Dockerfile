# ==========================================================
# DEVELOPMENT IMAGE (Placeholder)
# ==========================================================
FROM python:3.14-slim AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /repo

COPY requirements/base.txt requirements/base.txt
COPY requirements/dev.txt requirements/dev.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements/dev.txt

COPY . /repo/services/inventory-backend
COPY ../.. /repo

CMD ["python", "services/inventory-backend/manage.py", "runserver", "0.0.0.0:8000"]
