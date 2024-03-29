#!/usr/bin/env python3
from json import dumps
from sys import stdin, stdout
from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from mangum import Mangum

from .models import TerraformModule, TerraformModuleVersion
from .well_known import discovery_json
from ..exceptions import AfxException, NotFound
from ..globals import BASE_URI, LOGGER


APP = FastAPI()
MANGUM = Mangum(APP, lifespan="off")
routes = {
  "upload_module": f"{BASE_URI}/modules/upload_version/",
  "create_module": f"{BASE_URI}/modules/create/",
  "download_module": f"{BASE_URI}/modules/{{tenant}}/{{namespace}}/{{name}}/{{provider}}/{{version}}"
}


@APP.exception_handler(Exception)
def custom_exceptions(_: Any, e: Exception):
  if isinstance(e, NotFound):
    return JSONResponse(status_code=404, content={"error": str(e)})

  if isinstance(e, AfxException):
    return JSONResponse(status_code=400, content={"error": str(e)})

  LOGGER.exception(e)
  return JSONResponse(status_code=500, content={"message": "Internal Server Error", "code": 500})


@APP.get("/.well-known/terraform.json")
def discovery():
  data = discovery_json()
  return data


@APP.post(routes["create_module"])
def create_module(module: TerraformModule):
  module.save()
  LOGGER.info(f"Called create module with request: {module}")
  return module.item()


@APP.get(routes["download_module"])
def download_module(tenant, namespace, name, provider, version):
  sk = "~".join([TerraformModuleVersion.get_type(), namespace, name, provider, version])
  try:
    module = TerraformModuleVersion.fetch(tenant, sk, fail_if_missing=True)
  except NotFound:
    raise NotFound(f"No matching module found for {module.id}")

  res = module.presigned_download()

  return RedirectResponse(res, status_code=301)


@APP.post(routes["upload_module"])
def upload_module_version(version: TerraformModuleVersion):
  LOGGER.info(f"Creating db item for TF Module version: {version.id}")
  return version.presigned_post()


def handler(event, ctx):
  LOGGER.info(f"Routes: {routes}")
  LOGGER.info(f"Event: {dumps(event, indent=2, default=lambda x: str(x))}")
  return MANGUM(event, ctx)
