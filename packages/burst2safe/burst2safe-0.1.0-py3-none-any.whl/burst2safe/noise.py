from copy import deepcopy
from typing import Iterable

import lxml.etree as ET
import numpy as np

from burst2safe.base import Annotation, ListOfListElements
from burst2safe.utils import BurstInfo, flatten


class Noise(Annotation):
    def __init__(self, burst_infos: Iterable[BurstInfo], image_number: int):
        super().__init__(burst_infos, 'noise', image_number)
        self.range_vector_list = None
        self.azimuth_vector_list = None

    def create_range_vector_list(self):
        rg_vectors = [noise.find('noiseRangeVectorList') for noise in self.inputs]
        rg_vector_lol = ListOfListElements(rg_vectors, self.start_line, self.slc_lengths)
        self.range_vector_list = rg_vector_lol.create_filtered_list([self.min_anx, self.max_anx])

    def update_azimuth_vector(self, az_vector: ET.Element, line_offset: int):
        new_az_vector = deepcopy(az_vector)
        line_element = new_az_vector.find('line')

        lines = np.array([int(x) for x in line_element.text.split(' ')])
        lines += line_offset

        first_line = 0
        if np.any(lines <= first_line):
            first_index = np.where(lines == lines[lines <= first_line].max())[0][0]
        else:
            first_index = 0

        last_line = self.stop_line - self.start_line - 1
        if np.any(lines >= last_line):
            last_index = np.where(lines == lines[lines >= last_line].min())[0][0]
        else:
            last_index = lines.shape[0] - 1

        new_az_vector.find('firstAzimuthLine').text = str(lines[first_index])
        new_az_vector.find('lastAzimuthLine').text = str(lines[last_index])

        slice = np.s_[first_index : last_index + 1]
        count = str(last_index - first_index + 1)

        line_element.text = ' '.join([str(x) for x in lines[slice]])
        line_element.set('count', count)

        az_lut_element = new_az_vector.find('noiseAzimuthLut')
        az_lut_element.text = ' '.join(az_lut_element.text.split(' ')[slice])
        az_lut_element.set('count', count)
        return new_az_vector

    def create_azimuth_vector_list(self):
        az_vectors = [noise.find('noiseAzimuthVectorList') for noise in self.inputs]
        updated_az_vectors = []
        for i, az_vector_set in enumerate(az_vectors):
            slc_offset = sum(self.slc_lengths[:i])
            az_vectors = az_vector_set.findall('noiseAzimuthVector')
            updated_az_vector_set = []
            for az_vector in az_vectors:
                line_offset = slc_offset - self.start_line
                updated_az_vector = self.update_azimuth_vector(az_vector, line_offset)
                updated_az_vector_set.append(updated_az_vector)
            updated_az_vectors.append(updated_az_vector_set)

        updated_az_vectors = flatten(updated_az_vectors)

        new_az_vector_list = ET.Element('noiseAzimuthVectorList')
        new_az_vector_list.set('count', str(len(updated_az_vectors)))
        for az_vector in updated_az_vectors:
            new_az_vector_list.append(az_vector)
        self.azimuth_vector_list = new_az_vector_list

    def assemble(self):
        self.create_ads_header()
        self.create_range_vector_list()
        self.create_azimuth_vector_list()

        noise = ET.Element('noise')
        noise.append(self.ads_header)
        noise.append(self.range_vector_list)
        noise.append(self.azimuth_vector_list)
        noise_tree = ET.ElementTree(noise)

        ET.indent(noise_tree, space='  ')
        self.xml = noise_tree
