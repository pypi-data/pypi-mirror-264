# Tagashy Generic Permission Manager

![pipeline](https://gitlab.com/Tagashy/tgpm/badges/develop/pipeline.svg)
![coverage](https://gitlab.com/Tagashy/tgpm/badges/develop/coverage.svg)
![release](https://gitlab.com/Tagashy/tgpm/-/badges/release.svg)

## Getting started


## Description
TGPM provide a permission management system where permissions can be set for different users on various resources. It supports different permission scopes like self, children allowed, and children denied, as well as different permission types like read and write. The PermissionDenied exception is raised when a user tries to perform an action without the necessary permissions. 


## Installation

`pip install tgpm`

## Usage

Most use-cases are documented in the integration tests.
### System instantiation
```python
from typing import Annotated

from tgpm.tgpm import AsyncConnectedTGPM, get_tgpm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
# WARNING CODE EXECUTION HERE
resource_security_manager = get_tgpm(User)
resource_security_manager.generate_permission_for_all_models()


# WARNING END CODE EXECUTION HERE
def get_connected_permission_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AsyncConnectedTGPM:
    return resource_security_manager.use(session)
```
### create permissions
```python
@router.post("/")
async def create_project(project: schemas.ProjectCreation,
                         service: Annotated[ProjectService, Depends(get_project_service)],
                         user: Annotated[User, Security(get_current_active_user, scopes=[Scopes.PROJECT_CREATE.value])],
                         connected_tgpm: Annotated[AsyncConnectedTGPM, Depends(get_connected_permission_service)],
                         ) -> schemas.Project:
    """
    create a project for a given customer.
    """
    project = await service.create_project(project.application_name, creator_id=user.id)
    permission = connected_tgpm.add_permission_on(Project).for_(user.id).with_(scope=PermissionScope.CHILDREN_ALLOWED)
    await permission.with_(permission_type=PermissionType.READ).where(resource_id=project.id)
    await permission.with_(permission_type=PermissionType.WRITE).where(resource_id=project.id)
    return project
```
### validate permissions
```python
class ResourceValidator:
    def __init__(self, model: type[DeclarativeBase]):
        self.model = model

    def __call__(self, connected_tgpm: Annotated[AsyncConnectedTGPM, Depends(get_connected_permission_service)]):
        return connected_tgpm.get_permission_validator(resource_type=self.model)

ProjectResourceValidator = ResourceValidator(Project)

@router.post("/")
async def create_host(
        project_id: UUID,
        user: Annotated[User, Security(get_current_active_user, scopes=[Scopes.HOST_CREATE.value])],
        validate_that: Annotated[ValidateThat, Depends(ProjectResourceValidator)],
        host: schemas.HostCreation,
        service: Annotated[HostService, Depends(get_host_service)]) -> schemas.Host:
    """
    allow to create a host directly.
    This endpoint is a public API but is currently unused by the code. It is available though swagger API

    :param host: the host information in the body
    :param service: the host service
    :return: the created host
    """
    await validate_that(user.id).can_write(project_id)
    return await service.create_host(host=host)
```
## Support

Contributions and feedback are welcome! You can:

- [create an issue](https://gitlab.com/Tagashy/tgpm/issues/new)
- look for TODO in the code and provide a MR with changes
- provide a MR for support of new class

## Roadmap

- Library Usage

## Authors and acknowledgment

Currently developed by Tagashy, but any help is welcomed and credited here.

## License

See the [LICENSE](LICENSE) file for licensing information as it pertains to
files in this repository.
