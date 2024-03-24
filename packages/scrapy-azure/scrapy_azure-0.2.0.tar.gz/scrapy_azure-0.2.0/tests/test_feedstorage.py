from scrapy_azure.feedstorage import AzureBlobFeedStorage


def test_azure_blob_feed_storage_with_sas_token() -> None:
    """Test AzureBlobFeedStorage.credential is None when SAS token is in the URI."""
    blob_uri = "https://contoso.blob.core.windows.net/mycontainer/myblob?s=1"
    storage = AzureBlobFeedStorage(blob_uri)
    assert storage.uri == blob_uri
    assert storage.credential is None


def test_azure_blob_feed_storage_without_sas_token() -> None:
    """Test AzureBlobFeedStorage.credential is not None when SAS token is not in the URI."""
    blob_uri = "https://contoso.blob.core.windows.net/mycontainer/myblob"
    storage = AzureBlobFeedStorage(blob_uri)
    assert storage.uri == blob_uri
    assert storage.credential is not None


def test_azure_blob_feed_storage_with_wasbs_scheme() -> None:
    """Test AzureBlobFeedStorage.uri starts with "https" when the original URI scheme is not "https"."""
    original_blob_uri = "wasbs://contoso.blob.core.windows.net/mycontainer/myblob"
    expected_blob_uri = "https://contoso.blob.core.windows.net/mycontainer/myblob"
    storage = AzureBlobFeedStorage(original_blob_uri)
    assert storage.uri == expected_blob_uri


def test_azure_blob_feed_storage_with_overwrite_option() -> None:
    """Test AzureBlobFeedStorage.should_overwrite is True when the overwrite option is True."""
    blob_uri = "https://contoso.blob.core.windows.net/mycontainer/myblob"
    storage = AzureBlobFeedStorage(blob_uri, feed_options={"overwrite": True})
    assert storage.uri == blob_uri
    assert storage.should_overwrite


def test_azure_blob_feed_storage_without_overwrite_option() -> None:
    """Test AzureBlobFeedStorage.should_overwrite is False when the overwrite option is not set."""
    blob_uri = "https://contoso.blob.core.windows.net/mycontainer/myblob"
    storage = AzureBlobFeedStorage(blob_uri)
    assert storage.uri == blob_uri
    assert not storage.should_overwrite
