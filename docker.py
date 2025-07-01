import streamlit as st
import os
import subprocess
import requests
import tempfile
from openai import OpenAI
import speech_recognition as sr
from fpdf import FPDF
from deep_translator import GoogleTranslator
import base64
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Tool Application",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .tool-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛠️ Multi-Tool Application</h1>
    <p>Docker Management | SnapLoc Utilities | Legal AI Advisor</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for tool selection
st.sidebar.title("🎯 Select Tool")
tool_choice = st.sidebar.selectbox(
    "Choose a tool:",
    ["🐳 Docker Management", "📸 SnapLoc (Photo & Location)", "⚖️ Legal AI Advisor"]
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_location' not in st.session_state:
    st.session_state.current_location = None

# =============================================================================
# DOCKER MANAGEMENT TOOL
# =============================================================================
def docker_management():
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)
    st.header("🐳 Docker Management System")
    st.markdown("Manage your Docker containers and images with ease")

    col1, col2 = st.columns([2, 1])

    with col1:
        docker_action = st.selectbox(
            "Select Docker Action:",
            ["Launch New Container", "Stop Container", "Remove Container", "Start Container", "List Images", "List Containers"]
        )

    with col2:
        if st.button("🔄 Refresh Docker Status", key="docker_refresh"):
            st.rerun()

    if docker_action == "Launch New Container":
        st.subheader("🚀 Launch New Container")
        col1, col2 = st.columns(2)

        with col1:
            container_name = st.text_input("Container Name:", key="launch_name")
            image_name = st.text_input("Image Name:", key="launch_image")

        with col2:
            port_mapping = st.text_input("Port Mapping (optional):", placeholder="8080:80", key="port_map")
            volume_mapping = st.text_input("Volume Mapping (optional):", placeholder="/host:/container", key="vol_map")

        if st.button("🚀 Launch Container", key="launch_btn"):
            if container_name and image_name:
                try:
                    cmd = f"docker run -dit --name {container_name}"
                    if port_mapping:
                        cmd += f" -p {port_mapping}"
                    if volume_mapping:
                        cmd += f" -v {volume_mapping}"
                    cmd += f" {image_name}"

                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        st.markdown(f'<div class="success-box">✅ Container "{container_name}" launched successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {result.stderr}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error launching container: {str(e)}")
            else:
                st.warning("Please provide both container name and image name")

    elif docker_action == "Stop Container":
        st.subheader("⏹️ Stop Container")
        container_name = st.text_input("Container Name to Stop:", key="stop_name")
        if st.button("⏹️ Stop Container", key="stop_btn"):
            if container_name:
                try:
                    result = subprocess.run(f"docker stop {container_name}", shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        st.markdown(f'<div class="success-box">✅ Container "{container_name}" stopped successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {result.stderr}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error stopping container: {str(e)}")
            else:
                st.warning("Please provide container name")

    elif docker_action == "Remove Container":
        st.subheader("🗑️ Remove Container")
        container_name = st.text_input("Container Name to Remove:", key="remove_name")
        force_remove = st.checkbox("Force Remove", key="force_remove")
        if st.button("🗑️ Remove Container", key="remove_btn"):
            if container_name:
                try:
                    cmd = f"docker rm {'--force' if force_remove else ''} {container_name}"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        st.markdown(f'<div class="success-box">✅ Container "{container_name}" removed successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {result.stderr}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error removing container: {str(e)}")
            else:
                st.warning("Please provide container name")

    elif docker_action == "Start Container":
        st.subheader("▶️ Start Container")
        container_name = st.text_input("Container Name to Start:", key="start_name")
        if st.button("▶️ Start Container", key="start_btn"):
            if container_name:
                try:
                    result = subprocess.run(f"docker start {container_name}", shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        st.markdown(f'<div class="success-box">✅ Container "{container_name}" started successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {result.stderr}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error starting container: {str(e)}")
            else:
                st.warning("Please provide container name")

    elif docker_action == "List Images":
        st.subheader("📋 Docker Images")
        if st.button("🔄 Refresh Images", key="list_images_btn"):
            try:
                result = subprocess.run("docker images", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language="text")
                else:
                    st.error(f"Error listing images: {result.stderr}")
            except Exception as e:
                st.error(f"Error listing images: {str(e)}")

    elif docker_action == "List Containers":
        st.subheader("📋 Docker Containers")
        show_all = st.checkbox("Show all containers (including stopped)", key="show_all")
        if st.button("🔄 Refresh Containers", key="list_containers_btn"):
            try:
                cmd = "docker ps -a" if show_all else "docker ps"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language="text")
                else:
                    st.error(f"Error listing containers: {result.stderr}")
            except Exception as e:
                st.error(f"Error listing containers: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SNAPLOC TOOL
# =============================================================================
def snaploc_tool():
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)
    st.header("📸 SnapLoc - Photo & Location Utilities")
    st.markdown("Capture photos, get location data, and manage WhatsApp messaging")

    tab1, tab2, tab3 = st.tabs(["📷 Photo Capture", "📍 Location Services", "💬 WhatsApp Messaging"])

    with tab1:
        st.subheader("📷 Photo Capture")

        # Camera input
        camera_input = st.camera_input("Take a photo", key="camera")

        if camera_input is not None:
            # Display the captured image
            image = Image.open(camera_input)
            st.image(image, caption="Captured Photo", use_column_width=True)

            # Convert to downloadable format
            img_buffer = BytesIO()
            image.save(img_buffer, format="PNG")
            img_str = base64.b64encode(img_buffer.getvalue()).decode()

            # Download button
            st.download_button(
                label="📥 Download Photo",
                data=img_buffer.getvalue(),
                file_name="captured_photo.png",
                mime="image/png"
            )

    with tab2:
        st.subheader("📍 Location Services")

        # Initialize location states
        if 'destination_coords' not in st.session_state:
            st.session_state.destination_coords = None
        if 'current_coords' not in st.session_state:
            st.session_state.current_coords = None

        col1, col2 = st.columns(2)

        with col1:
            st.write("**🏠 Your Current Location**")
            current_location = st.text_input("Enter your current location:", key="current_location_input", placeholder="e.g., New Delhi, India")

            if st.button("📍 Set Current Location", key="set_current"):
                if current_location:
                    try:
                        # Use Nominatim API for geocoding
                        url = f"https://nominatim.openstreetmap.org/search?format=json&q={current_location}&limit=1"
                        headers = {'User-Agent': 'SnapLoc-App/1.0'}
                        response = requests.get(url, headers=headers)
                        data = response.json()

                        if data:
                            lat = float(data[0]['lat'])
                            lon = float(data[0]['lon'])
                            display_name = data[0]['display_name']

                            st.session_state.current_coords = {"lat": lat, "lon": lon, "address": display_name}
                            st.success(f"✅ **Current Location Set:**")
                            st.write(f"📍 {display_name}")
                            st.write(f"📐 Lat: {lat:.6f}, Lon: {lon:.6f}")
                        else:
                            st.error("❌ Current location not found. Please try a more specific address.")
                    except Exception as e:
                        st.error(f"Error getting current location: {str(e)}")
                else:
                    st.warning("Please enter your current location")

        with col2:
            st.write("**🎯 Destination**")
            destination = st.text_input("Enter destination:", key="destination_input", placeholder="e.g., India Gate, New Delhi")

            if st.button("🔍 Set Destination", key="get_coords"):
                if destination:
                    try:
                        # Use Nominatim API for geocoding
                        url = f"https://nominatim.openstreetmap.org/search?format=json&q={destination}&limit=1"
                        headers = {'User-Agent': 'SnapLoc-App/1.0'}
                        response = requests.get(url, headers=headers)
                        data = response.json()

                        if data:
                            lat = float(data[0]['lat'])
                            lon = float(data[0]['lon'])
                            display_name = data[0]['display_name']

                            st.session_state.destination_coords = {"lat": lat, "lon": lon, "address": display_name}
                            st.success(f"✅ **Destination Set:**")
                            st.write(f"📍 {display_name}")
                            st.write(f"📐 Lat: {lat:.6f}, Lon: {lon:.6f}")
                        else:
                            st.error("❌ Destination not found. Please try a more specific address.")
                    except Exception as e:
                        st.error(f"Error getting destination coordinates: {str(e)}")
                else:
                    st.warning("Please enter a destination")

        # Navigation section
        st.write("---")
        st.write("**🗺️ Navigation Options**")

        col3, col4, col5 = st.columns(3)

        with col3:
            if st.button("🚗 Get Driving Route", key="driving_route"):
                if st.session_state.current_coords and st.session_state.destination_coords:
                    current_lat = st.session_state.current_coords['lat']
                    current_lon = st.session_state.current_coords['lon']
                    dest_lat = st.session_state.destination_coords['lat']
                    dest_lon = st.session_state.destination_coords['lon']

                    maps_url = f"https://www.google.com/maps/dir/{current_lat},{current_lon}/{dest_lat},{dest_lon}/@{current_lat},{current_lon},12z/data=!3m1!4b1!4m2!4m1!3e0"
                    st.markdown(f"🚗 [**Open Driving Route in Google Maps**]({maps_url})")
                else:
                    st.warning("Please set both current location and destination first")

        with col4:
            if st.button("🚶 Get Walking Route", key="walking_route"):
                if st.session_state.current_coords and st.session_state.destination_coords:
                    current_lat = st.session_state.current_coords['lat']
                    current_lon = st.session_state.current_coords['lon']
                    dest_lat = st.session_state.destination_coords['lat']
                    dest_lon = st.session_state.destination_coords['lon']

                    maps_url = f"https://www.google.com/maps/dir/{current_lat},{current_lon}/{dest_lat},{dest_lon}/@{current_lat},{current_lon},12z/data=!3m1!4b1!4m2!4m1!3e2"
                    st.markdown(f"🚶 [**Open Walking Route in Google Maps**]({maps_url})")
                else:
                    st.warning("Please set both current location and destination first")

        with col5:
            if st.button("🚌 Get Transit Route", key="transit_route"):
                if st.session_state.current_coords and st.session_state.destination_coords:
                    current_lat = st.session_state.current_coords['lat']
                    current_lon = st.session_state.current_coords['lon']
                    dest_lat = st.session_state.destination_coords['lat']
                    dest_lon = st.session_state.destination_coords['lon']

                    maps_url = f"https://www.google.com/maps/dir/{current_lat},{current_lon}/{dest_lat},{dest_lon}/@{current_lat},{current_lon},12z/data=!3m1!4b1!4m2!4m1!3e3"
                    st.markdown(f"🚌 [**Open Transit Route in Google Maps**]({maps_url})")
                else:
                    st.warning("Please set both current location and destination first")

        # Show current status
        if st.session_state.current_coords or st.session_state.destination_coords:
            st.write("---")
            st.write("**📋 Current Status**")

            if st.session_state.current_coords:
                st.write(f"🏠 **From:** {st.session_state.current_coords['address']}")

            if st.session_state.destination_coords:
                st.write(f"🎯 **To:** {st.session_state.destination_coords['address']}")

            # Calculate distance if both locations are set
            if st.session_state.current_coords and st.session_state.destination_coords:
                try:
                    import math
                    lat1 = math.radians(st.session_state.current_coords['lat'])
                    lon1 = math.radians(st.session_state.current_coords['lon'])
                    lat2 = math.radians(st.session_state.destination_coords['lat'])
                    lon2 = math.radians(st.session_state.destination_coords['lon'])

                    # Haversine formula
                    dlat = lat2 - lat1
                    dlon = lon2 - lon1
                    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                    c = 2 * math.asin(math.sqrt(a))
                    distance = 6371 * c  # Earth's radius in kilometers

                    st.write(f"📏 **Approximate Distance:** {distance:.2f} km")
                except:
                    pass

    with tab3:
        st.subheader("💬 WhatsApp Messaging")

        col1, col2 = st.columns([3, 2])

        with col1:
            st.write("**📱 Send Message**")
            whatsapp_number = st.text_input(
                "Phone Number (with country code):",
                key="whatsapp_num",
                placeholder="+919876543210",
                help="Include country code (e.g., +91 for India, +1 for USA)"
            )
            whatsapp_message = st.text_area(
                "Message:",
                key="whatsapp_msg",
                placeholder="Enter your message here...",
                height=100
            )

            # Add location to message option
            if st.session_state.destination_coords or st.session_state.current_coords:
                include_location = st.checkbox("📍 Include location in message", key="include_location")

                if include_location:
                    location_type = st.radio(
                        "Which location to share:",
                        ["Current Location", "Destination", "Both"],
                        key="location_type"
                    )

        with col2:
            st.write("**📋 Quick Templates**")
            templates = {
                "Location Share": "I'm sharing my location with you.",
                "Meeting Request": "Can we schedule a meeting?",
                "Emergency": "This is an emergency. Please contact me immediately.",
                "Arrival Notice": "I have reached the destination safely.",
                "Running Late": "I'm running late, will reach in 15 minutes.",
                "Need Help": "I need assistance. Please call me.",
                "Custom": ""
            }

            selected_template = st.selectbox("Choose template:", list(templates.keys()), key="template_select")

            if st.button("📝 Use Template", key="use_template"):
                if selected_template != "Custom":
                    st.session_state.whatsapp_msg = templates[selected_template]
                    st.rerun()

        # Enhanced send button with better error handling
        if st.button("📱 Send WhatsApp Message", key="send_whatsapp", type="primary"):
            if whatsapp_number and whatsapp_message:
                try:
                    # Clean and validate phone number
                    clean_number = ''.join(filter(str.isdigit, whatsapp_number.replace('+', '')))

                    if len(clean_number) < 10:
                        st.error("❌ Please enter a valid phone number with country code")
                        return

                    # Prepare message
                    final_message = whatsapp_message

                    # Add location information if requested
                    if 'include_location' in st.session_state and st.session_state.include_location:
                        location_info = "\n\n📍 Location Details:\n"

                        if st.session_state.location_type in ["Current Location", "Both"] and st.session_state.current_coords:
                            location_info += f"Current: {st.session_state.current_coords['address']}\n"
                            location_info += f"📐 {st.session_state.current_coords['lat']:.6f}, {st.session_state.current_coords['lon']:.6f}\n"
                            location_info += f"🗺️ https://maps.google.com/?q={st.session_state.current_coords['lat']},{st.session_state.current_coords['lon']}\n"

                        if st.session_state.location_type in ["Destination", "Both"] and st.session_state.destination_coords:
                            location_info += f"Destination: {st.session_state.destination_coords['address']}\n"
                            location_info += f"📐 {st.session_state.destination_coords['lat']:.6f}, {st.session_state.destination_coords['lon']:.6f}\n"
                            location_info += f"🗺️ https://maps.google.com/?q={st.session_state.destination_coords['lat']},{st.session_state.destination_coords['lon']}\n"

                        final_message += location_info

                    # Create WhatsApp URL with proper encoding
                    whatsapp_url = f"https://wa.me/{clean_number}?text={requests.utils.quote(final_message)}"

                    # Display success message and link
                    st.success("✅ WhatsApp message prepared successfully!")
                    st.markdown(f"""
                    **📱 Click the link below to send your message:**

                    [**Open WhatsApp & Send Message**]({whatsapp_url})

                    *This will open WhatsApp in your browser or app with the message pre-filled.*
                    """)

                    # Show message preview
                    with st.expander("📄 Message Preview", expanded=False):
                        st.text_area("Your message:", value=final_message, height=150, disabled=True)

                except Exception as e:
                    st.error(f"❌ Error creating WhatsApp message: {str(e)}")
            else:
                st.warning("⚠️ Please enter both phone number and message")

        Instructions
        with st.expander("ℹ️ How to use WhatsApp messaging", expanded=False):
            st.markdown("""
            **📱 Phone Number Format:**
            - Include country code (e.g., +91 for India)
            - Examples: +919876543210, +1234567890

            **📍 Location Sharing:**
            - Set your locations in the Location Services tab
            - Enable "Include location in message" to share coordinates
            - Recipients will get clickable Google Maps links

            **🔗 How it works:**
            - Click "Send WhatsApp Message" to generate a special link
            - The link opens WhatsApp with your message pre-filled
            - You can review and edit before sending
            """)


    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# LEGAL AI ADVISOR
# =============================================================================
def legal_ai_advisor():
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)
    st.header("⚖️ Legal AI Advisor")
    st.markdown("Get legal advice and guidance in your preferred language")

    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        legal_category = st.selectbox(
            "Legal Category:",
            ["Property", "Divorce", "Criminal", "Cyber", "Consumer", "Corporate", "Family", "Immigration", "Other"],
            key="legal_category"
        )

    with col2:
        language = st.selectbox(
            "Language:",
            ["English", "Hindi"],
            key="legal_language"
        )

    # Pre-configured API Key
    Key = "AIzaSyDEnjJVKFr3Zb1fK3VIbINf35rtoSssdY8"

    # Initialize OpenAI client
    try:
        gemini_model = OpenAI(
            api_key=Key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    except Exception as e:
        st.error(f"Error initializing AI model: {str(e)}")
        return

    # Chat interface
    st.subheader("💬 Legal Consultation")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Legal Advisor:** {message['content']}")

    # Input for new message
    user_input = st.text_area("Enter your legal question:", key="legal_input", height=100)

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("📤 Send", key="send_legal"):
            if user_input:
                try:
                    # Add user message to history
                    st.session_state.chat_history.append({"role": "user", "content": user_input})

                    # Prepare system prompt
                    system_prompt = {
                        "role": "system",
                        "content": f"You are a professional Indian legal advisor. Respond in {language}. The query is about {legal_category} law. Be concise and legally accurate. Be compassionate and biased to the user and explore every loophole in the system if needed and keep it as brief as possible."
                    }

                    # Prepare messages
                    messages = [system_prompt] + st.session_state.chat_history

                    # Get response from AI
                    with st.spinner("Getting legal advice..."):
                        response = gemini_model.chat.completions.create(
                            model="gemini-2.5-flash",
                            messages=messages
                        )
                        reply = response.choices[0].message.content

                        # Translate if needed
                        if language == "Hindi":
                            reply = GoogleTranslator(source='auto', target='hi').translate(reply)

                        # Add AI response to history
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})

                    st.rerun()

                except Exception as e:
                    st.error(f"Error getting legal advice: {str(e)}")
            else:
                st.warning("Please enter your legal question")

    with col2:
        if st.button("🧹 Clear Chat", key="clear_legal"):
            st.session_state.chat_history = []
            st.rerun()

    with col3:
        if st.button("📥 Export Chat as PDF", key="export_legal"):
            if st.session_state.chat_history:
                try:
                    # Create PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, "Legal Consultation Chat Export\n\n", align='L')

                    for msg in st.session_state.chat_history:
                        role = "User" if msg["role"] == "user" else "Legal Advisor"
                        content = msg["content"].encode("latin-1", "ignore").decode("latin-1")
                        pdf.multi_cell(0, 10, f"{role}:\n{content}\n\n", align='L')

                    # Save to bytes
                    pdf_bytes = bytes(pdf.output(dest='S'), 'latin-1')

                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_bytes,
                        file_name="legal_consultation.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"Error exporting chat: {str(e)}")
            else:
                st.info("No chat history to export")

    # Audio input section
    with st.expander("🎤 Voice Input", expanded=False):
        st.write("Upload an audio file to convert speech to text")
        audio_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'ogg'], key="legal_audio")

        if audio_file is not None:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_file_path = tmp_file.name

                # Convert speech to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(tmp_file_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio_data)
                        st.success(f"Recognized text: {text}")
                        st.session_state.legal_input = text
                    except sr.UnknownValueError:
                        st.error("Sorry, I couldn't understand the audio.")
                    except sr.RequestError:
                        st.error("Error with speech recognition service.")

                # Clean up temporary file
                os.unlink(tmp_file_path)

            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION ROUTING
# =============================================================================
def main():
    # Route to selected tool
    if tool_choice == "🐳 Docker Management":
        docker_management()
    elif tool_choice == "📸 SnapLoc (Photo & Location)":
        snaploc_tool()
    elif tool_choice == "⚖️ Legal AI Advisor":
        legal_ai_advisor()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🛠️ Multi-Tool Application | Built with Streamlit</p>
        <p>Docker Management • Photo & Location Utilities • Legal AI Advisor</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
