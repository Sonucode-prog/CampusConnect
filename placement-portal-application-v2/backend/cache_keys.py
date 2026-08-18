from flask import request
from flask_jwt_extended import get_jwt_identity
from cache_utils import get_cache_version


def job_cache_key():
    version = get_cache_version("jobs")
    user_id = get_jwt_identity()

    return f"jobs:v{version}:user:{user_id}:{request.full_path}"


def student_job_cache_key():
    job_version = get_cache_version("jobs")
    application_version = get_cache_version("applications")
    user_id = get_jwt_identity()

    return (
        f"student_jobs:"
        f"jobs_v{job_version}:"
        f"applications_v{application_version}:"
        f"user:{user_id}:"
        f"{request.full_path}"
    )