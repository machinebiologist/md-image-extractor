""" Save embedded images from .md file & output modified .md referencing them

    Script to extract base64 embedded images from a markdown file, save them
    to disk as binary images, and output a modified version of the markdown
    file with references to the new image files.

    Machine Biology, 2023
"""
import argparse
import base64
import os
import re

from textwrap import dedent

def extract_images_from_md(md_file_path, output_dir, image_prefix, obsidian_format):
    """ Extracts embedded images from a markdown file, saves them to disk,
        and saves a modified version of the markdown file with references to
        the new image files.
    """
    with open(md_file_path, 'r', encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Regular expression to find data URLs in the markdown file
    pattern = r'(!\[([^\]]*)\]\(data:image/([^;]*);base64,([^\)]*)\))'
    matches = re.findall(pattern, md_content)

    for i, match in enumerate(matches):
        match_text, alt_text, image_type, base64_data = match

        # Decode Base64 data to binary
        binary_data = base64.b64decode(base64_data)

        # Create a unique filename for each image
        filename = f'{image_prefix}{i}.{image_type}'
        filepath = os.path.join(output_dir, filename)

        # Write the binary data to a file
        with open(filepath, 'wb') as image_file:
            image_file.write(binary_data)

        # Create the embed code referencing the new image file
        embed_code = f'![{alt_text}]({filename})'
        if obsidian_format:
            embed_code = f'![[{filename}]]'

        # Replace the data URL with the embed code
        md_content = md_content.replace(match_text, embed_code)

    # Get the filename portion of md_file_path
    md_base_filename = os.path.basename(md_file_path)
    md_out_filepath = os.path.join(output_dir, md_base_filename)

    # Write the modified markdown content back to the file
    with open(md_out_filepath, 'w', encoding="utf-8") as md_out_file:
        md_out_file.write(md_content)


def main(input_filename, output_dir, image_prefix, obsidian_format):
    """ Main function
    """
    # Create the output directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    print(dedent(f"""
        Processing markdown file: {input_filename}
        Saving images with prefix: {image_prefix}
        Writing embed code in {"Obsidian" if obsidian_format else "standard"} format
        Saving output to: {output_dir}"""))

    extract_images_from_md(input_filename, output_dir, image_prefix, obsidian_format)


if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description=('Extracts embedded images from a markdown file, '
                     'saves them to disk, '
                     'and updates the markdown file to embed the saved files.')
    )
    parser.add_argument('input_filename', type=str, help='The name of the input file')
    parser.add_argument(
        '--output_dir',
        type=str,
        default='output',
        help='The destination folder for output (defaults to "output")'
    )
    parser.add_argument(
        '--image_prefix',
        type=str,
        default='image',
        help=('Prefix for image filenames '
              '(e.g. the "image_" portion of "image_0.png", "image_1.png", etc.)')
    )
    parser.add_argument(
        '--obsidian_format',
        action="store_true",
        help='Outputs the image embed code in obsidan format: ![[image_name.png]]'
    )

    args = parser.parse_args()

    main(args.input_filename, args.output_dir, args.image_prefix, args.obsidian_format)
