import requests

# https://api.forecast.solar/estimate/:lat/:lon/:dec/:az/:kwp
baseurl = "https://api.forecast.solar/"
baseurl_estimate = f"{baseurl}estimate/"
lat = 40.13337331729221
lon = -122.46943148433246
dec = 5 # Roughly 5 degrees?
az  = 0 # 0 = South?
kwp = 10 # kW?

parks_endpoint = f"{baseurl_estimate}{lat}/{lon}/{dec}/{az}/{kwp}"
print(parks_endpoint)

# r = requests.get(parks_endpoint)
print(r.text)
print(r.json())

with open("resp_text.json", "wb") as file:
  file.write(r.content)