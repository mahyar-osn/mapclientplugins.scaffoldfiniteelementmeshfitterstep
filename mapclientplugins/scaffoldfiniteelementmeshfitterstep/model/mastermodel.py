from opencmiss.utils.zinc import createFiniteElementField, createSquare2DFiniteElement,\
    createVolumeImageField, createMaterialUsingImageField

import imagesize
import cv2

from opencmiss.utils.zinc import defineStandardVisualisationTools


from PySideX import QtCore


def create_model(context):
    default_region = context.getDefaultRegion()
    region = default_region.createChild('images')
    coordinate_field = createFiniteElementField(region)
    field_module = region.getFieldmodule()
    scale_field = field_module.createFieldConstant([2, 3, 1])
    scale_field.setName('scale')
    duration_field = field_module.createFieldConstant(1.0)
    duration_field.setManaged(True)
    duration_field.setName('duration')
    offset_field = field_module.createFieldConstant([+0.5, +0.5, 0.0])
    scaled_coordinate_field = field_module.createFieldMultiply(scale_field, coordinate_field)
    scaled_coordinate_field = field_module.createFieldAdd(scaled_coordinate_field, offset_field)
    scaled_coordinate_field.setManaged(True)
    scaled_coordinate_field.setName('scaled_coordinates')
    createSquare2DFiniteElement(field_module, coordinate_field,
                                    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])


def _load_images(images, frames_per_second, region):
    field_module = region.getFieldmodule()
    frame_count = len(images)
    image_dimensions = [0, 0]
    image_based_material = None
    if frame_count > 0:
        # Assume all images have the same dimensions.
        width, height = imagesize.get(images[0])
        if width != -1 or height != -1:
            cache = field_module.createFieldcache()
            scale_field = field_module.findFieldByName('scale')
            scale_field.assignReal(cache, [width, height, 1.0])
            duration = frame_count / frames_per_second
            duration_field = field_module.findFieldByName('duration')
            duration_field.assignReal(cache, duration)
            image_dimensions = [width, height]
        image_field = createVolumeImageField(field_module, images)
        image_based_material = createMaterialUsingImageField(region, image_field)
        image_based_material.setName('images')
        image_based_material.setManaged(True)

    return image_dimensions, image_based_material


def _get_video_info(filename):
    cap = cv2.VideoCapture(filename)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if cap.isOpened():
        flag, capture = cap.read()
        width = capture.shape[1]
        height = capture.shape[0]
        return [width, height], fps, total_frame


def _get_image_info(filename):
    image = cv2.imread(filename)
    width = image.shape[1]
    height = image.shape[0]
    return [width, height]


class MasterModel(object):

    def __init__(self, model_description, image_available=False, filename=None, is_temporal=False):

        self._description = model_description
        self._context = self._description.get_context()

        if is_temporal:
            timekeeper_module = self._context.getTimekeepermodule()
            self._timekeeper = timekeeper_module.getDefaultTimekeeper()
            self._timer = QtCore.QTimer()
            self._current_time = 0.0
            self._time_value_update = None
            self._frame_index_update = None

        if image_available:
            if is_temporal:
                self._image_dimension, self._fps, self._total_frames = _get_video_info(filename)
            else:
                self._image_dimension = _get_image_info(filename)
                self._fps, self._total_frames = None, None

            self._image_plane_model = ImagePlaneModel(self)
            self._image_plane_model.set_image_information(self._fps,
                                                          self._image_dimension)


