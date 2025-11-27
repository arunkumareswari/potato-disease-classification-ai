import requests

url = "https://us-central1-nice-azimuth-477813-r1.cloudfunctions.net/predict"

# Your potato image path
image_path = r"D:\Projects\Deep Learning\Potato Disease Classification\Dataset\Potato___Late_blight\00b1f292-23dd-44d4-aad3-c1ffb6a6ad5a___RS_LB 4479.JPG"
with open(image_path, 'rb') as img:
    files = {'file': img}
    response = requests.post(url, files=files)
    print(response.json())