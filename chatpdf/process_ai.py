import os
from pathlib import Path
from shutil import copyfile
# class pdf_ai_process:
# 	pdf_vector_path= None
	
# 	def pdf_to_vector(self, file):
# 		result= "./media/vector/"
# 		pdf_vector_path= result
# 		return pdf_vector_path

# 	def ai(self, message):
# 		result= "fuck you "+ str(message)+ " i have recieved it"
# 		return result  


def ai(message, file):
	result= "fuck you "+ str(message)+ " i have recieved it\n you are chatting with: "+ str(file)
	return result


def pdf_to_vector(pdf_path):
    # Process the PDF file and generate the vector database
    vector_path = save_file_to_media(pdf_path)

    return vector_path




# Define your Django settings
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def save_file_to_media(file_path, new_folder_name= "vector"):
    # Ensure the new folder exists inside MEDIA_ROOT
    vector_folder = os.path.join(MEDIA_ROOT, new_folder_name)
    os.makedirs(vector_folder, exist_ok=True)

    # Get the filename from the original path
    file_name = os.path.basename(file_path)

    # Define the destination path
    destination_path = os.path.join(vector_folder, file_name)

    # Copy the file to the new destination
    try:
        copyfile(file_path, destination_path)
        print(f"File saved successfully to: {destination_path}")
        return destination_path
    except FileNotFoundError:
        print("Error: File not found.")
        return None

