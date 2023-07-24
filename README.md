# Markdown Image Extractor

This repository contains a Python script that extracts base64 embedded images from a markdown file, saves them to disk as binary images, and outputs a modified version of the markdown file with references to the new image files.

The script supports output with both the standard markdown image embed format (`!(alt text)[filename.png]`) and Obsidian markdown image embed format (`![[image_name.png]]`)

## Usage

This project requires Python 3.8 or above.

The script can be run from the command line with the following arguments:

- `input_filename`: The name of the input markdown file
- `--output_dir`: The destination folder for output (defaults to "output")
- `--image_prefix`: Prefix for image filenames (e.g. the "image_" portion of "image_0.png", "image_1.png", etc.)
- `--obsidian_format`: Outputs the image embed code in Obsidian format: `![[image_name.png]]`

Example usage:

```bash
python main.py input.md --output_dir output --image_prefix image_ --obsidian_format
```

This will process the `input.md` file, save the extracted images to the `output` directory with filenames starting with `image_`, and output a modified version of the `input.md` file with image references in Obsidian format.

## License

This project is licensed under the terms of the MIT license.
