import logging
from typing import Any, BinaryIO, Dict, Optional
from urllib.parse import urlparse, urlunparse

from azure.identity import DefaultAzureCredential
from azure.storage.blob import upload_blob_to_url
from scrapy.crawler import Crawler
from scrapy.extensions.feedexport import BlockingFeedStorage

logger = logging.getLogger(__name__)


def is_sas_token_in_url(url: str) -> bool:
    """Check if the URL contains a SAS token."""
    return "?" in url


def mask_sas_token(url: str) -> str:
    if is_sas_token_in_url(url):
        return urlunparse(urlparse(url)._replace(query="<SAS>"))
    return url


class AzureBlobFeedStorage(BlockingFeedStorage):
    def __init__(self, uri: str, *, feed_options: Optional[Dict[str, Any]] = None):
        feed_options = feed_options or {}
        self.should_overwrite = feed_options.get("overwrite", False)

        # The URI scheme must be "https"
        parsed_url = urlparse(uri)
        if parsed_url.scheme != "https":
            parsed_url = parsed_url._replace(scheme="https")
        self.uri = urlunparse(parsed_url)

        # If the URI contains a SAS token, use it as the credential
        if is_sas_token_in_url(self.uri):
            self.credential = None
        else:
            self.credential = DefaultAzureCredential()

        logger.info(
            "Initialized AzureBlobFeedStorage; URI=%s, overwrite=%s",
            mask_sas_token(self.uri),
            self.should_overwrite,
        )

    def _store_in_thread(self, file: BinaryIO) -> None:
        file.seek(0)
        result = upload_blob_to_url(
            self.uri,
            data=file,
            credential=self.credential,
            overwrite=self.should_overwrite,
        )
        file.close()
        logger.info(
            "Uploaded to Azure BLOB Storage; URI=%s, etag=%s, client_request_id=%s, request_id=%s",
            mask_sas_token(self.uri),
            result.get("etag"),
            result.get("client_request_id"),
            result.get("request_id"),
        )

    @classmethod
    def from_crawler(
        cls,
        crawler: Crawler,
        uri: str,
        *,
        feed_options: Optional[Dict[str, Any]] = None,
    ) -> "AzureBlobFeedStorage":
        return cls(uri, feed_options=feed_options)
