from fastapi import FastAPI, Query, HTTPException
from typing import Annotated

from schema import JobCreate, JobResponse, JobQuery
from db import connect_database, close_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/create-jobs", response_model=JobResponse)
def post_jobs(job_data: JobCreate):

    connection, cursor = connect_database()
    try:
        cursor.execute(
            """
            INSERT INTO jobs (model, input)
            VALUES (%s, %s)
            RETURNING id, model, input, status;
            """,
            (job_data.model, job_data.input)
        )
        job = cursor.fetchone()

        connection.commit()
        return {
            "id": job[0],
            "model": job[1],
            "input": job[2],
            "status": job[3],
        }
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        close_connection(connection, cursor)

@app.get("/jobs/{id}", response_model=JobResponse)
def get_job(query: Annotated[JobQuery, Query()]):
    connection, cursor = connect_database()

    try:
        cursor.execute(
            """
            SELECT id, model, input, status
            FROM jobs
            WHERE id = %s;
            """,
            (query.id, )
        )
        fetched_job = cursor.fetchone()
        if not fetched_job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {
            "id": fetched_job[0],
            "model": fetched_job[1],
            "input": fetched_job[2],
            "status": fetched_job[3],
        }
    except Exception as e:
        raise e
    finally:
        close_connection(connection, cursor)