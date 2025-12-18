"""MCP server with date and time tools using FastMCP."""

import sqlite3
import json
from datetime import datetime
from typing import Any, Optional
from pathlib import Path
from fastmcp import FastMCP

# Создание MCP сервера
mcp = FastMCP("Date and Time Server")

# Путь к базе данных
DB_PATH = Path("tasks.db")


def init_database():
    """Инициализирует базу данных и создает таблицу заданий."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'in_progress',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect(DB_PATH)


# Инициализация базы данных при импорте
init_database()


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


@mcp.tool()
async def create_task(text: str) -> dict[str, Any]:
    """Создает новое задание с указанным текстом. Статус по умолчанию: 'in_progress'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO tasks (text, status, created_at) VALUES (?, ?, ?)",
        (text, "in_progress", created_at)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    result = {
        "id": task_id,
        "text": text,
        "status": "in_progress",
        "created_at": created_at,
        "completed_at": None
    }
    
    return format_mcp_response(json.dumps(result, ensure_ascii=False, indent=2))


@mcp.tool()
async def list_tasks(status: Optional[str] = None) -> dict[str, Any]:
    """Возвращает список заданий. Если указан status, фильтрует по статусу ('in_progress' или 'completed')."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status:
        cursor.execute(
            "SELECT id, text, status, created_at, completed_at FROM tasks WHERE status = ? ORDER BY created_at DESC",
            (status,)
        )
    else:
        cursor.execute(
            "SELECT id, text, status, created_at, completed_at FROM tasks ORDER BY created_at DESC"
        )
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append({
            "id": row[0],
            "text": row[1],
            "status": row[2],
            "created_at": row[3],
            "completed_at": row[4]
        })
    
    conn.close()
    
    result = {
        "tasks": tasks,
        "count": len(tasks)
    }
    
    return format_mcp_response(json.dumps(result, ensure_ascii=False, indent=2))


@mcp.tool()
async def get_task(task_id: int) -> dict[str, Any]:
    """Возвращает задание по его ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, text, status, created_at, completed_at FROM tasks WHERE id = ?",
        (task_id,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return format_mcp_response(json.dumps({"error": f"Задание с ID {task_id} не найдено"}, ensure_ascii=False))
    
    result = {
        "id": row[0],
        "text": row[1],
        "status": row[2],
        "created_at": row[3],
        "completed_at": row[4]
    }
    
    return format_mcp_response(json.dumps(result, ensure_ascii=False, indent=2))


@mcp.tool()
async def complete_task(task_id: int) -> dict[str, Any]:
    """Помечает задание как выполненное. Устанавливает статус 'completed' и время выполнения."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем, существует ли задание
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        return format_mcp_response(json.dumps({"error": f"Задание с ID {task_id} не найдено"}, ensure_ascii=False))
    
    completed_at = datetime.now().isoformat()
    cursor.execute(
        "UPDATE tasks SET status = 'completed', completed_at = ? WHERE id = ?",
        (completed_at, task_id)
    )
    conn.commit()
    
    # Получаем обновленное задание
    cursor.execute(
        "SELECT id, text, status, created_at, completed_at FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    result = {
        "id": row[0],
        "text": row[1],
        "status": row[2],
        "created_at": row[3],
        "completed_at": row[4]
    }
    
    return format_mcp_response(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    mcp.run()
