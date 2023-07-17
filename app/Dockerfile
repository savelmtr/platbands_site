FROM python:3.10-slim

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH /root/.local/bin:${PATH}

COPY requirements.txt .

RUN pip install --no-warn-script-location --disable-pip-version-check \
    -r requirements.txt

CMD [ "python", "main.py" ]
