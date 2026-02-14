# Школьный проект

### Веб-приложение для музыкантов: создание гамм, визуализация на грифе инструментов.

## Технологии
- **Backend**: FastAPI, MongoDB, JWT, Pytest
- **Frontend**: Vue 3, TypeScript, Bootstrap 5, Pinia
- **DevOps**: Docker, Docker Compose

## Backend
### Из корня
- Запуск сервера с автоматическим обновлением при изменениях: <br>
``` uvicorn backend.app.main:app --env-file ./backend/.env.development ``` <br>

<br>

- Запуск всех тестов: <br>
``` pytest backend/tests ``` <br>


## Frontend
### Из корня
- Запуск фронтэнда <br>
``` npm run dev --prefix frontend ``` 

## После запуска:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Демо-данные
При первом запуске через Docker Compose автоматически загружаются данные из дампа `/bd/dump`
