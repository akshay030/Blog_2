# src/utils/permissions.py

from fastapi import Depends, HTTPException, status
from src.utils.helper import is_authenticated
from src.users.models import UserRole

def require_roles(*allowed_roles):
    def checker(user=Depends(is_authenticated)):

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return user

    return checker