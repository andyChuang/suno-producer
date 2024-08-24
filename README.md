# suno-producer

Generate and download the music by customer generate feature from Suno.

## Prerequisites
1. Follow the readme in this repo to launch a Suno API server
https://github.com/gcui-art/suno-api?tab=readme-ov-file

2. Prepare the config named "config.json"
```
{
    "api_server":"Your suno API server",
    "tags": "The tags",
    "title": "The title of the song",
    "download_root": "The download folder",
    "round_num": [integer] The generated song number will be round_num * 2
}
```
3. Install the library via PIP and run this python code. Call `python main.py --help` to get the command
    1. `download` will download the songs which matching the title in the config
    2. `get-custom-music` will create the new songs based on the config


## Refs
- https://suno.gcui.art/docs