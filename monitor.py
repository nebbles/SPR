import numpy as np
import matplotlib.pyplot as plt
from ansi import ansi
from pprint import pprint
from tools import *

class ImageMonitor:
    def __init__(self, stack_name, gcode):
        self.name = stack_name
        self.gcode = gcode
        self.delta_threshold = 10
        self.window_size = 5
        self.delta_drop_threshold = 20
        self.history_avgs = {'inside perimeter': [[None, None, None]],
                             'bound offset 50': [[None, None, None]],
                             'bound offset 100': [[None, None, None]],
                             'bound offset 200': [[None, None, None]],
                             'calibration plane': [[None, None, None]],
                             'whole image': [[None, None, None]]}
        self.history_deltas = {'inside perimeter': [[None, None, None], [None, None, None]],
                               'bound offset 50': [[None, None, None], [None, None, None]],
                               'bound offset 100': [[None, None, None], [None, None, None]],
                               'bound offset 200': [[None, None, None], [None, None, None]],
                               'calibration plane': [[None, None, None], [None, None, None]],
                               'whole image': [[None, None, None], [None, None, None]]}
        self.first_image = True
        self.layer_n = None
        self.layer_flags = {
            'standard': {'inside perimeter': [],
                         'bound offset 50': [],
                         'bound offset 100': [],
                         'bound offset 200': [],
                         'calibration plane': [],
                         'whole image': []},
            'moving average': {'inside perimeter': [],
                               'bound offset 50': [],
                               'bound offset 100': [],
                               'bound offset 200': [],
                               'calibration plane': [],
                               'whole image': []},
            'material flow': {'inside perimeter': [],
                              'bound offset 50': [],
                              'bound offset 100': [],
                              'bound offset 200': [],
                              'calibration plane': [],
                              'whole image': []}
        }

        self.moving_average = {'inside perimeter': [[None, None, None]],
                               'bound offset 50': [[None, None, None]],
                               'bound offset 100': [[None, None, None]],
                               'bound offset 200': [[None, None, None]],
                               'calibration plane': [[None, None, None]],
                               'whole image': [[None, None, None]]}
        self.mov_av_deltas = {'inside perimeter': [[None, None, None], [None, None, None]],
                              'bound offset 50': [[None, None, None], [None, None, None]],
                              'bound offset 100': [[None, None, None], [None, None, None]],
                              'bound offset 200': [[None, None, None], [None, None, None]],
                              'calibration plane': [[None, None, None], [None, None, None]],
                              'whole image': [[None, None, None], [None, None, None]]}

    def run_detector(self):
        # try:

        # FOR GENERAL CHANNEL AVERAGES
        if len(self.history_avgs['inside perimeter']) > 2:
            for region_name in self.history_deltas:
                current_frame = self.history_avgs[region_name][-1]
                previous_frame = self.history_avgs[region_name][-2]
                delta = [i-j for i, j in zip(current_frame, previous_frame)]
                self.history_deltas[region_name].append(delta)

        for region_name in self.history_deltas:
            for colour_delta in self.history_deltas[region_name][-1]:
                if colour_delta != None and abs(colour_delta) > self.delta_threshold:
                    self.layer_flags['standard'][region_name].append(
                        self.layer_n)

        # FOR MOVING AVERAGE WINDOW
        if len(self.moving_average['inside perimeter']) > 2:
            for region_name in self.mov_av_deltas:
                current_frame = self.moving_average[region_name][-1]
                previous_frame = self.moving_average[region_name][-2]
                delta = [i-j for i, j in zip(current_frame, previous_frame)]
                self.mov_av_deltas[region_name].append(delta)

        for region_name in self.mov_av_deltas:
            for colour_delta in self.mov_av_deltas[region_name][-1]:
                if colour_delta != None and abs(colour_delta) > self.delta_threshold:
                    self.layer_flags['moving average'][region_name].append(
                        self.layer_n)

        # DETECTING A RUN OUT OF FILAMENT
        print("mov av last:", self.mov_av_deltas['inside perimeter'][-1][2])
        negative_streak = True
        for av in self.mov_av_deltas['inside perimeter'][-self.delta_drop_threshold:]:
            if av[2] is None:
                negative_streak = False
                break
            if av[2] >= 0:
                negative_streak = False
                break
        if negative_streak == True:
            ansi.ansi.printwarning("10 negative deltas in row")
            self.layer_flags['material flow']['inside perimeter'].append(
                self.layer_n)

    def update_moving_average(self):
        for region_name in self.history_avgs:
            window = self.history_avgs[region_name][-self.window_size:]
            window = np.array(window, dtype=np.float)
            av = np.average(window, axis=0)
            # print(region_name, av)
            self.moving_average[region_name].append(av)

    def add_image(self, image, layer_n):
        self.layer_n = layer_n
        im = image.copy()
        print_region = gcode_layer_to_tf_perim(self.gcode[layer_n])
        brect = bounding_rect(print_region[0])

        out = extract_region(im, print_region)
        self.history_avgs['inside perimeter'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=50)
        out = extract_region(im, roi, print_region[0])
        self.history_avgs['bound offset 50'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=100)
        out = extract_region(im, roi, print_region[0])
        self.history_avgs['bound offset 100'].append(np.average(out, axis=0))

        roi = offset_rect(brect, percent=200)
        out = extract_region(im, roi, print_region[0])
        self.history_avgs['bound offset 200'].append(np.average(out, axis=0))

        roi = np.int32(target_map)
        out = extract_region(im, roi, print_region[0])
        self.history_avgs['calibration plane'].append(np.average(out, axis=0))

        mask = np.zeros(im.shape[0:2])
        cv2.fillPoly(mask, print_region, 1)
        mask = mask.astype(np.bool)
        maskinv = np.invert(mask)
        self.history_avgs['whole image'].append(
            np.average(im[maskinv], axis=0))

        if not self.first_image:
            pass
        self.update_moving_average()
        self.first_image = False

        self.run_detector()

    def check_for_flags(self):
        n_flags = len(self.layer_flags['moving average']['inside perimeter'])
        print("Number of flags: ", n_flags)
        return n_flags > 0

    def plot_deltas(self, display=False, save=False):
        n_regions = len(self.history_deltas)
        fig, ax = plt.subplots(nrows=n_regions, sharex=True, figsize=(15, 6))
        for i, region_name in enumerate(self.history_deltas):
            deltas = np.array(self.history_deltas[region_name])
            fig.axes[i].plot(deltas[:, 0], color='blue', marker='')
            fig.axes[i].plot(deltas[:, 1], color='green', marker='')
            fig.axes[i].plot(deltas[:, 2], color='red', marker='')
            fig.axes[i].set_ylabel(
                region_name, rotation='horizontal', ha='right')
            for x in self.layer_flags[region_name]:
                fig.axes[i].axvline(x, ls=':', color='y')

        fig.suptitle(self.name)
        if save:
            fig.savefig('{}-{}.png'.format(date(), self.name))
        if display:
            plt.show()
        plt.close('all')

    def plot_moving_average(self, display=False, save=False):
        n_regions = len(self.moving_average)
        fig, ax = plt.subplots(ncols=2, nrows=n_regions,
                            sharex=True, figsize=(15, 6))
        for i, region_name in enumerate(self.moving_average):
            savg = np.array(self.history_avgs[region_name])
            mavg = np.array(self.moving_average[region_name])

            ax[i, 0].plot(savg[:, 0], color='blue', marker='')
            ax[i, 0].plot(savg[:, 1], color='green', marker='')
            ax[i, 0].plot(savg[:, 2], color='red', marker='')

            ax[i, 1].plot(mavg[:, 0], color='blue', marker='')
            ax[i, 1].plot(mavg[:, 1], color='green', marker='')
            ax[i, 1].plot(mavg[:, 2], color='red', marker='')

            ax[i, 0].set_ylabel(
                region_name, rotation='horizontal', ha='right')
            pprint(self.layer_flags)
            for x in self.layer_flags['standard'][region_name]:
                ax[i, 0].axvline(x, ls=':', color='y')
            for x in self.layer_flags['moving average'][region_name]:
                ax[i, 1].axvline(x, ls=':', color='y')
            for x in self.layer_flags['material flow'][region_name]:
                ax[i, 1].axvline(x, ls=':', color='r')

        ax[0, 0].set_title(
            "Raw avg BGR values\n(theshold={})".format(self.delta_threshold))
        ax[0, 1].set_title(
            "Filtered avg BGR values\n(threshold={}; window size={}; drop threshold={})".format(self.delta_threshold, self.window_size, self.delta_drop_threshold))

        fig.suptitle(self.name)
        if save:
            fig.savefig('{}-{}.png'.format(date(), self.name))
        if display:
            plt.show()
        plt.close('all')
