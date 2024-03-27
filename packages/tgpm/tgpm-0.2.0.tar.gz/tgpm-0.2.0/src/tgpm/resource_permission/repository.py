from logging import getLogger
from typing import Sequence, Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from tgpm.model_permission_generator import PermissionType, PermissionScope, PermissionModelProtocol
from tgpm.resource_permission.statement_generator import ResourcePermissionStatementGenerator

logger = getLogger(__name__)


class ResourcePermissionRepository[T]:
    """
    Repository class for resource permissions.
    """

    def __init__(self, session: AsyncSession, statement_generator: ResourcePermissionStatementGenerator[T]):
        """
        Initialize the ResourcePermissionRepository.

        :param session: The async session.
        :type session: AsyncSession
        :param statement_generator: The statement generator.
        :type statement_generator: ResourcePermissionStatementGenerator[T1, T2]
        """
        self.session = session
        self.statement_generator = statement_generator

    async def has_permission_on(self, user_id: Any, resource_id: Any, permission_type: PermissionType) -> bool:
        """
        Check if the user has permission on the resource.

        :param user_id: The user ID.
        :type user_id: T1
        :param resource_id: The resource ID.
        :type resource_id: T2
        :param permission_type: The permission type.
        :type permission_type: PermissionType
        :return: True if the user has permission, False otherwise.
        :rtype: bool
        """
        permission_queries = self.statement_generator.get_permission_queries(user_id, resource_id, permission_type)
        permissions = await self.get_permissions(permission_queries)

        if any(permission.scope in [PermissionScope.DENIED, PermissionScope.CHILDREN_DENIED] for permission in
               permissions if permission is not None):
            denied_permissions = (permission for permission in permissions
                                  if permission is not None and permission.scope in [PermissionScope.DENIED,
                                                                                     PermissionScope.CHILDREN_DENIED])
            logger.info("User %s explicitly denied access to resource %s:%s due to %s", user_id,
                        self.statement_generator.resource_type, resource_id, denied_permissions)
            return False
        if all(permission is None for permission in permissions):
            logger.debug("User %s has no permissions matching resource %s:%s", user_id,
                         self.statement_generator.resource_type, resource_id)
            return False
        return True

    async def get_permissions(self, permission_queries: Sequence[Select]) -> list[PermissionModelProtocol]:
        """
        Execute a list of query and return a permission if matching or none for each query

        :param permission_queries: the list of queries to execute
        :type permission_queries: Sequence[Select]
        :return: a list of permission models or None
        """
        return [(await self.session.execute(query)).unique().scalars().one_or_none() for query in permission_queries]
