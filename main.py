from __future__ import print_function
import sys
import json
import requests


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_channel_ids(subs_json):
    ids = []
    for item in subs_json["items"]:
        if "snippet" in item:
            if "resourceId" in item["snippet"]:
                if "channelId" in item["snippet"]["resourceId"]:
                    ids.append(item["snippet"]["resourceId"]["channelId"])
                else:
                    eprint("ERROR channelId not in resourceId in snippet in item:\n{}".format(json.dumps(item, indent=4)))
            else:
                eprint("ERROR resourceId not in snippet in item:\n{}".format(json.dumps(item, indent=4)))
        else:
            eprint("ERROR snippet not in item:\n{}".format(json.dumps(item, indent=4)))

    if len(ids) != subs_json["pageInfo"]["totalResults"]:
        eprint("Channel retrieval mismatch! {} != {}", len(ids), subs_json["pageInfo"]["totalResults"])

    return ids


def generate_subscription_url(api_subscribe_url: str, ids_str: str):
    return "{}?id={}".format(api_subscribe_url, ids_str)


def generate_subscription_urls(api_subscribe_url: str, ids: list, maxlength: int = 2000):
    urls = []

    current_batch = "{}?id=".format(api_subscribe_url)
    for i in range(len(ids)):
        if len("{}?id={}".format(api_subscribe_url, current_batch) + ids[i]) > maxlength:
            # If adding one more ID will exceed maxlength, process the current batch now.
            urls.append(current_batch)
            current_batch = "{}?id=".format(api_subscribe_url)
        elif i == len(ids) - 1:
            # Last entry
            if current_batch != "{}?id=".format(api_subscribe_url):
                # If there are still a batch to process, process it.
                urls.append(current_batch)

        # If no IDs added yet
        if current_batch == "{}?id=".format(api_subscribe_url):
            current_batch += ids[i]
        else:
            # If IDs already present, prefix a delimiter
            current_batch += ',' + ids[i]

    return urls


# def subscribe(urls: list):
#     for url in urls:
#         # Set (required) headers.
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded"
#         }
#
#
#     pass

if __name__ == '__main__':
    with open("config.json") as f:
        config = json.load(f)

    with open("my_subs.json", "r", encoding="utf-8") as f:
        subs = json.load(f)

    channel_ids = get_channel_ids(subs)
    print(channel_ids)
    print("Retrived {} channel IDs.".format(len(channel_ids)))

    sub_urls = generate_subscription_urls(config["api_subscribe_url"], channel_ids)

    for url in sub_urls:
        print("curl -X POST {}".format(url))


