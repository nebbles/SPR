import time
import os
from octorest import OctoRest
from pprint import pprint
from ansi import ansi
from tools import *
from monitor import ImageMonitor

def get_snapshots_dir():
    """
    Finds the active snapshot directory for the most recent (current) print.

    The images are always stored in /home/pi/.octoprint/data/octolapse/snapshots/{generated_folder}/354def78-9eea-409a-ad23-ee966dfff4ba/{filename}
    """
    path_snapshots = "/home/pi/.octoprint/data/octolapse/snapshots/"

    if not os.path.exists("/home/pi"):
        path_snapshots = "test_env_live_demo/"  # DEBUGGING PURPOSES ON LOCAL MACHINE

    print(os.path.exists("/Volumes/Local SPR Pi/.octoprint"))
    path_snapshots = "/Volumes/Local SPR Pi/.octoprint/data/octolapse/snapshots/"

    path_snapshots = "live_snapshots_env/snapshots/"  # DEBUGGING PURPOSES ON LOCAL MACHINE

    # os._exit(0)

    print("Checking the octolapse snapshots data directory...")
    if os.path.exists(path_snapshots):
        ansi.printok("Snapshots directory found.")
    else:
        raise NotADirectoryError("The snapshots directory does not exist.")

    print("Retreiving folders from octolapse directory...")
    # snapshot_subdirs = [x[0] for x in os.walk(path_snapshots)][1:]
    for r, ds, fs in os.walk(path_snapshots):
        snapshot_subdirs = [os.path.join(r, d) for d in ds]
        break
    
    subdirs_ordered = sorted(snapshot_subdirs, key=os.path.getctime)
    if len(subdirs_ordered) == 0:
        raise IndexError("There are no subdirectories in the expected folder.")
    # print("Newest directory is last:", subdirs_ordered)
    # print(subdirs_ordered)

    active_dir = subdirs_ordered[-1]
    ansi.printok("The newest dir is: {}".format(active_dir))
    elapsed_time = time.time() - os.path.getctime(active_dir)
    ansi.printok("The folder was created {:.0f} seconds ago".format(elapsed_time))
    
    # Append correct subfolder to dir
    active_dir = os.path.join(
        subdirs_ordered[-1], "354def78-9eea-409a-ad23-ee966dfff4ba/")
    return active_dir, elapsed_time


def check_snapshots_dir(active_dir):
    print("Checking the status of the active snapshot directory:", active_dir)
    files = []
    for root, d, f in os.walk(active_dir):
        for filename in f:
            # print(filename)
            if filename.endswith(".jpg"):
                files.append(os.path.join(root, filename))
        # files.extend(f)
        break  # only look at top level

    files = sorted(files, key=os.path.getctime)
    # print("Contents of active directory (in order of modified time) are:")
    # pprint(files)

    count = len(files)
    ansi.printok("Current number of .jpg files: {}".format(count))
    if count == 0:
        most_recent = None
        ansi.printwarning("There are no .jpg files available yet.")
    else:
        most_recent = files[-1]
        ansi.printok("Most recent image file: {}".format(most_recent))
    return count, most_recent


def get_current_layer(most_recent_image):
    """
    Example of most recent image file would be:
        ...ee966dfff4ba/CalibrationCube000002.jpg
    """
    return int(most_recent_image[-10:-4])


def main():
    print("Establishing connection to printer...")
    url = "http://146.169.216.149/"
    api_key = "5CB7AD5DD66D488997CCD9C93E6F8701"
    printer = OctoRest(url=url, apikey=api_key)
    ansi.printok("Connected to printer. Here is current job info:")
    pprint(printer.job_info())

    control_printer = True

    # get gcode data
    gcode_data = get_gcode()
    
    # create a new monitor object
    monitor = ImageMonitor("LIVE DEMO", gcode_data)
    
    # start the print
    print("Starting the print now")
    printer.print()
    
    # check for folder created in the last 30 sec
    sdir, etime = get_snapshots_dir()
    while etime > 30: # time since folder created (seconds)
        ansi.printwarning("The active directory was created more than 30 seconds ago. Checking again for a more recent active folder.")
        sdir, etime = get_snapshots_dir()
        time.sleep(2)
    
    # watch folder for a new image
    last_processed_layer = 0
    while True:
        images_taken, latest_image = check_snapshots_dir(sdir)
        
        if images_taken > 0:
            layer_num = get_current_layer(latest_image)
            if layer_num > last_processed_layer:
                im = fetch_image(latest_image)
                im_warped = warp_image(im, updated_source_map2)
                
                # add image to stack
                monitor.add_image(im_warped, layer_num)
                
                # check for detector flags on the moving average
                error_occured = monitor.check_for_flags()
                if error_occured:
                    ansi.printerror(" ---> Error detected in print on layer {}".format(layer_num))
                    if control_printer: printer.pause()
                    return
                
                last_processed_layer = layer_num
                ansi.printok("Processed new image for layer {}".format(layer_num))
                continue
            
            if layer_num == 132:
                ansi.printok("Print has completed SUCCESSFULLY")
                print("Ending program...")
                return

        print("There are no new images available at {:.0f}".format(time.time()))
        time.sleep(2)
    
    # if error, pause the print
    # if layer number is the last layer. stop the monitor
    layer_num = get_current_layer(latest_image)

    # printer.pause()
    # printer.cancel()


    return


    try:
        if input("Scan mode? ") == 'y':
            for i in range(500):
                print("")
                pprint(printer.job_info())
                time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        print("Done")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt.")
    finally:
        print("\nDone.")
