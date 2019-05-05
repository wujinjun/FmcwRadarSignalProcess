#%%
# 构建一个类，用于读取雷达数据
import numpy as np
import matplotlib.pyplot as plt
import tools
import time
import cv2 as cv
def time_count(start_time):
    print("time used: ",time.time() - start_time)

class radar_data_reader():
    def __init__(self):
        # 数据读取
        self.max_n_frames = 64  # 数据帧数长度
        self.data_path = "./test.bin"
        self.data_reshape = tools.read_frames_data(self.data_path)

        # RTM, DTM, ATM placeholder的构建
        # 信号处理数据尺寸设置
        self.window_length = 32
        self.range_size = 64
        self.doppler_size = 128
        self.angle_size = 80
        # placeholder 初始化
        self.rtm_placeholder = np.zeros(shape=(self.range_size, self.window_length))  # RTM placeholder
        self.dtm_placeholder = np.zeros(shape=(self.doppler_size, self.window_length))  # DTM placeholder
        self.atm_placeholder = np.zeros(shape=(self.angle_size, self.window_length))  # ATM placeholder


        # 图像输出尺寸设置
        self.weight = 300
        self.hight = 300
        self.rtm = np.zeros(shape=(self.weight, self.hight))
        self.dtm = np.zeros(shape=(self.weight, self.hight))
        self.atm = np.zeros(shape=(self.weight, self.hight))

    def get_one_frame(self,seq_frame):
        # 读取1帧数据
        data_filtered = tools.get_data(self.data_reshape, seq_frame)
        return data_filtered

    def do_fft_1d(self,data_filtered):
        # 1D-fft 嵌套求解fft
        fft_total, fft_out_of_nchirps = tools.fft_1d(data_filtered)
        return fft_total, fft_out_of_nchirps

    def get_rtm(self,fft_out_of_nchirps):
        # RTM
        range_bin = tools.get_rtm_bin(fft_out_of_nchirps)
        self.rtm_placeholder = tools.get_dynamic_tm(range_bin, self.rtm_placeholder)
        self.rtm = cv.resize(self.rtm_placeholder[0:32,:], (self.weight,self.hight))

    def get_dtm(self, fft_total, fft_out_of_nchirps):
        # DTM
        doppler_bin = tools.get_dtm_bin(fft_total, fft_out_of_nchirps)
        self.dtm_placeholder = tools.get_dynamic_tm(doppler_bin, self.dtm_placeholder)
        self.dtm = cv.resize(self.dtm_placeholder,(self.weight,self.hight))

    def get_atm(self, data_filtered):
        # ATM
        snapshot_number = 64
        angle_bin = tools.get_atm_bin(data_filtered, snapshot_number)
        self.atm_placeholder = tools.get_dynamic_tm(angle_bin, self.atm_placeholder)
        self.atm = cv.resize(self.atm_placeholder,(self.weight,self.hight))

    def update_image(self, seq_frame):
        # 更新图
        # 输入参数是帧序号
        data_filtered = self.get_one_frame(seq_frame)
        fft_total, fft_out_of_nchirps = self.do_fft_1d(data_filtered)
        self.get_rtm(fft_out_of_nchirps)
        self.get_dtm(fft_total, fft_out_of_nchirps)
        self.get_atm(data_filtered)

if __name__ == '__main__':
    data_reader = radar_data_reader()
    for seq_frame in range(data_reader.max_n_frames):
        data_reader.update_image(seq_frame)
        cv.imshow("123",data_reader.rtm)
        # print(data_reader.rtm.shape)
        cv.waitKey(20)
