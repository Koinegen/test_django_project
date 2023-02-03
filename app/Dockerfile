# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update \
    && apt install gcc python3-dev musl-dev ffmpeg -y

WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]