import os
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter


class Filter:   #基类
    def __init__(self, image, parameter_list):
        self.image = image
        self.parameter_list = parameter_list   #储存了图片大小，显示格式等信息

    def filter(self, pic):
        pass  #查到写PASS可以不改变执行顺序并起到补充格式的作用


class Edge_extraction(Filter):  #子类，处理边缘
    def __init__(self, image, parameter_list):
        super(Edge_extraction, self).__init__(image, parameter_list)

    def filter(self, pic):
        pic = pic.filter(ImageFilter.EDGE_ENHANCE)   #先增强一下
        pic = pic.filter(ImageFilter.FIND_EDGES)   #提取边缘
        return pic


class Sharp(Filter):    #子类，锐化
    def __init__(self, image, parameter_list):
        super(Sharp, self).__init__(image, parameter_list)

    def filter(self, pic):
        pic = pic.filter(ImageFilter.SHARPEN)  #调用函数锐化
        return pic


class Vague(Filter):     #子类，模糊
    def __init__(self, image, parameter_list):
        super(Vague, self).__init__(image, parameter_list)

    def filter(self, pic):
        pic = pic.filter(ImageFilter.GaussianBlur)   #调用函数模糊
        return pic


class Resize(Filter):   #子类，调整大小
    def __init__(self, image, parameter_list):
        super(Resize, self).__init__(image, parameter_list)

    def filter(self, pic):   #根据参数调整大小
        pic = pic.resize((self.parameter_list[0], self.parameter_list[1]))
        return pic


class ImageShop:
    def __init__(self, pic_format, pic_file, pic_list, pic_processed, image, parameter_list):
        self.pic_format = pic_format
        self.pic_file = pic_file
        self.pic_list = pic_list
        self.pic_processed = pic_processed
        self.image = image
        self.parameter_list = parameter_list

    def load_images(self):  #加载图片
        all_list = os.listdir(self.pic_file)  #文件夹中所有文件
        for file in all_list:
            if self.pic_format in file:    #根据格式筛选
                self.pic_list.append(self.pic_file+'\\'+file)
        print(self.pic_list)
        return

    def _batch_ps(self, Filter):  #内部调用、批量处理函数
        for i in range(len(self.pic_processed)):
            pic = Filter.filter(self.pic_processed[i])
            self.pic_processed[i] = pic
        print(pic)
        return

    def batch_ps(self, x, *y):  #外部调用、批量处理函数
        ImageShop.load_images(self)  #加载图片
        for i in self.pic_list:
            self.pic_processed.append(Image.open(i))
        if x == 'Edge_extraction':  #批量提取边缘
            ImageShop._batch_ps(self, Edge_extraction(self.image, self.parameter_list))
        elif x == 'Sharp':   #批量锐化
            ImageShop._batch_ps(self, Sharp(self.image, self.parameter_list))
        elif x == 'Vague':  #批量模糊
            ImageShop._batch_ps(self, Vague(self.image, self.parameter_list))
        elif x == 'Resize':  #批量调整大小
            ImageShop._batch_ps(self, Resize(self.image, self.parameter_list))
        for yy in y:   #与上面代码相同，根据指令批量处理图片
            if yy == 'Edge_extraction':
                ImageShop._batch_ps(self, Edge_extraction(self.image, self.parameter_list))
            elif yy == 'Sharp':
                ImageShop._batch_ps(self, Sharp(self.image, self.parameter_list))
            elif yy == 'Vague':
                ImageShop._batch_ps(self, Vague(self.image, self.parameter_list))
            elif yy == 'Resize':
                ImageShop._batch_ps(self, Resize(self.image, self.parameter_list))
        return

    def display(self):  #批量显示处理后图片
        num_row = self.parameter_list[2]   #显示格式
        num_col = self.parameter_list[3]
        plot_num = self.parameter_list[4]
        if len(self.pic_processed) > plot_num:
            self.pic_processed = self.pic_processed[0:plot_num]
        m = len(self.pic_processed)
        n = 0
        #当足行足列时
        while m/num_row*num_col != 0:
            for i in range(num_col*num_row):
                pic = self.pic_processed[n]
                n += 1
                plt.subplot(num_row, num_col, i+1)
                plt.imshow(pic)
            m = m - num_col*num_row
            plt.show()
        #不能足行足列时
        while m > 0:
            t = m
            for j in range(m):
                pic = self.pic_processed[n]
                n += 1
                plt.subplot(1, t, j+1)
                plt.imshow(pic)
                m = m-1
            plt.show()
        return

    def save(self, path):  #保存图片
        for i in range(len(self.pic_processed)):
            pic = self.pic_processed[i]
            name = str(i)
            save_path = path + name + self.pic_format
            pic.save(save_path)
        return


class TestImageShop:  #测试类
    def __init__(self, pic_format, pic_file, pic_list, pic_processed, image, parameter_list):
        self.Test = ImageShop(pic_format, pic_file, pic_list, pic_processed, image, parameter_list)

    def batch_ps(self, x):  #批量处理
        self.Test.batch_ps(x, 'Vague', 'Resize')

    def display(self):   #显示
        self.Test.display()

    def save(self, path):  #储存
        self.Test.save(path)


def main():
    image = 0
    parameters_list = [600, 500, 2, 3, 18]
    pic_file = 'D:\pyctry\one\picture'
    pic_format = '.jpg'
    pic_list = []
    pic_processed = []
    x = 'Edge_extraction'
    path = 'D:\pyctry\one\p_picture'
    test = TestImageShop(pic_format, pic_file, pic_list, pic_processed, image, parameters_list)
    test.batch_ps(x)
    test.save(path)
    test.display()
    return


main()
