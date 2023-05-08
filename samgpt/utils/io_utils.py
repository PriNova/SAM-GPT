import os

# Function to check if a folder exists. If it does not, it will be created.
def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)