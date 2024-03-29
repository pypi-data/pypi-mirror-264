from fastapi import APIRouter, Depends, HTTPException
from typing import List

from guisurfer.server.models import JobModel, V1UserProfile
from guisurfer.auth.transport import get_current_user
from guisurfer.job.base import Job

router = APIRouter()


@router.get("/v1/jobs", response_model=List[JobModel])
async def list_jobs(current_user: V1UserProfile = Depends(get_current_user)):
    jobs = Job.find(owner_id=current_user.email)
    return [job.to_schema() for job in jobs]


@router.get("/v1/jobs/{job_id}", response_model=JobModel)
async def get_job(job_id: str, current_user: V1UserProfile = Depends(get_current_user)):
    job = Job.find(id=job_id, owner_id=current_user.email)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job[0].to_schema()
