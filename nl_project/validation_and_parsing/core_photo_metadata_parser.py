from .parser import Parser, pd
from collections import defaultdict
import numpy as np


class CorePhotoMetadataParser(Parser):
    prepend_to_filename = '31_5-7 Eos/11.Core_Data/Core_Photos/'

    def parse_to_df(self, input_dict: dict) -> pd.DataFrame:
        """Want header info, file name references, and depths covered for each photo"""
        output_dict = defaultdict(list)
        header_info = dict()
        if 'lines' in input_dict.keys():
            for line in input_dict['lines']:
                if 'data:\\' in line:
                    file_name = line.split('\\')[-1].split('(')[0][:-1]
                    depth_range = line.split('(')[1].split('_')[4].replace(',', '.')
                    output_dict['top_depth'].append(float(depth_range.split('-')[0]))
                    output_dict['bottom_depth'].append(float(depth_range.split('-')[1]))
                    output_dict['file_name'].append(file_name)
                    output_dict['file_key'].append(self.prepend_to_filename + file_name)
                elif ':' in line:
                    split_line = line.split(':')
                    header_info[split_line[0].replace(' ', '')] = split_line[1].replace('\n', '')
                else:
                    continue

        else:
            raise ValueError('Wrong parser for input data')
        output = pd.DataFrame(output_dict)
        for key, value in header_info.items():
            output[key] = value
        return output

    def parse_to_array(self, input_dict: dict) -> np.ndarray:
        raise ValueError('Core photo metadata does not parse to an array')
