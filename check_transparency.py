from PIL import Image
import sys
import requests
from io import BytesIO

def check_transparency(path_or_url):
    try:
        if path_or_url.startswith('http'):
            response = requests.get(path_or_url)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(path_or_url)
        
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            if img.mode == 'RGBA':
                extrema = img.getextrema()
                if extrema[3][0] < 255:
                    print("Image has transparency.")
                else:
                    print("Image has an alpha channel but is fully opaque.")
            else:
                 print("Image might have transparency.")
        else:
            print("Image has no alpha channel (no transparency).")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_transparency(sys.argv[1])
    else:
        print("Please provide a path or URL.")
