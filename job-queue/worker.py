import time
import random

from typing import Optional

from db import connect_database, close_connection

def get_job(cursor, id: Optional[int], status: Optional[int], columns):

    cols_str = ", ".join(columns)
    if id and status == "pending":
        
        cursor.execute(
            f"""
            SELECT {cols_str}
            FROM jobs
            WHERE id = %s AND status = %s
            LIMIT 1
            FOR UPDATE SKIP LOCKED;
            """,
            (id, status)
        )
    elif not id:
        cursor.execute(
            f"""
            SELECT {cols_str}
            FROM jobs
            WHERE status = %s
            LIMIT 1
            FOR UPDATE SKIP LOCKED;
            """,
            (status,)
        )
    else:
        cursor.execute(
            f"""
            SELECT {cols_str}
            FROM jobs
            WHERE id = %s
            LIMIT 1;
            """,
            (id,)
        )

    row = cursor.fetchone()
    
    return row

def update_state(cursor, id, status):
    if status == "started":
        cursor.execute(
            """
            UPDATE jobs
            SET
                attempts = attempts + 1,
                status = "processing",
                started_at = NOW()
            WHERE id = %s;
            """,
            (id, )
        )
    elif status == "failed":
        cursor.execute(
            """
            UPDATE jobs
            SET
                status = 'failed',
            WHERE id = %s;
            """,
            (id,)
        )
    elif status == "completed":
        cursor.execute(
            """
            UPDATE jobs
            SET
                status = 'completed',
                completed = NOW()
            WHERE id = %s;
            """,
            (id,)
        )


def worker(id: Optional[int] = None):

    connection, cursor = connect_database()
    columns = ["id", "model", "input", "status", "attempts"]
    current_id = id

    try:
        status = "pending"

        row = get_job(cursor, id, status, columns)

        if not row:
            print("All rows are processed")
            return None

        current_id = row["id"]
        print(f"Fetched row id: {current_id}, updated status: {status}")

        if random.random() < 0.9:
            raise RuntimeError("Simulated Failure")
        
        time.sleep(5)
        status = "started"
        update_state(cursor, current_id, status)
        connection.commit()
        print(f"Processing row id: {current_id}, updated status: {status}")

        if random.random() < 0.1:
            raise RuntimeError("Simulated inference failure.")

        time.sleep(9)
        status = "completed"
        update_state(cursor, status, current_id)
        if random.random() < 0.1:
            raise RuntimeError("Simulated failure")

        connection.commit()

        row = get_job(cursor, current_id, status, columns)

        if random.random() < 0.1:
            raise RuntimeError("Simulated failure")
        
        
        print(f"Successfully processed row id: {current_id}, updated status: {status}")

        return {
            "id": row["id"],
            "model": row["model"],
            "input": row["input"],
            "status": row["status"],
        }
    except Exception as e:
        connection.rollback()
        print(f"Error processing job {current_id}: {e}")

        if current_id:
            cursor.execute("SELECT attempts FROM jobs WHERE id = %s;", (current_id,))
            err_row = cursor.fetchone()
            attempts = err_row["attempts"] if err_row else 5

            if attempts < 5:
                backoff_time = attempts * 3
                print(f"Retrying job {current_id} in {backoff_time}s (Attempt {attempts}/5)...")
                time.sleep(backoff_time)

                cursor.execute("UPDATE jobs SET status = 'pending' WHERE id = %s;", (current_id))
                connection.commit()
            else:
                print(f"Job {current_id} exceeded max attempts. marking as failed")
                update_state(cursor, current_id, "failed")
                connection.commit()
        return None
        
    finally:
        close_connection(connection, cursor)

# Testing worker
if __name__ == "__main__":
    worker()