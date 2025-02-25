import uvicorn

import logging

# # Создаем фильтр логов для эндпоинта /is-scanned
# class FilterPollingLogs(logging.Filter):
#     def filter(self, record):
#         return "POST /is-scanned" not in record.getMessage()

# # Добавляем фильтр к Uvicorn логгеру
# logging.getLogger("uvicorn.access").addFilter(FilterPollingLogs())


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)