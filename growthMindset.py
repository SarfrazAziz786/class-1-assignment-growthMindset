import streamlit as st
import pandas as pd
import os
from io import BytesIO
from PIL import Image

#set up our App
st.set_page_config(page_title= "⁜Data sweeper", layout='wide')

#Custom css
dark_mode = """

    <style>
    .stApp{
        background-color:gold;
        color:white;
        }
    </style>
        """,
st.markdown(dark_mode, unsafe_allow_html=True)

#title and description
st.title("File Converter and Cleaner by Sarfraz Aziz")
st.write("Transform your files between CSV and EXCEL , JPEG or JPG and PDF formats  with built in data. Creating the project for quarter 3 GIAIC")


#file uploader

uploaded_files = st.file_uploader("Upload your file (csv or excel):", type=["CSV","XLSX"],accept_multiple_files=(True))

#Image file upload
uploaded_images = st.file_uploader("Upload JPEG or JPG Image", type = ["jpeg", "jpg"], accept_multiple_files=True)


#Convert image to PDF
if uploaded_images is not None:
        if st.button("Convert Images to PDF"):
            #Create an empty list to hold the images
            image_list = [] 

            #Loop through the uploaded images
            for uploaded_image in uploaded_images:
                
                #Open the images using PIL library
                image = Image.open(uploaded_image)
                
                #Convert image to RGB if it's not in RGB format (for PDF compatibility)
                if image.mode != "RGB":
                    image = image.convert('RGB')
                image_list.append(image)

                if image_list:

                    #Create a ByteIO buffer to save the PDF
                    pdf_buffer = BytesIO()

                    #save the images as PDF
                    image_list[0].save(pdf_buffer, format="PDF", save_all = True, append_images = image_list[1:])
                    pdf_buffer.seek(0)

                    st.download_button("Download PDF",
                    data = pdf_buffer,
                    file_name="converted_images.pdf",
                    mime="application/pdf"
                    )
                else:
                    st.error("No valid images found")
                  




if uploaded_files:
      # Loop through each uploaded file
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        
        #Display info about the file
        st.write(f"**File Name:** {file.name}" )
        st.write(f"**File Size:** {file.size/1024}" )
        
        
        
        # Show a preview of the dataframe.
        
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())


        # Data Cleaning Options
        st.subheader("🔍Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"File missing values for {file.name}"):
                    numuric_cols = df.select_dtypes(include=['number']).columns
                    df[numuric_cols] = df[numuric_cols].fillna(df[numuric_cols].mean())
                    st.write("Missing values have been filled!")


    #Choose Specific Columns to Keep or Convert
    st.subheader("🎯Select Columns to Convert ")
    columns = st.multiselect(f"Choose columns for {file.name}", df.columns.tolist() , default = df.columns.tolist())
    df = df[columns]


    #Data Visualization
    st.subheader("🔍Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    #Convert the File -> CSV to EXCEL
    st.subheader("Conversion Option")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV","EXCEL"], key=file.name)

    if st.button(f"Convert {file.name}"):
        buffer=BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type="text/csv"

        elif conversion_type == "EXCEL":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext,".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)


        # Download Button
        
        st.download_button(
        label=f"⬇️ Download {file.name} as {conversion_type}",
        data=buffer,
        file_name=file.name.replace(file_ext, f".{conversion_type.lower()}"),
        mime=mime_type
        )
        
    
    
    

    st.success("🎉All files processed successfully")




