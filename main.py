from yolact.neweval import normalmain
import uuid
import streamlit as st
import os
import numpy as np
from PIL import Image


# image_path = "image1.jpg"
# bg_image = r"D:\Data science\ineuron\Background\YOLO-CPU\pexels-pixabay-207353.jpg"

# # ouput_image_path = uuid.uuid1() + ".jpg"

# ouput_image_path = str(uuid.uuid1()) + ".jpg"

# status = normalmain(image_path,bg_image,ouput_image_path)
# print(status)

os.makedirs('result',exist_ok=True)

def save_uploaded_file(uploaded_file,bg_file):
    try:
        os.makedirs('uploads',exist_ok=True)
        with open(os.path.join('uploads',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        with open(os.path.join('uploads',bg_file.name),'wb') as f:
            f.write(bg_file.getbuffer())
        return 1,os.path.join('uploads',uploaded_file.name),os.path.join('uploads',bg_file.name)
    except Exception as e:
        print(F"Error is {e}")
        return 0

app_mode = st.sidebar.selectbox('Application mode',
['About App','Upload image'])
if app_mode =='About App':
    with open("README.md", "r", encoding="utf-8") as fh:
        readme = ""
        unwanted_list = ['<h2>','![GIF]','## Dataset','<a href=','A demo']
        for line in fh:            
            if line.startswith(tuple(unwanted_list)): 
                continue
            readme = readme + line
    st.markdown(readme)

elif app_mode == "Upload image":
    # WINDOW = st.image([])  
    uploaded_file = st.file_uploader(label="Upload an image", type=[ "jpg", "jpeg",'png'])
    bg_file = st.file_uploader(label="Upload an Background image", type=[ "jpg", "jpeg",'png'])
    if uploaded_file and bg_file is not None:
        status,inp_path,bg_path = save_uploaded_file(uploaded_file,bg_file)
        if status:
            merge = st.button("Merge")
            if merge:
                ouput_image_path = os.path.join('result',str(uuid.uuid1()) + ".jpg")
                status = normalmain(inp_path,bg_path,ouput_image_path)

                inp_image = np.array(Image.open(uploaded_file)) 
                bg_image = np.array(Image.open(bg_file)) 
                out_image = np.array(Image.open(ouput_image_path)) 

                img_list = [inp_image,bg_image,out_image]
                headers = ["Uploaded image","Background image","Merged image"]

                i=-1
                cont2 = st.container()
                for col in cont2.columns(len(img_list)):
                    i+=1
                    with col:
                        st.header(headers[i])
                        st.image(img_list[i])
        else:
            print("File is not proper")