from ..globals import BASE_URI

def discovery_json():
  return {
    "modules.v1": f"https://{BASE_URI}/v1/modules"
  }
