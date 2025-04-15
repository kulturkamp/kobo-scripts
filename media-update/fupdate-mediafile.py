import requests, json, dotenv, os

dotenv.load_dotenv()

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
XFORM = os.getenv('XFORM')



headers = {'Authorization': f'Token {TOKEN}'}
url = f"{URL}/assets/{XFORM}/files/"

#get form media list
response = requests.get(url, headers=headers, params={'format': 'json'})
media_json = response.json()

#in this example, i handle one file for one form
#naturally you can iterate over a list of form ids and over a list of files, logic is the same
MEDIA_PATH =  os.getenv('MEDIA_PATH')
MEDIA_NAME = os.path.basename(MEDIA_PATH)

#DELETE

#if file is in the form media, delete it first
#if not, it will be just uploaded(depending on your goal you may want to terminate if media is not present)
for media in media_json['results']:
    if media['metadata']['filename'] == MEDIA_NAME:
        del_url = media['url']
        response = requests.delete(del_url, headers=headers)
        print('deleted ', response)
        break



#UPLOAD

post_url = f"{URL}/assets/{XFORM}/files.json"
#read updated file
bytes_content = open(MEDIA_PATH, 'rb')
files =  {'content': bytes_content}
#does not work without json.dumps() here for some reason idk
data = {'description': 'Input and equipment media file', 'metadata': json.dumps({'filename': MEDIA_NAME}), 'file_type': 'form_media'}

response = requests.post(url=post_url, headers=headers, data=data, files=files)
print('uploaded ', response)

#REDEPLOY

asset_url = f"{URL}/assets/{XFORM}/"
redeploy_headers = {
    'Accept': 'application/json',
    'Authorization': f'Token {TOKEN}'
}

response = requests.get(asset_url, headers=redeploy_headers, params={'format': 'json'})
version_to_deploy = response.json()['version_id']
deployment_data = {
    'version_id': version_to_deploy,
    'active': True
}
response = requests.patch(asset_url + 'deployment/', headers=redeploy_headers, data=deployment_data)
print('redeployed ', response)
