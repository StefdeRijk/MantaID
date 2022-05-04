from ImageCompare import image_compare
from SaveImages import get_folder_id
# import glob

def append_file_list(list, file_list, filter1, filter2):
    for file in file_list:
        if file and filter1 in file["title"] and filter2 in file["title"]:
            list.append(file)
    return (list)

def append_file_list_white(list, file_list, filter1, filter2):
    for file in file_list:
        if file and filter1 not in file["title"] and filter2 in file["title"]:
            list.append(file)
    return (list)

def get_files(database_folder, attributes, drive):
    files = []
    if attributes[1] == "Black":
        if attributes[2] == "Male" or attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "Black", drive)
            files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".M")
        if attributes[2] == "Female" or attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "Black", drive)
            files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".F")
        if attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "Black", drive)
            files = append_file_list(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".U")
    else :
        if attributes[2] == "Male" or attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "White", drive)
            files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".M")
        if attributes[2] == "Female" or attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "White", drive)
            files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".F")
        if attributes[2] == "Unknown":
            folder = get_folder_id(database_folder, "White", drive)
            files = append_file_list_white(files, drive.ListFile({'q': "'" + folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList(), "Black", ".U")
    return files

def go_through_database(file, amount_of_mantas, database_folder, attributes, drive):
    #index 0 = percentage similar, index 1 = file (drive object), index 2 = name of manta
    matches = []
    for i in range(amount_of_mantas):
        temp = [0, "", ""]
        matches.append(temp)
    files = get_files(database_folder, attributes, drive)
    # files = []
    # for filename in glob.glob('1. MASTER ID Database Alfredi (ALL) BF/*.jpg'):
    #     files.append(filename)
    for filess in files:
        print(filess["title"])
        # print(filess)
    print(len(files))
    for i in range(2): #range(len(files)):
        current_file = files[i]["title"]
        # current_file = files[i]
        files[i].GetContentFile("temp.jpeg", mimetype="image/jpeg")
        current_result = 1 #image_compare(file, "temp.jpeg")
        current_manta_name = current_file.split("- ")[-1].split(".")[0]
        for j in range(len(matches)):
            if current_result >= matches[j][0]:
                temp = []
                temp.append(current_result)
                temp.append(files[i])
                temp.append(current_manta_name)
                matches.insert(j, temp)
                del matches[-1:]      
                break  
        print(i)
    return matches