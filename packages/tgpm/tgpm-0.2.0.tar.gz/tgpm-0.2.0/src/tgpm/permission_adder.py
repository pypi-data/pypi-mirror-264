from typing import Any

from sqlgen import AsyncRepository

from tgpm.exc import UserNotSet
from tgpm.model_permission_generator import PermissionScope, PermissionType


class PermissionAdder[T]:
    """
    Class to add permissions to a repository in a human-readable way.
    """

    def __init__(self, repository: AsyncRepository[T], permission_scope: PermissionScope = PermissionScope.SELF,
                 permission_type: PermissionType = PermissionType.READ,
                 user_id=None):
        """
        Initialize the PermissionAdder.

        :param repository: The AsyncRepository instance for permission model.
        :type repository: AsyncRepository
        :param permission_scope: The permission scope to generate.
        :type permission_scope: PermissionScope, optional
        :param permission_type: The permission type to generate.
        :type permission_type: PermissionType, optional
        :param user_id: The user ID.
        :type user_id: T1, optional
        """
        self.repository = repository
        self.permission_scope = permission_scope
        self.permission_type = permission_type
        self.user_id = user_id

    def for_(self, user_id: Any) -> "PermissionAdder[T]":
        """
        Specify the user ID for whom the permission is being added.

        :param user_id: The user ID.
        :type user_id: Any
        :return: Self
        :rtype: PermissionAdder[T]
        """
        self.user_id = user_id
        return self

    def with_(self, *, scope: PermissionScope = None,
              permission_type: PermissionType = None) -> "PermissionAdder[T]":
        """
        Specify the scope and/or permission type.

        :param scope: The permission scope.
        :type scope: PermissionScope, optional
        :param permission_type: The permission type.
        :type permission_type: PermissionType, optional
        :return: Self
        :rtype: PermissionAdder[T1, T2, T3]
        """
        if scope is not None:
            self.permission_scope = scope
        if permission_type is not None:
            self.permission_type = permission_type
        return self

    async def where(self, *, resource_id: Any):
        """
        Specify the resource ID and add the permission to the repository.

        :param resource_id: The resource ID.
        :type resource_id: T2
        :return: The result of creating the permission.
        :rtype: T3
        :raises UserNotSet: If user ID is not set before calling this method.
        """
        if self.user_id is None:
            raise UserNotSet()
        return await create_permission(self.repository, self.user_id, resource_id, self.permission_scope,
                                       self.permission_type)


async def create_permission(repository: AsyncRepository, user_id, resource_id, permission_scope: PermissionScope,
                            permission_type: PermissionType):
    """
    Create a permission in the repository.

    :param repository: The AsyncRepository instance for permission model.
    :type repository: AsyncRepository
    :param user_id: The user ID.
    :param resource_id: The resource ID.
    :param permission_scope: The permission scope.
    :type permission_scope: PermissionScope
    :param permission_type: The permission type.
    :type permission_type: PermissionType
    :return: The result of creating the permission.
    :rtype: T3
    """
    return await repository.create(
        user_id=user_id,
        resource_id=resource_id,
        scope=permission_scope,
        type_=permission_type,
    )
