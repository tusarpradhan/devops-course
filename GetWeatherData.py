#!/usr/bin/env python
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; replace-tabs on;

import logging
import os
import sys
import requests
import json


def get_location_forecast(location):
    loc_resp = requests.get(
        "https://www.metaweather.com/api/location/search/",
        params=dict(query=location)
    )
    loc_woeid = loc_resp.json()[0]["woeid"]

    forecast_resp = requests.get(
        "https://www.metaweather.com/api/location/%s/" % loc_woeid
    )
    forecast_resp.raise_for_status()
    return forecast_resp.json().get("consolidated_weather")


def main():
    for location in sys.argv[1:]:
        forecast = get_location_forecast(location)
        with open("forecasts/%s.json" % location, "wb") as fp:
            json.dump(forecast, fp)
        logging.info("Downloaded forecast for %s" % location)


if __name__ == '__main__':
    main()
