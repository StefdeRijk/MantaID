from ImageCompare import image_compare
from SaveImages import get_folder_id, get_manta_id
import glob
import cv2
import threading
from tkinter import *
import tkinter as tk
import socket

def show_background(root, background_image):
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #quit_button
    quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Raleway", 16), bg="#00243f", fg="white", height=4, width=16)
    quit_button.place(relx=0.25, rely=0.8, relwidth=0.125, relheight=0.125)

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


def go_through_database(master, database_folder, attributes, drive, preprocessed_image, background_image, home_page):
    sift = cv2.xfeatures2d.SIFT_create()
    file = cv2.imread(preprocessed_image)
    keypoints_file, descriptors_file = sift.detectAndCompute(file, None)

    #index 0 = percentage similar, index 1 = file (drive object), index 2 = name of manta
    matches = []
    files = glob.glob('C:\\Users\\USER\\Desktop\\MantaID\\Database\\*.jpg') #TODO make this a setting
    files = get_files(attributes, files)
    total_files = len(files)

    frame = Frame()
    show_background(master, background_image)

    text = tk.StringVar()
    text.set(str(0) + " / " + str(total_files))
    label = tk.Label(master, textvariable=text, font=("Raleway", 56), bg="#264b77", fg="white")
    label.place(relx=0.175, rely=0.4, relwidth=0.7, relheight=0.2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    master.update()

    for i in range(len(files)):
        while internet() is False:
            pass
        thread = threading.Thread(target=compare_file, args=(files[i], descriptors_file, database_folder, drive, matches,))
        thread.start()
        thread.join()
        text.set(str(i) + " / " + str(total_files))
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        master.update()
    
    matches.sort(key=lambda row: (row[0]))
    return matches

def compare_file(file, descriptors_file, database_folder, drive, matches):
    current_file = file
    current_result = image_compare(descriptors_file, current_file)
    current_manta_name = current_file.split("- ")[-1].split(".")[0]
    drive_file = get_drive_file(file, database_folder, drive)
    matches.append([current_result, drive_file, current_manta_name])
    return

def cancel_button_function(home_page, master):
    HomePage = home_page(master)
    HomePage.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False