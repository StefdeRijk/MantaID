from distutils.file_util import copy_file
import shutil
import glob
import os
def create_new_dir(manta_name, attributes, database_folder):
	last_manta = glob.glob(database_folder + "/MR Folders for each individual/*", recursive=True)[-1]
	last_manta_folder = os.path.basename(last_manta)
	last_manta_id = int(last_manta_folder.split(".")[0].split("-")[-1])
	new_manta_id = last_manta_id + 1
	if attributes[0] == "Reef manta":
		species_letter = ".A"
	elif attributes[0] == "Oceanic manta":
		species_letter = ".B"
	else:
		species_letter = ".U"
	if attributes[2] == "Male":
		sex_letter = ".M"
	elif attributes[2] == "Female":
		sex_letter = ".F"
	else:
		sex_letter = ".U"
	if new_manta_id < 1000:
		new_manta_id = "0" + str(new_manta_id)
	else:
		new_manta_id = str(new_manta_id)
	folder_name = "MR-" + new_manta_id + species_letter + sex_letter + " - " + manta_name
	folder_path = os.path.join(os.path.dirname(last_manta), folder_name)
	os.mkdir(folder_path)
	return folder_path, folder_name

def save_new_image(file, manta_name, attributes, database_folder, folder_path, folder_name):
	copy_file_path = shutil.copy2(file, folder_path)
	new_file_path = os.path.join(os.path.dirname(copy_file_path), folder_name) + ".jpg"
	os.rename(copy_file_path, new_file_path)