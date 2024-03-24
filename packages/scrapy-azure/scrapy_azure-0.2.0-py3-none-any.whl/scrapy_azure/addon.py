from scrapy.settings import Settings


class AzureAddon:
    def update_settings(self, settings: Settings) -> None:
        feed_storages = settings.get("FEED_STORAGES") or {}
        feed_storages["wasbs"] = "scrapy_azure.feedstorage.AzureBlobFeedStorage"
        settings.set("FEED_STORAGES", feed_storages, priority="addon")
