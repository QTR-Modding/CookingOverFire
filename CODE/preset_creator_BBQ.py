from funcs import *
from utils import get_fire_sources, get_food_source_comments, get_food_sources
from config import cfg
import os
import shutil

cooking_duration = 0.06
# tint_color = "f30a86a3"
tint_color = "ff006433"
cooking_sound = "0x1~quantAoTBBQ.esp"
cooking_smoke = "_quantSmokeExhaleFX"
fire_group_main = "qAoTFireMain"
fire_group_inv = "qAoTFireInv"

if __name__ == "__main__":
    fire_sources = get_fire_sources()
    food_sources = get_food_sources()
    food_source_comments = get_food_source_comments()

    specific_fire_sources = ['Torch01', 'Torch01Shadow', 'FireSalts']
    specific_fire_source_set = set(specific_fire_sources)
    main_fire_sources = [fire for fire in fire_sources if fire not in specific_fire_source_set]
    inv_fire_sources = [fire for fire in fire_sources if fire in specific_fire_source_set]

    output_base = os.path.normpath(cfg['PATH']['OUTPUT'])
    form_group_dir = os.path.join(
        output_base,
        "main",
        "SKSE",
        "Plugins",
        "AlchemyOfTime",
        "formGroups"
    )
    if not os.path.exists(form_group_dir):
        os.makedirs(form_group_dir)

    with open(os.path.join(form_group_dir, f"{fire_group_main}.txt"), "w") as file:
        file.write("\n".join(main_fire_sources) + "\n")

    with open(os.path.join(form_group_dir, f"{fire_group_inv}.txt"), "w") as file:
        file.write("\n".join(inv_fire_sources) + "\n")

    group_nodes = []
    if main_fire_sources:
        group_nodes.append((fire_group_main, None))
    if inv_fire_sources:
        group_nodes.append((fire_group_inv, fire_group_inv))

    for filename, pairs in food_sources.items():
        print(f"File: {filename}")
        wrapped_blocks = []
        comments = food_source_comments[filename]
        for from_, to_ in pairs.items():
            transformers_block = []
            for fire_group, container_group in group_nodes:
                if container_group:
                    transformerNode = transformer_node(
                        FormEditorID=fire_group,
                        finalFormEditorID=to_,
                        duration=cooking_duration,
                        color=tint_color,
                        sound=cooking_sound,
                        art_object=cooking_smoke,
                        containers=container_group
                    )
                    transformerNode = add_comment_to_keys(
                        transformerNode,
                        {'containers': 'trick to make it function only outside inventories'}
                    )
                else:
                    transformerNode = transformer_node(
                        FormEditorID=fire_group,
                        finalFormEditorID=to_,
                        duration=cooking_duration,
                        color=tint_color,
                        sound=cooking_sound,
                        art_object=cooking_smoke
                    )

                transformerNode = add_comment_to_keys(
                    transformerNode,
                    {'finalFormEditorID': comments[to_]}
                )
                transformers_block.append(transformerNode)
            transformers_block = concatenate_nodes(*transformers_block)
            forms_block = owner_block(
                owner_title="forms",
                owners=from_
            )
            forms_block = add_comment_to_keys(
                forms_block,
                {'forms': comments[from_]}
            )
            child_blocks = {
                'transformers': transformers_block
            }
            wrapped_block = block_wrapper(forms_block, child_blocks, start="")
            wrapped_block = f"{wrapped_block.replace('\n', '\n')}"
            wrapped_blocks.append(wrapped_block)
        wrapped_blocks = concatenate_nodes(*wrapped_blocks)
        wrapped_blocks = 'formsLists:\n' + wrapped_blocks
        # write the output to a file
        folder_path = cfg['PATH']['OUTPUT']
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(folder_path + f"quantAoTBBQ_{filename.split('.')[0]}.yml", "w") as file:
            file.write(wrapped_blocks)

    # Shared path components
    base_relative_path = "SKSE/Plugins/AlchemyOfTime/FOOD/addon"
    file_prefix = "quantAoTBBQ_"

    # Mapping for special renamed files
    special_files = {
        f"{file_prefix}burnt_Vanilla_SFE.yml": f"SFE/{base_relative_path}/{file_prefix}burnt_skyrim_esm.yml",
        f"{file_prefix}Vanilla_SFE.yml": f"SFE/{base_relative_path}/{file_prefix}skyrim_esm.yml",
    }

    # List of YAML files (relative parts without the prefix and shared path)
    yaml_files = [
        "CACO/burnt_CACO.yml",
        "CACO/caco.yml",
        "Gourmet/gourmet.yml",
        "Hunterborn/burnt_Hunterborn.yml",
        "Hunterborn/Hunterborn.yml",
        "LvxMagicks - Turkey Dinner - CoF_Patch/lvxmagicks_turkey.yml",
        "main/burnt_skyrim_esm.yml",
        "main/dragonborn_esm.yml",
        "main/hearthfires_esm.yml",
        "main/skyrim_esm.yml",
        "SFE/burnt_skyrim_food_expansion.yml",
        "SFE/skyrim_food_expansion.yml",
        "SFSS/burnt_SFSS.yml",
        "SFSS/SFSS.yml",
        "SFSS_CACO/SFSS_CACO.yml",
        "SHO/SHO.yml",
        "SHO/burnt_SHO.yml",
        "SBO/SBO.yml",
        "HAV/HAV.yml",
        "HAV/burntHAV.yml",
        "CC_Fishing/cc_fishing.yml",
        "MMM/meats_meals.yml",
        "DiverseFoods/diverse_foods.yml",
        "CannibalHarvest/cannibal_harvest.yml",
    ]

    # Ensure output_base exists
    if not os.path.exists(output_base):
        os.makedirs(output_base)

    # Organize files into their individual folders
    for yaml_file in yaml_files:
        # Extract the filename with prefix
        filename = file_prefix + os.path.basename(yaml_file)
        source_file = os.path.join(output_base, filename)

        # Handle special renamed files
        if filename in special_files:
            target_path = special_files[filename]
        else:
            target_path = os.path.join(os.path.dirname(yaml_file), base_relative_path, filename)

        # Create the full output path
        full_output_path = os.path.join(output_base, os.path.dirname(target_path))
        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path)

        # Move the file if it exists
        destination_file = os.path.join(full_output_path, filename)
        if os.path.exists(source_file):
            shutil.move(source_file, destination_file)
            print(f"Moved: {source_file} -> {destination_file}")
        else:
            print(f"Warning: Source file {source_file} does not exist. Skipping.")

    # Handle special files explicitly
    for special_file, target_path in special_files.items():
        source_file = os.path.join(output_base, special_file)
        full_output_path = os.path.join(output_base, os.path.dirname(target_path))
        destination_file = os.path.join(full_output_path, os.path.basename(target_path))

        # Ensure directories exist
        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path)

        # Move the special file
        if os.path.exists(source_file):
            shutil.move(source_file, destination_file)
            print(f"Moved special file: {source_file} -> {destination_file}")
        else:
            print(f"Warning: Special source file {source_file} does not exist. Skipping.")

    print("YAML files organized into individual folders, including special cases.")
