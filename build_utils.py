import shutil
import os


def copy_datas_to_dist():
    source_dir = "assets/"
    destination_dir = "dist/assets/"
    if os.path.isdir(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    if not os.path.exists("dist/video"):
        os.mkdir("dist/video")
    if not os.path.exists("dist/data"):
        os.mkdir("dist/data")


if __name__ == "__main__":
    copy_datas_to_dist()
