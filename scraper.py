import re
from typing_extensions import Self
import requests
import pandas as pd


class ShopeeAPI:
    def __init__(self, url_list: list) -> None:
        self.url_list = url_list

    def scrape(self) -> None:
        shop_ids = []
        item_ids = []
        offset = 0
        idx = 0

        for url in self.url_list:
            r = re.search(r"i\.(\d+)\.(\d+)", url)
            shop_ids.append(r[1])
            item_ids.append(r[2])

        ratings_url = "https://shopee.ph/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}" +\
            "&limit=20&offset={offset}&shopid={shop_id}&type=0"

        data_format = {"userid": [], "username": [], "item": [], "item_type": [], "ctime": [], "comment": [], "rating": [],
                       "product_quality": [], "seller_service": [], "delivery_service": [], "has_template_tag": [],
                       "template_tags": [], "tags": [], "is_oversea": [], "origin_region": [], "like_count": [],
                       "is_repeated_purchase": [], "exclude_scoring_due_low_logistic": []}

        # Scraper - API
        while True:
            if len(self.url_list) == idx:
                break
            data = requests.get(
                ratings_url.format(shop_id=shop_ids[idx], item_id=item_ids[idx], offset=offset)).json()

            i = 1
            for i, rating in enumerate(data["data"]["ratings"], 1):
                data_format["userid"].append(rating["userid"])
                data_format["username"].append(rating["author_username"])
                data_format["item"].append(rating["product_items"][0]["name"])
                data_format["item_type"].append(idx)
                data_format["ctime"].append(rating["ctime"])
                data_format["comment"].append(rating["comment"])
                data_format["rating"].append(rating["rating_star"])
                data_format["product_quality"].append(
                    rating["detailed_rating"]["product_quality"])
                data_format["seller_service"].append(
                    rating["detailed_rating"]["seller_service"])
                data_format["delivery_service"].append(
                    rating["detailed_rating"]["delivery_service"])
                data_format["has_template_tag"].append(
                    rating["has_template_tag"])
                data_format["template_tags"].append(rating["template_tags"])
                data_format["tags"].append(rating["tags"])
                data_format["is_oversea"].append(
                    rating["sip_info"]["is_oversea"])
                data_format["origin_region"].append(
                    rating["sip_info"]["origin_region"])
                data_format["like_count"].append(rating["like_count"])
                data_format["is_repeated_purchase"].append(
                    rating["is_repeated_purchase"])
                data_format["exclude_scoring_due_low_logistic"].append(
                    rating["exclude_scoring_due_low_logistic"])

            if i % 20:
                df = pd.DataFrame(data_format)
                df.to_csv("data/data"+str(idx)+".csv", index=False)
                data_format = {"userid": [], "username": [], "item": [], "item_type": [], "ctime": [],
                               "comment": [], "rating": [], "product_quality": [], "seller_service": [],
                               "delivery_service": [], "has_template_tag": [], "template_tags": [],
                               "tags": [], "is_oversea": [], "origin_region": [], "like_count": [],
                               "is_repeated_purchase": [], "exclude_scoring_due_low_logistic": []}
                idx += 1
                offset = 0
            else:
                offset += 20
