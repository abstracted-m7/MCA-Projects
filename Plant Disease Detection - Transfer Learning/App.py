"""
🌱 Plant Disease Detection - Streamlit App
Uses pre-trained transfer learning model from Google Colab

Usage:
    1. Place model file: plant_disease_model.h5
    2. Place class file: class_indices.json
    3. Run: streamlit run app.py
"""

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

# ============================================================================
# Page Configuration
# ============================================================================
st.set_page_config(
    page_title="Plant Disease Detector",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Custom CSS
# ============================================================================
st.markdown("""
<style>
    .main {
        padding-top: 0px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Load Model and Class Indices
# ============================================================================
# @st.cache_resource
# def load_model():
#     """Load pre-trained model from file"""
#     try:
#         model = tf.keras.models.load_model('plant_disease_model.h5')
#         return model
#     except FileNotFoundError:
#         st.error("❌ Model file 'plant_disease_model.h5' not found!")
#         st.info("📝 Make sure the model file is in the same directory as this script")
#         return None
#fix part
@st.cache_resource
def load_model():
    """Load pre-trained model from file"""
    try:
        model = tf.keras.models.load_model(
            'plant_disease_model.h5',
            compile=False   # ✅ IMPORTANT FIX
        )
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

@st.cache_resource
def load_classes():
    """Load class indices from JSON file"""
    try:
        with open('class_indices.json', 'r') as f:
            class_indices = json.load(f)
        return class_indices
    except FileNotFoundError:
        st.error("❌ Class file 'class_indices.json' not found!")
        st.info("📝 Make sure the class indices file is in the same directory as this script")
        return None

# ============================================================================
# Sidebar Navigation
# ============================================================================
st.sidebar.title("🌱 Plant Disease Detector")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Section:",
    ["🏠 Home", "🔮 Predict", "📊 About Model", "ℹ️ Help"]
)

# ============================================================================
# Load Model and Classes
# ============================================================================
model = load_model()
class_indices = load_classes()

# Convert class indices for easy lookup
if class_indices:
    idx_to_class = {str(v): k for k, v in class_indices.items()}
else:
    idx_to_class = {}

# ============================================================================
# PAGE 1: HOME
# ============================================================================
if page == "🏠 Home":
    st.title("🌱 Plant Disease Detection")
    st.markdown("Using Transfer Learning with MobileNetV2")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome! 👋
        
        This application uses **transfer learning** to detect plant diseases from leaf images.
        
        **How it works:**
        1. Upload a plant leaf image (JPG, PNG)
        2. The model analyzes the image
        3. Get instant disease diagnosis
        4. View confidence scores
        
        **What you can detect:**
        - Disease type from leaf appearance
        - Plant species
        - Health status
        
        ### Key Features:
        - ⚡ Fast predictions (~1 second)
        - 🎯 High accuracy (82%+)
        - 📱 Mobile-friendly interface
        - 🔬 Transfer learning powered
        """)
    
    with col2:
        st.info("""
        ### Quick Stats
        - **Model**: MobileNetV2
        - **Classes**: 38
        - **Accuracy**: 82%
        - **Speed**: ~1 sec/image
        """)
    
    st.markdown("---")
    st.subheader("📸 Ready to predict?")
    st.markdown("Go to **🔮 Predict** tab to upload an image!")

# ============================================================================
# PAGE 2: PREDICT
# ============================================================================
elif page == "🔮 Predict":
    st.title("🔮 Predict Plant Disease")
    
    if model is None or class_indices is None:
        st.error("❌ Model or class file not found. Please check the setup.")
        st.stop()
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose a plant leaf image",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of a plant leaf"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            
            # Display original size
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            st.markdown("### 📋 Image Details")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Width", f"{image.width}px")
            with col_b:
                st.metric("Height", f"{image.height}px")
            with col_c:
                st.metric("Format", image.format)
    
    with col2:
        if uploaded_file is not None:
            st.subheader("🔮 Prediction Results")
            
            # Show loading status
            with st.spinner("🔄 Analyzing image..."):
                # Preprocess image
                # Resize to model input size (192, 192)
                img_resized = image.convert('RGB').resize((192, 192))
                img_array = np.array(img_resized) / 255.0
                
                # Add batch dimension
                img_batch = np.expand_dims(img_array, axis=0)
                
                # Make prediction
                predictions = model.predict(img_batch, verbose=0)
            
            # Get top prediction
            pred_class_idx = np.argmax(predictions[0])
            pred_confidence = np.max(predictions[0])
            pred_class = idx_to_class.get(str(pred_class_idx), "Unknown")
            
            # Display top prediction
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; color: white; text-align: center;">
                <h3 style="margin: 0;">Predicted Class</h3>
                <h2 style="margin: 10px 0 0 0; font-size: 28px;">{pred_class}</h2>
                <p style="margin: 10px 0 0 0; font-size: 20px;">{pred_confidence*100:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Top 5 predictions
            st.markdown("### 📊 Top 5 Predictions")
            
            # Get top 5
            top_5_indices = np.argsort(predictions[0])[-5:][::-1]
            
            # Create results dataframe
            results = []
            for idx in top_5_indices:
                class_name = idx_to_class.get(str(idx), "Unknown")
                confidence = predictions[0][idx]
                results.append({
                    "Class": class_name,
                    "Confidence": f"{confidence*100:.2f}%",
                    "Score": confidence
                })
            
            # Display as table
            for i, result in enumerate(results, 1):
                col_rank, col_class, col_conf = st.columns([0.5, 2, 1])
                with col_rank:
                    st.metric(f"#{i}", "")
                with col_class:
                    st.write(result["Class"])
                with col_conf:
                    st.write(result["Confidence"])
            
            # Confidence visualization
            st.markdown("### 📈 Confidence Scores")
            
            classes_display = [idx_to_class.get(str(idx), "Unknown") for idx in top_5_indices]
            confidences = [predictions[0][idx] * 100 for idx in top_5_indices]
            
            # Bar chart
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.barh(classes_display, confidences, color='#667eea')
            
            # Color the highest bar differently
            bars[0].set_color('#764ba2')
            
            ax.set_xlabel('Confidence (%)')
            ax.set_title('Prediction Confidence Scores')
            ax.set_xlim([0, 100])
            
            # Add value labels
            for i, (bar, conf) in enumerate(zip(bars, confidences)):
                ax.text(conf + 2, i, f'{conf:.1f}%', va='center')
            
            st.pyplot(fig, use_container_width=True)

# ============================================================================
# PAGE 3: ABOUT MODEL
# ============================================================================
elif page == "📊 About Model":
    st.title("📊 Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Architecture
        
        **Base Model**: MobileNetV2
        - Pre-trained on ImageNet
        - 3.5M parameters
        - Designed for mobile/edge devices
        
        **Custom Head**:
        - Dense(128) + ReLU
        - Dropout(0.3)
        - Dense(64) + ReLU
        - Dropout(0.3)
        - Dense(38) + Softmax
        
        **Total Parameters**: ~3.7M
        **Model Size**: 12-14 MB
        **Inference Speed**: ~1-2 seconds
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Performance
        
        **Training Results**:
        - Training Accuracy: 88%
        - Validation Accuracy: 82%
        - Training Loss: 0.38
        - Validation Loss: 0.48
        
        **Dataset**:
        - Total Images: 54,306
        - Classes: 38
        - Image Size: 192×192
        - Train/Val Split: 80/20
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎓 Transfer Learning Benefits
    
    This model uses **transfer learning**, which means:
    
    1. **Pre-trained Base**: Started with ImageNet weights (trained on 1M+ images)
    2. **Fine-tuning**: Only customized the top layers for plant diseases
    3. **Fast Training**: Completed in ~30 minutes (instead of hours)
    4. **High Accuracy**: Achieved 82% with just 54K images
    
    **Why Transfer Learning Works**:
    - Lower layers learn general features (edges, colors, textures)
    - Upper layers learn task-specific features (disease patterns)
    - Reusing learned features = better accuracy with less data
    """)

# ============================================================================
# PAGE 4: HELP
# ============================================================================
elif page == "ℹ️ Help":
    st.title("ℹ️ Help & FAQ")
    
    st.markdown("""
    ### ❓ Frequently Asked Questions
    
    **Q: What formats does the app accept?**
    A: JPG, JPEG, and PNG images. File size should be < 25MB.
    
    **Q: How accurate is the model?**
    A: The model achieves 82% validation accuracy. It works best with clear images of leaves.
    
    **Q: What should I photograph?**
    A: Take close-up photos of affected leaves with good lighting. Avoid shadows.
    
    **Q: What if it predicts wrong?**
    A: Upload a clearer image or try a different angle. Disease patterns vary.
    
    **Q: Can I use it offline?**
    A: Yes! Download the model and run this app locally with `streamlit run app.py`
    
    ---
    
    ### 📋 Best Practices
    
    ✅ **DO**:
    - Use clear, well-lit images
    - Photograph the entire leaf
    - Include multiple leaves if possible
    - Take photos during daytime
    
    ❌ **DON'T**:
    - Use blurry photos
    - Include hands or tools
    - Upload in low light
    - Use screenshots or diagrams
    
    ---
    
    ### 🔧 Troubleshooting
    
    **App says model not found**:
    - Check `plant_disease_model.h5` is in the same folder as app
    - Check `class_indices.json` is in the same folder
    
    **Prediction takes too long**:
    - First prediction is slow (model loads)
    - Subsequent predictions are fast
    - Restart app if very slow
    
    **Wrong predictions**:
    - Try a clearer image
    - Ensure full leaf is visible
    - Check for overlapping leaves
    
    ---
    
    ### 📧 Support
    
    For issues or questions:
    1. Check image quality first
    2. Try with different image
    3. Restart the application
    4. Check TensorFlow version compatibility
    
    ---
    
    ### 🎓 Learn More
    
    - [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
    - [Transfer Learning](https://en.wikipedia.org/wiki/Transfer_learning)
    - [PlantVillage Dataset](https://www.plantvillage.psu.edu/)
    """)

# ============================================================================
# Footer
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 20px;">
    <p>🌱 Plant Disease Detection using Transfer Learning</p>
    <p>Built with TensorFlow & Streamlit</p>
    <p>Model: MobileNetV2 | Classes: 38 | Accuracy: 82%</p>
</div>
""", unsafe_allow_html=True)