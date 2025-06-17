# Composite Image Creator

A Python utility that intelligently creates composite images from 4 input images by automatically arranging them to produce the most square-like result possible.

## Features

- 🖼️ **Smart Image Arrangement**: Automatically analyzes image orientations and arranges them optimally
- 📐 **Square-Optimized Results**: Algorithms designed to create near-square composite images
- 🎛️ **Multiple Interfaces**: Both command-line tool and web app available
- 📏 **Size Control**: Optional downscaling to reduce file sizes
- 🔧 **Format Support**: Works with PNG, JPG, and JPEG images
- 📊 **Detailed Analytics**: Provides orientation analysis and arrangement insights

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd compimage
```

2. **Create a virtual environment**:
```bash
python -m venv .venv
```

3. **Activate the virtual environment**:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

Launch the interactive Streamlit web app:

```bash
streamlit run composite_image_app.py
```

**Features of the Web App:**
- 📁 Drag & drop file upload for 4 images
- 🔍 Real-time image preview and analysis
- 📊 Orientation metrics (portrait, landscape, square counts)
- 🎚️ Interactive downscaling slider
- 💾 One-click download of results
- 📋 Detailed arrangement strategy explanations

### Command Line Tool

For batch processing or automation:

```bash
python composite_image_creator.py image1.jpg image2.png image3.jpg image4.png output.png
```

**With downscaling:**
```bash
python composite_image_creator.py image1.jpg image2.png image3.jpg image4.png output.png --downscale 0.5
```

**Command line options:**
- `--downscale FACTOR`: Scale down the final image (0.1 to 1.0)
  - `1.0` = original size (default)
  - `0.5` = 50% size 
  - `0.25` = 25% size

## How It Works

### Intelligent Arrangement Strategies

The tool uses different arrangement strategies based on the input image orientations:

1. **4 Landscape Images**:
   - Creates 2 vertical pairs (images stacked)
   - Joins pairs horizontally for optimal square result

2. **4 Portrait Images**:
   - Creates 2 horizontal pairs (images side-by-side)
   - Joins pairs vertically for optimal square result

3. **Mixed Orientations (2+ portrait, 2+ landscape)**:
   - Joins portrait images horizontally
   - Joins landscape images vertically
   - Combines results in the arrangement closest to square

4. **3+ Same Orientation**:
   - Groups pairs optimally
   - Tests multiple arrangements to find the most square result

5. **Fallback (mixed/square images)**:
   - Uses 2×2 grid arrangement

### Size Optimization

- **Automatic Format Detection**: Saves PNG or JPEG based on output filename
- **Compression**: Uses optimized settings (PNG compress_level=6, JPEG quality=85)
- **Downscaling**: Optional size reduction while maintaining aspect ratios
- **File Size Reporting**: Shows final file size and compression ratios

## Examples

### Example 1: Mixed Orientations (Ideal)
```bash
# Input: 2 portrait photos + 2 landscape photos
python composite_image_creator.py portrait1.jpg portrait2.jpg landscape1.jpg landscape2.jpg result.png
```
**Result**: Near-perfect square composite

### Example 2: All Landscape Photos
```bash
# Input: 4 landscape photos
python composite_image_creator.py landscape1.jpg landscape2.jpg landscape3.jpg landscape4.jpg result.png --downscale 0.5
```
**Result**: Square composite at 50% size

### Example 3: Web App Workflow
1. Run `streamlit run composite_image_app.py`
2. Upload 4 images via drag & drop
3. Review orientation analysis
4. Adjust downscale factor if needed
5. Click "Create Composite Image"
6. Download the result

## File Structure

```
compimage/
├── composite_image_creator.py    # Core logic and CLI tool
├── composite_image_app.py        # Streamlit web application
├── requirements.txt              # Python dependencies
└── README.md                    # This documentation
```

## Requirements

- **Python**: 3.7+
- **Pillow**: ≥10.0.0 (image processing)
- **Streamlit**: ≥1.28.0 (web app)
- **NumPy**: ≥1.24.0 (image arrays)

## Tips for Best Results

1. **Mix Orientations**: Use 2 portrait + 2 landscape images for optimal square results
2. **Similar Sizes**: Images of similar dimensions work best
3. **Quality vs Size**: Use downscaling for web sharing, keep original size for printing
4. **Format Choice**: Use PNG for screenshots/graphics, JPEG for photos

## Error Handling

The tool includes robust error handling for:
- ❌ Incorrect number of images (must be exactly 4)
- ❌ Missing or invalid image files
- ❌ Invalid downscale factors
- ❌ Unsupported image formats

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

## License

MIT License

Copyright (c) 2025 Wolfgang Knupp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

