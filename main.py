# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import numpy
import json
import pickle
from U_P_U_P import get_U_P_U_P_dict
import torch
from dict_and_sim_and_dis import *
from New_id_data import get_new_id_data
from U_P_C_P import get_U_P_C_P_dict



# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    dataset_add='dataset_tsmc2014/dataset_TSMC2014_TKY.txt'
    #dataset_add = 'dataset_tsmc2014/dataset_TSMC2014_NYC.txt'#首次跟换数据的时候要重新运行保存数据的代码
    #经过尝试，Distance_threshold=0.03时，每个用户的路径高达数千2000-15000
    Distance_threshold=0.03#地点间的欧氏距离阈值，超过的地点不算临近点#更改时需要重新运行get_Venue_Venue_threshold_tensor
    User_User_consin_threshold=0.8#用户余弦相似度阈值，超过的才能算邻居用户


    #获取新id数据
    #dataset,user_num,venue_num,category_num=get_new_id_data(dataset_add)#运行一次后保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_dataset.pkl'
    #pickle.dump(dataset,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    dataset=pickle.load(open(save_file_add,'rb'))


    #获取用户、地点、地点分类数量
    #save_User_Venue_Category_num_list=[user_num,venue_num,category_num]#保存数据的代码(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_save_User_Venue_Category_num_list.pkl'
    #pickle.dump(save_User_Venue_Category_num_list,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    save_User_Venue_Category_num_list=pickle.load(open(save_file_add,'rb'))
    user_num=save_User_Venue_Category_num_list[0]
    venue_num=save_User_Venue_Category_num_list[1]
    category_num=save_User_Venue_Category_num_list[2]


    #获取用户-地点的对应字典
    #User_Venue_dict=get_User_Venue_dict(dataset)#获取用户-地点的对应字典，用于找路径U——P#运行一次后保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_User_Venue_dict.pkl'
    #pickle.dump(User_Venue_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    User_Venue_dict=pickle.load(open(save_file_add,'rb'))


    #获取地点-用户的对应字典
    #Venue_User_dict=get_Venue_User_dict(dataset)#获取地点-用户的对应字典，用于找路径P——U#运行一次后保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_Venue_User_dict.pkl'
    #pickle.dump(Venue_User_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    Venue_User_dict=pickle.load(open(save_file_add,'rb'))


    #获取地点分类-地点的对应字典
    #Category_Venue_dict=get_Category_Venue_dict(dataset)#获取地点分类-地点的对应字典，用于找路径C-P#运行一次后保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_Category_Venue_dict.pkl'
    #pickle.dump(Category_Venue_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    Category_Venue_dict=pickle.load(open(save_file_add,'rb'))


    # 获取地点-地点分类的对应字典
    #Venue_Category_dict=get_Venue_Category_dict(dataset)#获取地点-地点分类的对应字典，用于找路径P-C#运行一次后保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_Venue_Category_dict.pkl'
    #pickle.dump(Venue_Category_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    Venue_Category_dict=pickle.load(open(save_file_add,'rb'))


    # 获取用户之间的余弦相似度矩阵UxU
    #User_User_sim_tensor=get_User_User_sim_tensor(User_Venue_dict, user_num, venue_num)#获取用户之间的余弦相似度矩阵UxU，用于给用户的邻居加上限制，只要高于0.8以上的邻居才可以加算作邻居用户#用一次就保存(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_User_User_sim_tensor.pkl'
    #with open(save_file_add,'wb')as file_to_save:#保存数据的代码(已保存，不再使用)
        #print('正在保存User_User_sim_tensor.pkl')
        #pickle.dump(User_User_sim_tensor, file_to_save)#保存数据的代码(已保存，不再使用)
        #print('保存成功')
    User_User_sim_tensor=pickle.load(open(save_file_add,'rb'))


    #用于给地点的近邻地点加上限制，只有距离较近的地点才可以算作临近地点
    #Venue_Venue_threshold_tensor=get_Venue_Venue_threshold_tensor(dataset,user_num, venue_num,Distance_threshold)#用于给地点的近邻地点加上限制，只有距离较近的地点才可以算作临近地点，运行一次保存到文件，后续要用就读取文件#（已保存,不再使用）
    save_file_add = dataset_add[:-4] + '_Venue_Venue_threshold_tensor.pkl'
    #print('正在保存User_User_sim_tensor.pkl')
    #pickle.dump(Venue_Venue_threshold_tensor,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    #print('保存成功')
    Venue_Venue_threshold_tensor=pickle.load(open(save_file_add,'rb'))


    #获取用户活动记录
    #User_Venue_time_dict=get_User_Venue_time_dict(dataset)#耗时十分钟，建议运行一次保存到文件，（已保存,不再使用）
    save_file_add = dataset_add[:-4] + '_User_Venue_time_dict.pkl'
    #pickle.dump(User_Venue_time_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    User_Venue_time_dict=pickle.load(open(save_file_add,'rb'))



    #获取用户-地点-用户-地点路径
    #U_P_U_P_dict=get_U_P_U_P_dict(User_Venue_dict,Venue_User_dict,User_User_sim_tensor,User_User_consin_threshold)#（已保存,不再使用）
    save_file_add = dataset_add[:-4] + '_U_P_U_P_dict.pkl'
    #pickle.dump(U_P_U_P_dict,open(save_file_add,'wb'))#保存数据的代码(已保存，不再使用)
    U_P_U_P_dict=pickle.load(open(save_file_add,'rb'))



    # 获取用户-地点-类别-地点路径
    U_P_C_P_dict=get_U_P_C_P_dict(User_Venue_dict,Venue_Category_dict,Category_Venue_dict,Venue_Venue_threshold_tensor,user_num)#获取用户-地点-类别-地点路径，通过地点间距离阈值矩阵限制临近点#耗时半个小时，用一次就保存#(已保存，不再使用)
    save_file_add = dataset_add[:-4] + '_U_P_C_P_dict.pkl'
    pickle.dump(U_P_C_P_dict, open(save_file_add, 'wb'))#保存数据的代码(已保存，不再使用)
    U_P_C_P_dict = pickle.load(open(save_file_add, 'rb'))

    print('hi')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
