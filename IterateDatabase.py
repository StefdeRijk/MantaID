from ImageCompare import image_compare

def get_files(database_folder, attributes, drive):
    fileList = drive.ListFile({'q': "'" + database_folder + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()

    if attributes[0] == "Oceanic manta":
        for file in fileList:
            if file["title"] == "MR Master Birostris ID Shots BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    elif attributes[1] == "Black":
        for file in fileList:
            if file["title"] == "MR Master Alfredi ID Shots Melanistic BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    elif attributes[2] == "Male":
        for file in fileList:
            if file["title"] == "MR Master Alfredi ID Shots Male BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    elif attributes[2] == "Female":
        for file in fileList:
            if file["title"] == "MR Master Alfredi ID Shots Female BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    elif attributes[1] == "White":
        for file in fileList:
            if file["title"] == "MR Master Alfredi ID Shots *ale BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    else:
        for file in fileList:
            if file["title"] == "MR Master Birostris ID Shots BF":
                files = drive.ListFile({'q': "'" + file["id"] + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    return files

def go_through_database(file, amount_of_mantas, database_folder, attributes, drive):
    #index 0 = percentage similar, index 1 = path to file, index 2 = name of manta
    matches = []
    for i in range(amount_of_mantas):
        temp = [0, "", ""]
        matches.append(temp)
    current_folder_results = []
    current_folder_files = []
    files = get_files(database_folder, attributes, drive)
    print(len(files))
    for i in range(len(files)):
        current_file = files[i]["title"]
        files[i].GetContentFile("temp.jpeg")
        current_result = image_compare(file, "temp.jpeg")
        current_manta_name = current_file.split("- ")[-1].split(".")[0]
        if i < len(files) - 1:
            next_manta_name = files[i + 1]["title"].split("- ")[-1].split(".")[0]
        else :
            next_manta_name = None
        if current_manta_name == next_manta_name:
            current_folder_results.append(current_result)
            current_folder_files.append(files[i])
        else :
            current_folder_results.append(current_result)
            current_folder_files.append(files[i])
            max_result = max(current_folder_results)
            max_result_index = current_folder_results.index(max_result)
            for j in range(len(matches)):
                if max_result >= matches[j][0]:
                    temp = []
                    temp.append(max_result)
                    temp.append(current_folder_files[max_result_index])
                    temp.append(current_manta_name)
                    matches.insert(j, temp)
                    del matches[-1:]      
                    current_folder_results = []
                    current_folder_files = []
                    max_result = 0
                    break  
        print(i)
    return matches