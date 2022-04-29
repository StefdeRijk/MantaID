import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from IterateDatabase import go_through_database
from SaveImages import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

settings_file = open("settings.txt", "r")


amount_of_mantas = int(settings_file.readline().split(" ")[-1])
show_all_mantas = bool(int(settings_file.read().split(" ")[-1]))

settings_file.close()


gauth = GoogleAuth()

gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)
fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList:
    if "Database" in file["title"]:
        root_folder_id = file["id"]


print(root_folder_id)

root = tk.Tk()
root.title("MantaID")
root.iconbitmap("icon.ico")
root.state("zoomed")

#background image
background_image = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(background_image)


def show_background():
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #quit_button
    quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Raleway", 16), bg="#00243f", fg="white", height=4, width=16)
    quit_button.place(relx=0.25, rely=0.8, relwidth=0.125, relheight=0.125)

def settings_button_function(master, page, file, manta_name, attributes, matches):
    SettingsPage = settings_page(master, page, file, manta_name, attributes, matches)
    show_page(SettingsPage.frame)

def get_resized_image(reference_image, frame, file, widget_width, widget_height):
    aspect_ratio_img = reference_image.width() / reference_image.height()
    frame.update()
    aspect_ratio_label = (frame.winfo_screenwidth() * widget_width) / (frame.winfo_screenheight() * widget_height - 10)
    if aspect_ratio_img > aspect_ratio_label:
        new_width = int(frame.winfo_screenwidth() * widget_width)
        new_height = int(new_width / aspect_ratio_img)
    else:
        new_height = int(frame.winfo_screenheight() * widget_height)
        new_width = int(new_height * aspect_ratio_img)
    new_reference_image = Image.open(file)
    resized_reference_image = new_reference_image.resize((new_width, new_height), Image.ANTIALIAS)
    return (resized_reference_image)

def correct_date_format(string):
    if string[2] != '-' or string[5] != '-':
        return 0
    day = ""
    day = string[0:2]
    if int(day) > 31 or int(day) < 0 or not day.isnumeric():
        return 0
    month = ""
    month = string[3:5]
    if int(month) > 12 or int(month) < 0  or not month.isnumeric():
        return 0
    year = ""
    year = string[6:8]
    if int(year) < 0 or not year.isnumeric():
        return 0
    return 1

def show_page(page):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)
        

class settings_page:
    def __init__(self, master, previous_page, file, manta_name, attributes, matches):
        self.frame = Frame()
        show_background()

        back_button = tk.Button(master, text="Back", command=lambda:back_button_function(previous_page, master, file, manta_name, attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white")
        back_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function(previous_page, master, file, manta_name, attributes, matches):
            PreviousPage = previous_page(master, file, manta_name, attributes, matches)
            show_page(PreviousPage.frame)

        set_matches_button_text = tk.StringVar()
        set_matches_button = tk.Button(master, text="Set amount of matches", command=lambda:set_matches_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        set_matches_button.place(relx=0.75, rely=0.1, relwidth=0.125, relheight=0.125)
        set_matches_label = tk.Label(master, text="Current amount of matches: " + str(amount_of_mantas), font=("Raleway", 16), bg="#3c5b74", fg="white")
        set_matches_label.place(relx=0.125, rely=0.1, relwidth=0.4, relheight=0.125)
        set_matches_instruction_label = tk.Label(master, textvariable=set_matches_button_text, font=("Raleway", 16), bg="#006699", fg="white")
        set_matches_button_text.set("Insert amount of matches below")
        set_matches_instruction_label.place(relx=0.55, rely=0.1, relwidth=0.175, relheight=0.0325)
        set_matches_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center")
        set_matches_entry_box.place(relx=0.55, rely=0.15, relwidth=0.175, relheight=0.075)

        def set_matches_button_function():
            global amount_of_mantas
            entered_value = set_matches_entry_box.get()
            if entered_value and entered_value.isnumeric():
                settings_file_read = open("settings.txt", "r")
                settings_file_data = settings_file_read.read()
                settings_file_read.close()
                first_line = settings_file_data.split("\n")[0]
                replace_value = first_line.split("= ")[-1]
                settings_file_data = settings_file_data.replace(replace_value, entered_value)
                settings_file_write = open("settings.txt", "w")
                settings_file_write.write(settings_file_data)
                settings_file_write.close()
                settings_file = open("settings.txt", "r")
                amount_of_mantas = int(settings_file.readline().split(" ")[-1])
                settings_file.close()
            else :
                set_matches_button_text.set("Please enter a number")
                return
            settings_button_function(master, previous_page, file, manta_name, attributes, matches)

        if show_all_mantas == True:
            show_mantas_bool = "Yes"
        else :
            show_mantas_bool = "No"
        show_all_mantas_button = tk.Button(master, text="Show all mantas", command=lambda:show_all_mantas_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        show_all_mantas_button.place(relx=0.75, rely=0.55, relwidth=0.125, relheight=0.125)
        show_all_mantas_label = tk.Label(master, text="Show all mantas: " + show_mantas_bool, font=("Raleway", 16), bg="#3c5b74", fg="white")
        show_all_mantas_label.place(relx=0.125, rely=0.55, relwidth=0.4, relheight=0.125)
        show_all_mantas_listbox = tk.Listbox(master, font=("Raleway", 16), bg="#006699", fg="White", justify="center", highlightbackground="Black")
        show_all_mantas_listbox.insert(0, "")
        show_all_mantas_listbox.insert(1, "Yes")
        show_all_mantas_listbox.insert(2, "No")
        show_all_mantas_listbox.place(relx=0.55, rely=0.55, relwidth=0.175, relheight=0.125)

        def show_all_mantas_button_function():
            global show_all_mantas
            entered_value = show_all_mantas_listbox.get(ANCHOR)
            if entered_value:
                if entered_value == "Yes":
                    entered_value = str(1)
                else :
                    entered_value = str(0)
                settings_file_read = open("settings.txt", "r")
                settings_file_data = settings_file_read.read()
                settings_file_read.close()
                first_line = settings_file_data.split("\n")[3]
                replace_value = first_line.split("= ")[-1]
                settings_file_data = settings_file_data.replace(replace_value, entered_value)
                settings_file_write = open("settings.txt", "w")
                settings_file_write.write(settings_file_data)
                settings_file_write.close()
                settings_file = open("settings.txt", "r")
                first_line =settings_file.read().split("\n")[3]
                show_all_mantas = bool(int(first_line.split(" ")[-1]))
                settings_file.close()
            else :
                return
            settings_button_function(master, previous_page, file, manta_name, attributes, matches)

class home_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        self.frame = Frame()
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, home_page, manta_name, None, None, None), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        #open images
        self.open_button_text = tk.StringVar()
        self.open_button = tk.Button(master, textvariable=self.open_button_text, command=lambda:open_files(file), font=("Raleway", 16), bg="#264b77", fg="white", height=4, width=16)
        self.open_button_text.set("Open image")
        self.open_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def open_files(file):
            self.open_button_text.set("Loading...")
            files = filedialog.askopenfile(parent=master, mode="rb", title="Choose file", filetypes=[("Images", "*.jpg; *.jpeg; *.JPG")])
            if files:
                file = files.name
                SelectionPage = selection_page(master, file, manta_name, attributes, matches)
                show_page(SelectionPage.frame)
            else :
                self.open_button_text.set("Open image")
                home_page(master, file, manta_name, attributes, matches)

class large_img_page:
    def __init__(self, master, file, manta_name, attributes, matches, previous_page):
        self.frame = Frame()
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, large_img_page, file, manta_name, self.attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        #cancel button
        self.cancel_button = tk.Button(master, text="Cancel", command=lambda:cancel_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.cancel_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function():
            HomePage = home_page(master, file, manta_name, attributes, matches)
            show_page(HomePage.frame)
        
        back_button = tk.Button(master, text="Back", command=lambda:back_button_function(master, file, attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        back_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function(master, file, attributes):
            PreviousPage = previous_page(master, file, manta_name, attributes, matches)
            show_page(PreviousPage.frame)
        
        #large image
        self.large_image = Image.open(file)
        self.large_image=ImageTk.PhotoImage(self.large_image)
        self.resized_large_image = get_resized_image(self.large_image, self.frame, file, 0.8, 0.7)
        self.resized_large_image=ImageTk.PhotoImage(self.resized_large_image)
        self.large_label = tk.Label(master, image=self.resized_large_image, bg="#264b77")
        self.large_label.image = self.resized_large_image
        self.large_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.7)

class selection_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        self.frame = Frame()
        self.attributes_number = 0
        self.attributes = [attributes] * 5 # species - colour - gender - date - dive site
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, selection_page, file, manta_name, self.attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        #cancel button
        self.cancel_button = tk.Button(master, text="Cancel", command=lambda:cancel_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.cancel_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function():
            HomePage = home_page(master, file, manta_name, attributes, matches)
            show_page(HomePage.frame)

        #process button
        self.process_button = tk.Button(master, text="Process", command=lambda:process_button_function(), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.process_button["state"] = "disabled"
        self.process_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def process_button_function():
            global root_folder_id
            if "Oceanic" in self.attributes[0]:
                root_folder_id = get_folder_id(root_folder_id, "birostris", drive)
            elif "Reef" in self.attributes[0]:
                root_folder_id = get_folder_id(root_folder_id, "alfredi", drive)
            matches = go_through_database(file, amount_of_mantas, root_folder_id, self.attributes, drive)
            ProcessPage = process_page(master, file, manta_name, self.attributes, matches)
            show_page(ProcessPage.frame)

        def show_full_img_button_function():
            LargeImgPage = large_img_page(master, file, manta_name, self.attributes, matches, selection_page)
            show_page(LargeImgPage.frame)

        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.resized_reference_image = get_resized_image(self.reference_image, self.frame, file, 0.3, 0.15)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_small_label = tk.Label(master, image=self.resized_reference_image, bg="#264b77")
        self.reference_small_label.image = self.resized_reference_image
        self.reference_small_label.place(relx=0.175, rely=0.05, relwidth=0.3, relheight=0.15)
        self.show_full_img_button = tk.Button(root, text="Show large image", command=lambda:show_full_img_button_function(), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.show_full_img_button.place(relx=0.175, rely=0.225, relwidth=0.3, relheight=0.04)

        def select_attributes(index, box, button):
            if index == 3 and not correct_date_format(box.get()):
                self.date_button_text.set("Wrong date format: DD-MM-YY")
                return
            else:
                self.date_button_text.set("Enter date of sighting below: DD-MM-YY")
            if index < 3:
                self.attributes[index] = box.get(ANCHOR)
            else:
                self.attributes[index] = box.get()
            button["state"] = DISABLED
            self.attributes_number += 1
            if self.attributes_number == 5:
                self.process_button["state"] = NORMAL

        #species listbox
        self.species_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.species_listbox.place(relx=0.525, rely=0.05, relwidth=0.3, relheight=0.15)
        self.species_listbox.insert(0, "Reef manta")
        self.species_listbox.insert(1, "Oceanic manta")
        self.species_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(0, self.species_listbox, self.species_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.species_select_button.place(relx=0.525, rely=0.225, relwidth=0.3, relheight=0.04)

        #colour listbox
        self.colour_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.colour_listbox.place(relx=0.525, rely=0.3, relwidth=0.3, relheight=0.15)
        self.colour_listbox.insert(0, "Black")
        self.colour_listbox.insert(1, "White")
        self.colour_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(1, self.colour_listbox, self.colour_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.colour_select_button.place(relx=0.525, rely=0.475, relwidth=0.3, relheight=0.04)

        #gender listbox
        self.gender_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.gender_listbox.place(relx=0.525, rely=0.55, relwidth=0.3, relheight=0.15)
        self.gender_listbox.insert(0, "Male")
        self.gender_listbox.insert(1, "Female")
        self.gender_listbox.insert(2, "Unknown")
        self.gender_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(2, self.gender_listbox, self.gender_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.gender_select_button.place(relx=0.525, rely=0.725, relwidth=0.3, relheight=0.04)

        #date entry_box
        self.date_button_text = tk.StringVar()
        self.date_button_text.set("Enter date of sighting below: DD-MM-YY")
        self.date_button = tk.Button(master, text="Set date", command=lambda:select_attributes(3, self.date_entry_box, self.date_button), font=("Raleway", 16), bg="#006699", fg="white")
        self.date_button.place(relx=0.175, rely=0.475, relwidth=0.3, relheight=0.04)
        self.date_label = tk.Label(master, textvariable=self.date_button_text, font=("Raleway", 16), bg="#264b77", fg="white")
        self.date_label.place(relx=0.175, rely=0.3, relwidth=0.3, relheight=0.07)
        self.date_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#264b77", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.date_entry_box.place(relx=0.175, rely=0.38, relwidth=0.3, relheight=0.07)

        #dive site entry_box
        self.set_dive_site_button = tk.Button(master, text="Set dive site", command=lambda:select_attributes(4, self.set_dive_site_entry_box, self.set_dive_site_button), font=("Raleway", 16), bg="#006699", fg="white")
        self.set_dive_site_button.place(relx=0.175, rely=0.725, relwidth=0.3, relheight=0.04)
        self.set_dive_site_label = tk.Label(master, text="Enter dive site below: ", font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_dive_site_label.place(relx=0.175, rely=0.55, relwidth=0.3, relheight=0.07)
        self.set_dive_site_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#264b77", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.set_dive_site_entry_box.place(relx=0.175, rely=0.63, relwidth=0.3, relheight=0.07)

class process_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        global amount_of_mantas
        self.frame = Frame()
        self.matches = matches
        self.match_index = 0
        self.number_of_mantas = amount_of_mantas
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, process_page, file, manta_name, attributes, self.matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        def show_matches():
            ShowMatchImage = show_match_image(master, self.matches, self.match_index)
            ShowMatchLabel = show_match_label(master, self.matches, self.match_index)
            ShowMatchImage.frame.place(relx=0.525, rely=0.025, relwidth=0.425, relheight=0.675)
            ShowMatchLabel.frame.place(relx=0.4375, rely=0.725, relwidth=0.125, relheight=0.05)

        show_matches()

        #retry button
        self.cancel_button = tk.Button(master, text="Use different image", command=lambda:cancel_button_function(), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.cancel_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function():
            HomePage = home_page(master, file, manta_name, attributes, self.matches)
            show_page(HomePage.frame)
        
        #previous button
        self.previous_button = tk.Button(master, text="Previous", command=lambda:previous_button_function(), font=("Raleway", 16), bg="#686873", fg="white", height=3, width=16)
        self.previous_button.place(relx=0.25, rely=0.725, relwidth=0.125, relheight=0.05)

        def previous_button_function():
            self.match_index -= 1
            set_button_state()
            show_matches()

        #next button
        self.next_button = tk.Button(master, text="Next", command=lambda:next_button_function(), font=("Raleway", 16), bg="#686873", fg="white", height=3, width=16)
        self.next_button.place(relx=0.625, rely=0.725, relwidth=0.125, relheight=0.05)
        
        def next_button_function():
            self.match_index += 1
            set_button_state()
            show_matches()

        def set_button_state():
            if self.match_index == (self.number_of_mantas - 1) or self.matches[self.match_index + 1][1] == "":
                self.next_button["state"] = DISABLED
            else :
                self.next_button["state"] = NORMAL
            if self.match_index == 0:
                self.previous_button["state"] = DISABLED
            else :
                self.previous_button["state"] = NORMAL

        set_button_state()

        #save button
        self.save_button = tk.Button(master, text="Save image", command=lambda:save_button_function(file), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.save_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.05)

        def save_button_function(file):
            SavePage = save_page(master, file, "", attributes, self.matches, self.match_index)
            show_page(SavePage.frame)

        #new_button
        new_button = tk.Button(master, text="New manta", command=lambda:new_button_function(master, file, attributes), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        new_button.place(relx=0.8, rely=0.825, relwidth=0.075, relheight=0.075)

        def new_button_function(master, file, attributes):
            WarningPage = warning_page(master, file, "", attributes, self.matches)
            self.frame.place_forget()
            show_page(WarningPage.frame)

        #remove button
        self.remove_button = tk.Button(master, text="Remove suggestion", command=lambda:remove_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.remove_button.place(relx=0.4375, rely=0.875, relwidth=0.125, relheight=0.05)

        def remove_button_function():
            self.matches.pop(self.match_index)
            if self.match_index == (self.number_of_mantas - 1):
                self.match_index -= 1
            self.number_of_mantas -= 1
            if self.number_of_mantas == 0:
                cancel_button_function()
            else :
                set_button_state()
                show_matches()

        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.resized_reference_image = get_resized_image(self.reference_image, self.frame, file, 0.425, 0.675)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_label = tk.Label(master, image=self.resized_reference_image, bg="#006699")
        self.reference_label.image = self.resized_reference_image
        self.reference_label.place(relx=0.05, rely=0.025, relwidth=0.425, relheight=0.675)

class warning_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        self.frame = Frame()
        self.manta_name = manta_name
        show_background()

        #settings_button
        self.settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, new_manta_page, file, self.manta_name, attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        self.settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        back_button = tk.Button(master, text="Back", command=lambda:back_button_function(master, file, attributes), font=("Raleway", 16), bg="#3c5b74", fg="white")
        back_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function(master, file, attributes):
            PreviousPage = process_page(master, file, self.manta_name, attributes, matches)
            show_page(PreviousPage.frame)

        self.warning_label = tk.Label(master, text="Warning!\n\nPlease ask a project scientist \nto check if the manta \nis a new individual.", font=("Raleway", 46), bg="#bc5334", fg="white")
        self.warning_label.place(relx=0.1, rely=0.05, relwidth=0.75, relheight=0.7)
        
        continue_button = tk.Button(master, text="Continue", command=lambda:continue_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        continue_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def continue_button_function():
            NewMantaPage = new_manta_page(master, file, "", attributes, matches)
            self.frame.place_forget()
            show_page(NewMantaPage.frame)

class new_manta_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        self.frame = Frame()
        self.manta_name = manta_name
        show_background()

        #settings_button
        self.settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, new_manta_page, file, self.manta_name, attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        self.settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        back_button = tk.Button(master, text="Cancel", command=lambda:cancel_button_function(master, file, attributes), font=("Raleway", 16), bg="#3c5b74", fg="white")
        back_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function(master, file, attributes):
            PreviousPage = process_page(master, file, self.manta_name, attributes, matches)
            show_page(PreviousPage.frame)
        
        self.add_manta_button = tk.Button(master, text="Add manta", command=lambda:add_manta_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        self.add_manta_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def add_manta_button_function():
            save_new_manta(manta_name, attributes, root_folder_id, file, drive)
            HomePage = home_page(master, file, manta_name, attributes, matches)
            self.frame.place_forget()
            show_page(HomePage.frame)
        
        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.resized_reference_image = get_resized_image(self.reference_image, self.frame, file, 0.25, 0.55)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_small_label = tk.Label(master, image=self.resized_reference_image, bg="#3c5b74")
        self.reference_small_label.image = self.resized_reference_image
        self.reference_small_label.place(relx=0.075, rely=0.05, relwidth=0.25, relheight=0.575)
        self.show_full_img_button = tk.Button(root, text="Show large image", command=lambda:show_full_img_button_function(), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.show_full_img_button.place(relx=0.075, rely=0.65, relwidth=0.25, relheight=0.1)

        def show_full_img_button_function():
            LargeImgPage = large_img_page(master, file, manta_name, attributes, matches, new_manta_page)
            show_page(LargeImgPage.frame)

        self.manta_name_button_text = tk.StringVar()
        self.set_manta_name_button = tk.Button(master, text="Set manta name", command=lambda:set_manta_name_button_function(master, file, attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_name_button.place(relx=0.75, rely=0.05, relwidth=0.125, relheight=0.125)
        self.set_manta_name_label = tk.Label(master, text="Name: " + self.manta_name, font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_name_label.place(relx=0.35, rely=0.05, relwidth=0.175, relheight=0.125)
        self.set_manta_name_instruction_label = tk.Label(master, textvariable=self.manta_name_button_text, font=("Raleway", 16), bg="#006699", fg="white")
        self.manta_name_button_text.set("Insert new manta name below")
        self.set_manta_name_instruction_label.place(relx=0.55, rely=0.05, relwidth=0.175, relheight=0.0325)
        self.set_manta_name_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.set_manta_name_entry_box.place(relx=0.55, rely=0.1, relwidth=0.175, relheight=0.075)

        def set_manta_name_button_function(master, file, attributes):
            global root_folder_id
            new_name = self.set_manta_name_entry_box.get()
            if new_name:
                if attributes[1] == "Black":
                    if new_name.find("Black"):
                        self.manta_name_button_text.set("Name must include 'Black'")
                        return
                if new_name_unique(new_name, drive, root_folder_id):
                    self.manta_name = new_name
                    NewMantaPage = new_manta_page(master, file, self.manta_name, attributes, matches)
                    show_page(NewMantaPage.frame)
                else:
                    self.manta_name_button_text.set("Name must be unique")
        
        self.set_dive_site_button = tk.Button(master, text="Set dive site", command=lambda:set_dive_site_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_dive_site_button.place(relx=0.75, rely=0.2, relwidth=0.125, relheight=0.125)
        self.set_dive_site_label = tk.Label(master, text="Dive site: " + attributes[4], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_dive_site_label.place(relx=0.35, rely=0.2, relwidth=0.175, relheight=0.125)
        self.set_dive_site_instruction_label = tk.Label(master, text="Enter dive site below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_dive_site_instruction_label.place(relx=0.55, rely=0.2, relwidth=0.175, relheight=0.0325)
        self.set_dive_site_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.set_dive_site_entry_box.place(relx=0.55, rely=0.25, relwidth=0.175, relheight=0.075)

        def set_dive_site_button_function(attributes):
            new_dive_site = self.set_dive_site_entry_box.get()
            if new_dive_site:
                attributes[4] = new_dive_site
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes, matches)
                show_page(NewMantaPage.frame)

        self.date_button_text = tk.StringVar()
        self.date_button_text.set("Change date of sighting below")
        self.set_date_button = tk.Button(master, text="Set date", command=lambda:set_date_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_date_button.place(relx=0.75, rely=0.35, relwidth=0.125, relheight=0.125)
        self.set_date_label = tk.Label(master, text="Date: " + attributes[3], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_date_label.place(relx=0.35, rely=0.35, relwidth=0.175, relheight=0.125)
        self.set_date_instruction_label = tk.Label(master, textvariable=self.date_button_text, font=("Raleway", 16), bg="#006699", fg="white")
        self.set_date_instruction_label.place(relx=0.55, rely=0.35, relwidth=0.175, relheight=0.0325)
        self.set_date_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.set_date_entry_box.place(relx=0.55, rely=0.4, relwidth=0.175, relheight=0.075)

        def set_date_button_function(attributes):
            if not correct_date_format(self.set_date_entry_box.get()):
                self.date_button_text.set("Wrong date format: DD-MM-YY")
                return 
            new_date = self.set_date_entry_box.get()
            if new_date:
                attributes[3] = new_date
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes, matches)
                show_page(NewMantaPage.frame)

        self.set_manta_gender_button = tk.Button(master, text="Set manta gender", command=lambda:set_manta_gender_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_gender_button.place(relx=0.75, rely=0.5, relwidth=0.125, relheight=0.125)
        self.set_manta_gender_label = tk.Label(master, text="Gender: " + attributes[2], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_gender_label.place(relx=0.35, rely=0.5, relwidth=0.175, relheight=0.125)
        self.set_manta_gender_instruction_label = tk.Label(master, text="Change manta gender below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_manta_gender_instruction_label.place(relx=0.55, rely=0.5, relwidth=0.175, relheight=0.0325)
        self.set_manta_gender_listbox = tk.Listbox(master, font=("Raleway", 14), bg="#006699", fg="White", justify="center", highlightbackground="Black")
        self.set_manta_gender_listbox.place(relx=0.55, rely=0.55, relwidth=0.175, relheight=0.075)
        self.set_manta_gender_listbox.insert(0, "Male")
        self.set_manta_gender_listbox.insert(1, "Female")
        self.set_manta_gender_listbox.insert(2, "Unknown")

        def set_manta_gender_button_function(attributes):
            new_gender = self.set_manta_gender_listbox.get(ANCHOR)
            if new_gender:
                attributes[2] = new_gender
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes, matches)
                show_page(NewMantaPage.frame)
        
        self.manta_species_label = tk.Label(master, text="Species: " + attributes[0], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.manta_species_label.place(relx=0.35, rely=0.65, relwidth=0.25, relheight=0.1)

        self.manta_colour_label = tk.Label(master, text="Colour: " + attributes[1], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.manta_colour_label.place(relx=0.625, rely=0.65, relwidth=0.25, relheight=0.1)

class save_page:
     def __init__(self, master, file, manta_name, attributes, matches, match_index):
        self.frame = Frame()
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, process_page, file, manta_name, attributes, self.matches), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        #retry button
        self.cancel_button = tk.Button(master, text="Use different image", command=lambda:cancel_button_function(), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.cancel_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function():
            HomePage = home_page(master, file, manta_name, attributes, matches)
            show_page(HomePage.frame)
        
        #back button
        self.back_button = tk.Button(master, text="Cancel", command=lambda:back_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.back_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function():
            HomePage = process_page(master, file, manta_name, attributes, matches)
            show_page(HomePage.frame)
        
        #save button
        self.save_button = tk.Button(master, text="Save image", command=lambda:save_button_function(file, drive), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.save_button.place(relx=0.675, rely=0.35, relwidth=0.125, relheight=0.125)

        def save_button_function(file, drive):
            global root_folder_id
            save_image_in_match_folder(file, drive, matches[match_index][1]['title'], root_folder_id, attributes, matches[match_index][2])
            cancel_button_function()
        
        #save button
        self.save_as_master_button = tk.Button(master, text="Save image as master", command=lambda:save_as_master_button_function(file, drive), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.save_as_master_button.place(relx=0.675, rely=0.075, relwidth=0.125, relheight=0.125)

        def save_as_master_button_function(file, drive):
            global root_folder_id
            self.save_as_master_button["state"] = "disabled"
            save_image_in_master_folder(file, drive, matches[match_index][1]['title'], root_folder_id, attributes)
            save_page(master, file, manta_name, attributes, matches, match_index)
        
        self.safe_multiple_files_button_text = tk.StringVar()
        self.safe_multiple_files_button_text.set("Save multiple files")
        self.safe_multiple_files_button = tk.Button(master, textvariable=self.safe_multiple_files_button_text, command=lambda:safe_multiple_files_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.safe_multiple_files_button.place(relx=0.675, rely=0.55, relwidth=0.125, relheight=0.125)

        def safe_multiple_files_button_function():
            self.safe_multiple_files_button_text.set("Loading...")
            files = filedialog.askopenfilenames(parent=master, title="Choose files", filetypes=[("Images", "*.jpg; *.jpeg; *.JPG")])
            if files:
                file_list = list(files)
                save_multiple_images_in_match_folder(file, drive, matches[match_index][1]['title'], root_folder_id, attributes, file_list, matches[match_index][2])
                cancel_button_function()
        self.safe_multiple_files_button_text.set("Save multiple files")

        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.resized_reference_image = get_resized_image(self.reference_image, self.frame, file, 0.575, 0.725)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_label = tk.Label(master, image=self.resized_reference_image, bg="#006699")
        self.reference_label.image = self.resized_reference_image
        self.reference_label.place(relx=0.05, rely=0.025, relwidth=0.575, relheight=0.725)

class show_match_image:
    def __init__(self, master, matches, i):
        self.frame = Frame()
        #compare image
        matches[i][1].GetContentFile("temp_match.jpeg")
        self.compare_image = Image.open("temp_match.jpeg")
        self.compare_image = ImageTk.PhotoImage(self.compare_image)
        self.resized_compare_image = get_resized_image(self.compare_image, self.frame, "temp_match.jpeg", 0.425, 0.675)
        self.resized_compare_image=ImageTk.PhotoImage(self.resized_compare_image)
        self.compare_label = tk.Label(master, image=self.resized_compare_image, bg="#006699")
        self.compare_label.image = self.resized_compare_image
        self.compare_label.place(relx=0.525, rely=0.025, relwidth=0.425, relheight=0.675)

class show_match_label:
    def __init__(self, master, matches, i):
        self.frame = Frame()
        #result label
        self.match_name = matches[i][2]
        self.result_label_text = self.match_name
        self.result_label = tk.Label(master, text=self.result_label_text, font=("Raleway", 16), bg="#b67929", fg="white", height=3, width=16)
        self.result_label.place(relx=0.4375, rely=0.725, relwidth=0.125, relheight=0.05)

HomePage = home_page(root, "", None, None, None)
root.mainloop()
