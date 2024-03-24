from datetime import datetime
from typing import List, Literal, Optional, Tuple
from uuid import UUID

from nebula.server.schemas.states import StateType
from nebula.server.utilities.schemas import NebulaBaseModel


class GraphState(NebulaBaseModel):
    id: UUID
    timestamp: datetime
    type: StateType
    name: str


class GraphArtifact(NebulaBaseModel):
    id: UUID
    created: datetime
    key: Optional[str]
    type: str
    is_latest: bool


class Edge(NebulaBaseModel):
    id: UUID


class Node(NebulaBaseModel):
    kind: Literal["flow-run", "task-run"]
    id: UUID
    label: str
    state_type: StateType
    start_time: datetime
    end_time: Optional[datetime]
    parents: List[Edge]
    children: List[Edge]
    artifacts: List[GraphArtifact]


class Graph(NebulaBaseModel):
    start_time: datetime
    end_time: Optional[datetime]
    root_node_ids: List[UUID]
    nodes: List[Tuple[UUID, Node]]
    artifacts: List[GraphArtifact]
    states: List[GraphState]
