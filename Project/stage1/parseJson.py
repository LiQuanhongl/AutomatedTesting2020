import json
import os
from PIL import Image

# 控件要分成的类别
classList = ["CheckBox", "EditText", "ImageButton", "ImageView", "ProgressBar", "RadioButton",
             "SeekBar", "Spinner", "Switch", "ToggleButton", "TextView", "Button"]


def getClassAndBound(v, li):  # 解析获得v及其子控件的类别和坐标
    if v is not None:
        if v["visible-to-user"] is True:
            info = []
            info.append(v["class"])
            info.append(v["bounds"])
            li.append(info)
        if "children" in v.keys():
            for i in range(len(v["children"])):
                getClassAndBound(v["children"][i], li)


def judgeClass(c):  # 返回控件的类别号
    global classList
    for i in range(len(classList)):
        if classList[i].lower() in c.lower():  # 这里如果android的类名中含有classList的类，就认为是属于这一类的
            return i
    return -1


def judgeClose(e1, e2):  # 判断两个元素的边界框是否相近
    for i in range(4):
        if abs(e1[i] - e2[i]) >= 5:  # 这里设定坐标相差在5以内就很靠近
            return False
    return True


def yoloCheck(p):  # 检查数据是否符合yolov3的要求
    if p[0] + p[2] / 2 > 1:
        return False
    if p[0] - p[2] / 2 < 0:
        return False
    if p[1] + p[3] / 2 > 1:
        return False
    if p[1] - p[3] / 2 < 0:
        return False
    for i in range(4):
        if p[i] > 1 or p[i] < 0:
            return False
    return True


def parse(s, name):  # 解析出其所有类和坐标
    global classList

    li = []
    getClassAndBound(s["activity"]["root"], li)  # 这里获取了s的所有控件类型和坐标
    elementList = []
    # 如果有符合的类，就把其加进去,并去除相近的控件
    while len(li) >= 1:
        classnum = judgeClass(li[0][0])
        if classnum == -1:
            del (li[0])
        else:
            tmp = []
            tmp.append(classnum)
            tmp.append(li[0][1])
            elementList.append(tmp)
            i = 1
            while i < len(li):
                if (judgeClose(li[0][1], li[i][1])):  # 这里判断其是否接近
                    del (li[i])
                else:
                    i += 1
            del (li[0])

    # 获取图片的尺寸，有的图片是1080*1920的，有的图片是540*960的
    img_path = "ATMobile2020-1/" + os.path.splitext(name)[0] + ".jpg"
    img = Image.open(img_path)

    yolo_para_list = []

    # 缩放操作，以及计算符合yolov3格式的数据
    for i in range(len(elementList)):
        center_point_x = (elementList[i][1][0] + elementList[i][1][2]) / 2 / 1440  # 控件的中心点x坐标
        center_point_y = (elementList[i][1][1] + elementList[i][1][3]) / 2 / 2560  # 控件的中心点y坐标
        width = (elementList[i][1][2] - elementList[i][1][0]) / 1440  # 控件的宽度
        height = (elementList[i][1][3] - elementList[i][1][1]) / 2560  # 控件的高度

        yolo_para = []
        yolo_para.append(center_point_x)
        yolo_para.append(center_point_y)
        yolo_para.append(width)
        yolo_para.append(height)
        yolo_para_list.append(yolo_para)

        # 缩放成实际图片的坐标
        elementList[i][1][0] = round(elementList[i][1][0] / 1440 * img.width)
        elementList[i][1][1] = round(elementList[i][1][1] / 2560 * img.height)
        elementList[i][1][2] = round(elementList[i][1][2] / 1440 * img.width)
        elementList[i][1][3] = round(elementList[i][1][3] / 2560 * img.height)

    folderPath = "stage1_output"
    folder = os.path.exists(folderPath)
    if not folder:
        os.makedirs(folderPath)
    newFilePath = folderPath + "/" + os.path.splitext(name)[0] + ".txt"
    newFile = open(newFilePath, "w")
    for i in range(len(elementList)):  # 将缩放后的控件类别和位置写进文件中
        newFile.write(classList[elementList[i][0]])
        newFile.write(" (")
        newFile.write(str(elementList[i][1][0]))
        newFile.write(",")
        newFile.write(str(elementList[i][1][1]))
        newFile.write(")")
        newFile.write(" (")
        newFile.write(str(elementList[i][1][2]))
        newFile.write(",")
        newFile.write(str(elementList[i][1][3]))
        newFile.write(")")
        newFile.write("\n")
    newFile.close()

    # 这里生成符合yolov3的数据格式
    folderPath_yolo = "stage2_pre"
    folder_yolo = os.path.exists(folderPath_yolo)
    if not folder_yolo:
        os.makedirs(folderPath_yolo)
    newFilePath_yolo = folderPath_yolo + "/" + os.path.splitext(name)[0] + ".txt"
    newFile_yolo = open(newFilePath_yolo, "w")

    for i in range(len(yolo_para_list)):
        if (yoloCheck(yolo_para_list[i])):
            newFile_yolo.write(str(elementList[i][0]))
            for j in range(4):
                newFile_yolo.write(" ")
                newFile_yolo.write(str(yolo_para_list[i][j]))
            newFile_yolo.write("\n")
    newFile_yolo.close()


# 运行 parseJson.py 生成stage1_output文件夹为第一阶段结果，stage2_pre文件夹为图片对应的yolov3格式的标签
if __name__ == "__main__":
    Path = "ATMobile2020-1"
    jsonfolder = os.listdir(Path)
    # 对每个json文件进行处理
    for name in jsonfolder:
        if os.path.splitext(name)[1] == ".json":
            f = open(Path + "/" + name, "r")
            d = f.read()
            s = json.loads(d)
            parse(s, name)
            f.close()
    print("stage 1 finished.")

    # 运行 data_split.py 将数据集随机划分，生成yolo_data文件夹
    os.system("python data_split.py")
