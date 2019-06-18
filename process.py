import os
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint
from timeit import default_timer as timer
import ansi
from monitor import ImageMonitor
from tools import *

# pprint(plt.rcParams, depth=2)
plt.rcParams.update({
    "font.family": "serif",
    "savefig.dpi": 150,
    "axes.grid": True,
    "grid.linestyle": ":",
    'xtick.direction': 'in',
    'xtick.top': True,
    'ytick.direction': 'in',
    'ytick.right': True
})


def drawLayerWithPerim(img, layer_gcode):
    testim = img.copy()

    for i, perim in enumerate(layer_gcode):
        layer_gcode[i] = np.float32(perim).reshape(-1, 1, 2)

    gcode_tfmatrix = cv2.getPerspectiveTransform(gcode_cal_map, target_map)

    perim_tf = cv2.perspectiveTransform(layer_gcode[0], gcode_tfmatrix)
    cv2.polylines(testim, np.int32(perim_tf.reshape(1, -1, 2)),
                  True, (0, 0, 0))  # black

    perim_tf = cv2.perspectiveTransform(layer_gcode[1], gcode_tfmatrix)
    cv2.polylines(testim, np.int32(perim_tf.reshape(1, -1, 2)),
                  True, (255, 0, 0))  # blue

    # Draw the extrusion plane
    cv2.polylines(testim, np.int32([target_map]), True, (0, 255, 0))

    # Display
    cv2.imshow("Test perimeters", testim)
    cv2waitForQ()


def imageDiffDemo(start_layer, layer_change=10):
    # image comparison
    layerA = start_layer  # start layer
    layerB = layerA-1

    # EXPERIMENTAL OVERRIDE
    # layerA = 100  # start layer
    # layerB = 20

    for i in range(5):
        imgA = fetch_image(
            "snapshots/CalibrationCube/images_warped/CalibrationCube{:06d}.jpg".format(layerA))
        imgB = fetch_image(
            "snapshots/CalibrationCube/images_warped/CalibrationCube{:06d}.jpg".format(layerB))

        # imgDiff = imgA-imgB
        imgDiff = cv2.subtract(imgA, imgB)

        print(imgDiff.dtype)

        cv2.imshow("Img diff test", imgDiff)
        cv2waitForQ()

        layerA += layer_change
        layerB = layerA-1


def thresholdContoursDemo(im):
    cv2.namedWindow('contours')
    cv2.createTrackbar("Threshold", "contours", 0, 255, lambda val: None)
    while True:
        temp_im = im.copy()
        draw_im = im.copy()
        val = cv2.getTrackbarPos("Threshold", "contours")

        imgray = cv2.cvtColor(temp_im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(
            imgray, val, 255, 0)  # (imgray, 127, 255, 0)
        cv2.imshow("Contour test", thresh)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(draw_im, contours, -1, (0, 255, 0), 3)

        cv2.imshow("contours", draw_im)
        k = cv2.waitKey(1)
        if k == 113:  # q
            return


def cannyEdgeContourDemo(im):
    cv2.namedWindow('canny')
    cv2.createTrackbar("Min", "canny", 0, 255, lambda val: None)
    cv2.createTrackbar("Max", "canny", 0, 255, lambda val: None)
    while True:
        temp_im = im.copy()
        draw_im = im.copy()
        minVal = cv2.getTrackbarPos("Min", "canny")
        maxVal = cv2.getTrackbarPos("Max", "canny")

        edges = cv2.Canny(im, minVal, maxVal)

        # imgray = cv2.cvtColor(temp_im, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(
        #     imgray, val, 255, 0)  # (imgray, 127, 255, 0)
        # cv2.imshow("Contour test", thresh)
        # contours, hierarchy = cv2.findContours(
        #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(draw_im, contours, -1, (0, 255, 0), 3)

        cv2.imshow("canny", edges)
        k = cv2.waitKey(1)
        if k == 113:  # q
            return


def rgb_region_plotting_demo(gcode):

    total_l = 133
    layer_n = 0
    avg_bgrs = {'inner': {'b': [0], 'g': [0], 'r': [0]},
                'outer': {'b': [0], 'g': [0], 'r': [0]}}

    while layer_n < total_l-1:
        layer_n += 1

        image = fetch_image(layer_n)
        im = image.copy()
        roi = gcode_layer_to_tf_perim(gcode[layer_n])

        # print(im.shape)
        # print(type(im))
        # print(im.dtype)

        mask = np.zeros(im.shape[0:2])
        cv2.fillPoly(mask, roi, 1)
        mask = mask.astype(np.bool)
        maskinv = np.invert(mask)

        inner = np.zeros_like(im)
        inner[mask] = im[mask]
        outer = np.zeros_like(im)
        outer[maskinv] = im[maskinv]
        # cv2.imshow("masked", outer)

        avb = np.average(outer[mask][:, 0])
        avg = np.average(outer[mask][:, 1])
        avr = np.average(outer[mask][:, 2])

        avg_bgrs['inner']['b'].append(np.average(im[mask][:, 0]))
        avg_bgrs['inner']['g'].append(np.average(im[mask][:, 1]))
        avg_bgrs['inner']['r'].append(np.average(im[mask][:, 2]))
        avg_bgrs['outer']['b'].append(np.average(im[maskinv][:, 0]))
        avg_bgrs['outer']['g'].append(np.average(im[maskinv][:, 1]))
        avg_bgrs['outer']['r'].append(np.average(im[maskinv][:, 2]))

    # pprint(avg_bgrs)

    # cv2waitForQ()

    fig, ax = plt.subplots(nrows=2, sharex=True)
    fig.set_size_inches(5, 8)

    # print(avg_bgrs['inner']['b'])
    ax[0].plot(avg_bgrs['inner']['b'], color='blue', marker='')
    ax[0].plot(avg_bgrs['inner']['g'], color='green', marker='')
    ax[0].plot(avg_bgrs['inner']['r'], color='red', marker='')

    ax[1].plot(avg_bgrs['outer']['b'], color='blue', marker='')
    ax[1].plot(avg_bgrs['outer']['g'], color='green', marker='')
    ax[1].plot(avg_bgrs['outer']['r'], color='red', marker='')

    ax[0].set_title("Average pixel value INSIDE perimeter")
    ax[1].set_title("Average pixel value OUTSIDE perimeter")
    ax[1].set_xlabel("Layer")
    for a in ax:
        a.set_ylabel("Average pixel value")
        a.set_ylim(0, 255)
        a.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
    # plt.legend()

    # fig, ax = plt.subplots(nrows=3, sharex=True)
    # fig.set_size_inches(5, 8)
    # ax[0].boxplot(all_ttimes, showmeans=True)
    # ax[0].set_ylabel('Travel time (mins)')
    # ax[1].boxplot(all_wtimes, showmeans=True)
    # ax[1].set_ylabel('Waiting time (mins)')
    # ax[2].boxplot(all_jtimes, showmeans=True)
    # ax[2].set_ylabel('Journey time (mins)')
    # ax[2].set_xticklabels(algs)
    # fig.savefig('output/box_plot_comparison.png')

    plt.show()

    # go to average out[mask] as this contains the part I actually want to analyse
    #

    # cv2.polylines(im, np.int32([roi]), True, (0, 255, 0))
    # cv2.imshow("im", im)


def calc_areas_demo(gcode_data):
    areas = [None]
    for n, layer in enumerate(gcode_data):
        print("Number of perimeters: {} for layer {}".format(len(layer), n))
        if len(layer) == 0:
            continue
        elif len(layer) % 2 == 0:
            # n_regions = len(layer) // 2

            outer_perim = np.array(layer[-1])
            area = poly_area(outer_perim[:, 0], outer_perim[:, 1])

            areas.append(area)
            print("{:3d} {}".format(n, area))
            # print(np.shape(outer_perim))

        elif len(layer) == 4:
            pass
        else:
            raise ValueError(
                "Cannot calculate area accurately. Layer had an unrecognised number of perimeters.")

    fig, ax = plt.subplots()
    ax.plot(areas)
    ax.set_xlabel('Layer')
    ax.set_ylabel('Area of top layer')
    ax.set_xlim(0)
    plt.show()


def bounding_rect_demo(image, layer_gcode):
    im = image.copy()
    roi = gcode_layer_to_tf_perim(layer_gcode)  # extract region of interest
    pprint(roi)
    brect = bounding_rect(roi[0])
    pprint(brect)

    # cv2.polylines(im, np.int32(perim_tf.reshape(1, -1, 2)), True, (0, 0, 0))  # black
    cv2.polylines(im, roi, True, (0, 255, 0))
    cv2.polylines(im, [brect], True, (255, 0, 0))
    cv2.polylines(im, [offset_rect(brect, percent=50)], True, (255, 255, 0))
    cv2.polylines(im, [offset_rect(brect, percent=100)], True, (100, 255, 0))
    cv2.polylines(im, [offset_rect(brect, percent=200)], True, (0, 100, 200))
    cv2.polylines(im, [np.int32(target_map)], True, (0, 255, 255))

    cv2.namedWindow('Bounding rect')
    cv2.imshow("Bounding rect", im)
    cv2waitForQ()


def advanced_rgb_region_plotting_demo(gcode, image_folder, export_data={}, save_figs=False, display_figs=False):
    total_l = 133
    layer_n = 0

    # total_l = 101
    # layer_n = 99
    avg_bgrs = {'inside perimeter': [[None, None, None]],
                'bound offset 50': [[None, None, None]],
                'bound offset 100': [[None, None, None]],
                'bound offset 200': [[None, None, None]],
                'calibration plane': [[None, None, None]],
                'whole image': [[None, None, None]]}

    while layer_n < total_l-1:
        layer_n += 1

        image = fetch_image(
            "snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(image_folder, layer_n))
        im = image.copy()
        print_region = gcode_layer_to_tf_perim(gcode[layer_n])
        brect = bounding_rect(print_region[0])

        out = extract_region(im, print_region)
        avg_bgrs['inside perimeter'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=50)
        out = extract_region(im, roi, print_region[0])
        avg_bgrs['bound offset 50'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=100)
        out = extract_region(im, roi, print_region[0])
        avg_bgrs['bound offset 100'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=200)
        out = extract_region(im, roi, print_region[0])
        avg_bgrs['bound offset 200'].append(np.average(out, axis=0))

        roi = np.int32(target_map)
        out = extract_region(im, roi, print_region[0])
        avg_bgrs['calibration plane'].append(np.average(out, axis=0))

        mask = np.zeros(im.shape[0:2])
        cv2.fillPoly(mask, print_region, 1)
        mask = mask.astype(np.bool)
        maskinv = np.invert(mask)
        avg_bgrs['whole image'].append(np.average(im[maskinv], axis=0))

        # output = np.zeros_like(im)
        # output[mask] = im[mask]
    # return
    # pprint(avg_bgrs)

    # cv2waitForQ()

    if not display_figs and not save_figs:
        fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
        for i, region_name in enumerate(avg_bgrs.keys()):
            fig.axes[i].plot(np.array(avg_bgrs[region_name])
                             [:, 0], color='blue', marker='')
            fig.axes[i].plot(np.array(avg_bgrs[region_name])[
                :, 1], color='green', marker='')
            fig.axes[i].plot(np.array(avg_bgrs[region_name])
                             [:, 2], color='red', marker='')
            fig.axes[i].set_title(region_name)

        # ax[1].set_xlabel("Layer")
        for a in fig.axes:
            a.set_ylabel("Average pixel value")
            a.set_ylim(0, 255)
            a.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
        # plt.legend()

        if save_figs:
            fig.suptitle(image_folder, fontsize=16)
            fig.savefig('{}-{}.png'.format(date(), image_folder))

        if display_figs:
            plt.show()

    export_data[image_folder] = avg_bgrs
    return export_data


def warp_images(source_map, base_path="snapshots/CalibrationCube", save_mode=False):
    img_idx = 0
    for img_idx in range(133):
        # Read source image.

        image_path = os.path.join(base_path, "images/")
        file_base = "CalibrationCube"
        filename = "{}{:06d}.jpg".format(file_base, img_idx)
        filepath = os.path.join(image_path, filename)

        im_src = fetch_image(filepath, debug=True)

        # Source and corresponding targets of four keypoints in source image
        # Starting bottom left going clockwise

        # Create a copy of source image and then mark up with map
        imsrc_mkup = im_src.copy()
        cv2.polylines(imsrc_mkup, np.int32([source_map]), True, (0, 255, 0))

        # Create the transform matrix from one domain to the perspective corrected
        transform_matrix = cv2.getPerspectiveTransform(source_map, target_map)

        # Perform the perspective warp using the transform matrix
        rows, columns, channels = im_src.shape
        im_out = cv2.warpPerspective(im_src, transform_matrix, (columns, rows))

        # Export path
        output_root = os.path.join(base_path, "images_warped/")
        output_path = os.path.join(output_root, filename)
        if not os.path.exists(output_root):
            print("Output path did not exist. Making directory now: {}".format(
                output_root))
            os.mkdir(output_root)

        if not save_mode:
            # Display images
            cv2.imshow("Source Image marked up", imsrc_mkup)
            cv2.imshow("Warped Source Image", im_out)
            cv2waitForQ()
        else:
            print("Exporting {}".format(output_path))
            # cv2.imwrite(output_name_lines, im_src)
            cv2.imwrite(output_path, im_out)


def display_advanced_data(data, title="", save_fig=False, display_fig=False):
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
    for i, region_name in enumerate(data.keys()):
        pprint(np.array(data[region_name]))
        fig.axes[i].plot(np.array(data[region_name])
                         [:, 0], color='blue', marker='')
        fig.axes[i].plot(np.array(data[region_name])[
                         :, 1], color='green', marker='')
        fig.axes[i].plot(np.array(data[region_name])
                         [:, 2], color='red', marker='')
        fig.axes[i].set_title(region_name)

    # ax[1].set_xlabel("Layer")
    for a in fig.axes:
        a.set_ylabel("Average pixel value")
        a.set_ylim(0, 255)
        a.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
    # plt.legend()

    fig.suptitle(title, fontsize=16)
    if save_fig:
        fig.savefig('{}-{}.png'.format(date(), title))
    if display_fig:
        plt.show()


def analyse_new_stacks(gcode_data):
    dirs = ["CalibrationCube2_Success",
            "CalibrationCube2_PoorStart",
            "CalibrationCube2_StopFilament",
            "CalibrationCube2_Delaminate",
            "CalibrationCube2_Removed"]

    # for folder_name in dirs:
    #     warp_images(updated_source_map, "snapshots/{}".format(folder_name), save_mode=True)
    # return

    # layer = 10
    # im = fetch_image(
    #     "snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(dirs[0], layer))
    # drawLayerWithPerim(im, gcode_data[layer])

    data = {}
    for d in dirs:
        data = advanced_rgb_region_plotting_demo(
            gcode_data, d, export_data=data)

    # pprint(data, depth=2)

    reformatted_data = {}
    for subname in data[list(data.keys())[0]].keys():
        reformatted_data[subname] = {}
        for dataset in data.keys():
            reformatted_data[subname][dataset] = data[dataset][subname]

    plt.close('all')
    for region in reformatted_data:
        display_advanced_data(
            reformatted_data[region], title=region, save_fig=True)


def evaluate_stacks(gcode_data):

    # image_folder = "CalibrationCube3-1-LayerShift"
    # layer_n = 100
    # image = fetch_image("snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(image_folder, layer_n), debug=True)
    # cv2.imshow("test", image)
    # cv2waitForQ()

    dirs = [
        "CalibrationCube3-1-LayerShift",
        "CalibrationCube3-2-Success",
        "CalibrationCube3-3-Success",
        "CalibrationCube3-4-Success",
        "CalibrationCube3-5-Success",
        "CalibrationCube3-6-Filament",
        "CalibrationCube3-7-Filament",
        "CalibrationCube3-8-Filament",
        "CalibrationCube3-9-Removed",
        "CalibrationCube3-10-Removed",
        "CalibrationCube3-11-Removed",
        "CalibrationCube3-12-Knocked",
        "CalibrationCube3-13-Knocked",
        "CalibrationCube3-14-Knocked",
    ]

    # for d in dirs:
    #     layer = 0
    #     im = fetch_image(
    #         "snapshots/{}/images/CalibrationCube000{:03d}.jpg".format(d, layer))
    #     cv2.imshow("test", im)
    #     cv2waitForQ()
    #     # drawLayerWithPerim(im, gcode_data[layer])
    # return

    # for folder_name in dirs:
    #     warp_images(updated_source_map2, "snapshots/{}".format(folder_name), save_mode=True)
    # return

    # for d in dirs:
    #     layer = 100
    #     im = fetch_image(
    #         "snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(d, layer))
    #     # cv2.imshow("test", im)
    #     # cv2waitForQ()
    #     drawLayerWithPerim(im, gcode_data[layer])
    return

    data = {}
    for d in dirs:
        data = advanced_rgb_region_plotting_demo(
            gcode_data, d, export_data=data)

    # pprint(data, depth=2)

    reformatted_data = {}
    for subname in data[list(data.keys())[0]].keys():
        reformatted_data[subname] = {}
        for dataset in data.keys():
            reformatted_data[subname][dataset] = data[dataset][subname]

    plt.close('all')
    for region in reformatted_data:
        display_advanced_data(
            reformatted_data[region], title=region, display_fig=True)


def main():

    # warp_images()

    gcode_data = get_gcode()
    # pprint(gcode_data)

    # im = fetch_image(
    #     "snapshots/CalibrationCube/images_warped/CalibrationCube000100.jpg")
    # drawLayerWithPerim(im, gcode_data[100])

    # print(len(gcode_data))
    # for i, layer in enumerate(gcode_data):
    #     print(i, len(layer))

    # imageDiffDemo(20, 10)
    # thresholdContoursDemo(im)
    # cannyEdgeContourDemo(im)
    # rgb_region_plotting_demo(gcode_data)
    # calc_areas_demo(gcode_data)
    # bounding_rect_demo(im, gcode_data[100])
    # advanced_rgb_region_plotting_demo(gcode_data)

    # analyse_new_stacks(gcode_data)  # NEW IMAGE STACKS

    dirs = ["CalibrationCube2_Success",
            "CalibrationCube2_PoorStart",
            "CalibrationCube2_StopFilament",
            "CalibrationCube2_Delaminate",
            "CalibrationCube2_Removed"]

    # for d in dirs:
    #     image_folder = d
    #     monitor = ImageMonitor(image_folder)
    #     for layer_n in range(1, 133):
    #         image = fetch_image(
    #             "snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(image_folder, layer_n), debug=True)
    #         monitor.add_image(image, layer_n, gcode_data)
    #         monitor.compute_deltas()
    #     # monitor.plot_deltas(save=False)
    #     monitor.plot_moving_average(save=True)
    #     # return

    dirs = sorted([d for d in os.listdir("./snapshots")
                   if d.startswith("CalibrationCube3")])
    pprint(dirs)
    # return

    # evaluate_stacks(gcode_data)

    for d in dirs:
        image_folder = d
        monitor = ImageMonitor(image_folder, gcode_data)
        for layer_n in range(1, 133):
            image = fetch_image(
                "snapshots/{}/images_warped/CalibrationCube000{:03d}.jpg".format(image_folder, layer_n), debug=True)
            monitor.add_image(image, layer_n)

        # monitor.plot_deltas(save=False)
        monitor.plot_moving_average(save=True)
        return


if __name__ == "__main__":
    print("Perspective Test Script")

    start = timer()
    try:
        main()
    except Exception as err:
        import traceback
        traceback.print_exc()
    elapsed = timer()-start
    print("\nTime to execute script {:.0f}:{}".format(
        elapsed//60, elapsed % 60))
