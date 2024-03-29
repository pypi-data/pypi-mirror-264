#!/usr/bin/env python3
from __future__ import annotations

from typing import (
  Any,
  Dict,
  List
)

from boto3.dynamodb.conditions import Key, Attr
from dynamojo.index import IndexMap
from pydantic import validator
from dynamojo.config import DynamojoConfig, JoinedAttribute
from semantic_version import Version

from ..exceptions import InvalidVersion, NotFound
from ..globals import BUCKET, TABLE, S3_SIG4
from ..models import (
  ArtifactBase,
  Package,
  PackageStatus
)
from ..table import get_indexes


indexes = get_indexes() 


class TerraformModule(ArtifactBase):
  name: str
  provider: str
  owner: str = ""
  description: str = ""
  source: str = ""
  downloads: int = 0

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceNameProvider",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
      JoinedAttribute(
        attribute="typeNamespaceNameProvider",
        fields=[
          "type",
          "namespace",
          "name",
          "provider"
        ]
      )
    ],
    store_aliases=True,
    static_attributes=["name", "provider", "namespace", "dateTime"],
    mutators=[]
  )

  @property
  def versions(self) -> List[TerraformModuleVersion]:
    sk = self.typeNamespaceNameProvider.replace(self.type, TerraformModuleVersion.get_type())
    res = TerraformModuleVersion.query(
      KeyConditionExpression=Key("tenant").eq(self.tenant) & Key("typeNamespaceNameProvider").begins_with(sk)
    )
    return res.Items

  def get_versions(self, status: PackageStatus = None) -> List[TerraformModuleVersion]:
    if status is None:
      return self.versions
    else:
      sk = self.typeNamespaceNameProvider.replace(
        self.type, TerraformModuleVersion.get_type())
      res = TerraformModuleVersion.query(
        KeyConditionExpression=Key("tenant").eq(self.tenant) & Key(
          "typeNamespaceNameProvider").begins_with(sk),
        FilterExpression=Attr("status").eq(status.name)
      )
    return res.Items


class TerraformModuleVersion(Package):
  version: str
  name: str
  provider: str
  namespace: str
  published_at: str = None
  verified: bool = False
  downloads: int = 0
  package_data: Dict = {}
 
  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceNameProvider",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
      JoinedAttribute(
        attribute="typeNamespaceNameProvider",
        fields=[
          "type",
          "namespace",
          "name",
          "provider",
          "version"
        ]
      ),
      JoinedAttribute(
        attribute="id",
        separator="/",
        fields=[
          "namespace",
          "name",
          "provider",
          "version"
        ]
      )
    ],
    store_aliases=True,
    static_attributes=["name", "provider", "namespace", "dateTime", "version"],
    mutators=[]
  )

  def __init__(self, *args: List[Any], **kwargs: Dict[Any]):
    super().__init__(*args, **kwargs)

    if not self.module:
      raise NotFound("No matching module found for version")

    if self.published_at is None:
      self.published_at = self.dateTime

  @property
  def key(self) -> str:
    key = f"{self.s3_key_base}/{self.name}/{self.provider}/{self.version}.tgz"
    return key

  @property
  def module(self) -> TerraformModule:
    sk = "~".join([TerraformModule.get_type(), self.namespace, self.name, self.provider])
    module = TerraformModule.fetch(self.tenant, sk)
    return module

  def save(self, *args, **kwargs) -> Dict:
    existing_versions = [
      x.version for x in self.module.versions
    ]
    existing_versions.sort(key=lambda s: map(int, s.split('.')))
    if existing_versions and Version(self.version) < Version(existing_versions[-1]):
      raise InvalidVersion(f"Version {self.version} must be higher than {existing_versions[-1]} (Latest known version)")

    super().save(*args, **kwargs)

  @property
  def latest_version(self) -> TerraformModuleVersion:
    if not self.module:
      return
    versions = sorted(
      self.module.get_versions(status=PackageStatus.available),
      key=lambda x: x.item()["dateTime"]
    )
    if versions:
      return versions[-1]

  def presigned_post(self) -> Dict:
    if not self.module:
      raise NotFound(f"Module for {self.id} does not exist")

    if latest := self.latest_version:
      if Version(self.version) < Version(latest.version):
        raise InvalidVersion(
            f"Version {self.version} must be higher than {latest.version} (Latest known version)")
      if (
        latest.s3_object_exists()
        and latest.status == PackageStatus.available.name
      ):
        raise InvalidVersion(f"Version {self.id} already exists")

    self.status = PackageStatus.uploading
    self.save()

    res = S3_SIG4.generate_presigned_post(
      Bucket=BUCKET,
      Fields={"Content-Type": "application/tar+gzip"},
      Key=self.key,
      Conditions=[{"Content-Type": "application/tar+gzip"}],
      ExpiresIn=3600
    )
    return res
  
  def presigned_download(self) -> str:
    if not self.module:
      raise NotFound("Module does not exist. Create the module first, then upload a version")

    if self.status != PackageStatus.available.name:
      raise NotFound(f"Module version {self.id} does not exist")

    self.increment_downloads()
    self.increment_downloads()

    res = S3_SIG4.generate_presigned_url(
      "get_object",
      Params={
        "Bucket": BUCKET,
        "Key": self.key
      },
      ExpiresIn=30
    )

    return res

