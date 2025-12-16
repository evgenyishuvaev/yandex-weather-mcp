# Yandex Weather MCP Server

MCP сервер с инструментами для получения текущей даты и времени, реализованный с использованием FastMCP. Сервер поддерживает подключение клиентов по HTTP через JSON-RPC протокол.

## Установка

```bash
pip install -e .
```

## Использование

### HTTP режим (по умолчанию)

Запустите сервер в HTTP режиме:

```bash
python main.py
```

Сервер будет доступен по адресу `http://127.0.0.1:8000` (по умолчанию).

Вы можете настроить хост и порт через переменные окружения:

```bash
MCP_HOST=0.0.0.0 MCP_PORT=8080 python main.py
```

### Stdio режим

Для использования stdio транспорта (для интеграции с MCP клиентами через стандартный ввод/вывод):

```bash
MCP_TRANSPORT=stdio python main.py
```

## HTTP API

### Информация о сервере

```bash
GET http://127.0.0.1:8000/
```

Возвращает информацию о сервере и доступных инструментах.

### JSON-RPC Endpoint

```bash
POST http://127.0.0.1:8000/mcp
Content-Type: application/json
```

#### Пример запроса для получения текущей даты и времени:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_current_datetime",
    "arguments": {}
  },
  "id": 1
}
```

#### Пример ответа:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "2024-01-15T14:30:45.123456"
      }
    ]
  },
  "id": 1
}
```

#### Пример запроса для получения списка инструментов:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

## Доступные инструменты

Сервер предоставляет следующие инструменты:

1. **get_current_datetime** - Возвращает текущую дату и время в формате ISO 8601
2. **get_current_date** - Возвращает текущую дату в формате YYYY-MM-DD
3. **get_current_time** - Возвращает текущее время в формате HH:MM:SS
4. **get_current_timestamp** - Возвращает текущий Unix timestamp

## Примеры использования

### cURL

```bash
# Получить текущую дату и время
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_current_datetime",
      "arguments": {}
    },
    "id": 1
  }'
```

### Python

```python
import requests

url = "http://127.0.0.1:8000/mcp"
payload = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "get_current_datetime",
        "arguments": {}
    },
    "id": 1
}

response = requests.post(url, json=payload)
print(response.json())
```

## Технологии

- [FastMCP](https://github.com/jlowin/fastmcp) - фреймворк для создания MCP серверов
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) - протокол для взаимодействия с AI моделями

