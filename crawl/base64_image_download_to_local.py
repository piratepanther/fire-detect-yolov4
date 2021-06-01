import base64
# from io import BytesIO
import io
import os

from PIL import Image


def base64_image_download_to_local(src_link_base64, save_path,img_name):

    binary_image_data =base64.b64decode(src_link_base64)
    # file_like=io.BytesIO(binary_image_data)


    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)

    path = os.path.join(save_path, str(img_name) + '.jpg')
    file = open(path, "wb")
    file.write(binary_image_data)
    file.close()

    # image = Image.open(file_like)
    # image.show()