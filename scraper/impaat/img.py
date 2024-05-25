import os
import requests

url = "https://cb.imsc.res.in/imppat/images/2D_IMAGE/PNG/IMPHY007417.png"

response = requests.get(url)

if response.status_code == 200:
    filename = "image.png"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Image downloaded successfully. Saved as: {filename}")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
