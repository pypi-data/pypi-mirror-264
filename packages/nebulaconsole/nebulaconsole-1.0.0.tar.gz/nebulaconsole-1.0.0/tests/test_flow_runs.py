import time

import pytest

import nebula.client.schemas as client_schemas
from nebula import flow
from nebula.exceptions import FlowRunWaitTimeout
from nebula.flow_runs import wait_for_flow_run
from nebula.states import Completed


async def test_create_then_wait_for_flow_run(nebula_client):
    @flow
    def foo():
        pass

    flow_run = await nebula_client.create_flow_run(
        foo, name="petes-flow-run", state=Completed()
    )
    assert isinstance(flow_run, client_schemas.FlowRun)

    lookup = await wait_for_flow_run(flow_run.id, poll_interval=0)
    # Estimates will not be equal since time has passed
    assert lookup == flow_run
    assert flow_run.state.is_final()


async def test_create_then_wait_timeout(nebula_client):
    @flow
    def foo():
        time.sleep(9999)

    flow_run = await nebula_client.create_flow_run(
        foo,
        name="petes-flow-run",
    )
    assert isinstance(flow_run, client_schemas.FlowRun)

    with pytest.raises(FlowRunWaitTimeout):
        await wait_for_flow_run(flow_run.id, timeout=0)
