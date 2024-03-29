#!/usr/bin/env python3
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from hashlib import sha256
from re import match, sub
from typing import (
  Any,
  Dict,
  List,
  Union
)
from tarfile import open as open_tarfile
from urllib.parse import urlparse
from zipfile import ZipFile, is_zipfile

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from boto3.session import Session
from boto3 import resource
from bs4 import BeautifulSoup
from dynamojo.index import IndexMap
from dynamojo.config import DynamojoConfig, JoinedAttribute
from pydantic import validator
from html.parser import HTMLParser
from requests import head, get

from .indexes import make_index_page, get
from ..exceptions import AfxException, NotFound
from ..globals import BUCKET, TABLE, S3_SIG4, S3, LOGGER, HOSTNAME, BASE_URI
from ..models import (
  ArtifactBase,
  Package,
  PackageStatus
)
from ..table import get_indexes


indexes = get_indexes()

class PyPiRegistry(ArtifactBase):
  # Namespace is synonymous with name for this item
  index: str = None
  additional_indexes: List[str] = []

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespace",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
        JoinedAttribute(
            attribute="typeNamespace",
            fields=[
                "type",
                "namespace"
            ]
        )
    ],
    store_aliases=True,
    static_attributes=["name", "namespace", "dateTime"],
    mutators=[]
  )

  class IndexParser(HTMLParser):
    lasttag_type = None
    lasttag_href = None
    lasttag_data = None
    links = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
      self.lasttag_type = tag
      if tag == "a":
        self.lasttag_href = [x[1] for x in attrs if x[0] == "href"][0]

    def handle_data(self, data: Any):
      if self.lasttag_type == "a":
        self.links[data] = self.lasttag_href

  """
  def make_cache(self):
    for url in self.additional_indexes:
      links = get_index_links(url)
      for k, v in links.items():
        cache_item = PyPiCachedProject(
          tenant=self.tenant,
          url=v["href"],
          name=k
        )
        cache_item.save()
  """

  def batch_put_cache_items(self, items, index_url):
    index_loc = urlparse(index_url)
    if not index_url.endswith("/"):
      index_url += "/"

    table = Session().resource("dynamodb").Table(self._config.table)

    with table.batch_writer() as batch:
      for k, v in items.items():
        loc = urlparse(v)
        scheme = f"{loc.scheme or index_loc.scheme}://"
        if not loc.netloc:
          v = f"{index_loc.netloc}/{v}".replace("//", "/")

        v = f"{scheme}{v}"

        cache_item = PyPiCachedProject(
            tenant=self.tenant,
            url=v,
            name=k,
            namespace=self.namespace
        )
        batch.put_item(Item=cache_item._db_item())

  def make_cache(self):
    TABLE = resource("dynamodb").Table(self._config.table)

    for url in self.additional_indexes:
      if not url.endswith("/"):
        url += "/"

      res = get(url).content.decode("utf-8")
      if len(res) < 5000:
        print(res)
      parser = self.IndexParser()
      parser.feed(res)
      n = 30000
      link_list = list(parser.links.values())
      link_url_batches = [link_list[i:i + n] for i in range(0, len(link_list), n)]

      link_list = list(parser.links.keys())
      link_key_batches = [link_list[i:i + n] for i in range(0, len(link_list), n)]

      batches = [
        dict(zip(link_key_batches[i], link_url_batches[i])) for i, _ in enumerate(link_key_batches)
      ]

      with ThreadPoolExecutor() as X:
        X.map(self.batch_put_cache_items,  batches, [url for _ in batches])


  def cached_packages(self):
    sk = "~".join([PyPiCachedProject.get_type(), self.namespace, self.name])
    opts = {
      "KeyConditionExpression": Key("tenant").eq(self.tenant) & Key("typeNamespaceName").begins_with(sk)
    }
    items = []
    while True:
      res = self.query(**opts)
      items += res.Items
      if start_key := res.LastEvaluatedKey:
        opts["ExclusiveStartKey"] = start_key
      else:
        break

    return items

  @property
  def simple_index_key(self) -> str:
    return f"{self.tenant}/{self.type}/{self.namespace}/index.html"

  def presigned_index_download(self) -> str:
    res = S3.generate_presigned_url(
      "get_object",
      Params={
        "Bucket": BUCKET,
        "Key": self.simple_index_key
      }
    )
    return res

  def write_index(self) -> str:
    """
    Merges the current repository's index with any additional indexes.
    This can be wildly resource intensive is using something such as PyPi.org
    as an additional index. You should probably never ever call this from
    the API.
    """
    indexes = [
      BeautifulSoup(self.simple_index, "html.parser"),
      *self.additional_indexes
    ]
    html = make_index_page(indexes)
    S3.put_object(
      Body=html.encode(),
      Params={
        "Bucket": BUCKET,
        "Key": self.simple_index_key
      }
    )

  @property
  def projects(self) -> List[PyPiProject]:
    items = []
    sk = "~".join([PyPiProject.get_type(), self.namespace, ""])

    while True:
      opts = {
          "KeyConditionExpression": Key("tenant").eq(self.tenant) & Key("typeNamespaceName").begins_with(sk)
      }
      res = PyPiProject.query(**opts)

      if not res.LastEvaluatedKey:
        break

      opts["ExclusiveStartKey"] = res.LastEvaluatedKey

    items += res.Items

    return items

  @property
  def simple_index(self) -> str:
    html = f"""
    <html>
      <body>
        <h1>Package list for {self.namespace} registry</h1>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    url_base = f"https://{BASE_URI}/{self.tenant}/{self.namespace}/simple/"

    links = []
    for project in self.projects:
      href = f"{url_base}{project.name}"
      link = f"<a href=\"{href}\">{project.name}</a>"
      links.append(link)

    return str(soup)

  @validator("additional_indexes")
  def validate_urls(cls, vals):
    for val in vals:
      if not match("^(s3)|(https://).*", val):
        raise AfxException("Index url must be a valid S3 or HTTPS url")

      if val.startswith("https://"):
        try:
          res = head(val)
          res.raise_for_status()
        except Exception as e:
          raise AfxException(f"URL {val} returned with an invalid response: {e}")

      else:
        bucket = sub("s3://(.+)/.*", "\1", val)
        key = val.replace(f"s3://{bucket}", "")
        try:
          res = S3.list_objects_v2(Bucket=bucket, Prefix=key)
        except ClientError:
          res = []
        if "Contents" not in res:
          raise AfxException(f"Bucket or Key does not exist or cannot be accessed")

    return vals


class PyPiProject(ArtifactBase):
  name: str

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceName",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
      JoinedAttribute(
        attribute="typeNamespaceName",
        fields=[
          "type",
          "namespace",
          "name"
        ]
      )
    ],
    store_aliases=True,
    static_attributes=["name", "namespace", "dateTime"],
    mutators=[]
  )

  def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
    super().__init__(*args, **kwargs)
    if not self.registry:
      raise NotFound(f"Parent registry {self.namespace} does not exist.")

  @property
  def registry(self) -> str:
    sk = "~".join([PyPiRegistry.get_type(), self.namespace])
    return PyPiRegistry.fetch(self.tenant, sk)


  @classmethod
  def list(cls, tenant, namespace):
    items = []
    sk = "~".join([cls.get_type(), namespace, ""])
    LOGGER.info(sk)
    while True:
      opts = {
        "KeyConditionExpression": Key("tenant").eq(tenant) & Key("typeNamespaceName").begins_with(sk)
      }
      res = cls.query(**opts)

      if not res.LastEvaluatedKey:
        break

      opts["ExclusiveStartKey"] = res.LastEvaluatedKey

    items += res.Items

    return items

  @property
  def simple_package_index(self) -> str:
    html = """
    <html>
      <body>
        <h1>Files available for {self.name}</h1>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    for file in self.files:
      LOGGER.info(f"FILE: {file}")
      url = f"{file.url}#sha256={file.hash['sha256']}"
      link = f"<a href=\"{url}\" "
      if python_ver := file.metadata.get("requires_python"):
        link += f"data-requires-python=\"{python_ver}\" "
      link += f">{file.name}</a>"
      soup.body.append(link)

    return str(soup)

  @property
  def simple_index_key(self) -> str:
    return f"{self.tenant}/{self.type}/{self.namespace}/{self.name}/index.html"

  def write_index(self) -> str:
    html = self.simple_package_index
    S3.put_object(
      Body=html.encode(),
      Params={
        "Bucket": BUCKET,
        "Key": self.simple_index_key
      }
    )

  @property
  def files(self):
    sk = "~".join([f"{PyPiPackageFile.get_type()}", self.namespace, self.name, ""])
    res = PyPiPackageFile.query(
        KeyConditionExpression=Key("tenant").eq(self.tenant) & Key("typeNamespaceNameFilename").begins_with(sk)
    ).Items
    return res


  @validator("name", pre=True, always=True)
  def normalize_name(cls, name):
    return sub(r"[-_.]+", "-", name).lower()

  #def versions(self) -> List[PythonPackageVersion]:
  #  sk = "~".join([PythonPackageVersion.get_type(), self.namespace, self.name, ""])
  #  res = self.query(
  #    KeyConditionExpression=Key("tenant").eq(self.tenant) & Key("typeNamespaceName").begins_with(sk)
  #  )
  #  return res.Items

class PyPiPackageFile(Package):
  project_name: str
  filename: str
  url: str = None
  metadata: Dict[str, str]
  hash: Dict[str, str]
  yanked: Union[str, bool] = False
  dist_info_metadata: bool = False

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceNameFilename",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
      JoinedAttribute(
        attribute="typeNamespaceNameFilename",
        fields=[
          "type",
          "namespace",
          "project_name",
          "filename"
        ]
      )
    ],
    store_aliases=True,
    static_attributes=["name", "namespace", "dateTime"],
    mutators=[]
  )

  def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
    super().__init__(*args, **kwargs)
    if self.url is None:
      self.url = f"https://{HOSTNAME}{BASE_URI}/{self.tenant}/{self.namespace}/{self.project_name}/download/{self.filename}"

  @classmethod
  def get_hash(cls, fobj: Union[str, BytesIO]) -> Dict[str, str]:
    def get_hash(file_obj):
      hash = sha256()
      while True:
        data = file_obj.read(65536)
        if not data:
          break
        hash.update(data)
      return hash.hexdigest()

    if isinstance(fobj, str):
      with open(fobj, "rb") as f:
        res = {"sha256": get_hash(f)}
    else:
      res = {"sha256": get_hash(fobj)}

    return res

  @property
  def project(self):
    sk = "~".join([PyPiProject.get_type(), self.namespace, self.project_name])
    return PyPiProject.fetch(self.tenant, sk)

  @property
  def key(self) -> str:
    key = f"{self.s3_key_base}/{self.project_name}/{self.filename}"
    return key

  @classmethod
  def get_package_data(cls, fobj: BytesIO):
    def get_metadata_file():
      if is_zipfile(fobj):
        zfile = ZipFile(fobj)
        flist = zfile.namelist()
        fname = [x for x in flist if x.split("/")[1] in ("METADATA", "PKG-INFO")][0]
        lines = zfile.open(fname).readlines()
      else:
        fobj.seek(0)
        tfile = open_tarfile(fileobj=fobj, mode="r:gz")
        fname = [x.name for x in tfile.getmembers() if x.name.endswith("/PKG-INFO")][0]
        lines = tfile.extractfile(fname).readlines()
        LOGGER.info(f"METADATA readlines(): {lines}")
      
      return lines

    data = {}
    desc = ""
    for line in get_metadata_file():
      line = line.decode("utf-8").strip("\n")
      try:
        key, val = line.split(":")
        key = key.lower().replace("-", "_")
        val = val.strip()
        data[key] = val
      except ValueError:  # If there isn't a key then it's the description
        desc += line
    data["description"] = desc

    LOGGER.info(f"METADATA: {data}")
    return data

  def upload_to_s3(self, fobj: BytesIO):
    fobj.seek(0)
    S3.upload_fileobj(fobj, BUCKET, self.key)
    return True

  def presigned_upload(self) -> str:
    res = S3_SIG4.generate_presigned_post(
      "put_object",
      Params={
        "Bucket": BUCKET,
        "Key": self.key
      },
      ExpiresIn=630000,
      HttpMethod="POST"
    )
    self.status = PackageStatus.uploading.name
    self.save()

    return res

  def presigned_download(self) -> str:
    res = S3_SIG4.generate_presigned_url(
      "get_object",
      Params={
        "Bucket": BUCKET,
        "Key": self.key
      },
      ExpiresIn=30
    )
    return res


  def make_project(self):
    project = PyPiProject(
      tenant=self.tenant,
      name=self.project_name,
      namespace=self.namespace
    )
    project.save()
    return project


class PyPiCachedProject(ArtifactBase):
  name: str
  url: str = None

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceName",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
      JoinedAttribute(
        attribute="typeNamespaceName",
        fields=[
          "type",
          "namespace",
          "name"
        ]
      )
    ],
    store_aliases=True,
    static_attributes=["name", "namespace", "dateTime"],
    mutators=[]
  )


class PyPiCachedPackageFile(Package):
  project_name: str
  url: str = None

  _config = DynamojoConfig(
    indexes=indexes,
    index_maps=[
        IndexMap(index=indexes.table, sortkey="typeNamespaceNameFilename",
                  partitionkey="tenant")
    ],
    table=TABLE,
    joined_attributes=[
        JoinedAttribute(
            attribute="typeNamespaceName",
            fields=[
                "type",
                "namespace",
                "project_name"
            ]
        )
    ],
    store_aliases=True,
    static_attributes=["name", "namespace", "dateTime"],
    mutators=[]
  )
