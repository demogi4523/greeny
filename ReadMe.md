# Тестовое задание Разработчик (Python)

### Быстрый запуск

Запуск в *docker-compose*:
```
$ docker-compose build
...
$ docker-compose up
```

Важно!!!
1)  Подразумевается запуск в среде Linux, так как тесты завязаны на времени, а для синхронизации используются *Docker Volumes*
2)  Запуск может занять несколько минут в зависимости от хостовой машины(установка poetry и библиотек) 

Тесты не запускаются при старте docker-compose и docker, но после начала рабыты с контенерами тесты доступны как внутри(через консоль в контейнере после подключения(*docker attach* или *docker exec*))

### Запуск тестов

Стандартно через интерфейс pytest:
```
$ pytest
```

### Запуск проекта в среде Linux
Предполагается работа через пакетный менеджер poetry и запуск из корня проекта:

```
$ pwd
~/greeny
$ poetry show
Creating virtualenv ...-py3.8 in .venv
$ source .venv/...-py3.8/bin/activate
$ poetry install
$ docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  --rm \
  -e "MINIO_ROOT_USER=root" \
  -e "MINIO_ROOT_PASSWORD=qwerty123" \
  quay.io/minio/minio server /data --console-address ":9001"
$ docker run -d \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres
$ poetry run uvicorn app.main:app --reload
```

Также можно делать запросы через fastapi openapid в браузере по адресу *http://localhost:8000/docs*
Или просмотреть веб-консоль minio по aдресу *http://localhost:9001/login* или *http://localhost:9000*

## Состояние проекта
На данном этапе на проекте не реализована сторонняя авторизация.
Начал реализовывать OAUTH2 через github, но остановился, т.к.
minio python SDK не поддерживает управление пользователями ([ссылка](https://github.com/minio/minio-js/issues/814#issuecomment-554975323))

Если существует обходной путь, просьба сообщить мне 

Из минусов:

1)  Отсутствие модели пользователей
2)  Отсутствие линтинга
3)  Отсутствие precommit hooks

Предложения по улучшению приветствуются :)
