# from nis import match
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from IterateDatabase import go_through_database
import shutil

settings_file = open("settings.txt", "r")


amount_of_mantas = int(settings_file.readline().split(" ")[-1])
database_folder = settings_file.readline().split(" ")[-1]

settings_file.close()

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

def show_page(page):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)


class settings_page:
    def __init__(self, master, previous_page, file, manta_name, attributes, matches):
        global database_folder
        self.frame = Frame()
        self.new_database_folder = None
        show_background()

        back_button = tk.Button(master, text="Back", command=lambda:back_button_function(previous_page, master, file, manta_name, attributes, matches), font=("Raleway", 16), bg="#3c5b74", fg="white")
        back_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function(previous_page, master, file, manta_name, attributes, matches):
            PreviousPage = previous_page(master, file, manta_name, attributes, matches)
            show_page(PreviousPage.frame)

        set_matches_button = tk.Button(master, text="Set amount of matches", command=lambda:set_matches_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        set_matches_button.place(relx=0.75, rely=0.1, relwidth=0.125, relheight=0.125)
        set_matches_label = tk.Label(master, text="Current amount of matches: " + str(amount_of_mantas), font=("Raleway", 16), bg="#3c5b74", fg="white")
        set_matches_label.place(relx=0.125, rely=0.1, relwidth=0.4, relheight=0.125)
        set_matches_instruction_label = tk.Label(master, text="Insert amount of matches below", font=("Raleway", 16), bg="#006699", fg="white")
        set_matches_instruction_label.place(relx=0.55, rely=0.1, relwidth=0.175, relheight=0.0325)
        set_matches_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center")
        set_matches_entry_box.place(relx=0.55, rely=0.15, relwidth=0.175, relheight=0.075)

        def set_matches_button_function():
            global amount_of_mantas
            entered_value = set_matches_entry_box.get()
            if (entered_value):
                settings_file_read = open("settings.txt", "r")
                settings_file_data = settings_file_read.read()
                settings_file_read.close()
                first_line = settings_file_data.split("\n")[-2]
                replace_value = first_line.split(" ")[-1]
                settings_file_data = settings_file_data.replace(replace_value, entered_value)
                settings_file_write = open("settings.txt", "w")
                settings_file_write.write(settings_file_data)
                settings_file_write.close()
                settings_file = open("settings.txt", "r")
                amount_of_mantas = int(settings_file.readline().split(" ")[-1])
                settings_file.close()
            settings_button_function(master, previous_page, file)

        set_database_button = tk.Button(master, text="Set database folder", command=lambda:set_database_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        set_database_button.place(relx=0.75, rely=0.25, relwidth=0.125, relheight=0.125)
        set_database_label = tk.Label(master, text="Current database folder: " + database_folder, font=("Raleway", 16), bg="#3c5b74", fg="white")
        set_database_label.place(relx=0.125, rely=0.25, relwidth=0.4, relheight=0.125)
        self.browse_button_text = tk.StringVar()
        browse_button = tk.Button(master, textvariable=self.browse_button_text, command=lambda:browse_button_function(), font=("Raleway", 16), bg="#006699", fg="white")
        self.browse_button_text.set("Browse")
        browse_button.place(relx=0.55, rely=0.25, relwidth=0.175, relheight=0.125)

        def browse_button_function():
            self.browse_button_text.set("Loading...")
            self.new_database_folder = filedialog.askdirectory(parent=master, title="Choose database folder")
            self.browse_button_text.set("New folder is: " + self.new_database_folder.split("/")[-1])

        def set_database_button_function():
            global database_folder
            if self.new_database_folder:
                settings_file_read = open("settings.txt", "r")
                settings_file_data = settings_file_read.read()
                settings_file_read.close()
                first_line = settings_file_data.split("\n")[-1]
                replace_value = first_line.split(" ")[-1]
                settings_file_data = settings_file_data.replace(replace_value, self.new_database_folder)
                settings_file_write = open("settings.txt", "w")
                settings_file_write.write(settings_file_data)
                settings_file_write.close()
                settings_file = open("settings.txt", "r")
                database_folder = settings_file.read().split(" ")[-1]
                settings_file.close()
            settings_button_function(master, previous_page, file)

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
            files = filedialog.askopenfile(parent=master, mode="rb", title="Choose file", filetypes=[("Images", "*.png; *.jpg")])
            if files:
                file = files.name
                SelectionPage = selection_page(master, file, manta_name, attributes, matches)
                show_page(SelectionPage.frame)
            else :
                home_page(root)

class selection_page:
    def __init__(self, master, file, manta_name, attributes, matches):
        self.frame = Frame()
        self.attributes_number = 0
        self.attributes = [attributes] * 3 # species - colour - gender
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
            matches = go_through_database(file, amount_of_mantas, database_folder)
            ProcessPage = process_page(master, file, manta_name, self.attributes, matches)
            show_page(ProcessPage.frame)

        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.height = self.reference_image.height()
        self.width = self.reference_image.width()
        self.aspect_ratio = self.width / self.height
        self.new_width = int(324 * self.aspect_ratio)
        self.new_reference_image = Image.open(file)
        self.resized_reference_image = self.new_reference_image.resize((self.new_width,324), Image.ANTIALIAS)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_small_label = tk.Label(master, image=self.resized_reference_image, bg="#264b77")
        self.reference_small_label.image = self.resized_reference_image
        self.reference_small_label.place(relx=0.175, rely=0.05, relwidth=0.3, relheight=0.3)

        def select_attributes(index, listbox, button):
            self.attributes[index] = listbox.get(ANCHOR)
            button["state"] = DISABLED
            self.attributes_number += 1
            if self.attributes_number == 3:
                self.process_button["state"] = NORMAL

        #species listbox
        self.species_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.species_listbox.place(relx=0.525, rely=0.05, relwidth=0.3, relheight=0.2)
        self.species_listbox.insert(0, "Reef manta")
        self.species_listbox.insert(1, "Oceanic manta")
        self.species_listbox.insert(2, "Unknown")
        self.species_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(0, self.species_listbox, self.species_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.species_select_button.place(relx=0.525, rely=0.3, relwidth=0.3, relheight=0.05)

        #colour listbox
        self.colour_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.colour_listbox.place(relx=0.175, rely=0.4, relwidth=0.3, relheight=0.2)
        self.colour_listbox.insert(0, "Black")
        self.colour_listbox.insert(1, "White")
        self.colour_listbox.insert(2, "Unknown")
        self.colour_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(1, self.colour_listbox, self.colour_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.colour_select_button.place(relx=0.175, rely=0.65, relwidth=0.3, relheight=0.05)

        #gender listbox
        self.gender_listbox = tk.Listbox(master, bg="#264b77", font=("Raleway", 16), fg="white", width=10)
        self.gender_listbox.place(relx=0.525, rely=0.4, relwidth=0.3, relheight=0.2)
        self.gender_listbox.insert(0, "Male")
        self.gender_listbox.insert(1, "Female")
        self.gender_listbox.insert(2, "Unknown")
        self.gender_select_button = tk.Button(root, text="Select", command=lambda:select_attributes(2, self.gender_listbox, self.gender_select_button), font=("Raleway", 16), bg="#006699", fg="white", height=3, width=16)
        self.gender_select_button.place(relx=0.525, rely=0.65, relwidth=0.3, relheight=0.05)

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
            if self.match_index == (self.number_of_mantas - 1):
                self.next_button["state"] = DISABLED
            else :
                self.next_button["state"] = NORMAL
            if self.match_index == 0:
                self.previous_button["state"] = DISABLED
            else :
                self.previous_button["state"] = NORMAL

        set_button_state()

        #save button
        self.save_button = tk.Button(master, text="Save image", command=lambda:save_button_function(file, self.matches[self.match_index][1]), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.save_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.05)

        def save_button_function(src, dst):
            dst_cpy = dst.rsplit("\\", 1)[0] + "\\"
            manta_name = dst.split("\\")[-2]
            dst = dst_cpy + manta_name + "10.jpg"
            shutil.copy2(src, dst)
            cancel_button_function()

        #new_button
        new_button = tk.Button(master, text="New manta", command=lambda:new_button_function(master, file, attributes), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        new_button.place(relx=0.8, rely=0.825, relwidth=0.075, relheight=0.075)

        def new_button_function(master, file, attributes):
            NewMantaPage = new_manta_page(master, file, "", attributes, self.matches)
            self.frame.place_forget()
            show_page(NewMantaPage.frame)

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
        self.height = self.reference_image.height()
        self.width = self.reference_image.width()
        self.aspect_ratio = self.width / self.height
        self.new_width = int(729 * self.aspect_ratio)
        self.new_reference_image = Image.open(file)
        self.resized_reference_image = self.new_reference_image.resize((self.new_width,729), Image.ANTIALIAS)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_label = tk.Label(master, image=self.resized_reference_image, bg="#006699")
        self.reference_label.image = self.resized_reference_image
        self.reference_label.place(relx=0.05, rely=0.025, relwidth=0.425, relheight=0.675)

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
            HomePage = home_page(master, file)
            self.frame.place_forget()
            show_page(HomePage.frame)
        
        #reference image
        self.reference_image = Image.open(file)
        self.reference_image=ImageTk.PhotoImage(self.reference_image)
        self.height = self.reference_image.height()
        self.width = self.reference_image.width()
        self.aspect_ratio = self.width / self.height
        self.new_width = int(424 * self.aspect_ratio)
        self.new_reference_image = Image.open(file)
        self.resized_reference_image = self.new_reference_image.resize((self.new_width,424), Image.ANTIALIAS)
        self.resized_reference_image=ImageTk.PhotoImage(self.resized_reference_image)
        self.reference_small_label = tk.Label(master, image=self.resized_reference_image, bg="#264b77")
        self.reference_small_label.image = self.resized_reference_image
        self.reference_small_label.place(relx=0.075, rely=0.1, relwidth=0.25, relheight=0.575)

        self.set_manta_name_button = tk.Button(master, text="Set manta name", command=lambda:set_manta_name_button_function(master, file, attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_name_button.place(relx=0.75, rely=0.1, relwidth=0.125, relheight=0.125)
        self.set_manta_name_label = tk.Label(master, text="Name: " + self.manta_name, font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_name_label.place(relx=0.35, rely=0.1, relwidth=0.175, relheight=0.125)
        self.set_manta_name_instruction_label = tk.Label(master, text="Insert new manta name below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_manta_name_instruction_label.place(relx=0.55, rely=0.1, relwidth=0.175, relheight=0.0325)
        self.set_manta_name_entry_box = tk.Entry(master, font=("Raleway", 16), bg="#006699", fg="white", justify="center", highlightbackground="Black", highlightthickness=1)
        self.set_manta_name_entry_box.place(relx=0.55, rely=0.15, relwidth=0.175, relheight=0.075)

        def set_manta_name_button_function(master, file, attributes):
            new_name = self.set_manta_name_entry_box.get()
            if new_name:
                self.manta_name = new_name
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes)
                show_page(NewMantaPage.frame)
        
        self.set_manta_species_button = tk.Button(master, text="Set manta species", command=lambda:set_manta_species_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_species_button.place(relx=0.75, rely=0.25, relwidth=0.125, relheight=0.125)
        self.set_manta_species_label = tk.Label(master, text="Species: " + attributes[0], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_species_label.place(relx=0.35, rely=0.25, relwidth=0.175, relheight=0.125)
        self.set_manta_species_instruction_label = tk.Label(master, text="Change manta species below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_manta_species_instruction_label.place(relx=0.55, rely=0.25, relwidth=0.175, relheight=0.0325)
        self.set_manta_species_listbox = tk.Listbox(master, font=("Raleway", 14), bg="#006699", fg="White", justify="center", highlightbackground="Black")
        self.set_manta_species_listbox.place(relx=0.55, rely=0.3, relwidth=0.175, relheight=0.075)
        self.set_manta_species_listbox.insert(0, "Reef manta")
        self.set_manta_species_listbox.insert(1, "Oceanic manta")
        self.set_manta_species_listbox.insert(2, "Unknown")

        def set_manta_species_button_function(attributes):
            new_species = self.set_manta_species_listbox.get(ANCHOR)
            if new_species:
                attributes[0] = new_species
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes)
                show_page(NewMantaPage.frame)

        self.set_manta_colour_button = tk.Button(master, text="Set manta colour", command=lambda:set_manta_colour_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_colour_button.place(relx=0.75, rely=0.4, relwidth=0.125, relheight=0.125)
        self.set_manta_colour_label = tk.Label(master, text="Colour: " + attributes[1], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_colour_label.place(relx=0.35, rely=0.4, relwidth=0.175, relheight=0.125)
        self.set_manta_colour_instruction_label = tk.Label(master, text="Change manta colour below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_manta_colour_instruction_label.place(relx=0.55, rely=0.4, relwidth=0.175, relheight=0.0325)
        self.set_manta_colour_listbox = tk.Listbox(master, font=("Raleway", 14), bg="#006699", fg="White", justify="center", highlightbackground="Black")
        self.set_manta_colour_listbox.place(relx=0.55, rely=0.45, relwidth=0.175, relheight=0.075)
        self.set_manta_colour_listbox.insert(0, "Black")
        self.set_manta_colour_listbox.insert(1, "White")
        self.set_manta_colour_listbox.insert(2, "Unknown")

        def set_manta_colour_button_function(attributes):
            new_colour = self.set_manta_colour_listbox.get(ANCHOR)
            if new_colour:
                attributes[1] = new_colour
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes)
                show_page(NewMantaPage.frame)

        self.set_manta_gender_button = tk.Button(master, text="Set manta gender", command=lambda:set_manta_gender_button_function(attributes), font=("Raleway", 16), bg="#264b77", fg="white")
        self.set_manta_gender_button.place(relx=0.75, rely=0.55, relwidth=0.125, relheight=0.125)
        self.set_manta_gender_label = tk.Label(master, text="Gender: " + attributes[2], font=("Raleway", 16), bg="#3c5b74", fg="white")
        self.set_manta_gender_label.place(relx=0.35, rely=0.55, relwidth=0.175, relheight=0.125)
        self.set_manta_gender_instruction_label = tk.Label(master, text="Change manta gender below", font=("Raleway", 16), bg="#006699", fg="white")
        self.set_manta_gender_instruction_label.place(relx=0.55, rely=0.55, relwidth=0.175, relheight=0.0325)
        self.set_manta_gender_listbox = tk.Listbox(master, font=("Raleway", 14), bg="#006699", fg="White", justify="center", highlightbackground="Black")
        self.set_manta_gender_listbox.place(relx=0.55, rely=0.6, relwidth=0.175, relheight=0.075)
        self.set_manta_gender_listbox.insert(0, "Male")
        self.set_manta_gender_listbox.insert(1, "Female")
        self.set_manta_gender_listbox.insert(2, "Unknown")

        def set_manta_gender_button_function(attributes):
            new_gender = self.set_manta_gender_listbox.get(ANCHOR)
            if new_gender:
                attributes[2] = new_gender
                NewMantaPage = new_manta_page(master, file, self.manta_name, attributes)
                show_page(NewMantaPage.frame)

class show_match_image:
    def __init__(self, master, matches, i):
        self.frame = Frame()
        #compare image
        self.compare_image = Image.open(matches[i][1])
        self.compare_image = ImageTk.PhotoImage(self.compare_image)
        self.height = self.compare_image.height()
        self.width = self.compare_image.width()
        self.aspect_ratio = self.width / self.height
        self.new_width = int(729 * self.aspect_ratio)
        self.new_compare_image = Image.open(matches[i][1])
        self.resized_compare_image = self.new_compare_image.resize((self.new_width,729), Image.ANTIALIAS)
        self.resized_compare_image=ImageTk.PhotoImage(self.resized_compare_image)
        self.compare_label = tk.Label(master, image=self.resized_compare_image, bg="#006699")
        self.compare_label.image = self.resized_compare_image
        self.compare_label.place(relx=0.525, rely=0.025, relwidth=0.425, relheight=0.675)

class show_match_label:
    def __init__(self, master, matches, i):
        self.frame = Frame()
        #result label
        self.match_name = matches[i][2]
        self.match_percentage = matches[i][0]
        self.result_label_text = self.match_name + ": " + self.match_percentage + '%'
        self.result_label = tk.Label(master, text=self.result_label_text, font=("Raleway", 16), bg="#b67929", fg="white", height=3, width=16)
        self.result_label.place(relx=0.4375, rely=0.725, relwidth=0.125, relheight=0.05)

HomePage = home_page(root, "", None, None, None)
root.mainloop()