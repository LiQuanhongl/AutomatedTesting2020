import os
import shutil
import random

# 运行 data_split.py 将数据集随机划分，生成yolo_data文件夹
image_path = "ATMobile2020-1"
labels_path = "stage2_pre"

image_list = []
imagefolder = os.listdir(image_path)
for name in imagefolder:
    if os.path.splitext(name)[1] == ".jpg":
        image_list.append(name)

# 8：1：1 训练集：测试集：验证集 train:valid:test
random.seed(123)
valid_and_test = random.sample(image_list, 200)
test = random.sample(valid_and_test, 100)
train = set(image_list)
valid_and_test = set(valid_and_test)
train = train - valid_and_test
test = set(test)
valid = valid_and_test - test

yolo_path = "yolo_data"
yolo_folder = os.path.exists(yolo_path)
if not yolo_folder:
    os.makedirs(yolo_path)

# 在yolo_data文件夹中生成train.txt valid.txt images文件夹、labels文件夹、sample文件夹
f = open("yolo_data/train.txt", "w")
for train_name in train:
    f.write("data/custom/images/" + train_name)
    f.write("\n")
f.close()

g = open("yolo_data/valid.txt", "w")
for valid_name in valid:
    g.write("data/custom/images/" + valid_name)
    g.write("\n")
g.close()

yolo_images_path = "yolo_data/images"
yolo_images_folder = os.path.exists(yolo_images_path)
if not yolo_images_folder:
    os.makedirs(yolo_images_path)

yolo_labels_path = "yolo_data/labels"
yolo_labels_folder = os.path.exists(yolo_labels_path)
if not yolo_labels_folder:
    os.makedirs(yolo_labels_path)

yolo_sample_path = "yolo_data/samples"
yolo_sample_folder = os.path.exists(yolo_sample_path)
if not yolo_sample_folder:
    os.makedirs(yolo_sample_path)

for name in imagefolder:
    if name in train or name in valid:  # 如果是train和valid，复制图片文件到images文件夹，复制标签文件到labels文件夹
        shutil.copyfile(image_path + "/" + name, yolo_images_path + "/" + name)
        txt_name = os.path.splitext(name)[0] + ".txt"
        shutil.copyfile(labels_path + "/" + txt_name, yolo_labels_path + "/" + txt_name)
    if name in test:  # 如果是test,复制图片到samples文件夹
        shutil.copyfile(image_path + "/" + name, yolo_sample_path + "/" + name)

print("data split finished.")
