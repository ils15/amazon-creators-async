from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class BaseAPIResponse(BaseModel):
    """
    Base configuration for Amazon Creators API responses.
    Ensures lowerCamelCase mapping from the API JSON.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda string: "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
        )
    )

# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

class Image(BaseAPIResponse):
    url: Optional[str] = Field(None, alias="url")
    height: Optional[int] = None
    width: Optional[int] = None

class Images(BaseAPIResponse):
    primary: Optional[Dict[str, Image]] = None
    variants: Optional[List[Dict[str, Image]]] = None

class Money(BaseAPIResponse):
    """Represents a monetary value with amount, currency, and display format."""
    amount: Optional[float] = None
    currency: Optional[str] = None
    display_amount: Optional[str] = None

class Savings(BaseAPIResponse):
    """Represents savings information with money and percentage."""
    money: Optional[Money] = None
    percentage: Optional[int] = None

class SavingBasis(BaseAPIResponse):
    """Represents the original/basis price for calculating savings."""
    money: Optional[Money] = None
    saving_basis_type: Optional[str] = None
    saving_basis_type_label: Optional[str] = None

class Price(BaseAPIResponse):
    """
    Price structure from Amazon Creators API.
    Contains nested 'money', 'pricePerUnit', 'savingBasis', and 'savings' objects.
    """
    money: Optional[Money] = None
    price_per_unit: Optional[Money] = None
    saving_basis: Optional[SavingBasis] = None
    savings: Optional[Savings] = None

# ---------------------------------------------------------------------------
# OffersV2 sub-models
# ---------------------------------------------------------------------------

class AvailabilityInfo(BaseAPIResponse):
    """Availability information for an offer listing."""
    max_order_quantity: Optional[int] = None
    message: Optional[str] = None
    min_order_quantity: Optional[int] = None
    type: Optional[str] = None

class ConditionInfo(BaseAPIResponse):
    """Condition information for an offer listing."""
    condition_note: Optional[str] = None
    sub_condition: Optional[str] = None
    value: Optional[str] = None

class DealDetails(BaseAPIResponse):
    """Deal/promotion information for an offer listing."""
    access_type: Optional[str] = None
    badge: Optional[str] = None
    early_access_duration_in_milliseconds: Optional[int] = None
    end_time: Optional[str] = None
    percent_claimed: Optional[float] = None
    start_time: Optional[str] = None

class LoyaltyPoints(BaseAPIResponse):
    """Loyalty points for an offer (Japan marketplace only)."""
    points: Optional[int] = None

class MerchantInfo(BaseAPIResponse):
    """Seller/merchant information for an offer listing."""
    id: Optional[str] = None
    name: Optional[str] = None

class Listing(BaseAPIResponse):
    id: Optional[str] = None
    availability: Optional[AvailabilityInfo] = None
    condition: Optional[ConditionInfo] = None
    deal_details: Optional[DealDetails] = None
    delivery_info: Optional[Dict[str, Any]] = None
    is_buy_box_winner: Optional[bool] = None
    loyalty_points: Optional[LoyaltyPoints] = None
    merchant_info: Optional[MerchantInfo] = None
    price: Optional[Price] = None
    type: Optional[str] = None
    violates_map: Optional[bool] = None

class OffersV2(BaseAPIResponse):
    listings: Optional[List[Listing]] = None
    summaries: Optional[List[Dict[str, Any]]] = None

# ---------------------------------------------------------------------------
# ItemInfo sub-models
# ---------------------------------------------------------------------------

class ItemInfo(BaseAPIResponse):
    by_line_info: Optional[Dict[str, Any]] = None
    classifications: Optional[Dict[str, Any]] = None
    content_info: Optional[Dict[str, Any]] = None
    content_rating: Optional[Dict[str, Any]] = None
    external_ids: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, List[str]]] = None
    manufacture_info: Optional[Dict[str, Any]] = None
    product_info: Optional[Dict[str, Any]] = None
    technical_info: Optional[Dict[str, Any]] = None
    title: Optional[Dict[str, str]] = None
    trade_in_info: Optional[Dict[str, Any]] = None

# ---------------------------------------------------------------------------
# BrowseNodeInfo (attached to Items)
# ---------------------------------------------------------------------------

class SalesRank(BaseAPIResponse):
    display_name: Optional[str] = None
    rank: Optional[int] = None

class ItemBrowseNode(BaseAPIResponse):
    """Browse node entry attached to an Item's browseNodeInfo."""
    id: Optional[str] = None
    display_name: Optional[str] = None
    context_free_name: Optional[str] = None
    is_root: Optional[bool] = None
    sales_rank: Optional[int] = None
    ancestor: Optional['ItemBrowseNode'] = None

class WebsiteSalesRank(BaseAPIResponse):
    context_free_name: Optional[str] = None
    display_name: Optional[str] = None
    sales_rank: Optional[int] = None

class BrowseNodeInfo(BaseAPIResponse):
    """browseNodeInfo resource attached to an Item."""
    browse_nodes: Optional[List[ItemBrowseNode]] = None
    website_sales_rank: Optional[WebsiteSalesRank] = None

# ---------------------------------------------------------------------------
# SearchRefinements
# ---------------------------------------------------------------------------

class SearchRefinementBin(BaseAPIResponse):
    display_name: Optional[str] = None
    id: Optional[str] = None

class SearchRefinement(BaseAPIResponse):
    display_name: Optional[str] = None
    id: Optional[str] = None
    bins: Optional[List[SearchRefinementBin]] = None

class SearchRefinements(BaseAPIResponse):
    search_index: Optional[List[SearchRefinement]] = None

# ---------------------------------------------------------------------------
# VariationSummary
# ---------------------------------------------------------------------------

class VariationSummary(BaseAPIResponse):
    page_count: Optional[int] = None
    price_range: Optional[Dict[str, Any]] = None
    variation_count: Optional[int] = None

# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------

class Item(BaseAPIResponse):
    asin: str
    browse_node_info: Optional[BrowseNodeInfo] = None
    detail_page_url: Optional[str] = None
    images: Optional[Images] = None
    item_info: Optional[ItemInfo] = None
    offers_v2: Optional[OffersV2] = None
    parent_asin: Optional[str] = Field(None, alias="parentASIN")

# ---------------------------------------------------------------------------
# Top-level responses
# ---------------------------------------------------------------------------

class SearchResult(BaseAPIResponse):
    total_result_count: Optional[int] = None
    search_url: Optional[str] = None
    items: List[Item] = Field(default_factory=list)
    search_refinements: Optional[SearchRefinements] = None

class SearchItemsResponse(BaseAPIResponse):
    search_result: Optional[SearchResult] = None
    errors: Optional[List[Dict[str, str]]] = None

class GetItemsResult(BaseAPIResponse):
    items: List[Item] = Field(default_factory=list)

class GetItemsResponse(BaseAPIResponse):
    items_result: Optional[GetItemsResult] = None
    errors: Optional[List[Dict[str, str]]] = None

# ---------------------------------------------------------------------------
# BrowseNodes (GetBrowseNodes response tree)
# ---------------------------------------------------------------------------

class BrowseNode(BaseAPIResponse):
    id: Optional[str] = None
    display_name: Optional[str] = None
    context_free_name: Optional[str] = None
    is_root: Optional[bool] = None
    sales_rank: Optional[List[SalesRank]] = None
    ancestor: Optional['BrowseNode'] = None
    children: Optional[List['BrowseNode']] = None

class BrowseNodesResult(BaseAPIResponse):
    browse_nodes: List[BrowseNode] = Field(default_factory=list)

class GetBrowseNodesResponse(BaseAPIResponse):
    browse_nodes_result: Optional[BrowseNodesResult] = None
    errors: Optional[List[Dict[str, str]]] = None

# ---------------------------------------------------------------------------
# Variations
# ---------------------------------------------------------------------------

class VariationDimension(BaseAPIResponse):
    display_name: str
    name: str

class VariationsResult(BaseAPIResponse):
    items: List[Item] = Field(default_factory=list)
    variation_dimensions: Optional[List[VariationDimension]] = None
    variation_summary: Optional[VariationSummary] = None

class GetVariationsResponse(BaseAPIResponse):
    variations_result: Optional[VariationsResult] = None
    errors: Optional[List[Dict[str, str]]] = None

# Deal with recursive model definitions for Pydantic v2
BrowseNode.model_rebuild()
ItemBrowseNode.model_rebuild()
