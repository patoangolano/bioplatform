"""Admin panel endpoints for platform management."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_admin_user
from database import get_db
from models import Job, Sequence, User
from schemas import AdminUserUpdate, PlatformStats, SequenceResponse, UserRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserRead])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """Lista todos os usuarios com paginacao."""
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
    )
    return result.scalars().all()


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    payload: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """Atualiza campos de um usuario (ativar/desativar, tornar admin)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Remove um usuario da plataforma."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    await db.delete(user)
    await db.commit()


@router.get("/stats", response_model=PlatformStats)
async def platform_stats(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """Retorna estatisticas gerais da plataforma."""
    total_users = await db.scalar(select(func.count(User.id)))
    total_sequences = await db.scalar(select(func.count(Sequence.id)))
    total_jobs = await db.scalar(select(func.count(Job.id)))
    active_jobs = await db.scalar(
        select(func.count(Job.id)).where(Job.status.in_(["pending", "running"]))
    )
    completed_jobs = await db.scalar(
        select(func.count(Job.id)).where(Job.status == "completed")
    )
    failed_jobs = await db.scalar(
        select(func.count(Job.id)).where(Job.status == "failed")
    )

    return PlatformStats(
        total_users=total_users or 0,
        total_sequences=total_sequences or 0,
        total_jobs=total_jobs or 0,
        active_jobs=active_jobs or 0,
        completed_jobs=completed_jobs or 0,
        failed_jobs=failed_jobs or 0,
    )


@router.get("/sequences", response_model=list[SequenceResponse])
async def list_all_sequences(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """Lista todas as sequencias de todos os usuarios."""
    result = await db.execute(
        select(Sequence).offset(skip).limit(limit).order_by(Sequence.created_at.desc())
    )
    return result.scalars().all()


@router.get("/jobs")
async def list_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """Lista todos os jobs de todos os usuarios."""
    result = await db.execute(
        select(Job).offset(skip).limit(limit).order_by(Job.created_at.desc())
    )
    return [
        {
            "id": str(job.id),
            "sequence_id": str(job.sequence_id) if job.sequence_id else None,
            "job_type": job.job_type,
            "status": job.status,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error_message": job.error_message,
        }
        for job in result.scalars().all()
    ]
