import enum
from logging import getLogger
from typing import Protocol
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, class_mapper, Mapped, MappedColumn, relationship, \
    RelationshipProperty

logger = getLogger(__name__)


class PermissionScope(enum.Enum):
    """Enumeration representing the scope of permissions."""
    DENIED = "denied"  # for denying a specific resource allowed through children_allowed
    SELF = "self"  # allow only on self
    CHILDREN_ALLOWED = "children_allowed"  # allow self and children objects
    CHILDREN_DENIED = "children_denied"  # for denying child resources


class PermissionType(enum.Enum):
    READ = "read"
    WRITE = "write"  # no delete or update as if you can write you can blank the resource with is logically a delete


def get_primary_key(model: type[DeclarativeBase]) -> Column:
    mapper = class_mapper(model)
    assert len(mapper.primary_key) == 1
    return mapper.primary_key[0]


def get_foreign_key_for(model: type[DeclarativeBase]) -> ForeignKey:
    """
    generate a ForeignKey on the provided model primary key

    :param model: the model to get the primary key from
    :return: a foreign key on the primary key of model
    """

    return ForeignKey(get_primary_key(model))


class PermissionModelProtocol(Protocol):
    __tablename__: str
    user_id: MappedColumn
    resource_id: MappedColumn
    resource: RelationshipProperty
    scope: Mapped[PermissionScope]
    type_: Mapped[PermissionType]


class ModelPermissionGenerator:
    """Class to generate permission models for resources."""
    PERMISSION_SUFFIX = "permissions"

    def __init__(self, user_model: type[DeclarativeBase]):
        """
        Initialize the ModelPermissionGenerator.

        :param user_model: The user model class.
        :type user_model: Type[DeclarativeBase]
        """
        self.user_model = user_model

        class Base(DeclarativeBase):
            metadata = user_model.metadata
            registry = user_model.registry

        self.bases = (Base,)

    def generate_permission_model_for(self, model: type[DeclarativeBase]) -> type[PermissionModelProtocol]:
        """
        Generate a permission model for the specified resource model.

        :param model: The resource model class.
        :type model: Type[DeclarativeBase]
        :return: The generated permission model class.
        :rtype: Type[PermissionModelProtocol]
        """
        resource_id = mapped_column(get_foreign_key_for(model))
        attrs = {
            "__tablename__": f"{model.__tablename__}_{self.user_model.__tablename__}_{ModelPermissionGenerator.PERMISSION_SUFFIX}",
            "id": mapped_column(primary_key=True, default=uuid4),
            "user_id": mapped_column(get_foreign_key_for(self.user_model)),
            "resource_id": resource_id,
            "resource": relationship(model, foreign_keys=[resource_id]),
            "scope": mapped_column(nullable=False, default=PermissionScope.SELF, ),
            "type_": mapped_column(nullable=False, ),
            "__annotations__": {"id": Mapped[UUID], "scope": Mapped[PermissionScope], "type_": Mapped[PermissionType]}

        }
        permission_model = type(model.__name__ + "Permission", self.bases, attrs)
        logger.debug("Generated permission_model='%s' for model='%s'", permission_model, model)
        return permission_model

    def generate_permission_models_for_models(
            self,
            models: list[type[DeclarativeBase]]
    ) -> dict[type[DeclarativeBase], PermissionModelProtocol]:
        return {
            model: self.generate_permission_model_for(model) for model in models
            if not model.__tablename__.endswith(ModelPermissionGenerator.PERMISSION_SUFFIX)
        }
