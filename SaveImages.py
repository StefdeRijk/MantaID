def create_new_dir(manta_name, attributes, database_folder, drive):
	fileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for file in fileList:
		if file["title"] == "MR Folders for each individual":
			database_folder = file["id"]

	NewFileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	highest_id = -1
	for file in NewFileList:
		current_manta_id = int(file["title"].split(".")[0].split("-")[-1])
		if current_manta_id > highest_id:
			highest_id = current_manta_id
			last_manta = file["title"]
	last_manta_id = int(last_manta.split(".")[0].split("-")[-1])
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
	new_folder = drive.CreateFile({"title": folder_name, "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": database_folder}]})
	new_folder.Upload()
	folder_id = new_folder['id']

	return folder_id, folder_name

def save_new_image(file, folder_id, folder_name, drive):
	# Add dive site to folder name
	new_file = drive.CreateFile({"title": folder_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def save_image(file, drive, match_file, database_folder):
	fileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for files in fileList:
		if files["title"] == "MR Folders for each individual":
			database_folder = files["id"]

	manta_id = match_file['title'].split("-")[1].split(".")[0]
	NewFileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for files in NewFileList:
		if manta_id in files["title"]:
			dst_folder_id = files['id']
			break
	
	# Get correct file_name
	file_name = match_file['title'] + "1"
	new_file = drive.CreateFile({"title": file_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": dst_folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def new_name_unique(new_name, drive, database_folder):
	if "name" in new_name or "Name" in new_name:
		return 1
	
	fileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for files in fileList:
		if files["title"] == "MR Folders for each individual":
			database_folder = files["id"]
	
	NewFileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
	for files in NewFileList:
		manta_name = files['title'].split("- ")[-1].split(".")[0]
		if new_name.strip() == manta_name:
			return 0
	return 1
