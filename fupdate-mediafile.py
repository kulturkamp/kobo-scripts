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

MEDIA_NAME = 'adminslan.csv'

# delete
#if file is form media, delete it
#if not, it will be uploaded(depends on your goal you may want to terminate if media is not present)
for media in media_json['results']:
    if media['metadata']['filename'] == MEDIA_NAME:
        del_url = media['url']
        res = requests.delete(del_url, headers=headers)
        print(res)
        break



# upload

post_url = f"{URL}/assets/{XFORM}/files.json"
payload = {'filename': MEDIA_NAME}

bytes_content = open(MEDIA_NAME, 'rb')
files =  {'content': bytes_content}
data = {'description': 'Input and equipment media file', 'metadata': json.dumps({'filename': MEDIA_NAME}), 'file_type': 'form_media'}

response = requests.post(url=post_url, headers=headers, data=data, files=files)
print(response)

# redeploy

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
print(response)
