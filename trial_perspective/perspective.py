import cv2
import numpy as np

if __name__ == "__main__":
    print("Perspective Test Script")

    # Read source image.

    # img_path = "perspective_trial/CalibrationCube000000.jpg"
    # img_path = "perspective_trial/CalibrationCube000001.jpg"
    img_path = "perspective_trial/CalibrationCube000066.jpg"

    # output_name_lines = "perspective_trial/EmpyBed.jpg"
    output_name_lines = "perspective_trial/MidLayer.jpg"

    # output_name = "perspective_trial/EmpyBedWarped.jpg"
    # output_name = "perspective_trial/FirstLayerWarped.jpg"
    output_name = "perspective_trial/MidLayerWarped.jpg"

    im_src = cv2.imread(img_path)

    rows, columns, channels = im_src.shape

    # Four corners of the book in source image
    pts_src = np.float32([[378, 504],
                          [474, 194],
                          [918, 196],
                          [1057, 511]])
    # cv2.rectangle(im_src, pts_src)

    print(pts_src)
    cv2.polylines(im_src, np.int32([pts_src]), True, (0, 255, 0))

    pts_dst = np.float32([[400, 650],
                          [400, 150],
                          [900, 150],
                          [900, 650]])

    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    im_out = cv2.warpPerspective(im_src, matrix, (columns, rows))

    # # Display images
    cv2.imshow("Source Image", im_src)
    cv2.imshow("Warped Source Image", im_out)

    
    cv2.imwrite(output_name_lines, im_src)
    cv2.imwrite(output_name, im_out)

    cv2.waitKey(0)
