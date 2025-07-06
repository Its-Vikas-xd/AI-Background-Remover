import streamlit as st
from PIL import Image
from rembg import remove
import io
import base64

# Page setup
st.set_page_config(
    page_title="AI Background Remover | AI-Powered Tool",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with vibrant accessible colors
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        color: #2A2D43;
    }}
    
    :root {{
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #00BFA6;
        --dark: #2A2D43;
        --light: #F7F9FC;
    }}
    
    body {{
        background-color: #f0f2f6;
    }}
    
    .header {{
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, var(--primary) 0%, #7b68ee 100%);
        color: white;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 10px 20px rgba(108, 99, 255, 0.2);
    }}
    
    .feature-card {{
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        border: none;
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(108, 99, 255, 0.15);
    }}
    
    .feature-card h3, .feature-card p {{
        color: #2A2D43 !important;
    }}
    
    .success-badge {{
        background: linear-gradient(135deg, var(--accent) 0%, #00ccb1 100%);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        margin: 1.5rem auto;
        width: fit-content;
        box-shadow: 0 5px 15px rgba(0, 191, 166, 0.3);
    }}
    
    .download-btn {{
        background: linear-gradient(135deg, var(--secondary) 0%, #ff7e9a 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        display: block;
        text-align: center;
        margin: 1.5rem auto;
        width: 85%;
        font-size: 1.1rem;
        box-shadow: 0 5px 15px rgba(255, 101, 132, 0.3);
        transition: all 0.4s ease;
        border: none;
    }}
    
    .download-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 101, 132, 0.4);
        color: white !important;
    }}
    
    .upload-area {{
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }}
    
    .upload-area:hover {{
        border-color: var(--primary);
        background-color: #fafbff;
    }}
    
    .image-container {{
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23e5e7eb' fill-opacity='0.4' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E");
        border-radius: 16px;
        padding: 20px;
        display: flex;
        justify-content: center;
    }}
    
    .comparison-container {{
        display: flex;
        justify-content: space-around;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }}
    
    .comparison-box {{
        flex: 1;
        min-width: 300px;
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }}
    
    .comparison-box:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }}
    
    .comparison-header {{
        background: linear-gradient(135deg, var(--primary) 0%, #7b68ee 100%);
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
    }}
    
    footer {{
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid #e9ecef;
        background: white;
        border-radius: 20px 20px 0 0;
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    @media (max-width: 768px) {{
        .comparison-container {{
            flex-direction: column;
        }}
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: #2A2D43 !important;
    }}
    
    p, div, span {{
        color: #3d4457 !important;
    }}
    
    .dark-text {{
        color: #2A2D43 !important;
    }}
    
    .light-text {{
        color: #6c757d !important;
    }}
    
    /* Feature cards with icons */
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, var(--primary) 0%, #7b68ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    /* Color options styling */
    .color-options {{
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin: 20px 0;
    }}
    
    .color-option {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        border: 3px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .color-option:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    
    .color-option.selected {{
        border: 3px solid #2A2D43;
        transform: scale(1.15);
    }}
    
    .color-label {{
        text-align: center;
        font-size: 0.8rem;
        margin-top: 5px;
        color: #2A2D43;
    }}
    
    .color-preview {{
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .color-preview h4 {{
        margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# Introduction section
st.markdown("""
<div class="header">
    <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">✨ AI BACKGROUND REMOVER</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Remove backgrounds instantly with AI - 100% automatic and free!</p>
</div>
""", unsafe_allow_html=True)

# Features section using columns
st.markdown("## 🚀 Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Ultra-Fast Processing</h3>
        <p>Remove backgrounds in seconds </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Perfect Results</h3>
        <p>Hair, fur, complex edges - our AI handles it all</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Privacy Protected</h3>
        <p>Your images are never stored or shared with anyone</p>
    </div>
    """, unsafe_allow_html=True)

# How it works section
st.markdown("""
## 🌟 How It Works

<div style="display: flex; justify-content: space-between; flex-wrap: wrap; margin: 2rem 0;">
    <div style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">1️⃣</div>
        <h3>Upload</h3>
        <p>Any image (JPG, PNG supported)</p>
    </div>
    <div style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">2️⃣</div>
        <h3>AI Processing</h3>
        <p>Instant background removal</p>
    </div>
    <div style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">3️⃣</div>
        <h3>Download</h3>
        <p>Get your transparent PNG</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Function to remove background
def remove_background(image):
    try:
        input_image = Image.open(image)
        output_image = remove(input_image)
        return output_image
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        st.info("💡 Tip: Try using a different image format or check file size")
        return None

# Function to create download link
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    
    if img.mode == 'RGBA':
        img.save(buffered, format="PNG")
    else:
        img.save(buffered, format="PNG")
    
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="{filename}" class="download-btn pulse">{text}</a>'

# Function to add colored background
def add_colored_background(image, color_hex):
    """Add a colored background to a transparent image"""
    if color_hex is None:
        # Return the transparent image as is
        return image
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
        
    background = Image.new('RGBA', image.size, color_hex)
    composite = Image.alpha_composite(background, image)
    return composite.convert('RGB')

# Initialize session state for color selection
if 'selected_color' not in st.session_state:
    st.session_state.selected_color = None

# Define color options (name and hex value)
COLOR_OPTIONS = {
    "Transparent": None,
    "Pure White": "#FFFFFF",
    "Sky Blue": "#87CEEB",
    "Lime Green": "#32CD32",
    "Sunshine Yellow": "#FFD700",
    "Coral Pink": "#FF7F50",
    "Lavender": "#E6E6FA"
}

# File uploader section
st.markdown("---")
st.markdown('<h2 style="text-align: center;">📤 UPLOAD YOUR IMAGE</h2>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    " ",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed",
    key="file_uploader"
)

if uploaded_file is None:
    st.markdown("""
    <div class="upload-area">
        <div style="font-size: 5rem; color: #6C63FF;">📁</div>
        <h3 style="color: #2A2D43;">Drag & Drop Your Image Here</h3>
        <p style="color: #6c757d;">or click to browse files</p>
        <p style="font-size: 0.9rem; color: #6c757d; margin-top: 1rem;">Supports JPG, PNG (Max 10MB)</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    # File info
    file_size = len(uploaded_file.getvalue()) / 1024
    st.success(f"**File uploaded:** {uploaded_file.name} ({file_size:.1f} KB)")
    
    # Display original image
    st.subheader("Your Image Preview")
    st.image(uploaded_file, width=400, use_container_width=True)
    
    # Process button
    if st.button("✨ REMOVE BACKGROUND NOW", 
                 type="primary", 
                 use_container_width=True,
                 help="Click to process your image with AI"):
        
        with st.spinner("🧠 AI is working its magic..."):
            result = remove_background(uploaded_file)
            
            if result:
                st.balloons()
                st.markdown('<div class="success-badge">✅ BACKGROUND REMOVED SUCCESSFULLY!</div>', unsafe_allow_html=True)
                
                # Store result in session state
                st.session_state.result_image = result
                
                # Display comparison
                st.markdown("## Before & After")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="comparison-box">
                        <div class="comparison-header">Original</div>
                        <div style="padding: 1.5rem; display: flex; justify-content: center;">
                            <img src="data:image/png;base64,{orig}" width="100%" style="max-width: 300px; border-radius: 8px;">
                        </div>
                    </div>
                    """.format(orig=base64.b64encode(uploaded_file.getvalue()).decode()), 
                    unsafe_allow_html=True)
                
                with col2:
                    buffered = io.BytesIO()
                    result.save(buffered, format="PNG")
                    result_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    st.markdown("""
                    <div class="comparison-box">
                        <div class="comparison-header" style="background: linear-gradient(135deg, var(--accent) 0%, #00ccb1 100%);">Result</div>
                        <div class="image-container">
                            <img src="data:image/png;base64,{res}" width="100%" style="max-width: 300px; border-radius: 8px;">
                        </div>
                    </div>
                    """.format(res=result_str), 
                    unsafe_allow_html=True)
                
                # Download button for transparent version
                st.markdown(get_image_download_link(
                    result,
                    f"no_bg_{uploaded_file.name.split('.')[0]}.png",
                    "⬇ DOWNLOAD TRANSPARENT PNG"
                ), unsafe_allow_html=True)
                
                # Reset selected color
                st.session_state.selected_color = None
                
                # Force a rerun to update color selection UI
                

# Show color options and preview if we have a processed image
if 'result_image' in st.session_state and st.session_state.result_image:
    # Color selection section
    st.markdown("---")
    st.markdown("## 🎨 Choose a Background Color")
    
    # Create color options
    st.markdown('<div class="color-options">', unsafe_allow_html=True)
    cols = st.columns(len(COLOR_OPTIONS))
    for idx, (color_name, hex_code) in enumerate(COLOR_OPTIONS.items()):
        with cols[idx]:
            # Create a colored circle for each option
            if hex_code:
                color_style = f"background-color: {hex_code};"
            else:
                # Transparent option - checkerboard pattern
                color_style = """
                    background: 
                        linear-gradient(45deg, #ccc 25%, transparent 25%), 
                        linear-gradient(-45deg, #ccc 25%, transparent 25%),
                        linear-gradient(45deg, transparent 75%, #ccc 75%),
                        linear-gradient(-45deg, transparent 75%, #ccc 75%);
                    background-size: 10px 10px;
                    background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
                """    
            # Add border for selected color
            selected = "selected" if st.session_state.selected_color == hex_code else ""
            
            # Use st.button to handle selection
            if st.button(
                "",
                key=f"color_btn_{idx}",
                help=color_name
            ):
                st.session_state.selected_color = hex_code
               
                
            st.markdown(f"""
                <div class="color-option {selected}" 
                     style="{color_style}"
                     onclick="document.querySelector('button[data-testid=\"stButton:color_btn_{idx}\"]').click();">
                </div>
                <div class="color-label">{color_name}</div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Preview of selected color
    if st.session_state.selected_color is not None:
        st.markdown("### 🖼️ Preview with Selected Background")
        
        # Add colored background
        colored_image = add_colored_background(st.session_state.result_image, st.session_state.selected_color)
        st.image(colored_image, width=400, use_container_width=True)
        
        # Get color name for download button text
        color_name = [name for name, code in COLOR_OPTIONS.items() if code == st.session_state.selected_color][0]
        
        # Download button for colored version
        st.markdown(get_image_download_link(
            colored_image,
            f"colored_bg_{color_name.lower().replace(' ', '_')}_{uploaded_file.name.split('.')[0]}.png",
            f"⬇ DOWNLOAD WITH {color_name.upper()} BACKGROUND"
        ), unsafe_allow_html=True)
    else:
        st.info("👆 Select a background color to preview")
    
    # Reset option
    st.markdown("---")
    if st.button("🔄 PROCESS ANOTHER IMAGE", 
                 use_container_width=True,
                 type="secondary"):
        # Clear session state
        st.session_state.pop('result_image', None)
        st.session_state.pop('selected_color', None)
        st.rerun()

# Footer
st.markdown("""
<footer>
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 1rem; flex-wrap: wrap;">
        <span style="display: flex; align-items: center; gap: 5px;">✉️ itsvikassharma007@gmail.com</span>
        <span style="display: flex; align-items: center; gap: 5px;">🐦 https://x.com/ItsVikasXd</span>
        <span style="display: flex; align-items: center; gap: 5px;">💬 https://github.com/Its-Vikas-xd </span>
    </div>
    <p>© 2025 Vikas | All Rights Reserved</p>
    <p style="font-size: 0.8rem; margin-top: 1rem; color: #6c757d;">Powered by Streamlit, rembg, and advanced AI technology</p>
</footer>
""", unsafe_allow_html=True)