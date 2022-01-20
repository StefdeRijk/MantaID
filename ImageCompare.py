from skimage.metrics import structural_similarity
import cv2

def image_compare(file, compare_file):
    #Works well with images of different dimensions
    def orb_sim(img00, img01):
        orb = cv2.ORB_create()
        kp_a, desc_a = orb.detectAndCompute(img00, None)
        kp_b, desc_b = orb.detectAndCompute(img01, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc_a, desc_b)
        similar_regions = [i for i in matches if i.distance < 65]  
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    # #Needs images to be same dimensions
    # def structural_sim(img00, img01):
    #     sim, diff = structural_similarity(img00, img01, full=True)
    #     return sim

    img00 = cv2.imread(compare_file, 0)
    img01 = cv2.imread(file, 0)

    orb_similarity = orb_sim(img00, img01)

    # from skimage.transform import resize
    # img5 = resize(img01, (img00.shape[0], img00.shape[1]), anti_aliasing=True, preserve_range=True)

    # ssim = structural_sim(img00, img5)

    return orb_similarity # ((ssim * 2) + orb_similarity) / 3
