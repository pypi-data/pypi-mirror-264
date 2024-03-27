
import numpy as np
import torch
import os
import glob
from os.path import join,basename,dirname,isdir,isfile
import datetime
import logging

'''
https://www.barwe.cc/2022/06/24/dist-my-pkg-to-pypi

'''


DELIMITER_INFO=None


def get_info_numpy(varNp):
    '''
    import sys 
    sys.path.append("/Users/hjy/workspace/00_utils_sync/utils_folder")
    from utils import get_numpy_info
    '''
    # print("-"*20)
    print("".center(50, "-"))
    print(f"nummpy's shape is :{varNp.shape}")
    print(f"nummpy's dtype is :{varNp.dtype}")
    print(f"nummpy's max  num is :{varNp.max()}")
    print(f"nummpy's mean num is :{varNp.mean()}")
    print(f"nummpy's min  num is :{varNp.min()}")

    print(f"==>> varNp: {varNp}")
    # plt.hist(arrayNp.ravel(), bins='auto')
    # plt.ylim(10000)
    # plt.hist(arrayNp.ravel(), bins=255)
    # plt.show()
    # plt.close()

def get_info_tensor(varTorch):
    '''
    import sys 
    sys.path.append("/Users/hjy/workspace/00_utils_sync/utils_folder")
    from utils import get_numpy_info
    '''
    # print("-"*20)
    print("".center(50, "-"))
    print(f"tensor's shape is :{varTorch.shape}")
    print(f"tensor's dtype is :{varTorch.dtype}")
    print(f"tensor's device is :{varTorch.device}")
    print(f"tensor's max  num is :{varTorch.max()}")
    print(f"tensor's mean num is :{varTorch.mean()}")
    print(f"tensor's min  num is :{varTorch.min()}")
    # plt.hist(arrayNp.ravel(), bins='auto')
    # plt.ylim(10000)
    # plt.hist(arrayNp.ravel(), bins=255)
    # plt.show()
    # plt.close()


def get_info_list(a_list=None):
    print(f"==>> len(a_list): {len(a_list)}")
    if len(a_list)>0:
        # print(f"==>> a_list[0]: {a_list[0]}")
        if isinstance(a_list[0], np.ndarray):
            get_info_numpy(a_list[0])
        elif isinstance(a_list[0], torch.Tensor):
            get_info_tensor(a_list[0])


def get_info_dict(a_dict=None):
    # a_dict = {'a':1,'b':np.array([1,2]),'c':[4,2]}
    count = 0
    for k, v in a_dict.items():
        count+=1
        print("".center(25, "="),f"keys num = {count}","".center(25, "="))
        print(f"key, type(value) is : {k}: {type(v)}")

        if type(v) in (int,float,complex):
            print("".center(50, "-"))
            print(f"{k}: {v}")
        
        if isinstance(v, np.ndarray):
            get_info_numpy(v)
        
        if isinstance(v, torch.Tensor):
            get_info_tensor(v)

        if isinstance(v, tuple):
            print("".center(50, "-"))
            print(f"len of tuple is: {len(v)}")
            for i in range(len(v)):
                print(f"==>> type(v[i]): {type(v[i])}")

        if isinstance(v, list):
            print("".center(50, "-"))
            # print(f"len of list is: {len(v)}")
            # print(f"value is: {v}")
            get_info_list(v)

        if isinstance(v, dict):
            print(f"{k}:{v.keys()}")


def get_info(v):
    if isinstance(v, np.ndarray):
        get_info_numpy(v)
    elif isinstance(v, torch.Tensor):
        get_info_tensor(v)
    elif isinstance(v, list):
        get_info_list(v)
    elif isinstance(v, dict):
        get_info_dict(v)
    else:
        print("Func get_info get unknown type!")





# get_dict_info(a_dict=None)
def get_dict_content(a_dict):
    for k, v in a_dict.items():
        print('## dict content:')
        print(f'  {k}:{v}')
        # print(f'  {a_dict.get(key)}')
# a = {'abc':1, 'e':np.array([1,2])}
# prt_dict_content(a)
        
def get_info_npz_file(npzPath):
    npzFile = np.load(npzPath)
    # print(npzFile.files)
    for k in npzFile.files:
        print(f'key: {k}')
        print(f"   {k}'s shape is :{npzFile[k].shape}")
        print(f"   {k}'s dtype is :{npzFile[k].dtype}")
        print(f"   {k}'s max  num is :{npzFile[k].max()}")
        print(f"   {k}'s mean num is :{npzFile[k].mean()}")
        print(f"   {k}'s min  num is :{npzFile[k].min()}")

# get_info_npz_file('/home/hjy/workspace/interp_photo/04_inr/data/ERF/train_mini_ev_voxel_fp16/0001/1_4_events/04/00000_0t.npz')


def get_info_npy_file(npyPath):
    arrayNp = np.load(npyPath)
    get_info_numpy(arrayNp)

DELIMITER_PRINT=None

def print_list(a_list):
    import inspect
    frame = inspect.currentframe().f_back
    name_a_list=None
    for name, value in frame.f_locals.items():
        if value is a_list:
            name_a_list = name
    if name_a_list is not None:
        print(f'    {name_a_list}')
    for i, v in enumerate(a_list):
        if i<3 or i > len(a_list)-3:
            print(f"    {i}: {v}")
        elif i==3:
            print(f"    ...")

def print_list_all(a_list):
    import inspect
    frame = inspect.currentframe().f_back
    name_a_list=None
    for name, value in frame.f_locals.items():
        if value is a_list:
            name_a_list = name
    if name_a_list is not None:
        print(f'    {name_a_list}')
    for i, v in enumerate(a_list):

        print(f"        {i}: {v}")




DELIMITER_PATH=None
def get_home_dir():
    '''
    from utils import getHomeDir
    '''
    home = os.path.expanduser("~")
    print(f'home path is {home}')
    return home



#%%
def get_subfolder_path_list(data_root, verbose=False):
    # folders_path_l = [join(data_root,f) for f in os.listdir(data_root) if isdir(join(data_root,f))]
    folders_path_l = [p for p in sorted(glob.glob(f'{data_root}/*')) if os.path.isdir(p)]
    if verbose:
        print(f"==>> folders_path_l: {folders_path_l}")
    return folders_path_l

def get_subfile_path_list(data_root, verbose=False):
    '''
    other need suffix
        file_list = sorted(glob.glob("{}".format(folderPath) + f"/*.{suffix}"))
    
    '''
    # files_path_l = [join(data_root,f) for f in os.listdir(data_root) if isfile(join(data_root,f))]
    files_path_l = [p for p in sorted(glob.glob(f'{data_root}/*')) if os.path.isfile(p)]
    if verbose:
        print(f"==>> files_path_l: {files_path_l}")
    return files_path_l




def get_timestamp():
    return datetime.now().strftime('%y%m%d-%H%M%S')


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def mkdirs(paths):
    if isinstance(paths, str):
        mkdir(paths)
    else:
        for path in paths:
            mkdir(path)


def mkdir_and_rename(path):
    if os.path.exists(path):
        new_name = path + '_archived_' + get_timestamp()
        print('Path already exists. Rename it to [{:s}]'.format(new_name))
        logger = logging.getLogger('base')
        logger.info('Path already exists. Rename it to [{:s}]'.format(new_name))
        os.rename(path, new_name)
    os.makedirs(path)


