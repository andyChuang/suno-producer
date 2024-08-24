import time
import click
import json
import fire
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
  for times in range(config.round_num):
    config = get_config()

    req = get_generate_customized_music_request(config)

    with request.urlopen(req) as response:
      json_resp = json.loads(response.read().decode('utf-8'))
      handle_response(config, json_resp[0])
      handle_response(config, json_resp[1])
    print(f"Round {times+1} finished")
  
def get_generate_customized_music_request(config):
  return request.Request(url = f"{config.api_server}api/custom_generate", 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="POST")

def get_get_audio_info_request(config, song_id):
  return request.Request(url = f"{config.api_server}api/get?ids={song_id}", 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="GET")
  
def get_config():
   with open("suno-producer\\config.json","r") as file:
    x = json.loads(file.read(), object_hook=lambda d: SimpleNamespace(**d))
    return x

def handle_response(config, resp):
  song_id = resp['id']
  print(f"resp: ${json.dumps(resp)}")
  for retry_times in range(1, 100):
    print(f"Handle song {song_id} for {retry_times} times")
    with request.urlopen(get_get_audio_info_request(config, song_id)) as resp:
        song_info = json.loads(resp.read().decode('utf-8'))
        print(f"Song status: {song_info[0]['status']}")

    if(song_info[0]["status"] == "complete"):
      print(f"Start to download {song_info[0]['id']}")
      download_music(song_info[0]["audio_url"], f"{config.download_root}{song_info[0]['title']}_{int(time.time())}.mp3")
      break
    else:
      time.sleep(5)
   
def download_music(url, title):
    urllib.request.urlretrieve(url, title)

if __name__ == '__main__':

  try:
      go()
  except Exception as e:
    print(f"Error! {fire.Fire(e)}")