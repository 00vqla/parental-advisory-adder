# Parental Advisory Logo Adder

A Python GUI application that adds parental advisory explicit logos to album covers and images. 

---

![App Preview](preview.png)
*Main application window with live preview*

![Result Example](result.png)
*Example of a processed image with the Parental Advisory logo*

---

## ✨ Features

- **Multiple positioning options**: Bottom Left, Bottom Middle, Bottom Right
- **Adjustable logo size**: 50-200 pixels with real-time preview
- **Live preview**: See exactly how the logo will appear before processing
- **Batch processing**: Process multiple images at once with progress tracking
- **Crop modes**: Choose between "Crop to Center" or "Stretch to Square"
- **Transparency support**: Preserves transparency in PNG images

## 🖼️ Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png) - with transparency support
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## 📋 Requirements

- Python 3.6 or higher
- Pillow (PIL) library
- tkinter (usually included with Python)

## 🚀 Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or install Pillow directly:
   ```bash
   pip install Pillow
   ```

## 🎯 Usage

1. **Run the application**:
   ```bash
   pytho3 adder.py
   ```

2. **Select images**: Click "Browse Files" to select one or more image files

3. **Configure settings**:
   - **Position**: Choose Bottom Left, Bottom Middle, or Bottom Right
   - **Logo Width**: Adjust size using the slider (50-200 pixels)
   **Crop Mode**: 
     - "Crop to Center": Crops image to square from center
     - "Stretch to Square": Stretches image to square (may distort)

4. **Preview**: The preview updates automatically as you change settings

## 📁 File Structure

```
parental-advisory-adder/
├── adder.py                    # Main application
├── parental.png                # Parental advisory logo
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 How It Works

- **Original files are never modified** - new files are created with "_modified" suffix
- **Transparency is preserved** - PNG images with transparency remain transparent
- **Live preview** shows exactly what the final result will look like
- **Progress tracking** shows processing status for batch operations
- **Auto folder opening** - after processing, the output folder opens automatically

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool! 