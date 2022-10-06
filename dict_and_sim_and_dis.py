import math
import pandas as pd
import time
import torch
from tqdm import tqdm

def get_User_Venue_dict(dataset):
    print('getting get_User_Venue_dict')
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    User_Venue_dict={}#{User_id:[Venue_id,Venue_id],User_id:[....],.....}
    for line in dataset:
        User_id=line[0]
        Venue_id=line[1]
        if User_Venue_dict.get(User_id,-1)==-1:
            User_Venue_dict[User_id]=[Venue_id]
        else:
            if Venue_id not in User_Venue_dict[User_id]:
                User_Venue_dict[User_id].append(Venue_id)
    print('finish')
    return User_Venue_dict
def get_Venue_User_dict(dataset):
    print('getting Venue_User_dict')
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Venue_User_dict={}
    for line in dataset:
        User_id=line[0]
        Venue_id=line[1]
        if Venue_User_dict.get(Venue_id,-1)==-1:
            Venue_User_dict[Venue_id]=[User_id]
        else:
            if User_id not in Venue_User_dict[Venue_id]:
                Venue_User_dict[Venue_id].append(User_id)
    print('finish')
    return Venue_User_dict
def get_Category_Venue_dict(dataset):
    print('getting Category_Venue_dict')
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Category_Venue_dict={}
    for line in dataset:
        Venue_id=line[1]
        Category_id = line[2]
        if Category_Venue_dict.get(Category_id,-1)==-1:
            Category_Venue_dict[Category_id]=[Venue_id]
        else:
            if Venue_id not in Category_Venue_dict[Category_id]:
                Category_Venue_dict[Category_id].append(Venue_id)
    print('finish')
    return Category_Venue_dict
def get_Venue_Category_dict(dataset):
    print('getting Venue_Category_dict')
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Venue_Category_dict={}
    for line in dataset:
        Venue_id=line[1]
        Category_id = line[2]
        if Venue_Category_dict.get(Venue_id,-1)==-1:
            Venue_Category_dict[Venue_id]=[Category_id]
        else:
            if Category_id not in Venue_Category_dict[Venue_id]:
                Venue_Category_dict[Venue_id].append(Category_id)
    print('finish')
    return Venue_Category_dict
def get_User_User_sim_tensor(User_Venue_dict,user_num,venue_num):#计算用户中间的余弦相似度
    print('getting User_User_sim_tensor')
    User_Venue_tensor=torch.zeros(user_num,venue_num)
    x_index = []
    y_index = []
    num=0
    for key,value in User_Venue_dict.items():
        for venue in value:
            x_index.append(key)
            y_index.append(venue-user_num)
            num+=1
    value=torch.ones(num)
    index=(torch.LongTensor(x_index),torch.LongTensor(y_index))
    User_Venue_tensor.index_put_(index,value)
    sim_A=torch.matmul(User_Venue_tensor,User_Venue_tensor.T)
    temp_tensor_1=torch.sum(User_Venue_tensor,dim=1,keepdim=True)
    temp_tensor_1 = temp_tensor_1.sqrt()
    temp_tensor_2=temp_tensor_1.T
    sim_B=torch.matmul(temp_tensor_1,temp_tensor_2)
    User_User_sim_tensor=sim_A/sim_B
    print('finish')
    return User_User_sim_tensor
def get_Venue_Venue_threshold_tensor(dataset,user_num,venue_num,Distance_threshold):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]

    venue_coordinate_dict={}#{venue_id:[latitude,longitude]}
    for line in dataset:
        venue_id=line[1]
        latitude=float(line[3])
        longtitude=float(line[4])
        if venue_coordinate_dict.get(venue_id,-1)==-1:
            venue_coordinate_dict[venue_id]=[latitude,longtitude]

    print('getting Venue_Venue_threshold_tensor')

    B = torch.zeros(venue_num, 2).cuda()
    for venue_id_next in range(venue_num):
        B[venue_id_next] = torch.tensor(venue_coordinate_dict[venue_id_next + user_num])

    Venue_Venue_threshold_tensor=torch.zeros(venue_num,venue_num,dtype=torch.bool,device='cuda')#企图用tensor去算,结果发现更慢
    for venue_id in tqdm(range(venue_num)):#{venue_id:[latitude,longitude]}
        A=torch.tensor(venue_coordinate_dict[venue_id+user_num]).cuda()
        A=A-B
        A=A*A
        E=A[:,:1]
        F=A[:,1:]
        A=E+F
        A=torch.sqrt(A)
        A=-(A-Distance_threshold)
        A=torch.relu(A)
        A=A.type(dtype=torch.bool)
        Venue_Venue_threshold_tensor[venue_id]=torch.squeeze(A.T)

    print('finish')
    return Venue_Venue_threshold_tensor.cpu()
# def get_Venue_Venue_threshold_tensor(dataset,user_num,venue_num,Distance_threshold):#过于缓慢，已废弃
#     #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
#     Venue_Venue_threshold_tensor=torch.zeros(venue_num,venue_num,dtype=torch.bool)
#     venue_coordinate_dict={}#{venue_id:[latitude,longitude]}
#     for line in dataset:
#         venue_id=line[1]
#         latitude=float(line[3])
#         longtitude=float(line[4])
#         if venue_coordinate_dict.get(venue_id,-1)==-1:
#             venue_coordinate_dict[venue_id]=[latitude,longtitude]
#     from tqdm import tqdm
#     print('getting Venue_Venue_threshold_tensor')
#     for key_A,value_A in tqdm(venue_coordinate_dict.items()):#{venue_id:[latitude,longitude]}
#         for key_B,value_B in venue_coordinate_dict.items():
#             distence=math.sqrt(math.pow(value_A[0]-value_B[0],2)+math.pow(value_A[1]-value_B[1],2))
#             if distence<=Distance_threshold:
#                 Venue_Venue_threshold_tensor[key_A - user_num][key_B - user_num] = True
#     print('finish')
#     return Venue_Venue_threshold_tensor

def time_sort(user_venue_list):
    # utc_time= Tue Apr 03 21:42:44 +0000 2012
    # user_venue_list=[[venue_id,utctime],[..]...]
    user_venue_to_second_list = []
    # user_venue_to_second_list=[[venue_id,second],[]]
    for venue_id_and_utctime in user_venue_list:
        utctime_to_second = time.mktime(pd.to_datetime(venue_id_and_utctime[1]).timetuple())
        user_venue_to_second_list.append([venue_id_and_utctime[0], utctime_to_second])
    for venue_id_and_second_index in range(len(user_venue_to_second_list)):
        min_index = venue_id_and_second_index
        for next_index in range(len(user_venue_to_second_list)):
            if next_index > venue_id_and_second_index:
                if user_venue_to_second_list[next_index][1] < user_venue_to_second_list[min_index][1]:
                    min_index = next_index
        user_venue_to_second_list[venue_id_and_second_index], user_venue_to_second_list[min_index] = \
        user_venue_to_second_list[min_index], user_venue_to_second_list[venue_id_and_second_index]
    return user_venue_to_second_list

def get_User_Venue_time_dict(dataset):
    print('getting User_Venue_time_dict')
    User_Venue_time_dict={}#{user_id:[venue_id,venue_id]}按时间顺序排序用户去过的地点
    # [User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    print('step1/2')
    for line in tqdm(dataset):
        venue_id=line[1]
        user_id=line[0]
        utc_time=line[5]
        if User_Venue_time_dict.get(user_id,-1)==-1:
            User_Venue_time_dict[user_id]=[[venue_id,utc_time]]
        else:
            if [venue_id,utc_time] not in User_Venue_time_dict[user_id]:
                User_Venue_time_dict[user_id].append([venue_id, utc_time])
    print('step2/2')
    for key,value in tqdm(User_Venue_time_dict.items()):
        User_Venue_time_dict[key]=time_sort(value)
    print('finish')
    return User_Venue_time_dict

