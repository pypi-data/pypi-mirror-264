from sqlalchemy.orm import DeclarativeBase

from tgpm.model_permission_generator import PermissionModelProtocol


class Registry(dict[type[DeclarativeBase], PermissionModelProtocol]):
    pass
