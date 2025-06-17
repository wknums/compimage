#!/usr/bin/env python3
"""
composite_image_creator.py

Creates a composite image from 4 input images by intelligently arranging them:
- Groups portrait images and joins them horizontally
- Groups landscape images and joins them vertically  
- Combines the results to create a near-square composite image

Usage:
    python composite_image_creator.py image1.png image2.jpg image3.png image4.jpg output.png

Dependencies: Pillow (PIL)
"""

import os
import sys
import argparse
from PIL import Image
from typing import List, Tuple, Optional


def is_portrait(image_path: str) -> bool:
    """Check if an image is in portrait orientation (height > width)."""
    with Image.open(image_path) as img:
        return img.height > img.width


def is_landscape(image_path: str) -> bool:
    """Check if an image is in landscape orientation (width > height)."""
    with Image.open(image_path) as img:
        return img.width > img.height


def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    """Get the width and height of an image."""
    with Image.open(image_path) as img:
        return img.width, img.height


def join_images_horizontally(img1_path: str, img2_path: str) -> Image.Image:
    """Join two images horizontally (side by side)."""
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Calculate dimensions for the combined image
    width = img1.width + img2.width
    height = max(img1.height, img2.height)
    
    # Create new image and paste the two images
    combined_img = Image.new('RGB', (width, height), color='white')
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (img1.width, 0))
    
    return combined_img


def join_images_vertically(img1_path: str, img2_path: str) -> Image.Image:
    """Join two images vertically (one on top of the other)."""
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Calculate dimensions for the combined image
    width = max(img1.width, img2.width)
    height = img1.height + img2.height
    
    # Create new image and paste the two images
    combined_img = Image.new('RGB', (width, height), color='white')
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (0, img1.height))
    
    return combined_img


def join_pil_images_horizontally(img1: Image.Image, img2: Image.Image) -> Image.Image:
    """Join two PIL Image objects horizontally."""
    width = img1.width + img2.width
    height = max(img1.height, img2.height)
    
    combined_img = Image.new('RGB', (width, height), color='white')
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (img1.width, 0))
    
    return combined_img


def join_pil_images_vertically(img1: Image.Image, img2: Image.Image) -> Image.Image:
    """Join two PIL Image objects vertically."""
    width = max(img1.width, img2.width)
    height = img1.height + img2.height
    
    combined_img = Image.new('RGB', (width, height), color='white')
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (0, img1.height))
    
    return combined_img


def calculate_aspect_ratio_diff(width: int, height: int) -> float:
    """Calculate how far the aspect ratio is from square (1.0)."""
    aspect_ratio = width / height
    return abs(aspect_ratio - 1.0)


def create_composite_image(image_paths: List[str], output_path: str, downscale_factor: float = 1.0):
    """
    Create a composite image from 4 input images by grouping and arranging them optimally.
    
    Args:
        image_paths: List of 4 image file paths
        output_path: Path where the composite image will be saved
        downscale_factor: Factor to downscale the final image (0.5 = 50% size, 0.25 = 25% size)
    """
    if len(image_paths) != 4:
        raise ValueError("Exactly 4 images are required")
    
    if downscale_factor <= 0 or downscale_factor > 1:
        raise ValueError("Downscale factor must be between 0 and 1")
    
    # Validate all image files exist
    for img_path in image_paths:
        if not os.path.isfile(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
    
    # Separate images by orientation
    portrait_images = [img for img in image_paths if is_portrait(img)]
    landscape_images = [img for img in image_paths if is_landscape(img)]
    square_images = [img for img in image_paths if not is_portrait(img) and not is_landscape(img)]
    
    print(f"Portrait images: {len(portrait_images)}")
    print(f"Landscape images: {len(landscape_images)}")
    print(f"Square images: {len(square_images)}")
      # Handle different combinations of orientations
    if len(landscape_images) == 4:
        # Special case: 4 landscape images - join pairs vertically, then horizontally
        print("Joining 4 landscape images: creating 2 vertical pairs, then joining horizontally...")
        
        # Create two vertical pairs
        left_pair = join_images_vertically(landscape_images[0], landscape_images[1])
        right_pair = join_images_vertically(landscape_images[2], landscape_images[3])
        
        # Join the pairs horizontally to create the most square-like result
        final_image = join_pil_images_horizontally(left_pair, right_pair)
        print(f"4 landscape arrangement completed (aspect ratio: {final_image.width/final_image.height:.3f})")
        
    elif len(portrait_images) == 4:
        # Special case: 4 portrait images - join pairs horizontally, then vertically  
        print("Joining 4 portrait images: creating 2 horizontal pairs, then joining vertically...")
        
        # Create two horizontal pairs
        top_pair = join_images_horizontally(portrait_images[0], portrait_images[1])
        bottom_pair = join_images_horizontally(portrait_images[2], portrait_images[3])
        
        # Join the pairs vertically to create the most square-like result
        final_image = join_pil_images_vertically(top_pair, bottom_pair)
        print(f"4 portrait arrangement completed (aspect ratio: {final_image.width/final_image.height:.3f})")
        
    elif len(portrait_images) >= 2 and len(landscape_images) >= 2:
        # Mixed case: at least 2 portrait and 2 landscape
        print("Joining 2 portrait images horizontally and 2 landscape images vertically...")
        
        portrait_combined = join_images_horizontally(portrait_images[0], portrait_images[1])
        landscape_combined = join_images_vertically(landscape_images[0], landscape_images[1])
        
        # Try both arrangements and pick the one closest to square
        option1 = join_pil_images_vertically(portrait_combined, landscape_combined)
        option2 = join_pil_images_horizontally(portrait_combined, landscape_combined)
        
        diff1 = calculate_aspect_ratio_diff(option1.width, option1.height)
        diff2 = calculate_aspect_ratio_diff(option2.width, option2.height)
        
        final_image = option1 if diff1 <= diff2 else option2
        arrangement = "vertical" if diff1 <= diff2 else "horizontal"
        print(f"Best mixed arrangement: {arrangement} (aspect ratio diff: {min(diff1, diff2):.3f})")
        
    elif len(portrait_images) >= 3:
        # 3+ portrait images: join 2 horizontally, then combine with remaining
        print("Joining portrait images...")
        
        portrait_pair = join_images_horizontally(portrait_images[0], portrait_images[1])
        remaining_img = Image.open(portrait_images[2])
        
        # Try both arrangements
        option1 = join_pil_images_vertically(portrait_pair, remaining_img)
        option2 = join_pil_images_horizontally(portrait_pair, remaining_img)
        
        diff1 = calculate_aspect_ratio_diff(option1.width, option1.height)
        diff2 = calculate_aspect_ratio_diff(option2.width, option2.height)
        
        final_image = option1 if diff1 <= diff2 else option2
        
        # Handle 4th image if it exists
        if len(image_paths) > 3:
            fourth_img = Image.open(image_paths[3])
            # Try adding the 4th image in both orientations
            temp1 = join_pil_images_vertically(final_image, fourth_img)
            temp2 = join_pil_images_horizontally(final_image, fourth_img)
            
            diff1 = calculate_aspect_ratio_diff(temp1.width, temp1.height)
            diff2 = calculate_aspect_ratio_diff(temp2.width, temp2.height)
            
            final_image = temp1 if diff1 <= diff2 else temp2
            
    elif len(landscape_images) >= 3:
        # 3+ landscape images: join 2 vertically, then combine with remaining
        print("Joining landscape images...")
        
        landscape_pair = join_images_vertically(landscape_images[0], landscape_images[1])
        remaining_img = Image.open(landscape_images[2])
        
        # Try both arrangements
        option1 = join_pil_images_vertically(landscape_pair, remaining_img)
        option2 = join_pil_images_horizontally(landscape_pair, remaining_img)
        
        diff1 = calculate_aspect_ratio_diff(option1.width, option1.height)
        diff2 = calculate_aspect_ratio_diff(option2.width, option2.height)
        
        final_image = option1 if diff1 <= diff2 else option2
        
        # Handle 4th image if it exists
        if len(image_paths) > 3:
            fourth_img = Image.open(image_paths[3])
            # Try adding the 4th image in both orientations
            temp1 = join_pil_images_vertically(final_image, fourth_img)
            temp2 = join_pil_images_horizontally(final_image, fourth_img)
            
            diff1 = calculate_aspect_ratio_diff(temp1.width, temp1.height)
            diff2 = calculate_aspect_ratio_diff(temp2.width, temp2.height)
            
            final_image = temp1 if diff1 <= diff2 else temp2            
    else:
        # Fallback: arrange all images in a 2x2 grid (for mixed orientations or squares)
        print("Creating 2x2 grid arrangement for mixed/square images...")
        
        # Join first two images horizontally
        top_row = join_images_horizontally(image_paths[0], image_paths[1])
        # Join last two images horizontally  
        bottom_row = join_images_horizontally(image_paths[2], image_paths[3])
        # Join the two rows vertically
        final_image = join_pil_images_vertically(top_row, bottom_row)
        print(f"2x2 grid arrangement completed (aspect ratio: {final_image.width/final_image.height:.3f})")    
    # Apply downscaling if requested
    if downscale_factor < 1.0:
        original_width, original_height = final_image.size
        new_width = int(original_width * downscale_factor)
        new_height = int(original_height * downscale_factor)
        
        print(f"Downscaling from {original_width}x{original_height} to {new_width}x{new_height} ({downscale_factor:.1%})")
        final_image = final_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save the final composite image with optimization
    save_optimized_image(final_image, output_path)
    print(f"Composite image saved to: {output_path}")
    print(f"Final dimensions: {final_image.width}x{final_image.height}")
    print(f"Aspect ratio: {final_image.width/final_image.height:.3f}")


def save_optimized_image(image: Image.Image, output_path: str):
    """Save image with optimization to reduce file size while maintaining quality."""
    # Get file extension to determine format
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()
    
    if ext == '.png':
        # For PNG: use compression level 6 (good balance of speed vs compression)
        # and optimize to reduce file size
        image.save(output_path, format='PNG', optimize=True, compress_level=6)
    elif ext in ['.jpg', '.jpeg']:
        # For JPEG: use quality 85 (good balance of quality vs size)
        # and optimize
        image.save(output_path, format='JPEG', quality=85, optimize=True)
    else:
        # Default to PNG with optimization for unknown extensions
        if not output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            output_path = os.path.splitext(output_path)[0] + '.png'
        image.save(output_path, format='PNG', optimize=True, compress_level=6)
    
    # Print file size info
    file_size = os.path.getsize(output_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")


def main():
    """Command-line interface for the composite image creator."""
    parser = argparse.ArgumentParser(
        description="Create a composite image from 4 input images"
    )
    parser.add_argument(
        "images",
        nargs=4,
        help="Paths to 4 input images (PNG or JPG)"
    )
    parser.add_argument(
        "output",
        help="Path for the output composite image"
    )
    parser.add_argument(
        "--downscale",
        type=float,
        default=1.0,
        help="Downscale factor (0.1 to 1.0). E.g., 0.5 = 50%% size, 0.25 = 25%% size"
    )
    
    args = parser.parse_args()
    
    try:
        create_composite_image(args.images, args.output, args.downscale)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
