from datetime import datetime
from pathlib import Path
import exifread
import os
import shutil


def sort_pictures(input_path):
    picture_path = Path(input_path)
    picture_list = []

    # Adding all files found in the picture path to a list. We exclude subfolders
    for file in os.listdir(picture_path):
        tmp_path = picture_path / file
        if os.path.isdir(tmp_path):
            continue
        picture_list.append(file)

    for picture in picture_list:
        image_path = picture_path / picture
        if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.mov', '.mp4', '.gif', '.3gp']:
            # Opening the file
            f = open(image_path, 'rb')
            # Reading all of the exif tags. This returns a dictionnary with all values
            tags = exifread.process_file(f, details=False)
            # Checking if the Exif DateTimeOriginal key exists
            # and using this whenever possible to determine the date the picture/video was taken
            try:
                date = str(tags['EXIF DateTimeOriginal'])[0:10].replace(':', '-')
            # When the key doesn't exist we will use the creation date of the file instead
            except KeyError:
                fname = Path(image_path)
                mtime = fname.stat().st_mtime
                mtime = datetime.fromtimestamp(mtime)
                month = mtime.strftime('%m')
                year = mtime.strftime('%Y')
            else:
                month = date[5:7]
                year = date[0:4]

            f.close()

            # Checking if the directory with the Year / Month structure already exists. If not we create one.
            path_2_move = picture_path / year / month
            if os.path.isdir(path_2_move):
                pass
            else:
                os.makedirs(path_2_move)
            # Finally we move the file to the right directory
            new_picture_path = path_2_move / picture
            print(f'Moving File to {new_picture_path}')
            shutil.move(image_path, new_picture_path)


sort_pictures('U:/iPhone')
sort_pictures('U:/Xiaomi_Note_9')
