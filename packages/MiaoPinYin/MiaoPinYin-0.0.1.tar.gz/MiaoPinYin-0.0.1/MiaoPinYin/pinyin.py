import os
from collections.abc import Iterable
from playsound import playsound
from pypinyin import lazy_pinyin, Style


def say_zh(text: str):
    res = lazy_pinyin(text, style=Style.TONE3, neutral_tone_with_five=True, errors='ignore')
    say_pinyin(res)


def say_pinyin(text: str | list[str]) -> None:
    """
    播放拼音
    :param text: str | list[str] 拼音或通过pypinyin输出的已切割的拼音
    :return: 直接播放，不返回
    """

    def say_voc(voc: str):
        """
         播放单个拼音
        :param voc: 单个拼音
        :return: 直接播放，不返回
        """
        if __is_yun(voc[0]):
            playsound(f'./MiaoPinYin/data/ym/{voc[0:-1]}/{"1" if voc[-1] == "5" else voc[-1]}.mp3')
        else:
            if voc[1] == 'h':
                i = 2
            else:
                i = 1
            playsound(f'{this_path}/data/{voc[0:i]}/{voc[i:-1]}/{"1" if voc[-1] == "5" else voc[-1]}.mp3')

    # 回到say_pinyin了哈
    this_path = os.path.dirname(__file__).replace("\\", "/").replace(':/', '://')
    if isinstance(text, str):
        s = ''
        for ch in text:
            if not __is_num(ch):
                s += ch
            else:
                say_voc(s)
                s = ''
    elif isinstance(text, Iterable):
        for _ in text:
            say_voc(_)


# 判断是否为韵母
def __is_yun(ch: str) -> bool:
    """
    判断是否为韵母

    :param ch: 要判断的单个字符
    :return: bool值，否为韵母
    """
    if ch in ['a', 'e', 'o', 'i', 'u', 'v']:
        return True
    return False


def __is_num(ch: str) -> bool:
    """
    判断是否为1234

    :param ch: 要判断的单个字符
    :return: bool值，否为规定数字
    """
    if ch in ['1', '2', '3', '4']:
        return True
    return False

# def __ping_jie(path_1, path_2):
#     wavfile_1 = path_1.split('/')[-1]  # 提取音频1的文件名，如“1.wav"
#     wavfile_2 = path_2.split('/')[-1]  # 提取音频2的文件名，如“2.wav"
#     new_file_name = wavfile_1.split('.')[0] + '_' + wavfile_2.split('.')[
#         0] + '.wav'  # 此行代码用于对拼接后的文件进行重命名，此处是将需要拼接的两个文件名用'_'连接起来
#
#     signal_1, sr1 = sf.read(path_1)  # 调用soundfile载入音频
#     signal_2, sr2 = sf.read(path_2)  # 调用soundfile载入音频
#
#     if sr1 == sr2:  # 判断待拼接的两则音频采样率是否一致，若一致则拼接
#         new_signal = np.concatenate((signal_1, signal_2), axis=0,dtype=np.float32)
#         fs = 44100
#         stream = sd.OutputStream(samplerate=fs)
#         with stream:
#             stream.write(new_signal)
#         # new_path = os.path.join(new_dir_path, new_file_name)
#         # print(new_path)
#         #
#         # sf.write(new_path, new_signal, sr1)
#
#     else:
#         print("所需拼接的音频采样率不一致，需检查一下哈~")
