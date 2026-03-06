"""
String constants for the `resources` parameter of each Creators API operation.

Usage:
    from amazon_creators_async_api.resources import SearchItemsResources, GetItemsResources

    await client.search_items(
        keywords="laptop",
        resources=[
            SearchItemsResources.IMAGES_PRIMARY_LARGE,
            SearchItemsResources.ITEM_INFO_TITLE,
            SearchItemsResources.OFFERS_V2_PRICE,
        ],
    )
"""


class SearchItemsResources:
    """Valid resource strings for the SearchItems operation."""

    # BrowseNodeInfo
    BROWSE_NODE_INFO_BROWSE_NODES = "browseNodeInfo.browseNodes"
    BROWSE_NODE_INFO_BROWSE_NODES_ANCESTOR = "browseNodeInfo.browseNodes.ancestor"
    BROWSE_NODE_INFO_BROWSE_NODES_SALES_RANK = "browseNodeInfo.browseNodes.salesRank"
    BROWSE_NODE_INFO_WEBSITE_SALES_RANK = "browseNodeInfo.websiteSalesRank"

    # Images
    IMAGES_PRIMARY_SMALL = "images.primary.small"
    IMAGES_PRIMARY_MEDIUM = "images.primary.medium"
    IMAGES_PRIMARY_LARGE = "images.primary.large"
    IMAGES_VARIANTS_SMALL = "images.variants.small"
    IMAGES_VARIANTS_MEDIUM = "images.variants.medium"
    IMAGES_VARIANTS_LARGE = "images.variants.large"

    # ItemInfo
    ITEM_INFO_BY_LINE_INFO = "itemInfo.byLineInfo"
    ITEM_INFO_CLASSIFICATIONS = "itemInfo.classifications"
    ITEM_INFO_CONTENT_INFO = "itemInfo.contentInfo"
    ITEM_INFO_CONTENT_RATING = "itemInfo.contentRating"
    ITEM_INFO_EXTERNAL_IDS = "itemInfo.externalIds"
    ITEM_INFO_FEATURES = "itemInfo.features"
    ITEM_INFO_MANUFACTURE_INFO = "itemInfo.manufactureInfo"
    ITEM_INFO_PRODUCT_INFO = "itemInfo.productInfo"
    ITEM_INFO_TECHNICAL_INFO = "itemInfo.technicalInfo"
    ITEM_INFO_TITLE = "itemInfo.title"
    ITEM_INFO_TRADE_IN_INFO = "itemInfo.tradeInInfo"

    # OffersV2
    OFFERS_V2_AVAILABILITY = "offersV2.listings.availability"
    OFFERS_V2_CONDITION = "offersV2.listings.condition"
    OFFERS_V2_DEAL_DETAILS = "offersV2.listings.dealDetails"
    OFFERS_V2_IS_BUY_BOX_WINNER = "offersV2.listings.isBuyBoxWinner"
    OFFERS_V2_LOYALTY_POINTS = "offersV2.listings.loyaltyPoints"
    OFFERS_V2_MERCHANT_INFO = "offersV2.listings.merchantInfo"
    OFFERS_V2_PRICE = "offersV2.listings.price"
    OFFERS_V2_TYPE = "offersV2.listings.type"

    # Other
    PARENT_ASIN = "ParentASIN"
    SEARCH_REFINEMENTS = "searchRefinements"


class GetItemsResources:
    """Valid resource strings for the GetItems operation."""

    # BrowseNodeInfo
    BROWSE_NODE_INFO_BROWSE_NODES = "browseNodeInfo.browseNodes"
    BROWSE_NODE_INFO_BROWSE_NODES_ANCESTOR = "browseNodeInfo.browseNodes.ancestor"
    BROWSE_NODE_INFO_BROWSE_NODES_SALES_RANK = "browseNodeInfo.browseNodes.salesRank"
    BROWSE_NODE_INFO_WEBSITE_SALES_RANK = "browseNodeInfo.websiteSalesRank"

    # Images
    IMAGES_PRIMARY_SMALL = "images.primary.small"
    IMAGES_PRIMARY_MEDIUM = "images.primary.medium"
    IMAGES_PRIMARY_LARGE = "images.primary.large"
    IMAGES_VARIANTS_SMALL = "images.variants.small"
    IMAGES_VARIANTS_MEDIUM = "images.variants.medium"
    IMAGES_VARIANTS_LARGE = "images.variants.large"

    # ItemInfo
    ITEM_INFO_BY_LINE_INFO = "itemInfo.byLineInfo"
    ITEM_INFO_CLASSIFICATIONS = "itemInfo.classifications"
    ITEM_INFO_CONTENT_INFO = "itemInfo.contentInfo"
    ITEM_INFO_CONTENT_RATING = "itemInfo.contentRating"
    ITEM_INFO_EXTERNAL_IDS = "itemInfo.externalIds"
    ITEM_INFO_FEATURES = "itemInfo.features"
    ITEM_INFO_MANUFACTURE_INFO = "itemInfo.manufactureInfo"
    ITEM_INFO_PRODUCT_INFO = "itemInfo.productInfo"
    ITEM_INFO_TECHNICAL_INFO = "itemInfo.technicalInfo"
    ITEM_INFO_TITLE = "itemInfo.title"
    ITEM_INFO_TRADE_IN_INFO = "itemInfo.tradeInInfo"

    # OffersV2
    OFFERS_V2_AVAILABILITY = "offersV2.listings.availability"
    OFFERS_V2_CONDITION = "offersV2.listings.condition"
    OFFERS_V2_DEAL_DETAILS = "offersV2.listings.dealDetails"
    OFFERS_V2_IS_BUY_BOX_WINNER = "offersV2.listings.isBuyBoxWinner"
    OFFERS_V2_LOYALTY_POINTS = "offersV2.listings.loyaltyPoints"
    OFFERS_V2_MERCHANT_INFO = "offersV2.listings.merchantInfo"
    OFFERS_V2_PRICE = "offersV2.listings.price"
    OFFERS_V2_TYPE = "offersV2.listings.type"

    # Other
    PARENT_ASIN = "ParentASIN"


class GetVariationsResources:
    """Valid resource strings for the GetVariations operation."""

    # BrowseNodeInfo
    BROWSE_NODE_INFO_BROWSE_NODES = "browseNodeInfo.browseNodes"
    BROWSE_NODE_INFO_BROWSE_NODES_ANCESTOR = "browseNodeInfo.browseNodes.ancestor"
    BROWSE_NODE_INFO_BROWSE_NODES_SALES_RANK = "browseNodeInfo.browseNodes.salesRank"
    BROWSE_NODE_INFO_WEBSITE_SALES_RANK = "browseNodeInfo.websiteSalesRank"

    # Images
    IMAGES_PRIMARY_SMALL = "images.primary.small"
    IMAGES_PRIMARY_MEDIUM = "images.primary.medium"
    IMAGES_PRIMARY_LARGE = "images.primary.large"
    IMAGES_VARIANTS_SMALL = "images.variants.small"
    IMAGES_VARIANTS_MEDIUM = "images.variants.medium"
    IMAGES_VARIANTS_LARGE = "images.variants.large"

    # ItemInfo
    ITEM_INFO_BY_LINE_INFO = "itemInfo.byLineInfo"
    ITEM_INFO_CLASSIFICATIONS = "itemInfo.classifications"
    ITEM_INFO_CONTENT_INFO = "itemInfo.contentInfo"
    ITEM_INFO_CONTENT_RATING = "itemInfo.contentRating"
    ITEM_INFO_EXTERNAL_IDS = "itemInfo.externalIds"
    ITEM_INFO_FEATURES = "itemInfo.features"
    ITEM_INFO_MANUFACTURE_INFO = "itemInfo.manufactureInfo"
    ITEM_INFO_PRODUCT_INFO = "itemInfo.productInfo"
    ITEM_INFO_TECHNICAL_INFO = "itemInfo.technicalInfo"
    ITEM_INFO_TITLE = "itemInfo.title"
    ITEM_INFO_TRADE_IN_INFO = "itemInfo.tradeInInfo"

    # OffersV2
    OFFERS_V2_AVAILABILITY = "offersV2.listings.availability"
    OFFERS_V2_CONDITION = "offersV2.listings.condition"
    OFFERS_V2_DEAL_DETAILS = "offersV2.listings.dealDetails"
    OFFERS_V2_IS_BUY_BOX_WINNER = "offersV2.listings.isBuyBoxWinner"
    OFFERS_V2_LOYALTY_POINTS = "offersV2.listings.loyaltyPoints"
    OFFERS_V2_MERCHANT_INFO = "offersV2.listings.merchantInfo"
    OFFERS_V2_PRICE = "offersV2.listings.price"
    OFFERS_V2_TYPE = "offersV2.listings.type"

    # VariationSummary
    VARIATION_SUMMARY_PAGE_COUNT = "variationSummary.pageCount"
    VARIATION_SUMMARY_PRICE_RANGE = "variationSummary.priceRange"
    VARIATION_SUMMARY_VARIATION_COUNT = "variationSummary.variationCount"

    # Other
    PARENT_ASIN = "ParentASIN"


class GetBrowseNodesResources:
    """Valid resource strings for the GetBrowseNodes operation."""

    BROWSE_NODES_ANCESTOR = "browseNodes.ancestor"
    BROWSE_NODES_CHILDREN = "browseNodes.children"


# Convenience aliases (all resources in a flat namespace)
class Resources(
    SearchItemsResources,
    GetItemsResources,
    GetVariationsResources,
    GetBrowseNodesResources,
):
    """Flat namespace with all resource string constants across all operations."""
