import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from IterateDatabase import go_through_database
import shutil

amount_of_mantas = 3
database_folder = "Database"


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

def settings_button_function(master, page, file):
    SettingsPage = settings_page(master, page, file)
    show_page(SettingsPage.frame)

def show_page(page):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)


class settings_page:
    def __init__(self, master, previous_page, file):
        global database_folder
        self.frame = Frame()
        show_background()

        back_button = tk.Button(master, text="Back", command=lambda:back_button_function(previous_page, master, file), font=("Raleway", 16), bg="#3c5b74", fg="white")
        back_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def back_button_function(previous_page, master, file):
            PreviousPage = previous_page(master, file)
            show_page(PreviousPage.frame)

        set_matches_button = tk.Button(master, text="Set amount of matches", command=lambda:set_matches_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        set_matches_button.place(relx=0.75, rely=0.1, relwidth=0.125, relheight=0.125)
        set_matches_label = tk.Label(master, text="Current amount of matches: " + str(amount_of_mantas), font=("Raleway", 16), bg="#3c5b74", fg="white")
        set_matches_label.place(relx=0.125, rely=0.1, relwidth=0.6, relheight=0.125)

        def set_matches_button_function():
            global amount_of_mantas
            amount_of_mantas = 2

        set_database_button = tk.Button(master, text="Set database folder", command=lambda:set_database_button_function(), font=("Raleway", 16), bg="#264b77", fg="white")
        set_database_button.place(relx=0.75, rely=0.25, relwidth=0.125, relheight=0.125)
        set_database_label = tk.Label(master, text="Current database folder: " + database_folder, font=("Raleway", 16), bg="#3c5b74", fg="white")
        set_database_label.place(relx=0.125, rely=0.25, relwidth=0.6, relheight=0.125)

class home_page:
    def __init__(self, master, file):
        self.frame = Frame()
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, home_page, None), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
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
                SelectionPage = selection_page(master, file)
                show_page(SelectionPage.frame)
            else :
                home_page(root)

class selection_page:
    def __init__(self, master, file):
        self.frame = Frame()
        self.attributes_number = 0
        self.attributes = [None] * 3 # species - colour - gender
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, selection_page, file), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        settings_button.place(relx=0.125, rely=0.825, relwidth=0.075, relheight=0.075)

        #cancel button
        self.cancel_button = tk.Button(master, text="Cancel", command=lambda:cancel_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=3, width=16)
        self.cancel_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        def cancel_button_function():
            HomePage = home_page(master, file)
            show_page(HomePage.frame)

        #process button
        self.process_button = tk.Button(master, text="Process", command=lambda:process_button_function(), font=("Raleway", 16), bg="#264b77", fg="white", height=3, width=16)
        self.process_button["state"] = "disabled"
        self.process_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        def process_button_function():
            ProcessPage = process_page(master, file)
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
    def __init__(self, master, file):
        global amount_of_mantas
        self.frame = Frame()
        self.matches = go_through_database(file, amount_of_mantas, database_folder)
        self.match_index = 0
        self.number_of_mantas = amount_of_mantas
        show_background()

        #settings_button
        settings_button = tk.Button(master, text="Settings", command=lambda:settings_button_function(master, process_page, file), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
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
            HomePage = home_page(master, file)
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
        new_button = tk.Button(master, text="New manta", command=lambda:new_button_function(), font=("Raleway", 16), bg="#3c5b74", fg="white", height=4, width=16)
        new_button.place(relx=0.8, rely=0.825, relwidth=0.075, relheight=0.075)

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

HomePage = home_page(root, None)
root.mainloop()