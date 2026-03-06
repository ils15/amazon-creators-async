from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    item_ids: List[str] = Field(min_length=1, max_length=10)
    partner_tag: str
    partner_type: str = "Associates"
    marketplace: str
    resources: Optional[List[str]] = None
    condition: Optional[str] = None
    currency_of_preference: Optional[str] = None
    item_id_type: Optional[str] = "ASIN"
    languages_of_preference: Optional[List[str]] = None

class SearchItemsRequest(BaseAPIRequest):
    keywords: Optional[str] = None
    actor: Optional[str] = None
    artist: Optional[str] = None
    author: Optional[str] = None
    availability: Optional[str] = None
    brand: Optional[str] = None
    browse_node_id: Optional[str] = None
    condition: Optional[str] = None
    currency_of_preference: Optional[str] = None
    delivery_flags: Optional[List[str]] = None
    item_count: Optional[int] = Field(ge=1, le=10, default=10)
    item_page: Optional[int] = Field(ge=1, le=10, default=1)
    languages_of_preference: Optional[List[str]] = None
    marketplace: str
    max_price: Optional[int] = None
    min_price: Optional[int] = None
    min_reviews_rating: Optional[int] = Field(default=None, ge=1, le=4)
    min_saving_percent: Optional[int] = Field(default=None, ge=1, le=99)
    partner_tag: str
    partner_type: str = "Associates"
    properties: Optional[Dict[str, str]] = None
    resources: Optional[List[str]] = None
    search_index: Optional[str] = "All"
    sort_by: Optional[str] = None
    title: Optional[str] = None

    @model_validator(mode="after")
    def validate_search_criteria(self):
        if not any(
            [
                self.keywords,
                self.actor,
                self.artist,
                self.author,
                self.brand,
                self.browse_node_id,
                self.title,
            ]
        ):
            raise ValueError(
                "At least one search criterion must be provided: "
                "keywords, actor, artist, author, brand, browse_node_id, or title."
            )
        return self

class GetBrowseNodesRequest(BaseAPIRequest):
    browse_node_ids: List[str] = Field(min_length=1, max_length=10)
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
    resources: Optional[List[str]] = None
    variation_count: Optional[int] = Field(ge=1, le=10, default=10)
    variation_page: Optional[int] = Field(ge=1, le=10, default=1)
