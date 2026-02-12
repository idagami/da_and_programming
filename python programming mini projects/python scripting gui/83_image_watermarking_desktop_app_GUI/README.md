A simple desktop application that allows users to add custom text watermarks to images. Built with Python and Tkinter, this tool provides an intuitive GUI for watermarking photos with your company logo, copyright text, or any custom message.

## Features

- **Image Upload**: Support for JPEG, JPG, PNG, and GIF formats
- **Custom Watermark Text**: Add any text as a watermark
- **Live Preview**: See a thumbnail preview of your uploaded image
- **Easy Workflow**: Simple 3-step process (Upload → Add Watermark → Review)
- **Save Functionality**: Automatically saves watermarked images
- **Reset Option**: Clear all inputs and start fresh

## Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework
- **PIL (Pillow)** - Image processing
- **Custom Watermark Class** - Watermarking logic

## How to Use

1. **Step 1**: Click "Upload image" and select your image file
2. **Step 2**: Enter your watermark text (default: "Rainbow LTD") and click "Add watermark"
3. **Step 3**: Click "Review image" to view the watermarked result
4. Use "Reset" button to clear and start over

## Installation

```bash
pip install pillow
```

## Running the Application

```bash
python main.py
```

## Project Structure

- `main.py` - Main application GUI
- `watermark_class.py` - Watermarking functionality
- `logo.png` - Application logo

## Default Settings

- Preview width: 200px
- Default watermark: "Rainbow LTD"
- Window size: 500x400 (minimum)

## Requirements

- Python 3.13
- Pillow library
- Tkinter (usually included with Python)
