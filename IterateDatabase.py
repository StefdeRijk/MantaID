from ImageCompare import image_compare
import glob

def append_file_list(list, file_list, filter1, filter2):
    for file in file_list:
        if file and filter1 in file and filter2 in file:
            list.append(file)
    return (list)

def append_file_list_white(list, file_list, filter1, filter2):
    for file in file_list:
        if file and filter1 not in file and filter2 in file:
            list.append(file)
    return (list)

def get_files(attributes, file_list):
    files = []
    if attributes[1] == "Black":
        if attributes[2] == "Male" or attributes[2] == "Unknown":
            files = append_file_list(files, file_list, "Black", ".M")
        if attributes[2] == "Female" or attributes[2] == "Unknown":
            files = append_file_list(files, file_list, "Black", ".F")
        if attributes[2] == "Unknown":
            files = append_file_list(files, file_list, "Black", ".U")
    else :
        if attributes[2] == "Male" or attributes[2] == "Unknown":
            files = append_file_list_white(files, file_list, "Black", ".M")
        if attributes[2] == "Female" or attributes[2] == "Unknown":
            files = append_file_list_white(files, file_list, "Black", ".F")
        if attributes[2] == "Unknown":
            files = append_file_list_white(files, file_list, "Black", ".U")
    return files

def go_through_database(file, amount_of_mantas, database_folder, attributes, drive, preprocessed_image):
    #index 0 = percentage similar, index 1 = file (drive object), index 2 = name of manta
    matches = []
    for i in range(amount_of_mantas):
        temp = [0, "", ""]
        matches.append(temp)
    files = glob.glob('C:\\Users\\seder\\Desktop\\MantaID\\Database\\*.jpg') #TODO make this a setting
    files = get_files(attributes, files)
    print(len(files))
    for i in range(len(files)):
        current_file = files[i]
        current_result = image_compare(file, preprocessed_image)
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