import sys
from rembg import remove
from PIL import Image
import os

def remove_background(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    print(f"Processing {input_path}...")
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Saved transparent image to {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default behavior if no args provided, looking for the specific file mentioned
        input_file = "Macfly to the world logo.jpg"
        output_file = "Macfly_logo_transparent.png"
    else:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        else:
            base, _ = os.path.splitext(input_file)
            output_file = f"{base}_transparent.png"

    remove_background(input_file, output_file)
