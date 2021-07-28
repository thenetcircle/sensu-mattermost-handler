#!/usr/bin/python

import argparse
import sys
import json
import requests


def main():
    parser = argparse.ArgumentParser(description='push events to mattermost webhook')
    parser.add_argument('-u', type=str, dest='url', required=True, help='the url to mattermost webhook')
    args = parser.parse_args()

    lines = sys.stdin.readlines()
    obj = json.loads("".join(lines))

    host = obj['entity']['metadata']['name']
    check_name = obj['check']['metadata']['name']
    message = obj['check']['output'].replace('\n', ' ')
    occurrences = str(obj['check']['occurrences'])
    status = obj['check']['status']

    if status == 0:
        status = ':white_check_mark: OK'
    elif status == 1:
        status = ':warning: WARNING'
    elif status == 2:
        status = ':stop_sign: CRITICAL'
    else:
        status = ':grey_question: UNKNOWN'

    payload = {
        "username": "SensuGo",
        "icon_url": "https://raw.githubusercontent.com/sensu/web/828c7a0c2a6abb7ea215ca6ded903ba26045f542/logo.png",
        "text": "| **Server** | **" + host + "** |\n" +
                "|----|----|\n" +
                "| Check | " + check_name + " |\n" +
                "| Output | " + message + " |\n" +
                "| Occurrences | " + occurrences + " |\n" +
                "| Status | " + status + " |\n"
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.post(
            url=args.url,
            data=json.dumps(payload),
            headers=headers
        )
        print(response.text)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
