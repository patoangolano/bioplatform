"""Tests for SQLAlchemy models."""

import pytest

from apps.api.models import Job, Sequence, User


def test_user_model_fields():
    """User model should have all expected fields."""
    assert hasattr(User, "id")
    assert hasattr(User, "email")
    assert hasattr(User, "hashed_password")
    assert hasattr(User, "full_name")
    assert hasattr(User, "is_active")
    assert hasattr(User, "is_admin")
    assert hasattr(User, "created_at")


def test_sequence_model_fields():
    """Sequence model should have all expected fields."""
    assert hasattr(Sequence, "id")
    assert hasattr(Sequence, "sequence_type")
    assert hasattr(Sequence, "raw_sequence")
    assert hasattr(Sequence, "description")
    assert hasattr(Sequence, "organism")
    assert hasattr(Sequence, "created_at")
    assert hasattr(Sequence, "updated_at")


def test_job_model_fields():
    """Job model should have all expected fields."""
    assert hasattr(Job, "id")
    assert hasattr(Job, "sequence_id")
    assert hasattr(Job, "job_type")


def test_user_table_name():
    """User table should be 'users'."""
    assert User.__tablename__ == "users"


def test_sequence_table_name():
    """Sequence table should be 'sequences'."""
    assert Sequence.__tablename__ == "sequences"


def test_job_table_name():
    """Job table should be 'jobs'."""
    assert Job.__tablename__ == "jobs"
