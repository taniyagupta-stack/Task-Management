from fastapi import HTTPException

from database import get_connection


# Create a new task
def create_task_service(task):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, status, priority)
            VALUES (?, ?, ?, ?)
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority
            )
        )

        connection.commit()

        return {
            "message": "Task created successfully",
            "task_id": cursor.lastrowid,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        }

    finally:
        connection.close()


# Get tasks with pagination and filtering
def get_tasks_service(
    limit=10,
    offset=0,
    status=None,
    priority=None
):
    connection = get_connection()

    try:
        # SQL query to get tasks
        query = "SELECT * FROM tasks WHERE 1=1"

        # SQL query to count matching tasks
        count_query = "SELECT COUNT(*) FROM tasks WHERE 1=1"

        # Store query values
        params = []
        count_params = []

        # Filter tasks by status
        if status is not None:
            query += " AND status = ?"
            count_query += " AND status = ?"

            params.append(status)
            count_params.append(status)

        # Filter tasks by priority
        if priority is not None:
            query += " AND priority = ?"
            count_query += " AND priority = ?"

            params.append(priority)
            count_params.append(priority)

        # Count all tasks matching the filters
        total_tasks = connection.execute(
            count_query,
            count_params
        ).fetchone()[0]

        # Add pagination
        query += " ORDER BY id LIMIT ? OFFSET ?"

        params.extend([limit, offset])

        # Execute the query
        cursor = connection.execute(query, params)

        # Convert database rows into dictionaries
        tasks = [
            dict(row)
            for row in cursor.fetchall()
        ]

        return {
            "total_tasks": total_tasks,
            "returned_tasks": len(tasks),
            "limit": limit,
            "offset": offset,
            "tasks": tasks
        }

    finally:
        connection.close()


# Get one task by ID
def get_task_service(task_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return dict(task)

    finally:
        connection.close()


# Update a task
def update_task_service(task_id: int, task):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        existing_task = cursor.fetchone()

        if existing_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task_id
            )
        )

        connection.commit()

        return {
            "message": "Task updated successfully",
            "task_id": task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        }

    finally:
        connection.close()


# Delete a task
def delete_task_service(task_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        connection.commit()

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }

    finally:
        connection.close()