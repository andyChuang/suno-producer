import time
import click
import json
import fire
import uuid
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


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
  pass
  

@cli.command()
def get_custom_music():
  print("get custom music")
  config = get_config()
  for times in range(config.round_num):
    req = get_generate_customized_music_request(config)

    with request.urlopen(req) as response:
      json_resp = json.loads(response.read().decode('utf-8'))
      handle_response(config, json_resp[0])
      handle_response(config, json_resp[1])
    print(f"Round {times+1} finished")

@cli.command()
def download():
  print("download")
  config = get_config()
  with request.urlopen(get_get_audio_info_request(config)) as response:
      song_list = json.loads(response.read().decode('utf-8'))
      
      for song in list(filter(lambda x: x["title"] == config.title, song_list)):
        download_music(song["audio_url"], get_download_destination(config, song["title"]))


def get_generate_customized_music_request(config):
  return request.Request(url = f"{config.api_server}api/custom_generate", 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="POST")

  
def get_generate_customized_music_request(config):
  return request.Request(url = f"{config.api_server}api/custom_generate", 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="POST")

def get_get_audio_info_request(config, song_id = None):
  url = f"{config.api_server}api/get"
  if(song_id != None):
    url = f"{url}?ids={song_id}"
  return request.Request(url = url, 
                        data= json.dumps(Request(config).__dict__).encode(), 
                        headers={"Content-Type":"application/json"}, 
                        method="GET")
  
def get_config():
   with open("config.json","r") as file:
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
      download_music(song_info[0]["audio_url"], get_download_destination(config, song_info[0]['title']))
      break
    else:
      time.sleep(5)
   
def get_download_destination(config, song_title):
  return f"{config.download_root}{song_title}_{uuid.uuid4()}.mp3"
  
def download_music(url, destination):
    urllib.request.urlretrieve(url, destination)
    print(f"Download music {destination} successfully")

if __name__ == '__main__':

  try:
      cli()
  except Exception as e:
    print(f"Error! {fire.Fire(e)}")
