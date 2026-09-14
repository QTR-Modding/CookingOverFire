import os

cfg = {}

cfg['PATH'] = {}

# Build stable absolute paths from this file location so execution is
# independent from the current working directory.
_code_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.abspath(os.path.join(_code_dir, '..'))
_data_dir = os.path.join(_root_dir, 'DATA')

cfg['PATH']['ROOT'] = _root_dir + os.sep
cfg['PATH']['DATA'] = _data_dir + os.sep
cfg['PATH']['CODE'] = _code_dir + os.sep
cfg['PATH']['OUTPUT'] = os.path.join(_code_dir, 'output') + os.sep
cfg['PATH']['FIRE_SOURCES'] = os.path.join(_data_dir, 'fire_sources') + os.sep
cfg['PATH']['FOOD_SOURCES'] = os.path.join(_data_dir, 'food_matching') + os.sep
