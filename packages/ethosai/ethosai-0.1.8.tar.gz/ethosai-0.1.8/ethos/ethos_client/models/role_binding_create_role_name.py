from enum import Enum


class RoleBindingCreateRoleName(str, Enum):
    COLLABORATOR = "collaborator"
    OWNER = "owner"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
