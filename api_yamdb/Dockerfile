FROM python:3.9-slim as build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python:3.9-slim
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY . /app
ENV PYTHONUNBUFFERED 1