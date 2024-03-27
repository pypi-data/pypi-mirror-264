from logging import getLogger
from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeBase, Mapper, RelationshipDirection, class_mapper
from sqlgen.joins import resolve_model_joins, NoValidJoins

from tgpm.model_permission_generator import PermissionType, PermissionModelProtocol, PermissionScope
from tgpm.registry import Registry

logger = getLogger(__name__)


class ResourcePermissionStatementGenerator[T]:
    """
    Class to generate permission statements for a given resource.
    """

    def __init__(self, registry: Registry, resource_type: type[DeclarativeBase]):
        """
        Initialize the ResourcePermissionStatementGenerator.

        :param registry: The registry instance containing the mapping between Model and PermissionModel.
        :type registry: Registry
        :param resource_type: The resource model type.
        :type resource_type: Type[DeclarativeBase]
        """
        self.resource_type = resource_type
        self.registry = registry

    def get_permission_queries(self, user_id: Any, resource_id: Any, permission_type: PermissionType):
        """
        Get all permission queries for a given user, resource, and permission type.


        :param user_id: The user ID.
        :type user_id: T1
        :param resource_id: The resource ID.
        :type resource_id: T2
        :param permission_type: The permission type.
        :type permission_type: PermissionType
        :return: List of permission queries.
        :rtype: list[Select]
        """
        resource_permission_type = self.registry[self.resource_type]
        return [
            Select(resource_permission_type).filter(resource_permission_type.resource_id == resource_id,
                                                    resource_permission_type.user_id == user_id,
                                                    resource_permission_type.type_ == permission_type),
        ] + self.get_parent_permission_queries(user_id, resource_id, permission_type)

    def get_parent_permission_queries(self, user_id: Any, resource_id: Any, permission_type: PermissionType):
        """
        Get parent permission queries for a given user, resource, and permission type.

        :param user_id: The user ID.
        :type user_id: T1
        :param resource_id: The resource ID.
        :type resource_id: T2
        :param permission_type: The permission type.
        :type permission_type: PermissionType
        :return: List of parent permission queries.
        :rtype: list[Select]
        """
        visited_entities = []

        def inner(mapper: Mapper):
            """
            Recursive function to traverse parent entities and retrieve permission queries.

            :param mapper: The mapper object.
            :type mapper: Mapper
            :return: List of permission queries.
            :rtype: list[Select]
            """
            if mapper in visited_entities:
                logger.debug("ignoring %s as already visited", mapper)
                return []
            visited_entities.append(mapper)
            queries = []
            for relationship in filter(lambda r: r.direction == RelationshipDirection.MANYTOONE, mapper.relationships):
                permission_model = self.registry.get(relationship.entity.class_)
                if permission_model is not None:
                    try:
                        queries.append(
                            self.make_query_for_parent_model(permission_model, user_id, resource_id, permission_type))
                    except NoValidJoins:
                        logger.warning("Cannot generate queries between %s and %s due to relationship been defined "
                                       "only on one %s side. "
                                       "No CHILDREN_ALLOWED or CHILDREN_DENIED will be validated for %s",
                                       permission_model, mapper.entity, mapper.entity, permission_model)
                        continue  # no need to check the parent relationship if there is none to this one
                else:
                    logger.warning(
                        "%s is not defined within registry %s. ignoring potential parent permissions from it for %s",
                        relationship.entity, self.registry, self.resource_type)
                queries += inner(relationship.entity)
            return queries

        return inner(class_mapper(self.resource_type))

    def make_query_for_parent_model(self, permission_model: PermissionModelProtocol, user_id: Any,
                                    resource_id: Any, permission_type: PermissionType) -> Select[T]:
        """
        Generate a query for the parent permission model.

        :param permission_model: The permission model.
        :type permission_model: PermissionModelProtocol
        :param user_id: The user ID.
        :type user_id: T1
        :param resource_id: The resource ID.
        :type resource_id: T2
        :param permission_type: The permission type.
        :type permission_type: PermissionType
        :return: The generated query.
        :rtype: Select
        """
        statement = Select(permission_model).join(permission_model.resource)
        joined_resource_type = permission_model.resource.entity.class_
        constraint = resolve_model_joins(joined_resource_type, self.resource_type)
        for join in constraint.joins:
            statement = statement.join(join)
        statement = statement.filter(
            permission_model.scope.in_([PermissionScope.CHILDREN_ALLOWED, PermissionScope.CHILDREN_DENIED]),
            permission_model.type_ == permission_type,
            permission_model.user_id == user_id,
            constraint.joined_column == resource_id,
        )
        return statement
