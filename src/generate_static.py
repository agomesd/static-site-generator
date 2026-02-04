import os
import shutil


def generate_static(source_dir, target_dir):
    if not os.path.exists(source_dir):
        raise Exception(f"invalid source directory: {source_dir}")

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.mkdir(target_dir)
    files = os.listdir(source_dir)
    for file in files:
        if os.path.isfile(f"{source_dir}/{file}"):
            shutil.copyfile(f"{source_dir}/{file}", f"{target_dir}/{file}")
        else:
            generate_static(f"{source_dir}/{file}", f"{target_dir}/{file}")
