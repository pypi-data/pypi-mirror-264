from logging import getLogger
from typing import Any

from sqlalchemy.orm import DeclarativeBase

from tgpm.exc import UserNotSet
from tgpm.model_permission_generator import PermissionType
from tgpm.resource_permission.repository import ResourcePermissionRepository

logger = getLogger(__name__)


class PermissionDenied(Exception):
    """
    Exception raised when permission is denied.
    """

    def __init__(self, resource_type: type[DeclarativeBase], resource_id, user_id, permission_type: PermissionType):
        """
        Initialize the PermissionDenied exception.

        :param resource_type: The type of the denied resource.
        :param resource_id: The ID of the denied resource.
        :param user_id: The ID of the user.
        """
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.user_id = user_id
        self.permission_type = permission_type


class ValidateThat[T]:
    def __init__(self, repository: ResourcePermissionRepository[T], user_id: Any = None):
        """
        Initialize the ValidateThat instance.

        :param repository: The repository for resource permissions.
        :type repository: ResourcePermissionRepository[T1, T2]
        :param user_id: The user ID, defaults to None.
        :type user_id: T1, optional
        """
        self.repository = repository
        self.user_id = user_id

    def __call__(self, user_id: Any):
        """
        Set the user ID for validation.

        :param user_id: The user ID.
        :type user_id: T1
        :return: Instance of ValidateThat.
        :rtype: ValidateThat
        """
        self.user_id = user_id
        return self

    async def can_read(self, resource_id: Any, *, user_id: Any = None) -> None:
        """
        Check if the user has read permission on the resource.

        :param resource_id: The resource ID.
        :type resource_id: T2
        :param user_id: The user ID, defaults to None.
        :type user_id: T1, optional
        :raises PermissionDenied: If permission is denied.
        """
        user_id = user_id or self.user_id
        if user_id is None:
            raise UserNotSet()
        if not await self.repository.has_permission_on(user_id, resource_id, PermissionType.READ):
            raise PermissionDenied(self.repository.statement_generator.resource_type, resource_id, user_id,
                                   PermissionType.READ)

    async def can_write(self, resource_id: Any, *, user_id: Any = None) -> None:
        """
        Check if the user has write permission on the resource.

        :param resource_id: The resource ID.
        :type resource_id: T2
        :param user_id: The user ID, defaults to None.
        :type user_id: T1, optional
        :raises PermissionDenied: If permission is denied.
        """
        user_id = user_id or self.user_id
        if user_id is None:
            raise UserNotSet()
        if not await self.repository.has_permission_on(user_id, resource_id, PermissionType.WRITE):
            raise PermissionDenied(self.repository.statement_generator.resource_type, resource_id, user_id,
                                   PermissionType.WRITE)
