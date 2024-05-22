import streamlit as st
import requests
import os
# Define the URLs for the encoder and decoder endpoints
ENCODER_URL = "http://48.216.208.35:8000/fbis/encoder"
DECODER_URL = "http://48.216.208.35:8000/fbis/decoder"

# Set the title of the Streamlit app
st.title("Encoder/Decoder Service")

# Create a selectbox for choosing the service
service_option = st.selectbox("Choose a service:", ["Encoder", "Decoder"])

if service_option == "Encoder":
    st.header("Encoder Service")
    
    # File uploader for the encoder
    uploaded_file = st.file_uploader("Choose a text file to encode(compress):", type="txt")
    
    # Trigger the encoding process
    if st.button("Encode"):
        if uploaded_file is not None:
            try:
                files = {'file': uploaded_file}
                response = requests.post(ENCODER_URL, files=files)
                if response.status_code == 200:
                    encoded_data = response.json()
                    st.success("Encoded successfully!")
                    st.write("Encoded Text:")
                    st.text_area("", encoded_data.get("answer", ""))
                    os.remove(encoded_data.get("compressed_text_path", ""))
                else:
                    st.error("Failed to encode the text.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a text file to encode.")
else:
    st.header("Decoder Service")
    
    # Input field for the decoder
    uploaded_file = st.file_uploader("Choose a text file to decode(decompress):", type="txt")
    
    # Trigger the decoding process
    if st.button("Decode"):
        if uploaded_file is not None:
            try:
                files = {'file': uploaded_file}
                response = requests.post(DECODER_URL, files=files)
                if response.status_code == 200:
                    decoded_data = response.json()
                    st.success("Decoded successfully!")
                    st.write("Decoded Text:")
                    st.text_area("", decoded_data.get("answer", ""))
                    os.remove("", decoded_data.get("answer", ""))
                else:
                    st.error("Failed to decode the text.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter the path to the compressed text file.")