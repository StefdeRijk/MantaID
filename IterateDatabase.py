from ImageCompare import image_compare
import glob

def go_through_database(file, amount_of_mantas, database_folder):
    #index 0 = percentage similar, index 1 = path to file, index 2 = name of manta
    matches = []
    for i in range(amount_of_mantas):
        temp = [0, "", ""]
        matches.append(temp)
    current_folder_results = []
    current_folder_files = []
    files = glob.glob(database_folder + "/*/*.jpg")
    for i in range(len(files)):
        current_file = files[i]
        current_result = image_compare(file, current_file)
        current_manta_name = current_file.split("\\")[-2]
        if i < len(files) - 1:
            next_manta_name = files[i + 1].split("\\")[-2]
        else :
            next_manta_name = None
        if current_manta_name == next_manta_name:
            current_folder_results.append(current_result)
            current_folder_files.append(current_file)
        else :
            current_folder_results.append(current_result)
            current_folder_files.append(current_file)
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
    for i in range(0, len(matches)):
        matches[i][0] = matches[i][0] * 100
        matches[i][0] = int(matches[i][0] + 0.5)
        matches[i][0] = str(matches[i][0])
    return matches