#!/usr/bin/env  python3
from typing import List

from dynamojo import DynamojoConfig, IndexMap, JoinedAttribute, DynamojoBase

from .models import ArtifactBase
from .table import get_indexes
from .globals import TABLE

indexes = get_indexes()


class Tenant(ArtifactBase):
  name: str
  email: str
  owner_name: str

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="type",
                  partitionkey="tenant")
    ],
    table=TABLE,
    store_aliases=True,
    static_attributes=["name"],
    mutators=[]
  )


class ApiKey(ArtifactBase):
  name: str
  tenant: str
  namespaces: List[str]

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="type",
                  partitionkey="tenant")
    ],
    table=TABLE,
    store_aliases=True,
    static_attributes=["tenant"],
    mutators=[]
  )
  