from mibidata import tiff
import skimage.io as io
import glob
import os


def extract_single_channels_from_mibitiff(data_dir, mibitiff_files=None):
    """Load images from a series of MIBItiff tiff files.

    This function takes a set of MIBItiff tiff files and extracts the single_channel images.
    The type used to store the images will be the same as that of the images stored in the
    MIBItiff tiff files.

    Args:
        data_dir (str):
            directory containing MIBItiffs
        mibitiff_files (list):
            list of MIBItiff files to load (e.g. ['Point1', 'Point2']).
            If None, all MIBItiffs in data_dir are loaded.

    """

    if not mibitiff_files:
        mibitiff_files = glob.glob(os.path.join(data_dir, '*.tiff'))
    else:
        mibitiff_files = [os.path.join(data_dir, point + '.tiff')
                          for point in mibitiff_files]

    dtype = io.imread(os.path.join(data_dir, mibitiff_files[0]), plugin='tifffile').dtype

    # extract images from MIBItiff file
    channel_tuples = tiff.read(mibitiff_files[0]).channels
    channels = [channel_tuple[1] for channel_tuple in channel_tuples]

    for mibitiff_file in mibitiff_files:
        file_path = os.path.join(data_dir, mibitiff_file)
        save_dir = os.path.join(mibitiff_file.rsplit('.tiff', 1)[0], 'single_channel_TIFs')
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        mibitiff_img = tiff.read(file_path)[channels].astype(dtype)
        for channel in range(mibitiff_img.shape[2]):
            single_channel_image = mibitiff_img[:, :, channel]
            save_path = os.path.join(save_dir, f'{channel}.tif')
            io.imsave(save_path, single_channel_image, plugin='tifffile')
