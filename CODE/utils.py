import sys,os
sys.path.append('..')
from config import cfg

def extract_pairs_from_file(file_path):
    result = {}
    with open(file_path, 'r') as file:
        waiting_for_match = False
        for line in file:
            if ':' not in line: continue
            _, value = line.split(':', 1)
            if waiting_for_match:
                result[waiting_for_match] = value.strip()
                waiting_for_match = False
            else:
                result[value.strip()] = None
                waiting_for_match = value.strip()
    for key in list(result.keys()):
        if result[key] is None:
            raise ValueError(f"Key '{key}' has no value in file '{file_path}'")
    return result

def extract_pair_comments(file_path):
    result = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Match lines with "<key>: <value>"
            if ':' not in line: continue
            key, value = line.split(':', 1)
            result[value.strip()] = key.strip()
    
    return result

def get_fire_sources()->list[str]:
    fire_sources:list[str] = []
    # read fire sources from all txt files in the fire_sources directory
    for file in os.listdir(cfg['PATH']['FIRE_SOURCES']):
        if file.endswith(".txt"):
            with open(cfg['PATH']['FIRE_SOURCES'] + file) as f:
                for line in f:
                    if line.strip() not in fire_sources:
                        fire_sources.append(line.strip())
    return fire_sources

def get_food_sources():
    food_sources = {}
    for file in os.listdir(cfg['PATH']['FOOD_SOURCES']):
        if file.endswith(".txt"):
            filepath = cfg['PATH']['FOOD_SOURCES'] + file
            pairs = extract_pairs_from_file(filepath)
            food_sources[file]=pairs
    return food_sources

def get_food_source_comments():
    food_source_comments = {}
    for file in os.listdir(cfg['PATH']['FOOD_SOURCES']):
        if file.endswith(".txt"):
            filepath = cfg['PATH']['FOOD_SOURCES'] + file
            pairs = extract_pair_comments(filepath)
            food_source_comments[file]=pairs
    return food_source_comments