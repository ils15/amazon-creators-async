# Price Structure Usage Example

## Amazon Creators API v3.x Price Structure

The API returns a nested price structure. Here's how to access it:

```python
async with AmazonCreatorsAsyncClient(...) as client:
    result = await client.search_items(
        keywords="Monitor Gamer",
        item_count=5,
        resources=["itemInfo.title", "offersV2.listings.price"]
    )
    
    for item in result.search_result.items:
        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]  # First listing (usually buy box winner)
            
            # Access the current price
            if listing.price and listing.price.money:
                amount = listing.price.money.amount  # 588.9
                currency = listing.price.money.currency  # "BRL"
                display = listing.price.money.display_amount  # "R$ 588,90"
                print(f"Current Price: {display}")
            
            # Access savings (if available)
            if listing.price.savings:
                savings_amount = listing.price.savings.money.display_amount  # "R$ 31,09"
                savings_percent = listing.price.savings.percentage  # 5
                print(f"You save: {savings_amount} ({savings_percent}%)")
            
            # Access original price (before discount)
            if listing.price.saving_basis:
                original = listing.price.saving_basis.money.display_amount  # "R$ 619,99"
                print(f"Was: {original}")
            
            # Check if this is the buy box winner
            if listing.is_buy_box_winner:
                print("✓ Buy Box Winner")
```

## Response Structure

```json
{
  "offersV2": {
    "listings": [
      {
        "isBuyBoxWinner": true,
        "violatesMAP": false,
        "price": {
          "money": {
            "amount": 588.9,
            "currency": "BRL",
            "displayAmount": "R$ 588,90"
          },
          "savingBasis": {
            "money": {
              "amount": 619.99,
              "currency": "BRL",
              "displayAmount": "R$ 619,99"
            },
            "savingBasisType": "WAS_PRICE",
            "savingBasisTypeLabel": "De:"
          },
          "savings": {
            "money": {
              "amount": 31.09,
              "currency": "BRL",
              "displayAmount": "R$ 31,09"
            },
            "percentage": 5
          }
        }
      }
    ]
  }
}
```

## Pydantic Models

The package provides these models:

- **Money**: `amount`, `currency`, `display_amount`
- **Savings**: `money` (Money object), `percentage`
- **SavingBasis**: `money` (Money object), `saving_basis_type`, `saving_basis_type_label`
- **Price**: `money`, `saving_basis`, `savings`
- **Listing**: `id`, `price`, `is_buy_box_winner`, `violates_map`, `delivery_info`, `condition`
- **OffersV2**: `listings`, `summaries`
