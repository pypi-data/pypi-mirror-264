#!/usr/bin/env python3
from typing import Union, List

from bs4 import BeautifulSoup
from re import sub, match
from requests import get

from ..globals import S3

INDEX_PAGE_HTML = """
<html>
  <body>
    <h1>Simple Package Index</h1>
  </body>
</html>
"""

def fetch_index(url: str) -> BeautifulSoup:
  if url.startswith("s3://"):
    bucket = sub("s3://(.+)/.*", "\1", url)
    key = url.replace(f"s3://{bucket}", "")
    res = S3.get_object(
      Bucket=bucket,
      Key=key
    )["Body"]
    soup = BeautifulSoup(res.read().decode("utf-8"), "html.parser")
  else:
    res = get(url).text
    soup = BeautifulSoup(res, "html.parser")

  return soup


def get_index_links(sources: List[Union[str, BeautifulSoup]], url_base=None) -> str:
  if url_base and not url_base.endswith("/"):
    url_base += "/"
  sources.reverse()
  packages = {}
  for source in sources:
    if isinstance(source, BeautifulSoup):
      links = source.find_all("a")
    else:
      links = fetch_index(source).find_all("a")
    for link in links:
      if url_base and not match("(http(s)?//).+"):
        link["href"] = f"{url_base}{link['href']}"
      packages[str(link.string)] = link 
  return packages


def make_index_page(sources: List[Union[str, BeautifulSoup]]) -> str:
  links = list(get_index_links(sources).values())
  soup = BeautifulSoup(INDEX_PAGE_HTML, "html.parser")
  soup.body.extend(links)
  return str(soup)

