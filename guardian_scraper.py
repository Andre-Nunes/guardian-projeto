import requests
import json
import os
from datetime import datetime

API_KEY = os.environ.get("GUARDIAN_API_KEY")

def recolher_guardian(max_paginas=20):
    url = "https://content.guardianapis.com/search"
    artigos_total = []

    for pagina in range(1, max_paginas + 1):
        params = {
            "api-key": API_KEY,
            "page-size": 50,
            "page": pagina,
            "order-by": "newest",
            "show-fields": "headline,trailText,body",
            "q": "technology OR science"
        }

        try:
            r = requests.get(url, params=params)
            dados = r.json()

            if not dados.get("response", {}).get("results"):
                break

            for res in dados["response"]["results"]:
                artigos_total.append({
                    "id": res["id"],
                    "webTitle": res["webTitle"],
                    "webUrl": res["webUrl"],
                    "headline": res["fields"].get("headline"),
                    "trailText": res["fields"].get("trailText"),
                    "body": res["fields"].get("body"),
                    "timestamp": datetime.now().isoformat()
                })

        except Exception as e:
            print(f"Erro na página {pagina}: {str(e)}")
            break

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("artigos", exist_ok=True)
    with open(f"artigos/artigos_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(artigos_total, f, ensure_ascii=False, indent=2)

recolher_guardian()
