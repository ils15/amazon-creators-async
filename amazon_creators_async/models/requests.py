from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class BaseAPIRequest(BaseModel):
    """
    Base configuration for Amazon Creators API requests.
    Forces lowerCamelCase as required by the new API.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda string: "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
        )
    )

class GetItemsRequest(BaseAPIRequest):
    item_ids: List[str]
    partner_tag: str
    partner_type: str = "Associates"
    marketplace: str
    resources: Optional[List[str]] = None
    condition: Optional[str] = None
    currency_of_preference: Optional[str] = None
    languages_of_preference: Optional[List[str]] = None
    merchant: Optional[str] = None

class SearchItemsRequest(BaseAPIRequest):
    keywords: Optional[str] = None
    actor: Optional[str] = None
    artist: Optional[str] = None
    author: Optional[str] = None
    brand: Optional[str] = None
    browse_node_id: Optional[str] = None
    condition: Optional[str] = None
    currency_of_preference: Optional[str] = None
    delivery_flags: Optional[List[str]] = None
    item_count: Optional[int] = Field(ge=1, le=10, default=10) # 10 items max per page usually
    item_page: Optional[int] = Field(ge=1, le=10, default=1)
    languages_of_preference: Optional[List[str]] = None
    marketplace: str
    merchant: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    partner_tag: str
    partner_type: str = "Associates"
    resources: Optional[List[str]] = None
    search_index: Optional[str] = "All"
    sort_by: Optional[str] = None
    title: Optional[str] = None
from typing import List, Optional
from pydantic import Field

from .requests import BaseAPIRequest

# We need to re-import or define here since we are appending to the module
class GetBrowseNodesRequest(BaseAPIRequest):
    browse_node_ids: List[str]
    partner_tag: str
    partner_type: str = "Associates"
    marketplace: str
    languages_of_preference: Optional[List[str]] = None
    resources: Optional[List[str]] = None

class GetVariationsRequest(BaseAPIRequest):
    asin: str
    partner_tag: str
    partner_type: str = "Associates"
    marketplace: str
    condition: Optional[str] = None
    currency_of_preference: Optional[str] = None
    languages_of_preference: Optional[List[str]] = None
    merchant: Optional[str] = None
    offer_count: Optional[int] = Field(ge=1, le=10, default=1)
    resources: Optional[List[str]] = None
    variation_count: Optional[int] = Field(ge=1, le=10, default=10)
    variation_page: Optional[int] = Field(ge=1, le=10, default=1)
