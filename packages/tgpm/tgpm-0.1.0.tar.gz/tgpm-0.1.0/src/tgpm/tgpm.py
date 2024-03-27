from typing import TypeVar, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlgen import AsyncRepository, make_async_repository_class_for

from tgpm.model_permission_generator import ModelPermissionGenerator, PermissionModelProtocol, PermissionType
from tgpm.permission_adder import PermissionAdder
from tgpm.permission_validator import ValidateThat
from tgpm.registry import Registry
from tgpm.resource_permission.repository import ResourcePermissionRepository
from tgpm.resource_permission.statement_generator import ResourcePermissionStatementGenerator


class TGPM:
    """
    Class representing the system for managing permissions.
    This class handle te definition of the underlying permission system.
    """

    def __init__(self, user_model: type[DeclarativeBase], model_generator: ModelPermissionGenerator):
        """
        Initialize the Dradis system.

        :param user_model: The user model. (Must be a SQLAlchemy model defined on the same Base as the other
            models to generate permissions for)
        :type user_model: type[DeclarativeBase]
        """
        self.registry = Registry()
        self.user_model = user_model
        self.model_generator = model_generator

    def generate_permission_for_all_models(self):
        """
        Generate permissions models for all models defined in the sqlalchemy registry of the user model.
        Creating a new table for each one.

        Must be called after all models are defined or models created after must be manually included with
        get_permission_model_for.
        """

        models = [mapper.class_ for mapper in self.user_model.registry.mappers]
        models = filter(lambda model: model not in self.registry, models)
        self.registry.update(self.model_generator.generate_permission_models_for_models(models))

    def get_permission_model_for(self, resource_type: type[DeclarativeBase]) -> PermissionModelProtocol:
        """
        Get the permission model for a specific resource type. or generate one if not defined already.

        :param resource_type: The resource type.
        :type resource_type: type[DeclarativeBase]
        :return: The permission model.
        :rtype: PermissionModelProtocol
        """
        if resource_type not in self.registry:
            self.registry[resource_type] = self.model_generator.generate_permission_model_for(resource_type)
        return self.registry[resource_type]

    def use(self, session: AsyncSession) -> "AsyncConnectedTGPM":
        """
        Generate an instance of AsyncConnectedDradis allowing interaction with the permission system.

        :param session: The async session.
        :type session: AsyncSession
        :return: An instance of AsyncConnectedDradis.
        :rtype: AsyncConnectedTGPM
        """
        return AsyncConnectedTGPM(self, session)


T = TypeVar("T", bound=DeclarativeBase)


class AsyncConnectedTGPM[T]:
    """
    Class representing an instance of the permission system with a database session allowing it to interact
    with the permission system
    """

    def __init__(self, tgpm: TGPM, session: AsyncSession):
        """
        Initialize the async connected Dradis instance.

        :param tgpm: The Dradis system.
        :type tgpm: TGPM
        :param session: The async session.
        :type session: AsyncSession
        """
        self.tgpm = tgpm
        self.session = session

    def get_repository_for(self, resource_type: type[T]) -> AsyncRepository[T]:
        """
        Get the repository for a specific resource type.

        :param resource_type: The resource type.
        :type resource_type: type[DeclarativeBase]
        :return: The async repository.
        :rtype: AsyncRepository
        """
        permission_model = self.tgpm.get_permission_model_for(resource_type)
        permission_repository_type = make_async_repository_class_for(permission_model)
        return permission_repository_type(self.session)

    def add_permission_on(self, resource_type: type[T]) -> PermissionAdder[T]:
        """
        Add permission for a specific resource type.

        :param resource_type: The resource type.
        :type resource_type: type[DeclarativeBase]
        :return: The permission adder.
        :rtype: PermissionAdder
        """
        repository = self.get_repository_for(resource_type)
        return PermissionAdder(repository)

    def get_resource_permission_repository(self, resource_type: type[T]) -> ResourcePermissionRepository[T]:
        """
        get a permission repository for the given resource_type

        :param resource_type: The resource type.
        :type resource_type: type[DeclarativeBase]
        :return: The permission adder.
        :rtype: ResourcePermissionRepository[T]
        """
        statement_generator = ResourcePermissionStatementGenerator(self.tgpm.registry, resource_type)
        return ResourcePermissionRepository(self.session, statement_generator)

    def get_permission_validator(self, resource_type: type[T]) -> ValidateThat:
        """
        Get the permission validator for a specific resource type.

        :param resource_type: The resource type.
        :type resource_type: type[DeclarativeBase]
        :return: The permission validator.
        :rtype: ValidateThat
        """
        return ValidateThat(self.get_resource_permission_repository(resource_type))

    async def filter(self,
                     user_id: Any,
                     resources: list[T],
                     permission_type: PermissionType = PermissionType.READ
                     ) -> list[T]:
        """
        filter the list of resource returning only those that the given user can access

        :param user_id: the id of the user to check its permissions
        :param resources: the list of resources to filter
        :param permission_type: the type of permission to use for searching the allowed resource
        :return: a filtered list of resource with only those that the given user can read/write
            (depending on permission_type)
        """
        if len(resources) == 0:
            return resources
        resource_permission_repository = self.get_resource_permission_repository(resources[0].__class__)
        return [
            resource for resource in resources
            if await resource_permission_repository.has_permission_on(user_id, resource.id, permission_type)
        ]


def get_tgpm(user_model: type[DeclarativeBase]) -> TGPM:
    """
    factory to create a tgpm instance from a user model

    :param user_model: the user model to use for generating permissions
    :type user_model: type[DeclarativeBase]
    :return: a tgpm system instance
    :rtype: TGPM
    """
    return TGPM(user_model, ModelPermissionGenerator(user_model))
