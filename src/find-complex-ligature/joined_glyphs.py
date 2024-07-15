import os
from PIL import Image, ImageChops, ImageFilter
from pathlib import Path


def load_glyph(glyph, glyphs_folder):
    glyph_name = f"{glyph}_"
    
    for file_name in os.listdir(glyphs_folder):
        if file_name.startswith(glyph_name) and file_name.endswith('.png'):
            glyph_path = os.path.join(glyphs_folder, file_name)
            if os.path.exists(glyph_path):
                return Image.open(glyph_path).convert('RGBA')
    
    raise FileNotFoundError(f"Glyph image not found for {glyph} in {glyphs_folder}")


def trim_whitespace(image):
    """Trim the white space around an image."""
    bg = Image.new(image.mode, image.size, (255, 255, 255, 0))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def align_and_morph_glyphs(glyph_images):
    # Trim white space around each glyph
    trimmed_images = [trim_whitespace(img) for img in glyph_images]

    # Determine the maximum width and total height required for the ligature
    max_width = max(img.width for img in trimmed_images)
    total_height = sum(img.height for img in trimmed_images)

    # Create a blank image with the appropriate dimensions
    ligature = Image.new('RGBA', (max_width, total_height), (255, 255, 255, 0))

    y_offset = 0
    for img in trimmed_images:
        x_offset = (max_width - img.width) // 2  # Center-align the glyph horizontally
        ligature.paste(img, (x_offset, y_offset), img)
        y_offset += img.height

    # Morphing step: Adjust contours for better visual appearance
    # Note: This is a simplified example. Actual implementation may require more complex logic.
    ligature = morph_glyphs(ligature)

    return ligature


def morph_glyphs(ligature):
    # This is a placeholder for complex morphing logic
    # For demonstration, applying a slight blur to smooth out edges
    return ligature.filter(ImageFilter.GaussianBlur(1))


def create_ligature(glyphs, glyphs_folder):
    glyph_images = [load_glyph(glyph, glyphs_folder) for glyph in glyphs]
    return align_and_morph_glyphs(glyph_images)


def process_ligatures_from_file(input_file, glyphs_folder, output_folder):
    with open(input_file, 'r', encoding='utf-8') as file:
        ligatures = file.readlines()

    for ligature in ligatures:
        ligature = ligature.strip()
        if not ligature:
            continue

        try:
            ligature_image = create_ligature(ligature, glyphs_folder)
            output_path = os.path.join(output_folder, f"{ligature}.png")
            ligature_image.save(output_path)
            print(f"Saved ligature: {output_path}")
        except FileNotFoundError as e:
            print(e)


def main():
    input_file = '../../data/Tibetan_Essential_Glyphs.txt'
    glyphs_folder = '../../data/cleaned_images'
    output_folder = '../../data/ligatures'

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    process_ligatures_from_file(input_file, glyphs_folder, output_folder)


if __name__ == "__main__":
    main()
