import cv2
import numpy as np
from keras.models import load_model
from os import listdir
import os
import re

def process(video_path):
        # EXTRACTING FRAMES FROM INPUT GRAYSCALE VIDEO
    video_file = cv2.VideoCapture(video_path)
    output_folder = 'grayframes/'

    frame_count = 0

    while True:
        success, frame = video_file.read()
        if not success:
            break
        
        filename = f"{output_folder}/{frame_count:04d}.jpg"
        cv2.imwrite(filename, frame)
        frame_count += 1
            
    video_file.release()
    print(f'\n\n\n\n\t\t\t **********   Finished extracting {frame_count} frames  ***********\n\n\n')

    # PASSING FRAMES TO MODEL 
    path = "grayframes/"
    outPath = "outRGBframes/"

    model = load_model('1_basic.h5')

    for f in listdir(path):
        gray_img = cv2.imread(path+f, cv2.IMREAD_GRAYSCALE)

        resized_gray_img = cv2.resize(gray_img, (640, 360))

        input_img = np.reshape(resized_gray_img, (1, 360, 640, 1))

        input_img = input_img / 255.0

        predicted_img = model.predict(input_img)

        predicted_img = np.squeeze(predicted_img)

        predicted_img = predicted_img * 255.0

        predicted_img = predicted_img.astype(np.uint8)
        cv2.imwrite(outPath+f, predicted_img)

    print("Done")

    # CONVERTING PREDICTED RGB FRAMES TO VIDEO
    path = 'outRGBframes/'
    out_path = './output/'
    file_name = os.path.basename(video_path)
    out_video_name = file_name
    out_video_full_path = out_path+"out_"+out_video_name
    
    print(out_video_full_path)


    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)


    pre_imgs = os.listdir(path)
    pre_imgs = sorted_alphanumeric(pre_imgs)
    print(pre_imgs)
    img = []

    for i in pre_imgs:
        i = path+i
        img.append(i)


    cv2_fourcc = cv2.VideoWriter_fourcc(*'H264')

    frame = cv2.imread(img[0])
    size = list(frame.shape)
    del size[2]
    size.reverse()

    video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, 30, size) 

    for i in range(len(img)): 
        video.write(cv2.imread(img[i]))
        print('frame ', i+1, ' of ', len(img))

    video.release()
    print('outputed video to ', out_path)

    def clean_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

    clean_folder(output_folder)
    clean_folder(path)
    
    return out_video_full_path



'''



# Example usage
folder_path = '/path/to/folder'  # Replace with the actual folder path
clean_folder(folder_path)
'''