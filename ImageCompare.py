import cv2
def image_compare(descriptors_file, compare_file):
    new_compare_file = cv2.imread(compare_file)

    sift = cv2.xfeatures2d.SIFT_create()
    keypoints_compare_file, descriptors_compare_file = sift.detectAndCompute(new_compare_file, None)

    brute_force = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = brute_force.match(descriptors_file, descriptors_compare_file)

    matches = sorted(matches, key = lambda x: x.distance)
    return matches[0].distance
