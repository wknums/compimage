#!/usr/bin/env python3
"""
composite_image_app.py

Streamlit web app for creating composite images from 4 uploaded images.
Provides an intuitive interface to upload images and view the resulting composite.

Usage:
    streamlit run composite_image_app.py
"""

import streamlit as st
import os
import tempfile
from PIL import Image
import io
from composite_image_creator import (
    create_composite_image, 
    is_portrait, 
    is_landscape,
    get_image_dimensions
)

def save_uploaded_file(uploaded_file, temp_dir):
    """Save an uploaded file to a temporary directory and return the path."""
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def display_image_info(image_path, label):
    """Display information about an uploaded image."""
    width, height = get_image_dimensions(image_path)
    orientation = "Portrait" if is_portrait(image_path) else "Landscape" if is_landscape(image_path) else "Square"
    
    # Get file size
    file_size = os.path.getsize(image_path)
    file_size_mb = file_size / (1024 * 1024)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        img = Image.open(image_path)
        st.image(img, caption=label, width=150)
    with col2:
        st.write(f"**{label}**")
        st.write(f"Dimensions: {width} × {height}")
        st.write(f"Orientation: {orientation}")
        st.write(f"Aspect Ratio: {width/height:.2f}")
        st.write(f"File Size: {file_size_mb:.2f} MB")

def main():
    st.set_page_config(
        page_title="Composite Image Creator",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Composite Image Creator")
    st.markdown("""
    Upload 4 images (PNG or JPG) to create an intelligent composite image. 
    The app will automatically arrange portrait and landscape images for the best square-like result.
    """)
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("How it works:")
        st.markdown("""
        1. **Upload 4 images** (PNG or JPG format)
        2. **Preview** your images and their orientations
        3. **Generate** the composite image
        4. **Download** the result
        
        **Smart Arrangement:**
        - Portrait images are joined horizontally
        - Landscape images are joined vertically  
        - The final arrangement creates the most square-like result
        """)
        
        st.header("Tips:")
        st.markdown("""
        - Mix portrait and landscape images for best results
        - Images will be arranged automatically
        - The app tries to create a near-square composite
        - Large images may take a moment to process
        """)
    
    # File upload section
    st.header("📁 Upload Your Images")
    
    uploaded_files = st.file_uploader(
        "Choose 4 images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload exactly 4 images in PNG or JPG format"
    )
    
    if uploaded_files:
        if len(uploaded_files) != 4:
            st.error(f"Please upload exactly 4 images. You have uploaded {len(uploaded_files)} images.")
            return
        
        st.success(f"✅ {len(uploaded_files)} images uploaded successfully!")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            image_paths = []
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file, temp_dir)
                image_paths.append(file_path)
            
            # Display image previews and info
            st.header("🔍 Image Preview & Analysis")
            
            # Count orientations
            portrait_count = sum(1 for path in image_paths if is_portrait(path))
            landscape_count = sum(1 for path in image_paths if is_landscape(path))
            square_count = 4 - portrait_count - landscape_count
              # Display orientation summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Portrait Images", portrait_count)
            with col2:
                st.metric("Landscape Images", landscape_count)
            with col3:
                st.metric("Square Images", square_count)
            
            # Calculate total input file size
            total_input_size = sum(uploaded_file.size for uploaded_file in uploaded_files)
            total_input_mb = total_input_size / (1024 * 1024)
            st.info(f"📊 Total input files size: {total_input_mb:.2f} MB")
            
            # Display individual image info
            for i, (uploaded_file, image_path) in enumerate(zip(uploaded_files, image_paths)):
                with st.expander(f"Image {i+1}: {uploaded_file.name}", expanded=False):
                    display_image_info(image_path, f"Image {i+1}")
              # Generate composite button
            st.header("🎨 Generate Composite Image")
            
            # Downscale options
            st.subheader("📏 Image Size Options")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                downscale_factor = st.slider(
                    "Downscale Factor (reduces file size)",
                    min_value=0.25,
                    max_value=1.0,
                    value=1.0,
                    step=0.05,
                    help="1.0 = original size, 0.5 = 50% size, 0.25 = 25% size"
                )
            
            with col2:
                if downscale_factor < 1.0:
                    st.info(f"🔽 {downscale_factor:.0%} of original size")
                    size_reduction = (1 - downscale_factor**2) * 100
                    st.write(f"📉 ~{size_reduction:.0f}% smaller file")
                else:
                    st.info("📐 Original size")
            
            if st.button("🚀 Create Composite Image", type="primary", use_container_width=True):
                with st.spinner("Creating composite image... This may take a moment for large images."):
                    try:
                        # Create output path in temp directory
                        output_path = os.path.join(temp_dir, "composite_output.png")
                          # Create the composite image
                        create_composite_image(image_paths, output_path, downscale_factor)# Load and display the result
                        composite_img = Image.open(output_path)
                        
                        # Convert PIL image to bytes for download with optimization
                        img_buffer = io.BytesIO()
                        
                        # Save with optimization based on file extension
                        if output_path.lower().endswith('.png'):
                            composite_img.save(img_buffer, format='PNG', optimize=True, compress_level=6)
                        else:
                            # Default to PNG with optimization
                            composite_img.save(img_buffer, format='PNG', optimize=True, compress_level=6)
                        
                        img_bytes = img_buffer.getvalue()
                        
                        st.success("✅ Composite image created successfully!")
                        
                        # Display result
                        st.header("🎉 Your Composite Image")
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.image(composite_img, caption="Composite Image", use_container_width=True)
                        
                        with col2:
                            st.subheader("Image Details")
                            st.write(f"**Dimensions:** {composite_img.width} × {composite_img.height}")
                            st.write(f"**Aspect Ratio:** {composite_img.width/composite_img.height:.3f}")
                            
                            # Calculate and display file size
                            file_size_mb = len(img_bytes) / (1024 * 1024)
                            st.write(f"**File Size:** {file_size_mb:.2f} MB")
                            
                            # Compare with input sizes
                            total_input_mb = sum(uploaded_file.size for uploaded_file in uploaded_files) / (1024 * 1024)
                            compression_ratio = file_size_mb / total_input_mb if total_input_mb > 0 else 1
                            st.write(f"**Input Total:** {total_input_mb:.2f} MB")
                            if compression_ratio < 1.2:
                                st.write(f"**Compression:** ✅ {compression_ratio:.1f}x")
                            else:
                                st.write(f"**Size Ratio:** ⚠️ {compression_ratio:.1f}x")
                            
                            # Calculate how close to square it is
                            square_diff = abs((composite_img.width/composite_img.height) - 1.0)
                            if square_diff < 0.1:
                                st.write("📐 **Very close to square!**")
                            elif square_diff < 0.3:
                                st.write("📐 **Reasonably square**")
                            else:
                                st.write("📐 **More rectangular**")                        
                        # Download button
                        st.header("💾 Download Your Image")
                        
                        st.download_button(
                            label="📥 Download Composite Image",
                            data=img_bytes,
                            file_name="composite_image.png",
                            mime="image/png",
                            use_container_width=True                        )
                        
                        # Show arrangement info
                        with st.expander("🔍 View Arrangement Details", expanded=False):
                            st.write("**Arrangement Strategy Used:**")
                            if landscape_count == 4:
                                st.write("- ✅ **Optimal 4 Landscape Strategy:**")
                                st.write("  - Images 1&2 joined vertically (left pair)")
                                st.write("  - Images 3&4 joined vertically (right pair)")
                                st.write("  - Two pairs joined horizontally for square result")
                            elif portrait_count == 4:
                                st.write("- ✅ **Optimal 4 Portrait Strategy:**")
                                st.write("  - Images 1&2 joined horizontally (top pair)")
                                st.write("  - Images 3&4 joined horizontally (bottom pair)")  
                                st.write("  - Two pairs joined vertically for square result")
                            elif portrait_count >= 2 and landscape_count >= 2:
                                st.write("- ✅ **Mixed Orientation Strategy:**")
                                st.write("  - Portrait images joined horizontally")
                                st.write("  - Landscape images joined vertically") 
                                st.write("  - Results combined for optimal square ratio")
                            elif portrait_count >= 3:
                                st.write("- **Multiple Portrait Strategy:**")
                                st.write("  - Multiple portrait images arranged optimally")
                            elif landscape_count >= 3:
                                st.write("- **Multiple Landscape Strategy:**") 
                                st.write("  - Multiple landscape images arranged optimally")
                            else:
                                st.write("- **2×2 Grid Strategy:**")
                                st.write("  - Standard grid arrangement used")
                            
                            if downscale_factor < 1.0:
                                st.write(f"\n**Size Optimization:**")
                                st.write(f"- 🔽 Downscaled to {downscale_factor:.0%} of original size")
                                st.write(f"- 📉 Estimated file size reduction: ~{(1 - downscale_factor**2) * 100:.0f}%")
                            else:
                                st.write(f"\n**Size:** Original dimensions maintained")
                        
                    except Exception as e:
                        st.error(f"❌ Error creating composite image: {str(e)}")
                        st.exception(e)
    
    else:
        st.info("👆 Please upload 4 images to get started!")
        
        # Show example layout
        st.header("📋 Example Usage")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ideal Input:")
            st.markdown("""
            - 2 Portrait images (taller than wide)
            - 2 Landscape images (wider than tall)
            - Any image formats: PNG, JPG, JPEG
            """)
        
        with col2:
            st.subheader("Expected Output:")
            st.markdown("""
            - Smart arrangement for near-square result
            - Portrait images joined side-by-side
            - Landscape images stacked vertically
            - Optimized final composition
            """)

if __name__ == "__main__":
    main()
