"""MCP server with date and time tools using FastMCP."""

from datetime import datetime
from typing import Any
from fastmcp import FastMCP

# Создание MCP сервера
mcp = FastMCP("Date and Time Server")


def format_mcp_response(text: str) -> dict[str, Any]:
    """Форматирует ответ в соответствии со стандартом MCP."""
    return {
        "content": [
            {
                "type": "text",
                "text": text
            }
        ]
    }


@mcp.tool()
async def get_current_datetime() -> dict[str, Any]:
    """Возвращает текущую дату и время в формате ISO 8601."""
    return format_mcp_response(datetime.now().isoformat())


@mcp.tool()
async def get_current_date() -> dict[str, Any]:
    """Возвращает текущую дату в формате YYYY-MM-DD."""
    return format_mcp_response(datetime.now().date().isoformat())


@mcp.tool()
async def get_current_time() -> dict[str, Any]:
    """Возвращает текущее время в формате HH:MM:SS."""
    return format_mcp_response(datetime.now().time().isoformat())


@mcp.tool()
async def get_current_timestamp() -> dict[str, Any]:
    """Возвращает текущий Unix timestamp (количество секунд с 1 января 1970 года)."""
    return format_mcp_response(str(datetime.now().timestamp()))


if __name__ == "__main__":
    mcp.run()
