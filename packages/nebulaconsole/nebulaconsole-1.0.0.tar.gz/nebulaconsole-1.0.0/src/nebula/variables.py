from typing import Optional

from nebula.client.orchestration import NebulaClient
from nebula.client.utilities import get_or_create_client
from nebula.utilities.asyncutils import sync_compatible


@sync_compatible
async def get(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a variable by name. If doesn't exist return the default.
    ```
        from nebula import variables

        @flow
        def my_flow():
            var = variables.get("my_var")
    ```
    or
    ```
        from nebula import variables

        @flow
        async def my_flow():
            var = await variables.get("my_var")
    ```
    """
    variable = await _get_variable_by_name(name)
    return variable.value if variable else default


async def _get_variable_by_name(
    name: str,
    client: Optional[NebulaClient] = None,
):
    client, _ = get_or_create_client(client)
    variable = await client.read_variable_by_name(name)
    return variable
