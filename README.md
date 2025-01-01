# bing-wallpaper
Makes the daily-updating Bing.com wallpaper available to your apps.
# bing-wallpaper

This container makes the daily-updating Bing.com wallpaper available to your apps. It presents the wallpaper as an endpoint on your network so that you can point your other apps or utilities to it.

## Getting started

Using docker compose:

```bash
services:
  bing-wallpaper:
    image: ghcr.io/voltagesolutions/bing-wallpaper:latest
    container_name: bing-wallpaper
    ports:
      - "5000:5000"
```

Using docker run:

```bash
docker run -p 5000:5000 -d --name bing-wallpaper
```

## Example usage

If you are running an application like [homepage](https://github.com/gethomepage/homepage) you can point the application to bing-wallpaper. Homepage lets users configure a background in its `settings.yaml` file.

```bash
# Assumes you have a directory called 'homepage' from which the application runs.
nano /homepage/config/settings.yaml
```

```yml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/settings

background:
  image: http://your_ip_address:port
```

I use a custom DNS entry and proxy on my network so in my case the settings are instead:

```yml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/settings

background:
  image: http://bingwallpaper
```

## How does it work?

Some of the wallpapers Bing provides come have copyright that restrict users from downloading them. For this reason, bing-wallpaper does not download or cache the wallpaper - it retrieves the URL for the wallpaper and redirects to that.

Once bing-wallpaper is running, enter `http://your_ip_address:port` into your web browser or use the tool of your choice to `GET` the endpoint. Each time you make a call, bing-wallpaper follows these steps:

1. It connects to Bing's image archive at `https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1`.
1. The server will provide a json response. bing-wallpaper looks through the `images` collection and gets the `url` attribute from the first entry in the collection.
1. If it could successfully retrieve the `url` it will respond with a `302` and redirect there.
1. If it could **not** retrieve the `url` it will issue a blank response as a `200`. This results in a white screen.

For reference, here is a sample of the json response that Bing provides.

```json
{
    "images": [
        {
            "startdate": "20241231",
            "fullstartdate": "202412310800",
            "enddate": "20250101",
            "url": "/th?id=OHR.RioNewYear_EN-US7216341802_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp",
            "urlbase": "/th?id=OHR.RioNewYear_EN-US7216341802",
            "copyright": "New Year's Eve fireworks over Copacabana Beach, Rio de Janeiro, Brazil (© Wagner Meier/Getty Images)",
            "copyrightlink": "https://www.bing.com/search?q=New+Year%27s+Eve&form=hpcapt&filters=HpDate%3a%2220241231_0800%22",
            "title": "Midnight in Rio",
            "quiz": "/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20241231_RioNewYear%22&FORM=HPQUIZ",
            "wp": false,
            "hsh": "e169c3c75983c86a8814c728137f5556",
            "drk": 1,
            "top": 1,
            "bot": 1,
            "hs": []
        }
    ],
    "tooltips": {
        "loading": "Loading...",
        "previous": "Previous image",
        "next": "Next image",
        "walle": "This image is not available to download as wallpaper.",
        "walls": "Download this image. Use of this image is restricted to wallpaper only."
    }
}
```

## Debugging

bing-wallpaper* will write to Docker logs. If you want to debug it yourself, clone the repo. You can uncomment code sections like this to force failure scenarios.

```python
# Simulate network errors
#if os.environ.get("SIMULATE_NETWORK_ERROR") == "1":
#    raise requests.exceptions.ConnectionError("Simulated network error")
```
