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
$ poetry install
$ poetry run uvicorn app.main:app --reload
```

## Состояние проекта
На данном этапе на проекте не реализована сторонняя авторизация.
Начал реализовывать OAUTH2 через github, но остановился, т.к.
minio python SDK не поддерживает управление пользователями ([ссылка](https://github.com/minio/minio-js/issues/814#issuecomment-554975323))

Если существует обходной путь, просьба сообщить мне 
