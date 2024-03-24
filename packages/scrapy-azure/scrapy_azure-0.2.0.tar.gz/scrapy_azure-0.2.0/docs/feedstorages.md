# Feed storage backends

## Azure BLOB Storage

To enable the Azure BLOB Storage backend, use `AzureAddon` as follows:

```python
# Recommended
ADDONS = {"scrapy_azure.addon.AzureAddon": 1}

# You can configure FEED_STORAGES manually instead of using AzureAddon
FEED_STORAGES = {"wasbs": "scrapy_azure.feedstorage.AzureBlobFeedStorage"}
```

Then set `FEEDS` as follows:

```python
FEEDS = {
    "wasbs://myaccount.blob.core.windows.net/mycontainer/myblob": {
        "format": "jsonl",
        "overwrite": True,
    }
}
```
