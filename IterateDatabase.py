from ImageCompare import image_compare
from SaveImages import get_folder_id

def append_file_list(list, file_list, filter1, filter2):
    for file in file_list:
        if filter1 in file["title"] and filter2 in file["title"]:
            list.append(file)
    return (list)

def append_file_list_white(list, file_list, filter1, filter2):
    for file in file_list:
        if filter1 not in file["title"] and filter2 in file["title"]:
            list.append(file)
    return (list)

def get_files(database_folder, attributes, drive):
    files = []
    if attributes[1] == "Black" and (attributes[2] == "Male" or attributes[2] == "Unknown"):
        folder = get_folder_id(database_folder, "Black", drive)
        files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".M")
    if attributes[1] == "Black" and (attributes[2] == "Female" or attributes[2] == "Unknown"):
        folder = get_folder_id(database_folder, "Black", drive)
        files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".F")
    if attributes[1] == "Black" and attributes[2] == "Unknown":
        folder = get_folder_id(database_folder, "Black", drive)
        files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".U")

    if attributes[1] == "White" and (attributes[2] == "Male" or attributes[2] == "Unknown"):
        folder = get_folder_id(database_folder, "White", drive)
        files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".M")
    if attributes[1] == "White" and (attributes[2] == "Female" or attributes[2] == "Unknown"):
        folder = get_folder_id(database_folder, "White", drive)
        files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".F")
    if attributes[1] == "White" and attributes[2] == "Unknown":
        folder = get_folder_id(database_folder, "White", drive)
        files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".U")
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
    for filess in files:
        print(filess["title"])
    print(len(files))
    for i in range(len(files)):
        current_file = files[i]["title"]
        files[i].GetContentFile("temp.jpeg", mimetype="image/jpeg")
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