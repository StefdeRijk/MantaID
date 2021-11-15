import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile, askopenfiles, askopenfilenames
from skimage.metrics import structural_similarity
import cv2
import glob

amount_of_mantas = 3

def image_compare(file, compare_file):
    #Works well with images of different dimensions
    def orb_sim(img00, img01):
        orb = cv2.ORB_create()
        kp_a, desc_a = orb.detectAndCompute(img00, None)
        kp_b, desc_b = orb.detectAndCompute(img01, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc_a, desc_b)
        similar_regions = [i for i in matches if i.distance < 50]  
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    #Needs images to be same dimensions
    def structural_sim(img00, img01):
        sim, diff = structural_similarity(img00, img01, full=True)
        return sim

    img00 = cv2.imread(compare_file, 0)
    img01 = cv2.imread(file, 0)

    orb_similarity = orb_sim(img00, img01)

    from skimage.transform import resize
    img5 = resize(img01, (img00.shape[0], img00.shape[1]), anti_aliasing=True, preserve_range=True)

    ssim = structural_sim(img00, img5)

    return ((ssim * 2) + orb_similarity) / 3

def go_through_database(file):
    i = 0
    j = 0
    #index 0 = percentage similar, index 1 = path to file, index 2 = name of manta
    matches = [0, "", ""] * amount_of_mantas
    folder_array_results = []
    folder_array_files = []
    multiple_files = 0
    files = glob.glob("Database/*/*.jpg")
    for i in range(len(files)):
        compare_file = files[i]
        result = image_compare(file, compare_file)
        manta_name = compare_file.split("\\")[1]
        if i < len(files) - 1:
            next_name = files[i + 1].split("\\")[1]
        else :
            next_name = None
        if manta_name == next_name:
            folder_array_results.append(result)
            folder_array_files.append(compare_file)
            multiple_files += 1
        elif manta_name != next_name and multiple_files != 0:
            folder_array_results.append(result)
            max_result = max(folder_array_results)
            max_index = folder_array_results.index(max_result)
            folder_array_files.append(compare_file)
            multiple_files = 0
            while j < len(matches):
                if max_result >= matches[j]:
                    matches.insert(j, max_result)
                    j += 1
                    matches.insert(j, folder_array_files[max_index])
                    j += 1
                    matches.insert(j, manta_name)
                    j += 1
                    del matches[-3:]
                    folder_array_results = []
                    folder_array_files = []
                    break
                j += 3
            j = 0
            max_result = 0
        else :
            while j < len(matches):
                if result >= matches[j]:
                    matches.insert(j, result)
                    j += 1
                    matches.insert(j, files[i])
                    j += 1
                    matches.insert(j, manta_name)
                    j += 1
                    del matches[-3:]
                    folder_array_results = []
                    break
                j += 3
            j = 0
    i = 0
    while i < len(matches):
        matches[i] = matches[i] * 100
        if matches[i] - int(matches[i]) >= 0.5:
            matches[i] = int(matches[i] + 1)
        else :
            matches[i] = int(matches[i])
        matches[i] = str(matches[i])
        i += 3
    return matches

root = tk.Tk()
root.title("MantaID")
root.iconbitmap("icon.ico")
root.geometry("+%d+%d"%(0,0))

canvas = tk.Canvas(root, width=1920, height=1080)
canvas.grid(columnspan=5, rowspan=5)

#background image
background_image = Image.open("background.jpg")
background_image=ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#quit_button
quit_button = tk.Button(root, text="Quit", command=root.quit, font="Raleway", bg="#00243f", fg="white", height=4, width=16)
quit_button.place(relx=0.25, rely=0.8, relwidth=0.125, relheight=0.125)

def select_images(file):
    #cancel button
    cancel_button = tk.Button(root, text="Cancel", command=lambda:cancel_button_function(), font="Raleway", bg="#3c5b74", fg="white", height=3, width=16)
    cancel_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

    #process button
    params = [0, 1, 2]
    process_button = tk.Button(root, text="Process", command=lambda:process_page(file, params, [], 1), font="Raleway", bg="#264b77", fg="white", height=3, width=16)
    process_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

    def select_species():
        global species
        species = species_listbox.get(ANCHOR)
        species_select_button["state"] = DISABLED

    #species listbox
    species_listbox = tk.Listbox(root, bg="#264b77", font="Raleway", fg="white", width=10)
    species_listbox.place(relx=0.525, rely=0.05, relwidth=0.3, relheight=0.2)
    species_listbox.insert(0, "Reef manta")
    species_listbox.insert(1, "Oceanic manta")
    species_listbox.insert(2, "Unknown")
    species_select_button = tk.Button(root, text="Select", command=lambda:select_species(), font="Raleway", bg="#006699", fg="white", height=3, width=16)
    species_select_button.place(relx=0.525, rely=0.3, relwidth=0.3, relheight=0.05)

    def select_colour():
        global colour
        colour = colour_listbox.get(ANCHOR)
        colour_select_button["state"] = DISABLED

    #colour listbox
    colour_listbox = tk.Listbox(root, bg="#264b77", font="Raleway", fg="white", width=10)
    colour_listbox.place(relx=0.175, rely=0.4, relwidth=0.3, relheight=0.2)
    colour_listbox.insert(0, "Black")
    colour_listbox.insert(1, "White")
    colour_listbox.insert(2, "Unknown")
    colour_select_button = tk.Button(root, text="Select", command=lambda:select_colour(), font="Raleway", bg="#006699", fg="white", height=3, width=16)
    colour_select_button.place(relx=0.175, rely=0.65, relwidth=0.3, relheight=0.05)

    def select_gender():
        global gender
        gender = gender_listbox.get(ANCHOR)
        gender_select_button["state"] = DISABLED

    #gender listbox
    gender_listbox = tk.Listbox(root, bg="#264b77", font="Raleway", fg="white", width=10)
    gender_listbox.place(relx=0.525, rely=0.4, relwidth=0.3, relheight=0.2)
    gender_listbox.insert(0, "Male")
    gender_listbox.insert(1, "Female")
    gender_listbox.insert(2, "Unknown")
    gender_select_button = tk.Button(root, text="Select", command=lambda:select_gender(), font="Raleway", bg="#006699", fg="white", height=3, width=16)
    gender_select_button.place(relx=0.525, rely=0.65, relwidth=0.3, relheight=0.05)

    #reference image
    reference_image = Image.open(file)
    reference_image=ImageTk.PhotoImage(reference_image)
    height = reference_image.height()
    width = reference_image.width()
    aspect_ratio = width / height
    new_width = int(324 * aspect_ratio)
    new_reference_image = Image.open(file)
    resized_reference_image = new_reference_image.resize((new_width,324), Image.ANTIALIAS)
    resized_reference_image=ImageTk.PhotoImage(resized_reference_image)
    reference_small_label = tk.Label(root, image=resized_reference_image, bg="#264b77")
    reference_small_label.image = resized_reference_image
    reference_small_label.place(relx=0.175, rely=0.05, relwidth=0.3, relheight=0.3)

    def process_page(file, params, matches, get_data):
        cancel_button.destroy()
        process_button.destroy()
        gender_select_button.destroy()
        gender_listbox.destroy()
        species_select_button.destroy()
        species_listbox.destroy()
        colour_select_button.destroy()
        colour_listbox.destroy()
        reference_small_label.destroy()

        print(species, colour, gender)

        #save button
        save_button = tk.Button(root, text="Save image", command=lambda:save_button_function(), font="Raleway", bg="#3c5b74", fg="white", height=3, width=16)
        save_button.place(relx=0.4375, rely=0.8, relwidth=0.125, relheight=0.125)

        #retry button
        retry_button = tk.Button(root, text="Use different image", command=lambda:retry_button_function(), font="Raleway", bg="#264b77", fg="white", height=3, width=16)
        retry_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

        #previous button
        previous_button = tk.Button(root, text="Previous", command=lambda:previous_button_function(file, params, matches), font="Raleway", bg="#686873", fg="white", height=3, width=16)
        previous_button.place(relx=0.25, rely=0.725, relwidth=0.125, relheight=0.05)
        if params[0] == 0:
            previous_button["state"] = DISABLED
        else :
            previous_button["state"] = NORMAL

        #next button
        next_button = tk.Button(root, text="Next", command=lambda:next_button_function(file, params, matches), font="Raleway", bg="#686873", fg="white", height=3, width=16)
        next_button.place(relx=0.625, rely=0.725, relwidth=0.125, relheight=0.05)
        if params[0] == (amount_of_mantas - 1) * 3:
            next_button["state"] = DISABLED
        else :
            next_button["state"] = NORMAL

        #reference image
        reference_image = Image.open(file)
        reference_image=ImageTk.PhotoImage(reference_image)
        height = reference_image.height()
        width = reference_image.width()
        aspect_ratio = width / height
        new_width = int(729 * aspect_ratio)
        new_reference_image = Image.open(file)
        resized_reference_image = new_reference_image.resize((new_width,729), Image.ANTIALIAS)
        resized_reference_image=ImageTk.PhotoImage(resized_reference_image)
        reference_label = tk.Label(root, image=resized_reference_image, bg="#006699")
        reference_label.image = resized_reference_image
        reference_label.place(relx=0.05, rely=0.025, relwidth=0.425, relheight=0.675)

        if get_data == 1:
            matches = go_through_database(file)

        def next_button_function(file, params, matches):
            retry_button.destroy()
            result_label.destroy()
            next_button.destroy()
            previous_button.destroy()
            reference_label.destroy()
            compare_label.destroy()
            save_button.destroy()
            params[0] += 3
            params[1] += 3
            params[2] += 3
            process_page(file, params, matches, 0)

        def previous_button_function(file, params, matches):
            retry_button.destroy()
            result_label.destroy()
            next_button.destroy()
            previous_button.destroy()
            reference_label.destroy()
            compare_label.destroy()
            save_button.destroy()
            params[0] -= 3
            params[1] -= 3
            params[2] -= 3
            process_page(file, params, matches, 0)

        compare_image = Image.open(matches[params[1]])
        compare_image = ImageTk.PhotoImage(compare_image)
        height = compare_image.height()
        width = compare_image.width()
        aspect_ratio = width / height
        new_width = int(729 * aspect_ratio)
        new_compare_image = Image.open(matches[params[1]])
        resized_compare_image = new_compare_image.resize((new_width,729), Image.ANTIALIAS)
        resized_compare_image=ImageTk.PhotoImage(resized_compare_image)
        compare_label = tk.Label(root, image=resized_compare_image, bg="#006699")
        compare_label.image = resized_compare_image
        compare_label.place(relx=0.525, rely=0.025, relwidth=0.425, relheight=0.675)

        #result label
        match_name = matches[params[2]]
        match_percentage = matches[params[0]]
        result_label_text = match_name + ": " + match_percentage + '%'
        result_label = tk.Label(root, text=result_label_text, font="Raleway", bg="#b67929", fg="white", height=3, width=16)
        result_label.place(relx=0.4375, rely=0.725, relwidth=0.125, relheight=0.05)

        def retry_button_function():
            retry_button.destroy()
            result_label.destroy()
            next_button.destroy()
            previous_button.destroy()
            reference_label.destroy()
            compare_label.destroy()
            save_button.destroy()
            home()

    def cancel_button_function():
        cancel_button.destroy()
        home()

def home():
    #open images
    open_button_text = tk.StringVar()
    open_button = tk.Button(root, textvariable=open_button_text, command=lambda:open_files(), font="Raleway", bg="#264b77", fg="white", height=4, width=16)
    open_button_text.set("Open image")
    open_button.place(relx=0.625, rely=0.8, relwidth=0.125, relheight=0.125)

    def open_files():
        open_button_text.set("Loading...")
        files = askopenfile(parent=root, mode="rb", title="Choose files", filetypes=[("Images", "*.png; *.jpg")])
        if files:
            file = files.name
            open_button.destroy()
            select_images(file)
        else :
            home()

home()
root.mainloop()
