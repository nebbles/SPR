import numpy as np
import cv2
from datetime import datetime

source_map = np.float32([[378, 503],
                         [472, 193],
                         [916, 196],
                         [1056, 508]])
target_map = np.float32([[400, 650],
                         [400, 150],
                         [900, 150],
                         [900, 650]])
gcode_cal_map_centre = np.float32([[99, 155],
                                   [149, 155],
                                   [149, 55],
                                   [99, 55]])  # centre square
gcode_cal_map = np.float32([[99, 155],
                            [199, 155],
                            [199, 55],
                            [99, 55]])

updated_source_map = np.float32([[364, 520],
                                 [464, 205],
                                 [913, 208],
                                 [1059, 524]])
updated_source_map2 = np.float32([[362, 523],
                                  [465, 209],
                                  [912, 213],
                                  [1056, 531]])


def fetch_image(img_path, debug=True):
    if (type(img_path) is int) and (img_path >= 0):
        img_path = "snapshots/CalibrationCube/images_warped/CalibrationCube{:06d}.jpg".format(
            img_path)
        if debug:
            print("Fetching (with int) {}".format(img_path))
        return cv2.imread(img_path)

    if (type(img_path) is str):
        if debug:
            print("Fetching {}".format(img_path))
        return cv2.imread(img_path)

    print("Error must define an image path or layer number")
    return None

    # img_path = "perspective_trial/CalibrationCube000000.jpg"
    # img_path = "perspective_trial/CalibrationCube000001.jpg"
    # img_path = "perspective_trial/CalibrationCube000066.jpg"

    # output_name_lines = "perspective_trial/EmpyBed.jpg"
    # output_name_lines = "perspective_trial/MidLayer.jpg"

    # output_name = "perspective_trial/EmpyBedWarped.jpg"
    # output_name = "perspective_trial/FirstLayerWarped.jpg"
    # output_name = "perspective_trial/MidLayerWarped.jpg"


def warp_image(im_src, source_map, save_mode=False):
    # Source and corresponding targets of four keypoints in source image
    # Starting bottom left going clockwise

    # Create a copy of source image and then mark up with map
    # imsrc_mkup = im_src.copy()
    # cv2.polylines(imsrc_mkup, np.int32([source_map]), True, (0, 255, 0))

    # Create the transform matrix from one domain to the perspective corrected
    transform_matrix = cv2.getPerspectiveTransform(source_map, target_map)

    # Perform the perspective warp using the transform matrix
    rows, columns, channels = im_src.shape
    im_out = cv2.warpPerspective(im_src, transform_matrix, (columns, rows))

    return im_out

    # # Export path
    # output_root = os.path.join(base_path, "images_warped/")
    # output_path = os.path.join(output_root, filename)
    # if not os.path.exists(output_root):
    #     print("Output path did not exist. Making directory now: {}".format(
    #         output_root))
    #     os.mkdir(output_root)

    # if not save_mode:
    #     # Display images
    #     cv2.imshow("Source Image marked up", imsrc_mkup)
    #     cv2.imshow("Warped Source Image", im_out)
    #     cv2waitForQ()
    # else:
    #     print("Exporting {}".format(output_path))
    #     # cv2.imwrite(output_name_lines, im_src)
    #     cv2.imwrite(output_path, im_out)


def date():
    return datetime.today().strftime('%Y%m%d')


def poly_area(x, y):
    # x = None
    # y = None
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))


def nmap(x, in_min, in_max, out_min=0.0, out_max=1.0):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def gc_extract_coordinates(gcode_line):
    line = gcode_line.split(' ')
    coords = [None, None]
    for term in line:
        if term[0] == 'X':
            coords[0] = float(term[1:])
        if term[0] == 'Y':
            coords[1] = float(term[1:])

    # print(line)
    return coords


def gcode_layer_to_tf_perim(layer_gcode):
    perim_gcode = np.float32(layer_gcode[-1]).reshape(-1, 1, 2)
    gcode_tfmatrix = cv2.getPerspectiveTransform(gcode_cal_map, target_map)
    perim_tf = cv2.perspectiveTransform(perim_gcode, gcode_tfmatrix)
    return np.int32(perim_tf.reshape(1, -1, 2))


def get_gcode():
    gcode = []
    with open("snapshots/CalibrationCubeVerbose.gcode", 'r') as f:
        gcode = f.read().splitlines()

    processed_gcode = []  # empty list for each z layer
    layer_gcode = []
    perim_gcode = []
    layer = 0
    flag = 0
    for i, line in enumerate(gcode):
        if line == ";AFTER_LAYER_CHANGE":

            if len(perim_gcode) > 0:
                layer_gcode.append(perim_gcode)
                perim_gcode = []
            processed_gcode.append(layer_gcode)
            layer_gcode = []

            nextline = gcode[i+1]

            zheight = float(nextline[1:])
            layer = int(round((zheight-0.2)/0.15)+1)
            print("{:>5}  {:<8} {}  processing...".format(i, line, layer))

            if len(processed_gcode) != layer:
                print("ERROR!")
                return

        if len(line) > 0 and line[0] != ';':
            if "; move to first perimeter point" in line:
                if len(perim_gcode) > 0:
                    layer_gcode.append(perim_gcode)
                    perim_gcode = []
                perim_gcode.append(gc_extract_coordinates(line))
            if "; perimeter" in line:
                perim_gcode.append(gc_extract_coordinates(line))

        # if flag > 0:
        #     # print(i, line)
        #     flag -= 1

    # don't forget last perimeter segment!
    layer_gcode.append(perim_gcode)
    processed_gcode.append(layer_gcode)

    # for layer, perimeters in enumerate(processed_gcode):
    #     print("\nLayer {}".format(layer))
    #     for perim in perimeters:
    #         pprint(perim)

    return processed_gcode


def bounding_rect(poly):
    max_x = max(poly[:, 0])
    min_x = min(poly[:, 0])
    max_y = max(poly[:, 1])
    min_y = min(poly[:, 1])
    # print("max x {}".format(max_x))
    return np.array([[min_x, min_y],
                     [min_x, max_y],
                     [max_x, max_y],
                     [max_x, min_y]], dtype=np.int32)


def offset_rect(rect, percent):
    max_x = max(rect[:, 0])
    min_x = min(rect[:, 0])
    max_y = max(rect[:, 1])
    min_y = min(rect[:, 1])
    width = abs(max(rect[:, 0])-min(rect[:, 0]))
    height = abs(max(rect[:, 1])-min(rect[:, 1]))
    x_delta = abs(width*percent/100)
    y_delta = abs(height*percent/100)
    return np.array([[min_x-x_delta, min_y-y_delta],
                     [min_x-x_delta, max_y+y_delta],
                     [max_x+x_delta, max_y+y_delta],
                     [max_x+x_delta, min_y-y_delta]], dtype=np.int32)


def extract_region(im, roi, subtract_region=None):
    mask = np.zeros(im.shape[0:2])
    cv2.fillPoly(mask, [roi], 1)
    mask = mask.astype(np.bool)

    if subtract_region is not None:
        submask = np.zeros(im.shape[0:2])
        cv2.fillPoly(submask, [subtract_region], 1)
        submask = submask.astype(np.bool)

        mask = np.clip(mask.astype(np.float32) -
                       submask.astype(np.float32), 0, 1).astype(np.bool)

    return im[mask]


def cv2waitForQ():
    try:
        while True:
            k = cv2.waitKey(0)
            print("Key pressed:", k)
            if k == 113:
                break
            if k == 101:
                print("Forcing exit of program...")
                os._exit(0)
    except KeyboardInterrupt:
        print("\nInterrupted with Ctrl+C...")
        print("Forcing exit of program...")
        os._exit(0)
