!pip install --upgrade pip
import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import os
import time
import zipfile
from io import BytesIO
import base64
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Neural Style Transfer Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for professional styling
st.markdown("""
<style>
    /* Main containers and backgrounds */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Cards styling */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    h1 {
        background: linear-gradient(90deg, #8e44ad, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 1rem !important;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    .primary-btn {
        background: linear-gradient(45deg, #6366f1, #8b5cf6) !important;
        color: white !important;
    }
    
    .download-btn {
        background: linear-gradient(45deg, #10b981, #059669) !important;
        color: white !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.1rem !important;
        border: none !important;
    }
    
    /* Radio and checkbox styling */
    .stRadio>div {
        background-color: rgba(255, 255, 255, 0.6) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
    }
    
    /* Separator styling */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-image: linear-gradient(to right, #6366f1, #8b5cf6) !important;
    }
    
    /* Style gallery improvements */
    .style-card {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        margin-bottom: 1rem !important;
        border: 2px solid transparent !important;
    }
    
    .style-card:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15) !important;
        cursor: pointer !important;
        border: 2px solid #6366f1 !important;
    }
    
    .style-card.selected {
        border: 3px solid #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Image containers */
    .image-container {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center !important;
        padding: 1.5rem !important;
        margin-top: 3rem !important;
        border-top: 1px solid rgba(0,0,0,0.1) !important;
        font-size: 0.9rem !important;
        color: #64748b !important;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .loading-container {
        animation: pulse 1.5s infinite ease-in-out;
        text-align: center;
        padding: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.6);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-top: 3px solid #8b5cf6 !important;
        font-weight: bold;
        color: #2c3e50;
    }
    
    /* File uploader */
    .stFileUploader > div > button {
        background-color: rgba(99, 102, 241, 0.1) !important;
        border: 1px dashed #6366f1 !important;
        border-radius: 8px !important;
    }
    
    /* Toast message */
    .toast-message {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: fadeInOut 3s forwards;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-20px); }
        10% { opacity: 1; transform: translateY(0); }
        90% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-20px); }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        .css-1r6slb0, .css-12oz5g7 {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define paths
STYLES_DIR = "Styles"

# Session state initialization
if 'selected_styles' not in st.session_state:
    st.session_state['selected_styles'] = []
if 'results' not in st.session_state:
    st.session_state['results'] = []
if 'content_image' not in st.session_state:
    st.session_state['content_image'] = None
if 'processing_complete' not in st.session_state:
    st.session_state['processing_complete'] = False

# Helper functions
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_bg_from_base64(base64_data):
    return f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{base64_data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with st.spinner("Loading Neural Style Transfer model... This may take a moment"):
        model = hub.load('https://kaggle.com/models/google/arbitrary-image-stylization-v1/frameworks/TensorFlow1/variations/256/versions/1')
    return model

def preprocess_image(image, is_style=False):
    img = np.array(image).astype(np.float32)[np.newaxis, ...] / 255.
    if is_style:
        img = tf.image.resize(img, (256, 256))
    return img

def style_transfer(content_image, style_image, model):
    outputs = model(tf.constant(content_image), tf.constant(style_image))
    return outputs[0][0].numpy()

def create_zip(images, style_names=None):
    mem_file = BytesIO()
    with zipfile.ZipFile(mem_file, 'w') as zf:
        for idx, img in enumerate(images):
            img_buffer = BytesIO()
            Image.fromarray(img).save(img_buffer, format="PNG")
            name = style_names[idx] if style_names else f"style_{idx+1}"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zf.writestr(f"{name}_{timestamp}.png", img_buffer.getvalue())
    mem_file.seek(0)
    return mem_file

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}" class="download-link">{text}</a>'
    return href

def display_toast(message):
    toast_code = f"""
    <div class="toast-message" id="toast">
        {message}
    </div>
    <script>
        setTimeout(function() {{
            document.getElementById('toast').style.display = 'none';
        }}, 3000);
    </script>
    """
    st.markdown(toast_code, unsafe_allow_html=True)

def main():
    # Load the model
    model = load_model()
    
    # Header with animation
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🎨 Neural Style Transfer Studio</h1>
        <p style="font-size: 1.2rem; color: #4b5563; margin-bottom: 30px;">
            Transform your photos into artistic masterpieces powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab3 = st.tabs(["📸 Upload & Create", "ℹ️ About"])
    
    with tab1:
        # Two column layout for upload section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(to right, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
                        padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: #3b82f6; margin-bottom: 15px;">📤 Content Image</h3>
                <p style="margin-bottom: 15px;">Upload the photograph you want to transform</p>
            </div>
            """, unsafe_allow_html=True)
            
            content_file = st.file_uploader(
                "Choose a content image", 
                type=["jpg", "jpeg", "png", "webp"],
                key="content_uploader",
                help="This is the image that will be styled"
            )
            
            if content_file:
                content_img = Image.open(content_file).convert("RGB")
                st.session_state['content_image'] = content_img
                
                # Display with better styling
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(content_img, caption="Your Content Image", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Image info
                width, height = content_img.size
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.7); padding: 10px; border-radius: 8px; 
                            margin-top: 10px; font-size: 0.9rem; color: #4b5563;">
                    📊 Image dimensions: {width} × {height} pixels
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Style selection with improved UI
            st.markdown("""
            <div style="background: linear-gradient(to right, rgba(255,255,255,0.7), rgba(255,255,255,0.9)); 
                        padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: #8b5cf6; margin-bottom: 15px;">🖌️ Style Selection</h3>
                <p style="margin-bottom: 15px;">Choose an artistic style to apply</p>
            </div>
            """, unsafe_allow_html=True)
            
            style_option = st.radio(
                "Select Style Source:",
                ["🎨 Predefined Styles", "🖌️ Custom Style"],
                horizontal=True,
                help="Choose from our collection or upload your own style image"
            )
            
            if style_option == "🎨 Predefined Styles":
                # Filter for selection mode
                st.markdown('<div style="padding: 15px 0 10px 0;">', unsafe_allow_html=True)
                selection_mode = st.radio(
                    "Selection Mode:",
                    ["Single Style", "Multiple Styles"],
                    horizontal=True,
                    help="Choose one style or apply multiple styles to your image"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Custom style upload with better UI
                st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
                custom_style = st.file_uploader(
                    "Upload your style image", 
                    type=["jpg", "jpeg", "png", "webp"],
                    help="This image provides the artistic style to apply"
                )
                
                if custom_style:
                    custom_img = Image.open(custom_style).convert("RGB")
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(custom_img, caption="Your Style Image", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Style Gallery with enhanced UI
        if style_option == "🎨 Predefined Styles":
            st.markdown("""
            <div style="background: linear-gradient(to right, rgba(255,255,255,0.8), rgba(255,255,255,0.6)); 
                        padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Available Styles</h3>
                <p style="margin-bottom: 15px;">Click to select a style to apply to your image</p>
            </div>
            """, unsafe_allow_html=True)
            
            style_files = sorted([os.path.join(STYLES_DIR, f) for f in os.listdir(STYLES_DIR)])
            style_names = [os.path.splitext(os.path.basename(path))[0] for path in style_files]
            
            # Dynamic grid layout based on available styles
            cols_per_row = 5
            rows = (len(style_files) + cols_per_row - 1) // cols_per_row
            
            for i in range(rows):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i * cols_per_row + j
                    if idx < len(style_files):
                        with cols[j]:
                            with open(style_files[idx], "rb") as f:
                                img = Image.open(f).convert("RGB")
                                img.thumbnail((150, 150))
                                
                                # Check if this style is selected
                                is_selected = style_files[idx] in st.session_state['selected_styles']
                                selected_class = "selected" if is_selected else ""
                                
                                # Custom HTML/CSS for better style card display
                                st.markdown(f"""
                                <div class="style-card {selected_class}" id="style-{idx}" 
                                     onclick="this.classList.toggle('selected');">
                                """, unsafe_allow_html=True)
                                st.image(img, use_container_width=True, output_format="PNG")
                                st.markdown(f"""
                                <div style="text-align: center; padding: 8px 5px; 
                                            background-color: rgba(255,255,255,0.8); font-weight: 500;">
                                    {style_names[idx]}
                                </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Checkbox for style selection with better UX
                                if st.checkbox(
                                    f"Select", 
                                    key=f"style_{idx}",
                                    value=is_selected,
                                    label_visibility="collapsed"
                                ):
                                    if style_files[idx] not in st.session_state['selected_styles']:
                                        if selection_mode == "Single Style":
                                            st.session_state['selected_styles'] = [style_files[idx]]
                                        else:
                                            st.session_state['selected_styles'].append(style_files[idx])
                                elif style_files[idx] in st.session_state['selected_styles']:
                                    st.session_state['selected_styles'].remove(style_files[idx])
        
        # Process section with improved UI
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(to right, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
                    padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px; margin-bottom: 20px;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🖌️ Generate Your Masterpiece</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced settings collapsible section
        with st.expander("⚙️ Advanced Settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                output_size = st.slider(
                    "Output Quality", 
                    min_value=1, 
                    max_value=10, 
                    value=8,
                    help="Higher quality results in larger file sizes"
                )
            with col2:
                preserve_colors = st.checkbox(
                    "Preserve Original Colors (Experimental)", 
                    value=False,
                    help="Attempts to maintain the original image colors while applying style"
                )
        
        # Processing button with better placement and styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_ready = content_file and ((style_option == "🎨 Predefined Styles" and st.session_state['selected_styles']) or 
                                            (style_option == "🖌️ Custom Style" and custom_style))
            
            if process_ready:
                if st.button("🖌️ Generate Artwork", use_container_width=True, type="primary"):
                    with st.spinner("🎨 Creating your masterpiece..."):
                        try:
                            # Progress bar for better UX
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            content_img = st.session_state['content_image']
                            content = preprocess_image(content_img)
                            results = []
                            style_names_used = []
                            
                            if style_option == "🎨 Predefined Styles":
                                total_styles = len(st.session_state['selected_styles'])
                                for idx, style_path in enumerate(st.session_state['selected_styles']):
                                    status_text.text(f"Processing style {idx+1}/{total_styles}...")
                                    progress_bar.progress((idx) / total_styles)
                                    
                                    style_name = os.path.splitext(os.path.basename(style_path))[0]
                                    style_names_used.append(style_name)
                                    
                                    with open(style_path, "rb") as f:
                                        style_img = Image.open(f).convert("RGB")
                                    
                                    style = preprocess_image(style_img, is_style=True)
                                    result = style_transfer(content, style, model)
                                    result_img = (result * 255).astype(np.uint8)
                                    results.append(result_img)
                                    
                                    # Add slight delay for visual feedback
                                    time.sleep(0.5)
                                    progress_bar.progress((idx + 1) / total_styles)
                            else:
                                status_text.text("Processing custom style...")
                                progress_bar.progress(0.3)
                                
                                style_img = Image.open(custom_style).convert("RGB")
                                style_names_used.append("Custom")
                                
                                style = preprocess_image(style_img, is_style=True)
                                result = style_transfer(content, style, model)
                                result_img = (result * 255).astype(np.uint8)
                                results.append(result_img)
                                
                                progress_bar.progress(1.0)
                            
                            st.session_state['results'] = results
                            st.session_state['style_names'] = style_names_used
                            st.session_state['processing_complete'] = True
                            
                            # Success message
                            status_text.text("✨ Your artwork is ready!")
                            time.sleep(1)
                            progress_bar.empty()
                            status_text.empty()
                            
                            # Scroll to results
                            st.markdown('<script>document.getElementById("results-section").scrollIntoView();</script>', 
                                        unsafe_allow_html=True)
                            
                            # Add success animation
                            st.balloons()
                        
                        except Exception as e:
                            st.error(f"Error during processing: {str(e)}")
                            st.error("Please try again with different images or check your connection.")
            else:
                st.button(
                    "🖌️ Generate Artwork (Select content and style first)", 
                    disabled=True, 
                    use_container_width=True
                )
        
        # Results section with improved UI
        if st.session_state['processing_complete'] and st.session_state['results']:
            st.markdown("""
            <div id="results-section" style="background: linear-gradient(to right, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
                        padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 30px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">✨ Your Masterpieces</h3>
                <p style="margin-bottom: 15px;">Here are your styled images ready to download</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download options
            col1, col2 = st.columns([1, 1])
            with col1:
                if len(st.session_state['results']) > 1:
                    zip_buffer = create_zip(st.session_state['results'], st.session_state['style_names'])
                    st.download_button(
                        label="📦 Download All Images (ZIP)",
                        data=zip_buffer,
                        file_name=f"neural_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
            
            # Display results in grid
            st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
            cols = st.columns(min(3, len(st.session_state['results'])))
            for idx, result in enumerate(st.session_state['results']):
                with cols[idx % len(cols)]:
                    # Result card with shadow and better styling
                    st.markdown("""
                    <div style="background-color: white; border-radius: 12px; overflow: hidden; 
                                box-shadow: 0 6px 12px rgba(0,0,0,0.15); margin-bottom: 20px;">
                    """, unsafe_allow_html=True)
                    
                    # Image display
                    st.image(
                        result, 
                        use_container_width=True,
                        caption=f"Style: {st.session_state['style_names'][idx]}",
                        output_format="PNG"
                    )
                    
                    # Individual download button
                    result_pil = Image.fromarray(result)
                    img_buffer = BytesIO()
                    result_pil.save(img_buffer, format="PNG")
                    
                    st.download_button(
                        label=f"📥 Download",
                        data=img_buffer.getvalue(),
                        file_name=f"{st.session_state['style_names'][idx]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_{idx}"
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)  # Close results-section div
    
    # About tab with added content
    with tab3:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2>ℹ️ About Neural Style Transfer Studio</h2>
            <p style="font-size: 1.1rem; color: #4b5563; margin-bottom: 20px;">
                Learn more about this application and the technology behind it
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### What is Neural Style Transfer?
        Neural Style Transfer is a technique that uses deep neural networks to combine the content of one image with the style of another. It separates and recombines content and style, allowing you to create artistic images effortlessly.

        ### About This Application
        This Streamlit application enables you to:
        - Upload a content image to transform
        - Select from predefined styles or upload a custom style image
        - Generate and download styled images individually or as a ZIP file

        ### Technology Used
        - **Model**: Arbitrary Image Stylization from TensorFlow Hub
        - **Framework**: Streamlit for the interactive web interface
        - **Backend**: TensorFlow for real-time image processing

        ### Notes
        - For optimal results, use high-quality images.
        - Processing time depends on image size and complexity.
        """)

if __name__ == "__main__":
    main()
