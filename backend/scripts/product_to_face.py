import cv2
import numpy as np
import os
import os.path as osp
import shutil
from imutils import paths
from mlanomaly.postprocessing.visualize import visualize

if __name__ == '__main__':

    # img_dir = osp.join("images", "left")
    #
    # img_paths = list(paths.list_images(img_dir))
    # for img_path in img_paths:
    #
    #     id = img_path.split(osp.sep)[-2]
    #     if id.startswith("ann"): continue
    #
    #     face, ext = osp.splitext(osp.basename(img_path))
    #
    #     # Create output path
    #     output_path = osp.join(img_dir, f"face{face}", "normal", f"{id}{ext}")
    #     os.makedirs(osp.dirname(output_path), exist_ok=True)
    #     print(img_path, output_path)
    #
    #     shutil.copy(img_path, output_path)


    img_path = osp.join("app", "static", "raw", "demo3.jpeg")
    mask_path = osp.join("app", "static", "prediction", "demo2.jpg")
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path, 0)


    mask = np.zeros(img.shape[:2])

    prediction = visualize(img, mask=mask)
    output_path = osp.join("app", "static", "prediction", "demo3.jpeg")
    cv2.imwrite(output_path, prediction)

    cv2.imshow("img", prediction)
    cv2.waitKey(0)
