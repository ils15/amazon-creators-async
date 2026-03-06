import pytest
import httpx
from pydantic import ValidationError

from amazon_creators_async_api.client import AmazonCreatorsAsyncClient
from amazon_creators_async_api.models.requests import (
    GetItemsRequest,
    GetVariationsRequest,
    SearchItemsRequest,
)
from amazon_creators_async_api.models.responses import (
    AvailabilityInfo,
    ConditionInfo,
    DealDetails,
    Listing,
    LoyaltyPoints,
    MerchantInfo,
    Price,
    Money,
    Item,
    ItemInfo,
    BrowseNodeInfo,
    SearchRefinements,
    VariationSummary,
    VariationsResult,
)
from amazon_creators_async_api.resources import (
    SearchItemsResources,
    GetItemsResources,
    GetVariationsResources,
    GetBrowseNodesResources,
    Resources,
)


class MockResponse:
    def __init__(self, status_code, payload=None, text="", headers=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._payload


class MockHTTPClient:
    def __init__(self, outcomes):
        self._outcomes = list(outcomes)
        self.calls = 0

    async def post(self, *args, **kwargs):
        self.calls += 1
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.mark.asyncio
async def test_request_retries_network_errors_then_succeeds():
    mock_client = MockHTTPClient(
        [
            httpx.ConnectError("temporary network issue"),
            MockResponse(200, payload={"ok": True}),
        ]
    )
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        client=mock_client,
        version="3.1",
        max_retries=2,
        retry_backoff_seconds=0.01,
    )

    async def fake_token():
        return "token"

    client._auth_manager.get_valid_token = fake_token

    result = await client._request("searchItems", {"keywords": "keyboard"})
    assert result == {"ok": True}
    assert mock_client.calls == 2


@pytest.mark.asyncio
async def test_get_items_rejects_empty_item_ids():
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        version="3.1",
    )

    with pytest.raises(ValueError, match="item_ids must contain at least one ASIN"):
        await client.get_items([])

    await client.close()


@pytest.mark.asyncio
async def test_search_items_requires_at_least_one_criterion():
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        version="3.1",
    )

    with pytest.raises(ValidationError, match="At least one search criterion"):
        await client.search_items(item_count=1)

    await client.close()


# ---------------------------------------------------------------------------
# Request model field coverage
# ---------------------------------------------------------------------------

def test_search_items_request_new_fields():
    req = SearchItemsRequest(
        keywords="coffee",
        marketplace="www.amazon.com",
        partner_tag="tag-20",
        availability="IncludeOutOfStock",
        min_reviews_rating=3,
        min_saving_percent=10,
        properties={"key": "value"},
    )
    data = req.model_dump(by_alias=True, exclude_none=True)
    assert data["availability"] == "IncludeOutOfStock"
    assert data["minReviewsRating"] == 3
    assert data["minSavingPercent"] == 10
    assert data["properties"] == {"key": "value"}


def test_search_items_request_no_merchant_field():
    req = SearchItemsRequest(
        keywords="keyboard",
        marketplace="www.amazon.com",
        partner_tag="tag-20",
    )
    assert not hasattr(req, "merchant")


def test_get_items_request_item_id_type_default():
    req = GetItemsRequest(
        item_ids=["B0ASIN001"],
        marketplace="www.amazon.com",
        partner_tag="tag-20",
    )
    data = req.model_dump(by_alias=True, exclude_none=True)
    assert data["itemIdType"] == "ASIN"


def test_get_variations_request_no_offer_count():
    req = GetVariationsRequest(
        asin="B0ASIN001",
        marketplace="www.amazon.com",
        partner_tag="tag-20",
    )
    assert not hasattr(req, "offer_count")
    assert not hasattr(req, "merchant")


# ---------------------------------------------------------------------------
# Response model coverage
# ---------------------------------------------------------------------------

def test_listing_new_sub_models_parse():
    raw = {
        "id": "listing-1",
        "availability": {"maxOrderQuantity": 5, "message": "In Stock", "type": "Now"},
        "condition": {"value": "New", "subCondition": "New"},
        "dealDetails": {"badge": "LIGHTNING_DEAL", "percentClaimed": 60.0},
        "loyaltyPoints": {"points": 100},
        "merchantInfo": {"id": "merchant-1", "name": "Top Seller"},
        "price": {
            "money": {"amount": 29.99, "currency": "USD", "displayAmount": "$29.99"},
            "pricePerUnit": {"amount": 9.99, "currency": "USD"},
        },
        "type": "LIGHTNING_DEAL",
        "isBuyBoxWinner": True,
    }
    listing = Listing.model_validate(raw)
    assert listing.availability.max_order_quantity == 5
    assert listing.condition.value == "New"
    assert listing.deal_details.badge == "LIGHTNING_DEAL"
    assert listing.loyalty_points.points == 100
    assert listing.merchant_info.name == "Top Seller"
    assert listing.price.money.amount == 29.99
    assert listing.price.price_per_unit.amount == 9.99
    assert listing.type == "LIGHTNING_DEAL"
    assert listing.is_buy_box_winner is True


def test_item_info_full_fields_parse():
    raw = {
        "title": {"displayValue": "Test Product"},
        "classifications": {"productGroup": {"displayValue": "Electronics"}},
        "externalIds": {"eans": {"displayValues": ["1234567890"]}},
        "features": {"displayValues": ["Feature 1"]},
        "productInfo": {"color": {"displayValue": "Black"}},
    }
    info = ItemInfo.model_validate(raw)
    assert info.title == {"displayValue": "Test Product"}
    assert info.classifications is not None
    assert info.external_ids is not None


def test_item_has_browse_node_info_and_parent_asin():
    raw = {
        "asin": "B0TEST001",
        "parentASIN": "B0PARENT",
        "browseNodeInfo": {
            "browseNodes": [
                {"id": "123", "displayName": "Electronics", "isRoot": False}
            ]
        },
    }
    item = Item.model_validate(raw)
    assert item.parent_asin == "B0PARENT"
    assert item.browse_node_info.browse_nodes[0].id == "123"


def test_variation_summary_parses():
    raw = {
        "items": [],
        "variationSummary": {"variationCount": 12, "pageCount": 2},
    }
    result = VariationsResult.model_validate(raw)
    assert result.variation_summary.variation_count == 12


# ---------------------------------------------------------------------------
# Resources constants
# ---------------------------------------------------------------------------

def test_resources_constants_are_non_empty_strings():
    for name in dir(SearchItemsResources):
        if name.startswith("_"):
            continue
        val = getattr(SearchItemsResources, name)
        assert isinstance(val, str) and val, f"SearchItemsResources.{name} is empty"

    for name in dir(GetBrowseNodesResources):
        if name.startswith("_"):
            continue
        val = getattr(GetBrowseNodesResources, name)
        assert isinstance(val, str) and val


def test_resources_flat_namespace_includes_all():
    assert hasattr(Resources, "BROWSE_NODES_ANCESTOR")
    assert hasattr(Resources, "VARIATION_SUMMARY_VARIATION_COUNT")
    assert hasattr(Resources, "OFFERS_V2_PRICE")
    assert hasattr(Resources, "ITEM_INFO_TRADE_IN_INFO")
