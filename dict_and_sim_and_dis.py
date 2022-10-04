import math

import torch
def get_User_Venue_dict(dataset):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    User_Venue_dict={}#{User_id:[Venue_id,Venue_id],User_id:[....],.....}
    for line in dataset:
        User_id=line[0]
        Venue_id=line[1]
        if User_Venue_dict.get(User_id,-1)==-1:
            User_Venue_dict[User_id]=[Venue_id]
        else:
            User_Venue_dict[User_id].append(Venue_id)
    return User_Venue_dict
def get_Venue_User_dict(dataset):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Venue_User_dict={}
    for line in dataset:
        User_id=line[0]
        Venue_id=line[1]
        if Venue_User_dict.get(Venue_id,-1)==-1:
            Venue_User_dict[Venue_id]=[User_id]
        else:
            Venue_User_dict[Venue_id].append(User_id)
    return Venue_User_dict
def get_Category_Venue_dict(dataset):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Category_Venue_dict={}
    for line in dataset:
        Venue_id=line[1]
        Category_id = line[2]
        if Category_Venue_dict.get(Category_id,-1)==-1:
            Category_Venue_dict[Category_id]=[Venue_id]
        else:
            Category_Venue_dict[Category_id].append(Venue_id)
    return Category_Venue_dict
def get_Venue_Category_dict(dataset):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Venue_Category_dict={}
    for line in dataset:
        Venue_id=line[1]
        Category_id = line[2]
        if Venue_Category_dict.get(Venue_id,-1)==-1:
            Venue_Category_dict[Venue_id]=[Category_id]
        else:
            Venue_Category_dict[Venue_id].append(Category_id)
    return Venue_Category_dict
def get_User_User_sim_tensor(User_Venue_dict,user_num,venue_num):#计算用户中间的余弦相似度
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
    return User_User_sim_tensor
def get_Venue_Venue_distence_tensor(dataset,user_num,venue_num):
    #[User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time]
    Venue_Venue_distence_tensor=torch.zeros(venue_num,venue_num)
    venue_coordinate_dict={}#{venue_id:[latitude,longitude]}
    for line in dataset:
        venue_id=line[1]
        latitude=float(line[3])
        longtitude=float(line[4])
        if venue_coordinate_dict.get(venue_id,-1)==-1:
            venue_coordinate_dict[venue_id]=[latitude,longtitude]
    from tqdm import tqdm
    for key_A,value_A in tqdm(venue_coordinate_dict.items()):#{venue_id:[latitude,longitude]}
        for key_B,value_B in venue_coordinate_dict.items():
            Venue_Venue_distence_tensor[key_A-user_num][key_B-user_num]=math.sqrt(math.pow(value_A[0]-value_B[0],2)+math.pow(value_A[1]-value_B[1],2))
    return Venue_Venue_distence_tensor

