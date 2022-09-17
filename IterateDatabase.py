from ImageCompare import image_compare
from SaveImages import get_folder_id, get_manta_id
import glob
import cv2

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

def get_drive_file(database_file, drive_folder, drive):
    master_folder = get_folder_id(drive_folder, "MASTER", drive)
    master_folder = drive.ListFile({'q': "'" + master_folder + "' in parents and trashed=false and mimeType='image/jpeg'"}).GetList()
    for file in master_folder:
        if get_manta_id(file['title']) == get_manta_id(database_file):
            return file

def go_through_database(file, database_folder, attributes, drive, preprocessed_image):
    sift = cv2.xfeatures2d.SIFT_create()
    file = cv2.imread(file)
    keypoints_file, descriptors_file = sift.detectAndCompute(file, None)

    #index 0 = percentage similar, index 1 = file (drive object), index 2 = name of manta
    matches = []
    files = glob.glob('C:\\Users\\seder\\Desktop\\MantaID\\Database\\*.jpg') #TODO make this a setting
    files = get_files(attributes, files)

    print(len(files))

    for i in range(len(files)):
        current_file = files[i]
        current_result = image_compare(descriptors_file, current_file)
        current_manta_name = current_file.split("- ")[-1].split(".")[0]
        drive_file = get_drive_file(files[i], database_folder, drive)
        matches.append([current_result, drive_file, current_manta_name])
        print(i)

    matches.sort(key=lambda row: (row[0]))
    return matches