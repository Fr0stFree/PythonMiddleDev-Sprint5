## Проект «Cinema» / "FoodGram"
### Описание проекта
Cinema - облачный кинотеатр, предназначенный для просмотра фильмов онлайн. Так же возможно искать интересующие фильмы,
актеров, режиссеров, добавлять фильмы в избранное, оставлять комментарии и рейтинги.

Реализован следующий функционал:

1. [ ] Регистрация
2. [ ] Авторизация и аутентификация
3. [ ] Просмотр фильмов
4. [x] Поиск фильмов, актеров, режиссеров и сценаристов по частичному совпадению
5. [ ] Просмотр фильмов
6. [x] Операции в панели администратора

---

### Стек технологий
- Back-end: [Django](https://www.djangoproject.com/) + [FastAPI](https://fastapi.tiangolo.com/)
- Databases: [PostgreSQL](https://www.postgresql.org/) + [Redis](https://redis.io/) + [ElasticSearch](https://www.elastic.co/)
- Version Control: [Git](https://git-scm.com/) + [GitHub](https://github.com/)
- Containerization: [Docker](https://www.docker.com/)
- Infrastructure: [Nginx](https://nginx.org/)

---

### Инструкция по запуску проекта:

1. Клонируйте репозиторий
```bash
git clone git@github.com:Fr0stFree/Cinema.git
```
2. Запустите проект с помощью команд Makefile 
_(необходимо наличие установленного Docker и плагина compose V2)_
```bash
sudo make build
```
3. Наполните базу данных
```bash
sudo make loaddata
```
4. Перейдите по адресу http://localhost:8080/api/docs
---

