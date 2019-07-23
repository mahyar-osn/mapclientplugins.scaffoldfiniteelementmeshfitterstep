from opencmiss.utils.maths.algorithms import calculate_line_plane_intersection


class ImagePlaneModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._region = None
        self._frames_per_second = -1
        self._images_file_name_listing = []
        self._image_dimensions = [-1, -1]
        self._duration_field = None
        self._image_based_material = None
        self._scaled_coordinate_field = None
        self._time_sequence = []

    def set_image_information(self, frames_per_second, image_dimensions):
        self._frames_per_second = frames_per_second
        self._image_dimensions = image_dimensions
