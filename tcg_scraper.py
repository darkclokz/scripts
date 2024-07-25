"Code to notify on latest lowest price on cards"
import json
import urllib.parse
import requests

# card_name = input("Enter card name.\n")

CARD_DATA = '''{ 
"cards": [
{"cardName":"Blackcleave Cliffs", "setName":"Scars of Mirrodin", "condition":"Lightly Played" },
{ "cardName":"BlackCleave Cliffs", "setName":"Phyrexia: All Will Be One", "condition":"Lightly Played" },
{ "cardName":"Razorverge Thicket", "setName":"Scars of Mirrodin", "condition":"Lightly Played" }]}'''

CARD_NAMES = json.loads(CARD_DATA)

for card in CARD_NAMES["cards"]:
    card_name = urllib.parse.quote_plus(card["cardName"])
    print(card["cardName"])
    id_lookup_url = f"https://mp-search-api.tcgplayer.com/v1/search/request?q={
        card_name}&isList=false"

    id_lookup_data = {
        "algorithm": "sales_synonym_v2",
        "from": 0,
        "size": 24,
        "filters": {
            "term": {
                "productLineName": [
                    "magic"
                ]
            },
            "range": {},
            "match": {}
        },
        "listingSearch": {
            "context": {
                "cart": {}
            },
            "filters": {
                "term": {
                    "sellerStatus": "Live",
                    "channelId": 0
                },
                "range": {
                    "quantity": {
                        "gte": 1
                    }
                },
                "exclude": {
                    "channelExclusion": 0
                }
            }
        },
        "context": {
            "cart": {},
            "shippingCountry": "US",
            "userProfile": {
                "productLineAffinity": "Magic: The Gathering",
                "priceAffinity": 322
            }
        },
        "settings": {
            "useFuzzySearch": "true",
            "didYouMean": {}
        },
        "sort": {}
    }

    id_lookup_data = requests.post(
        id_lookup_url, json=id_lookup_data, timeout=5)

    id_response_data = id_lookup_data.json()

    json_formatted_str = json.dumps(id_response_data, indent=2)

    for entry in id_response_data["results"]:
        for entry_result in entry["results"]:
            if entry_result["setName"] == card["setName"]:
                PRODUCT_ID = int(entry_result["productId"])

    url = f"https://mp-search-api.tcgplayer.com/v1/product/{
        PRODUCT_ID}/listings"
    myobj = {
        "filters": {
            "term": {
                "sellerStatus": "Live",
                "channelId": 0,
                "language": [
                    "English"
                ]
            },
            "range": {
                "quantity": {
                    "gte": 1
                }
            },
            "exclude": {
                "channelExclusion": 0
            }
        },
        "from": 0,
        "size": 50,
        "sort": {
            "field": "price+shipping",
            "order": "asc"
        },
        "context": {
            "shippingCountry": "US",
            "cart": {}
        },
        "aggregations": [
            "listingType"
        ]
    }

    lowest_listing_data = requests.post(url, json=myobj, timeout=5)
    lowest_listing_response_data = lowest_listing_data.json()

    for entry in lowest_listing_response_data["results"]:
        for entry_result in entry["results"]:
            if entry_result["condition"] == "Lightly Played":
                print(f'Lowest lightly played price is {
                      entry_result["price"] + entry_result["shippingPrice"]}')
                break

    for entry in lowest_listing_response_data["results"]:
        for entry_result in entry["results"]:
            if entry_result["condition"] == "Near Mint":
                print(f'Lowest near mint price is {
                      entry_result["price"] + entry_result["shippingPrice"]}')
                break
    
    print("\n")
