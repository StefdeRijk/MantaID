import cv2
from cv2 import BRISK
from numpy import mat

def image_compare(file, compare_file):
    #Works well with images of different dimensions
    # def orb_sim(img00, img01):
    #     orb = cv2.ORB_create()
    #     kp_a, desc_a = orb.detectAndCompute(img00, None)
    #     kp_b, desc_b = orb.detectAndCompute(img01, None)
    #     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #     matches = bf.match(desc_a, desc_b)
    #     similar_regions = [i for i in matches if i.distance < 65]  
    #     if len(matches) == 0:
    #         return 0
    #     return len(similar_regions) / len(matches)

    file_gray = cv2.imread(file, flags = cv2.IMREAD_GRAYSCALE)
    compare_file_gray = cv2.imread(compare_file, flags = cv2.IMREAD_GRAYSCALE)

    # orb_similarity = orb_sim(img00, img01)

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
        sum_distance = 1
    sum_distance /= 1000
    sum_distance = 1 / sum_distance * (1 / len(matches))
    print(sum_distance)
    return sum_distance
