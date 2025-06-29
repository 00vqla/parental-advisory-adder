# Parental Advisory Logo Adder

A Python GUI application that adds parental advisory explicit logos to album covers in a user-selected folder.

## Features

- **Three positioning options**: Bottom Left, Bottom Middle, Bottom Right
- **Adjustable logo size**: 50-200 pixels
- **Live preview**: See how the logo will appear before processing
- **Batch processing**: Process multiple images at once
- **Automatic backup**: Original files are backed up with '_original' suffix
- **Modern light UI**: Clean and intuitive interface

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install Pillow directly:
   ```bash
   pip install Pillow
   ```

## Usage

1. **Run the program**:
   ```bash
   python adder.py
   ```

2. **Select a folder** containing your album cover images using the "Browse" button

3. **Choose logo position**:
   - Bottom Left
   - Bottom Middle  
   - Bottom Right

4. **Adjust logo size** using the slider (50-200 pixels)

5. **Preview the result** using the "Update Preview" button

6. **Process images** by clicking "Process Images"

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Important Notes

- **Backup**: Original files are automatically backed up with '_original' suffix before modification
- **Logo file**: The program requires `paec.png` to be in the same directory as the script
- **Batch processing**: All images in the selected folder will be processed
- **Confirmation**: You'll be asked to confirm before processing begins

## File Structure

```
batch parental/
├── adder.py                    # Main program
├── paec.png                    # Parental advisory logo
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Example

1. Place your album cover images in a folder
2. Run the program and select that folder
3. Choose "Bottom Right" position and size 120 pixels
4. Preview the result
5. Click "Process Images" to apply the logo to all images

The program will create backups of your original files and add the parental advisory logo to each image in the selected position. 