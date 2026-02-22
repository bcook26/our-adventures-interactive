from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow (recommended)
pillow_heif.register_heif_opener()

input_dir = Path("photos")
output_dir = input_dir / "updated_pics"
output_dir.mkdir(exist_ok=True)

pic_counter = 0

for file_path in input_dir.iterdir():
    if file_path.is_file() and file_path.suffix.lower() in [".heic", ".heif"]:
        heif_file = pillow_heif.read_heif(file_path)

        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )

        pic_counter += 1
        output_path = output_dir / f"pic_{pic_counter}.png"
        image.save(output_path, format="PNG")

print(f"Converted {pic_counter} images.")