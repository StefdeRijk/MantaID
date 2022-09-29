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

def format_date(date):
	new_date = ""
	new_date = date[0:2]
	if int(date[3:5]) == 1:
		new_date += "Jan"
	elif int(date[3:5]) == 2:
		new_date += "Feb"
	elif int(date[3:5]) == 3:
		new_date += "Mar"
	elif int(date[3:5]) == 4:
		new_date += "Apr"
	elif int(date[3:5]) == 5:
		new_date += "May"
	elif int(date[3:5]) == 6:
		new_date += "Jun"
	elif int(date[3:5]) == 7:
		new_date += "Jul"
	elif int(date[3:5]) == 8:
		new_date += "Aug"
	elif int(date[3:5]) == 9:
		new_date += "Sep"
	elif int(date[3:5]) == 10:
		new_date += "Oct"
	elif int(date[3:5]) == 11:
		new_date += "Nov"
	elif int(date[3:5]) == 12:
		new_date += "Dec"
	new_date += date[6:8]
	return new_date

def get_manta_id(manta_name):
	return int(manta_name.split(".")[0].split("-")[-1])

def get_species_and_sex_letter(attributes):
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
	return species_letter, sex_letter

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

def create_new_dir(manta_name, attributes, database_folder, drive):
	alfredi_dir, birostris_dir = get_folders_for_all_mantas(drive)
	highest_id = -1
	for file in alfredi_dir:
		current_manta_id = get_manta_id(file["title"])
		if current_manta_id > highest_id:
			highest_id = current_manta_id
	for file in birostris_dir:
		current_manta_id = get_manta_id(file["title"])
		if current_manta_id > highest_id:
			highest_id = current_manta_id
	last_manta_id = highest_id
	new_manta_id = last_manta_id + 1

	species_letter, sex_letter = get_species_and_sex_letter(attributes)
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
	new_file = drive.CreateFile({"title": folder_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def save_multiple_images_in_match_folder(file, drive, match_file_name, database_folder, attributes, file_list, manta_name):
	manta_name += " a"
	save_image_in_match_folder(file, drive, match_file_name, database_folder, attributes, manta_name)
	i = 0
	old_attachment = " a"
	for cur_file in file_list:
		attached_letter = " " + chr(ord('b') + i)
		manta_name = manta_name.replace(old_attachment, attached_letter)
		save_image_in_match_folder(cur_file, drive, match_file_name, database_folder, attributes, manta_name)
		i += 1
		old_attachment = attached_letter

def save_image_in_match_folder(file, drive, match_file_name, database_folder, attributes, manta_name):
	manta_id = get_manta_id(match_file_name)
	if manta_id < 10:
		manta_id = "000" + str(manta_id)
	elif manta_id < 100:
		manta_id = "00" + str(manta_id)
	elif manta_id < 1000:
		manta_id = "0" + str(manta_id)

	database_folder = get_folder_id(database_folder, "each", drive)
	dst_folder_id = get_folder_id(database_folder, manta_id, drive)
	
	species_letter, sex_letter = get_species_and_sex_letter(attributes)

	file_name = "MR-" + manta_id + species_letter + sex_letter + "." + format_date(attributes[3]) + "." + attributes[4] + " - " + manta_name
	new_file = drive.CreateFile({"title": file_name + ".jpg", "mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": dst_folder_id}]})
	new_file.SetContentFile(file)
	new_file.Upload()

def save_image_in_master_folder(file, drive, match_file_name, database_folder, attributes):
	folder_id = get_folder_id(database_folder, "MASTER", drive)
	manta_id = get_manta_id(match_file_name)

	NewFileList = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
	for files in NewFileList:
		ref_manta_id = get_manta_id(files['title'])
		if manta_id == ref_manta_id:
			files.Delete()
			print("deleted")
			print(files['title'])

	if manta_id < 10:
		manta_id = "000" + str(manta_id)
	elif manta_id < 100:
		manta_id = "00" + str(manta_id)
	elif manta_id < 1000:
		manta_id = "0" + str(manta_id)

	species_letter, sex_letter = get_species_and_sex_letter(attributes)
	manta_name = match_file_name.split("- ")[-1].split(".")[0]
	manta_name = "MR-" + str(manta_id) + species_letter + sex_letter + " - " + manta_name
	save_image_new_dir(file, folder_id, manta_name, drive)

def save_new_manta(manta_name, attributes, database_folder, file, drive):
	folder_id, folder_name = create_new_dir(manta_name, attributes, database_folder, drive)

	#safed in new folder
	save_image_in_match_folder(file, drive, folder_name, database_folder, attributes, manta_name)

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
