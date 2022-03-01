import cv2

def image_compare(file, compare_file):
    file_gray = cv2.imread(file, flags = cv2.IMREAD_GRAYSCALE)
    compare_file_gray = cv2.imread(compare_file, flags = cv2.IMREAD_GRAYSCALE)

    brisk = cv2.BRISK_create()
    keypoints_file, descriptors_file = brisk.detectAndCompute(file_gray, None)
    keypoints_compare_file, descriptors_compare_file = brisk.detectAndCompute(compare_file_gray, None)
    

    brute_force = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = brute_force.match(descriptors_file, descriptors_compare_file)
    matches = sorted(matches, key = lambda x: x.distance)
    sum_distance = 0
    for i in range(len(matches)):
        if (i == 15):
            break
        sum_distance += matches[i].distance
    if sum_distance == 0:
        sum_distance = 0.1
    sum_distance = 1 / sum_distance
    return sum_distance
