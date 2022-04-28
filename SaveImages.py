def	get_folder_id(root_dir, target_dir_title, drive):
	fileList = drive.ListFile({'q': "'" + root_dir + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for file in fileList:
		if target_dir_title in file["title"]:
			return file["id"]

def get_folders_for_all_mantas(drive):
	database_dir = get_folder_id("root", "Database", drive)
	birostris_dir = get_folder_id(database_dir, "birostris", drive)
	birostris_dir = get_folder_id(birostris_dir, "each", drive)
	birostris_dir = drive.ListFile({'q': "'" + birostris_dir + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	alfredi_dir = get_folder_id(database_dir, "alfredi", drive)
	alfredi_dir = get_folder_id(alfredi_dir, "each", drive)
	alfredi_dir = drive.ListFile({'q': "'" + alfredi_dir + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	return (alfredi_dir, birostris_dir)

def create_new_dir(manta_name, attributes, database_folder, drive):
	alfredi_dir, birostris_dir = get_folders_for_all_mantas(drive)
	highest_id = -1
	for file in alfredi_dir:
		current_manta_id = int(file["title"].split(".")[0].split("-")[-1])
		if current_manta_id > highest_id:
			highest_id = current_manta_id
	for file in birostris_dir:
		current_manta_id = int(file["title"].split(".")[0].split("-")[-1])
		if current_manta_id > highest_id:
			highest_id = current_manta_id
	last_manta_id = highest_id
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
	each_manta_folder = get_folder_id(database_folder, "each", drive)
	new_folder = drive.CreateFile({"title": folder_name, "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": each_manta_folder}]})
	new_folder.Upload()
	folder_id = new_folder['id']

	return folder_id, folder_name

def save_image_new_dir(file, folder_id, folder_name, drive):
	# Add dive site to folder name
	new_file = drive.CreateFile({"title": folder_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def save_image(file, drive, match_file, database_folder):
	manta_id = match_file['title'].split("-")[1].split(".")[0]
	print(database_folder)
	database_folder = get_folder_id(database_folder, "each", drive)
	dst_folder_id = get_folder_id(database_folder, manta_id, drive)
	
	# Get correct file_name
	file_name = match_file['title'] + "1"
	new_file = drive.CreateFile({"title": file_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": dst_folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def new_name_unique(new_name, drive, database_folder):
	if "name" in new_name or "Name" in new_name:
		return 1
	
	database_folder = get_folder_id(database_folder, "Folders for each individual", drive)
	
	NewFileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for files in NewFileList:
		manta_name = files['title'].split("- ")[-1].split(".")[0]
		if new_name.strip() == manta_name:
			return 0
	return 1

def save_new_manta(manta_name, attributes, database_folder, file, drive):
	folder_id, folder_name = create_new_dir(manta_name, attributes, database_folder, drive)

	#safed in new folder
	save_image_new_dir(file, folder_id, folder_name, drive)

	print(attributes)

	#safe in color folder
	if "Reef" in attributes[0] and "Black" in attributes[1]:
		folder_id = get_folder_id(database_folder, "Black", drive)
		save_image_new_dir(file, folder_id, folder_name, drive)
	elif "Reef" in attributes[0] and "White" in attributes[1]:
		folder_id = get_folder_id(database_folder, "White", drive)
		save_image_new_dir(file, folder_id, folder_name, drive)

	#safe in gender folder
	if "Reef" in attributes[0] and "Female" in attributes[2]:
		folder_id = get_folder_id(database_folder, "FEMALE", drive)
		save_image_new_dir(file, folder_id, folder_name, drive)
	elif "Reef" in attributes[0] and attributes[2] == "Male":
		folder_id = get_folder_id(database_folder, " MALE", drive)
		save_image_new_dir(file, folder_id, folder_name, drive)
	elif "Reef" in attributes[0] and attributes[2] == "Unknown":
		folder_id = get_folder_id(database_folder, "UNKNOWN", drive)
		save_image_new_dir(file, folder_id, folder_name, drive)

	#safe in master folder
	folder_id = get_folder_id(database_folder, "MASTER", drive)
	save_image_new_dir(file, folder_id, folder_name, drive)
