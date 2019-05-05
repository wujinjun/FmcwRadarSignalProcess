import numpy as np

# 雷达参数设置
n_tx = 2
n_rx = 4
n_adc_samples = 64
n_chrips = 128
n_frames = 64
n_adc_bits = 16
norm_factor = np.sqrt(2) / (np.power(2, n_adc_bits - 1) - 1)
#%% 2D-FFT 信号处理代码
# 输入是汉明窗滤波后的信号数据，
# 输出第一个参数是128个扫频累积的fft频谱（1*64），第二个参数是128个扫频的1D-FFT结果(128*64)
def fft_1d(data_filtered):
    fft_out_of_nchirps = []
    chirp_fft_cache = []  # chirp层
    for chirp_index in range(n_chrips):
        fft_meanout_perchrip = []
        rx_fft_cache = []  # rx层
        for rx_index in range(n_rx):
            tx_fft_cache = []  # tx层
            for tx_index in range(n_tx):
                temp_fft_out = np.fft.fft(data_filtered[chirp_index][tx_index][rx_index][:])  # [1,64]
                tx_fft_cache.append(temp_fft_out)  # shape: [x,64]
                fft_meanout_perchrip.append(temp_fft_out)
            tx_fft_cache = np.array(tx_fft_cache)  # list to numpy array
            rx_fft_cache.append(tx_fft_cache)  # shape: [x,2,64]
        chirp_fft_cache.append(rx_fft_cache)  # shape: [x,4,2,64]

        # 求8个天线通道的fft均值，并构造为128个扫频中的一个扫频
        rx_fft_cache = np.array(rx_fft_cache)  # list to numpy array
        fft_meanout_perchrip = np.array(fft_meanout_perchrip)  # list to numpy array
        fft_meanout_perchrip = fft_meanout_perchrip.reshape(n_rx * n_tx, n_adc_samples)  # reshape to 8*64
        fft_meanout_perchrip = np.mean(fft_meanout_perchrip, 0)
        fft_out_of_nchirps.append(fft_meanout_perchrip)
    fft_out_of_nchirps = np.array(fft_out_of_nchirps)
    fft_total = np.array([])
    fft_total = np.sum(fft_out_of_nchirps, 0)  # 128个扫频的累加
    # t = np.arange(64)
    # # freq = np.fft.fftfreq(t.shape[-1])
    # plt.plot(t, np.absolute(fft_total))
    # plt.show()
    return fft_total, fft_out_of_nchirps

#%% 得到RTM的一阵数据
#   输入第一个参数是（1*64）的fft距离谱
#   输出是一帧数据计算所得的距离谱
def get_rtm_bin(fft_out_of_nchirps):
    fft_out_of_nchirps = np.absolute(fft_out_of_nchirps)
    fft_self_ref = np.multiply(fft_out_of_nchirps, fft_out_of_nchirps)
    range_bin_unnorm = np.mean(fft_self_ref, 0)
    range_bin_norm = (range_bin_unnorm - np.min(range_bin_unnorm)) / np.absolute(
        np.max(range_bin_unnorm) - np.min(range_bin_unnorm))
    # range_bin_norm = (range_bin_norm)
    return range_bin_norm


#%% 得到DTM的一帧的数据
#   输入第一个参数是（1*64）的fft距离谱，用来得到峰值索引；第二个参数是128个扫频的1D-FFT结果(128*64)
#   输出是一帧数据计算所得的多普勒谱
def get_dtm_bin(fft_total, fft_out_of_nchirps):
    # 2D-FFT
    fft_out_of_nchirps = fft_out_of_nchirps.transpose()  # 128*64-->64*128
    fft2d = np.fft.fft2(fft_out_of_nchirps)  # 2DFFT
    fft2d = np.fft.fftshift(np.absolute(fft2d))
    fft2d[0:1] = fft2d[0:1][:] * 0.1  # 抑制天线泄露
    fft2d[32:] = fft2d[32:][:] * 0.1  # 抑制远距离无效目标
    # 得到RDM
    rdm = fft2d[:][:]  # 可以对图像进行裁剪
    # plt.imshow(np.absolute(rdm))

    # rdm图像的归一化
    norm_rdm = (rdm - np.mean(rdm)) / np.absolute(np.max(rdm) - np.min(rdm))
    # plt.imshow(np.absolute(norm_rdm))
    # 寻找rdm的峰值
    range_index = np.where(fft_total == np.max(fft_total[2:20]))  # 查找峰值索引
    # print(range_index)
    doppler_bin_unnorm = norm_rdm[range_index]  # 取出目标索引下的多普勒向数据
    doppler_bin_norm = (doppler_bin_unnorm - np.min(doppler_bin_unnorm)) / np.absolute(
        np.max(doppler_bin_unnorm) - np.min(doppler_bin_unnorm))
    return doppler_bin_norm

#%% 得到ATM的一帧的数据
#   输入第一个参数是（1*80）的角度谱；第二个参数是快拍数
#   输出是一帧数据计算所得的多普勒谱
def get_atm_bin(data_filtered,snapshot_number = 64):
    angle_bin_unnorm = classical_music(data_filtered,snapshot_number)
    angle_bin_norm = (angle_bin_unnorm - np.min(angle_bin_unnorm)) / np.absolute(
        np.max(angle_bin_unnorm) - np.min(angle_bin_unnorm))
    return angle_bin_norm



#%% 从读取的二进制数据中，按帧读取数据
# 第一个参数是输入，第二个参数指定的帧序号
def get_data(data_reshape,seq_frame):
    data_perframe_uint16 = data_reshape[seq_frame]
    # print(data_perframe_uint16[:20])
    data_perframe_int16 = data_perframe_uint16 - 2 ** 15   # uint16 to int16
    data_perframe_int16 = np.array(data_perframe_int16, dtype='int16')       # numpy类型需要转化为uint16
    # print(data_perframe_uint16)
    # print(data_perframe_int16)

    # 8路IQ信号
    data_iq = data_perframe_int16.reshape(-1, 8)
    data_iq = np.transpose(data_iq)

    # print(data_IQ)
    # 乒乓操作构造8路信号
    data_pingpong = np.array([data_iq[0], data_iq[2], data_iq[4], data_iq[6], data_iq[1], data_iq[3], data_iq[5], data_iq[7]])
    # 构造复数信号
    data_complex = data_pingpong[0:4] + 1j * data_pingpong[4:8]
    data_complex = np.transpose(data_complex)
    data_norm_complex = norm_factor * data_complex      # 归一化因子

    # reshape数据为 "扫频数>发射通道>接受通道>采样点"
    data_chirp_tx_nx_point = data_norm_complex.reshape(n_chrips,n_tx,n_rx,n_adc_samples)
    # print(data_[0][0][0][:])
    # print(data_[1][0][0][:])

    # hanning窗滤波
    hann_win = np.hanning(n_adc_samples)
    hann_win = hann_win/sum(hann_win)/n_chrips
    data_filtered = np.multiply(hann_win,data_chirp_tx_nx_point[:][:][:][:])
    return data_filtered

#%% 从路径中以二进制方式读取bin文件
#   输入是bin文件路径
#   输出是按帧排列的雷达数据
def read_frames_data(bindata_path):
    # 数据读取
    bindata_path = "./test.bin"
    with open(bindata_path, "rb") as f:
        data_fromfile = np.fromfile(f, dtype = np.uint16)

    # 文件读取数据的reshape
    data_reshape = data_fromfile.reshape(-1, n_tx * n_rx * n_adc_samples * n_chrips * 2)
    return data_reshape

#%% MUSIC，前向平滑
def compute_rf(data_8channel,snapshot_number):

    xf1 = data_8channel[0:6]
    xf2 = data_8channel[1:7]
    xf3 = data_8channel[2:8]
    rf1 = np.dot(xf1.transpose(), xf1) / snapshot_number
    rf2 = np.dot(xf2.transpose(), xf2) / snapshot_number
    rf3 = np.dot(xf3.transpose(), xf3) / snapshot_number
    rf = (rf1 + rf2 + rf3) / 3
    return rf

# MUSIC，后向平滑
def compute_rb(data_8channel,snapshot_number):
    xb1 = np.conjugate(data_8channel[8:2:-1])
    xb2 = np.conjugate(data_8channel[7:1:-1])
    xb3 = np.conjugate(data_8channel[6:0:-1])
    rb1 = np.dot(xb1.transpose(), xb1) / snapshot_number
    rb2 = np.dot(xb2.transpose(), xb2) / snapshot_number
    rb3 = np.dot(xb3.transpose(), xb3) / snapshot_number
    rb = (rb1 + rb2 + rb3) / 3
    return rb

# def music_64sample(data_filtered):
#     data_8channel = data_filtered.reshape(8, -1)
#     container = np.empty(shape=[80])
#     for start_pos in range(0, len(data_8channel[0]),64):
#         data_8channel_64sample = data_8channel[:,start_pos:start_pos+64]
#         # print(start_pos)
#         music_bin_res = classical_music(data_8channel_64sample)
#         container = np.row_stack((container,music_bin_res))
#     aaa = np.sum(container[3:8], 0)
#     # t = np.arange(80)
#     # plt.plot(t, np.absolute(aaa))
#     # plt.show()
#     return

#%% 经典music算法
# 第一个输入是滤波后信号，第二个输入是快拍数
# 输出是music角度估计谱
def classical_music(data_filtered, snapshot_number = 64):
    data_8channel = data_filtered.reshape(8, -1)
    xxx = data_8channel[:, :snapshot_number]
    searching_doa = range(-40, 40)
    sensor_number = 8
    source_number = 3
    wave_length = 3e8 / 77e9
    distance_of_antenna = wave_length / 2

    # MUISC 前向和后向平滑
    # rf = compute_rf(data_8channel, snapshot_number)
    # rb = compute_rb(data_8channel, snapshot_number)
    # rbf = (rf + rb) / 2

    Pmusic = []
    # print(xxx.shape)
    ref = np.dot(xxx, xxx.transpose()) / snapshot_number
    u, s, vh = np.linalg.svd(ref, full_matrices=True)
    Un = u[:, source_number:sensor_number]
    Gn = np.dot(Un, Un.transpose())
    j = np.complex(0, -1)
    atenna = np.array(range(sensor_number))

    two_pi_d = np.dot(np.dot(2, np.pi), distance_of_antenna)

    for th in range(len(searching_doa)):
        a_theta = np.exp(
            np.dot(j, atenna.transpose()) * two_pi_d * np.sin(np.dot(np.pi, searching_doa[th]) / 180) / wave_length)
        Pmusic.append(1 / np.absolute(np.dot(np.dot(a_theta.transpose(), Gn), a_theta)))
    Pmusic = 10 * np.log(np.array(Pmusic))
    return Pmusic


#%% 更新tm文件，在末尾增加新列，并去除头列
def get_dynamic_tm(data_bin, tm_placeholder):
    data_bin = np.reshape(data_bin, (data_bin.size,1))
    # print("range_bin.shape: ",range_bin.shape)
    tm_placeholder = np.column_stack((tm_placeholder, data_bin))
    # print("1 rtm_placeholder.shape: ",rtm_placeholder.shape)

    tm_placeholder = tm_placeholder[:, -32:]
    # print("2 rtm_placeholder.shape: ",rtm_placeholder.shape)

    return tm_placeholder

    # range_bin = np.reshape(range_bin,(range_bin.shape[0],1))
    # rtm_placeholder = np.column_stack((rtm_placeholder,range_bin))
    # rtm_placeholder = rtm_placeholder[:,-32:]
