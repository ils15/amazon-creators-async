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
    Price structure from Amazon Creators API v3.x.
    Contains nested 'money', 'savingBasis', and 'savings' objects.
    """
    money: Optional[Money] = None
    saving_basis: Optional[SavingBasis] = None
    savings: Optional[Savings] = None

class ItemInfo(BaseAPIResponse):
    title: Optional[Dict[str, str]] = None
    features: Optional[Dict[str, List[str]]] = None
    by_line_info: Optional[Dict[str, Any]] = None

class Listing(BaseAPIResponse):
    id: Optional[str] = None
    price: Optional[Price] = None
    delivery_info: Optional[Dict[str, Any]] = None
    condition: Optional[Dict[str, str]] = None
    is_buy_box_winner: Optional[bool] = None
    violates_map: Optional[bool] = None

class OffersV2(BaseAPIResponse):
    listings: Optional[List[Listing]] = None
    summaries: Optional[List[Dict[str, Any]]] = None

class Item(BaseAPIResponse):
    asin: str
    detail_page_url: Optional[str] = None
    images: Optional[Images] = None
    item_info: Optional[ItemInfo] = None
    offers_v2: Optional[OffersV2] = None

class SearchResult(BaseAPIResponse):
    total_result_count: Optional[int] = None
    search_url: Optional[str] = None
    items: List[Item] = Field(default_factory=list)

class SearchItemsResponse(BaseAPIResponse):
    search_result: Optional[SearchResult] = None
    errors: Optional[List[Dict[str, str]]] = None

class GetItemsResult(BaseAPIResponse):
    items: List[Item] = Field(default_factory=list)

class GetItemsResponse(BaseAPIResponse):
    items_result: Optional[GetItemsResult] = None
    errors: Optional[List[Dict[str, str]]] = None

# Model for Traverse Tree of BrowseNodes
class BrowseNode(BaseAPIResponse):
    id: Optional[str] = None
    display_name: Optional[str] = None
    context_free_name: Optional[str] = None
    is_root: Optional[bool] = None
    ancestor: Optional['BrowseNode'] = None
    children: Optional[List['BrowseNode']] = None

class BrowseNodesResult(BaseAPIResponse):
    browse_nodes: List[BrowseNode] = Field(default_factory=list)

class GetBrowseNodesResponse(BaseAPIResponse):
    browse_nodes_result: Optional[BrowseNodesResult] = None
    errors: Optional[List[Dict[str, str]]] = None

class VariationDimension(BaseAPIResponse):
    display_name: str
    name: str

class VariationsResult(BaseAPIResponse):
    items: List[Item] = Field(default_factory=list)
    variation_dimensions: Optional[List[VariationDimension]] = None

class GetVariationsResponse(BaseAPIResponse):
    variations_result: Optional[VariationsResult] = None
    errors: Optional[List[Dict[str, str]]] = None

# Deal with recursive model definition for Pydantic v2
BrowseNode.model_rebuild()
