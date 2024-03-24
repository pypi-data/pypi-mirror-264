from scrapy.settings import Settings

from scrapy_azure.addon import AzureAddon


def test_update_settings() -> None:
    """Test AzureAddon.update_settings adds AzureBlobFeedStorage to FEED_STORAGES."""
    original_storage_scheme = "file"
    original_storage_backend = "scrapy.extensions.feedexport.FileFeedStorage"
    settings = Settings(
        {"FEED_STORAGES": {original_storage_scheme: original_storage_backend}}
    )

    addon = AzureAddon()
    addon.update_settings(settings)

    assert settings.getdict("FEED_STORAGES") == {
        original_storage_scheme: original_storage_backend,
        "wasbs": "scrapy_azure.feedstorage.AzureBlobFeedStorage",
    }
