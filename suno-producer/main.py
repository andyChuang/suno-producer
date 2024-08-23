import time
import click
import json
import urllib.request
from urllib import request, parse
from types import SimpleNamespace

class Request:
  def __init__(self, config):
    self.prompt = ""
    self.tags = config.tags
    self.title = config.title
    self.make_instrumental = True
    self.wait_audio = True


@click.command()
def go():
  config = get_config()

  req = get_generate_customized_music_request(config)

  with request.urlopen(req) as response:
    json_resp = json.loads(response.read().decode('utf-8'))
    handle_response(config, json_resp[0])
    handle_response(config, json_resp[1])
  
def get_generate_customized_music_request(config):
  return request.Request(url = f"{config.api_server}api/custom_generate", 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="POST")

def get_get_audio_info_request(config, song_id):
  return request.Request(url = f"{config.api_server}api/get".format(f"?ids={song_id}"), 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="GET")
  
def get_config():
   with open("suno-producer\\config.json","r") as file:
    x = json.loads(file.read(), object_hook=lambda d: SimpleNamespace(**d))
    return x

def handle_response(config, response):
  
  for retry_times in range(1, 100):
    print(f"Handle song {response['id']} for {retry_times} times")
    with request.urlopen(get_get_audio_info_request(config, response["id"])) as response:
        song_info = json.loads(response.read().decode('utf-8'))
        print(f"Song status: {song_info}")

    if(song_info[0]["status"] == "complete"):
      print(f"Start to download {response['id']}")
      download_music(song_info[0]["audio_url"], f"{config.download_root}{song_info[0]['title']}")
      break
    else:
      time.sleep(5)
   
def download_music(url, title):
    urllib.request.urlretrieve(url, title)

if __name__ == '__main__':
  go()