FROM python:3.8

RUN mkdir greeny

COPY ./ /greeny/
# COPY ../pyproject.toml ../poetry.lock /app/ 

WORKDIR /greeny
# ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install pip --upgrade
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

# RUN cd /
# WORKDIR /
CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]
