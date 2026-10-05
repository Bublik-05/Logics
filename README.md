# L.O.G.I.C.S. — MVP

Один сквозной сценарий, работающий по-настоящему: загрузить документ → задать
вопрос → получить ответ, привязанный к конкретным фрагментам конкретного файла.
Никакого auth, очередей, памяти диалогов, фронтенда — они умышленно убраны
(см. `docs/MVP_SCOPE.md` зачем).

## Стек

FastAPI, Ollama (одна LLM, без абстракции над провайдерами), ChromaDB.
Postgres/Redis/Celery в этой версии нет вообще.

## Запуск

1. ```bash
   cp .env.example .env
   ```

2. ```bash
   docker compose -f docker/docker-compose.yml --env-file .env up --build
   ```

3. Скачать модели в Ollama (один раз):

   ```bash
   docker compose -f docker/docker-compose.yml exec ollama ollama pull llama3
   docker compose -f docker/docker-compose.yml exec ollama ollama pull nomic-embed-text
   ```

4. Открыть Swagger: <http://localhost:8000/docs>

## Проверка сценария (curl)

Загрузить документ:

```bash
curl -X POST http://localhost:8000/api/v1/documents/ \
  -F "file=@/путь/до/файла.pdf"
```

Ответ: `{"document_id": "...", "filename": "файла.pdf", "chunk_count": 12}`

Задать вопрос:

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "О чём этот документ?"}'
```

Ответ: `{"answer": "...", "sources": [{"filename": "файла.pdf", "chunk_index": 2, "snippet": "..."}]}`

Это и есть весь MVP — два содержательных эндпоинта плюс `/health`.

## Дальше

`docs/MVP_SCOPE.md` — что вырезано и в каком порядке это возвращать обратно,
когда сценарий заработает и появится время/мотивация на инфраструктуру.
