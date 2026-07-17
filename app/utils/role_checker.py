from fastapi import Depends
from fastapi import HTTPException

from app.utils.auth import get_current_user


class RoleChecker:

    def __init__(self, roles: list):

        self.roles = roles

    def __call__(
            self,
            current_user=Depends(get_current_user)
    ):

        if current_user.role not in self.roles:

            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )

        return current_user