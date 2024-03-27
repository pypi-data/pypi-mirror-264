![logo](LOGO.jpg)
# FastAPI2Cli\[ent]

![pipeline](https://gitlab.com/Tagashy/fastapi2cli/badges/master/pipeline.svg)
![coverage](https://gitlab.com/Tagashy/fastapi2cli/badges/master/coverage.svg)
![release](https://gitlab.com/Tagashy/fastapi2cli/-/badges/release.svg)

## Description

FastAPI2Cli\[ent] is a library to generate client for a [FastAPI](https://fastapi.tiangolo.com/) app.
It facilitates two primary usage scenarios:
- **[Typer CLI](https://typer.tiangolo.com/)**: Exposes every route of the FastAPI app through a [Typer](https://typer.tiangolo.com/) app. 
- **Library Usage**: Exports functions for calling the web server programmatically.

## Installation
You can install FastAPI2Cli[ent] via pip:

`pip install fastapi2cli`

## Usage

### Typer CLI

To generate a Typer app, use the **\`expose_app`** function:

```python
from fastapi2cli import expose_app
from fastapi import FastAPI

app = FastAPI()
@app.get("/user/{username}")
def get_user(username:str):
    ...

...

typer_app=expose_app(app)
typer_app()
```

This will output a CLI similar to:

```commandline
                                                                                
 Usage: test.py [OPTIONS] USERNAME                                              
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    username      TEXT  [default: None] [required]                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --server-url                PARSE_URL  the server base url (e.g.          │
│                                           https://127.0.0.1:443)             │
│                                           [default: None]                    │
│                                           [required]                         │
│    --install-completion                   Install completion for the current │
│                                           shell.                             │
│    --show-completion                      Show completion for the current    │
│                                           shell, to copy it or customize the │
│                                           installation.                      │
│    --help                                 Show this message and exit.        │
╰──────────────────────────────────────────────────────────────────────────────╯

```

FastAPI2Cli[ent] handles more complex scenarios for real apps. Here's an example with routers and dependencies:

#### router
the router expose two route, one for creating a host and one for a child model of a host.
Both of those app use some dependencies (the code is available after) and expect at least one path param and a body.
```python
router = APIRouter(
    prefix="/projects/{project_id}/hosts",
    tags=[Tags.HOST.value]
)


@router.post("/", dependencies=[Security(get_current_active_user, scopes=[Scopes.HOST_CREATE.value])])
async def create_host(host: schemas.HostCreation,
                      service: Annotated[HostService, Depends(get_host_service)]) -> schemas.Host:
    """
    allow to create a host directly.
    This endpoint is a public API but is currently unused by the code. It is available though swagger API

    :param host: the host information in the body
    :param service: the host service
    :return: the created host
    """
    return await service.create_host(host=host)

@router.post("/{host_id}/discovery",
             dependencies=[Security(get_current_active_user, scopes=[Scopes.HOST_READ.value])])
async def create_host_discovery(
        discovery: schemas.HostDiscoveryCreation,
        service: Annotated[HostDiscoveryService, Depends(get_host_discovery_service)]
) -> schemas.HostDiscovery:
    """
    create a discovery for a given host

    :param discovery: the data of the Host Discovery Scan
    :param service: host discovery service dependency for creating the info in db
    :return: the created DB model
    """
    return await service.create_discovery(discovery)

```

#### dependency
as we can see in the code the dependencies depends on other dependencies that needs the project_id defined as a path param in the router.
```python
async def get_db_session(
        session_maker: Annotated[async_sessionmaker, Depends(get_session_maker)]
) -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    async with session.begin():
        yield session


async def get_host_repository(session: Annotated[AsyncSession, Depends(get_db_session)],
                              project_id: UUID) -> HostRepository:
    return HostRepository(session, project_id=project_id)


async def get_host_service(repository: Annotated[HostRepository, Depends(get_host_repository)],
                           connection_manager: Annotated[
                               ConnectionManager, Depends(ConnectionManager.get_instance)]) -> HostService:
    return HostService(repository, connection_manager)

async def get_host_discovery_repository(session: Annotated[AsyncSession, Depends(get_db_session)],
                                        project_id: UUID, host_id: UUID) -> HostDiscoveryRepository:
    return HostDiscoveryRepository(session, project_id=project_id, host_id=host_id)


async def get_host_discovery_service(
        repository: Annotated[HostDiscoveryRepository, Depends(get_host_discovery_repository)]) -> HostDiscoveryService:
    return HostDiscoveryService(repository)
```
#### CLI Output

such example would generate the following commands:
```commandline
╭─ host ───────────────────────────────────────────────────────────────────────╮
│ create-host            allow to create a host directly. This endpoint is a   │
│                        public API but is currently unused by the code. It is │
│                        available though swagger API                          │
│ create-host-discovery  create a discovery for a given host                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```
##### Sub Commands
- create-host:
```commandline
 Usage: __main__.py create-host [OPTIONS] HOST_HOSTNAME PROJECT_ID              
                                                                                
 allow to create a host directly. This endpoint is a public API but is          
 currently unused by the code. It is available though swagger API               
 :param host: the host information in the body :param service: the host service 
 :return: the created host                                                      
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    host_hostname      TEXT  [default: None] [required]                     │
│ *    project_id         UUID  [default: None] [required]                     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --host-ip-address        IPVANYADDRESS  [default: None]                      │
│ --server-url             PARSE_URL      the server base url (e.g.            │
│                                         https://127.0.0.1:443)               │
│                                         [default: http://127.0.0.1:7465]     │
│ --help                                  Show this message and exit.          │
╰──────────────────────────────────────────────────────────────────────────────╯

```
- create-host-discovery:
```commandline
Usage: __main__.py create-host-discovery [OPTIONS] DISCOVERY_DIG               
                                          DISCOVERY_PING DISCOVERY_TRACEROUTE   
                                          DISCOVERY_SCAN_TCP DISCOVERY_SCAN_UDP 
                                          PROJECT_ID HOST_ID                    
                                                                                
 create a discovery for a given host                                            
 :param discovery: the data of the Host Discovery Scan :param service: host     
 discovery service dependency for creating the info in db :return: the created  
 DB model                                                                       
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    discovery_dig             TEXT  [default: None] [required]              │
│ *    discovery_ping            TEXT  [default: None] [required]              │
│ *    discovery_traceroute      TEXT  [default: None] [required]              │
│ *    discovery_scan_tcp        TEXT  [default: None] [required]              │
│ *    discovery_scan_udp        TEXT  [default: None] [required]              │
│ *    project_id                UUID  [default: None] [required]              │
│ *    host_id                   UUID  [default: None] [required]              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --server-url        PARSE_URL  the server base url (e.g.                     │
│                                https://127.0.0.1:443)                        │
│                                [default: http://127.0.0.1:7465]              │
│ --help                         Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### Complex Use Case

a more complex use-case would be the exposition of an app with some authentication for the user. 
this can be done like in the following snippet

```python
import asyncio

from rich.console import Console

from fastapi2cli.web.authentication import AuthenticationResolverBase
from jaws.webserver.authentication_manager import AuthenticationManagerInstance


class JawsAuthenticationResolver(AuthenticationResolverBase):
    def __init__(self, authentication_manager: AuthenticationManagerInstance):
        self.authentication_manager = authentication_manager

    def get_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer "+asyncio.run(self.authentication_manager.get_authentication_token())}


if __name__ == '__main__':
    from jaws.webserver.app import create
    from jaws.webserver.dependencies.user import get_current_user, get_current_active_user
    from jaws.webserver.dependencies.worker import get_current_active_api_key, get_api_key
    from jaws.config import Configuration
    from fastapi2cli import expose_app
    app = expose_app(
        create(),
        authenticated_dependencies=[get_current_user, get_current_active_user,
                                    get_api_key, get_current_active_api_key],
        server_url=Configuration.get_client_settings().SERVER_URL,
        authentication_resolver=JawsAuthenticationResolver(
            AuthenticationManagerInstance(Configuration.get_client_settings().SERVER_URL, Console()))
    )
    app()

```
This will output the following:
```commandline
 Usage: __main__.py [OPTIONS] COMMAND [ARGS]...                                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create-worker-registration   Create a new worker registration                │
│ get-user-by-id               Get a user by its id                            │
│ get-user-by-username         Get a user by its username                      │
│ get-users                    Get all the users                               │
│ login-for-access-token       login for OAuth2 username & password (& scopes) │
│ read-users-me                get the information about oneself               │
│ register                                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ customer ───────────────────────────────────────────────────────────────────╮
│ create-customer              allow to create a project directly.             │
│ get-customer-by-name         get a customer by its name                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ host ───────────────────────────────────────────────────────────────────────╮
│ create-host            allow to create a host directly. This endpoint is a   │
│                        public API but is currently unused by the code. It is │
│                        available though swagger API                          │
│ create-host-discovery  create a discovery for a given host                   │
│ get-host-by-id         get a host by its id                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ project ────────────────────────────────────────────────────────────────────╮
│ create-project          allow to create a project directly.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ webserver ──────────────────────────────────────────────────────────────────╮
│ create-webserver-discovery      create a discovery for a given webserver     │
│ take-webserver-by-id            get a webserver by its id                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ workloads ──────────────────────────────────────────────────────────────────╮
│ create-workload                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ health ─────────────────────────────────────────────────────────────────────╮
│ health                                                                       │
│ status       Get the status of the different process                         │
╰──────────────────────────────────────────────────────────────────────────────╯

```
### Library usage

(Work in Progress)

## Support

Contributions and feedback are welcome! You can:

- [create an issue](https://gitlab.com/Tagashy/fastapi2cli/issues/new)
- look for TODO in the code and provide a MR with changes
- provide a MR for support of new class

## Roadmap

- Library Usage

## Authors and acknowledgment

Currently developed by Tagashy, but any help is welcomed and credited here.
## License

See the [LICENSE](LICENSE) file for licensing information as it pertains to
files in this repository.
