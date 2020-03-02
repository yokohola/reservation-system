# reservation-system
# usages: django, drf, docker/docker-compose, black

Для зависимостей смотрите: requirements.txt


URL - None

Сервис для бронирования переговорных.
  - Регистрация и авторизация пользователей через basic-auth
  - Создание переговорных и их бронирование только авторизованным пользователям
  - Одна переговорная может содержать множество бронирований
  - Интервал и продолжительность бронирования должно быть кратно 30 минутам
  - Нет возможности забронировать повторно уже занятый промежуток времени




POST         /users/register/   - авторизация                                         - AllowAny

GET, POST    /api/rooms/        - список переговорных, создание переговорных          - Authorized
GET, DELETE  /api/rooms/<pk>/   - просмотр переговорной, удаление переговорной        - Authorized
GET, POST    /api/reserve/      - просмотр списка бронирований, создания бронирования - Authorized


Регистрация пользователя:

{
  "username": "username",
  "password": "password",
  "email": "example@example.com"
}

Для получения доступа к api воспользуйтесь (доступно для postman):
  http://username:password@127.0.0.1:8000/api/...

... или укажите header:
  Authorization: Basic .....

Если вы используйте httpie, укажите флаг "-a"


