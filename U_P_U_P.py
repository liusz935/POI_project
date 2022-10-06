def get_U_P_U_P_dict(User_Venue_dict,Venue_User_dict,User_User_sim_tensor,User_User_consin_threshold):
    print('getting U_P_U_P_dict')
    print('step 1/2')
    from tqdm import tqdm
    User_Venue_User_dict={}#用户-候选邻居用户{user_id:[user_id,user_id]....}
    for key_in_U_V , value_in_U_V in tqdm(User_Venue_dict.items()):
        User_Venue_User_dict[key_in_U_V]=[]
        for venue_id in value_in_U_V:
            User_Venue_User_dict[key_in_U_V]+=Venue_User_dict[venue_id]
        User_Venue_User_dict[key_in_U_V]=list(set(User_Venue_User_dict[key_in_U_V]))#去重
    print('step 2/2')
    User_Venue_User_Venue_dict={}
    for key_in_U_V_U,value_in_U_V_U in tqdm(User_Venue_User_dict.items()):
        User_Venue_User_Venue_dict[key_in_U_V_U]=[]
        for u_id in value_in_U_V_U:
            if User_User_sim_tensor[key_in_U_V_U][u_id]>User_User_consin_threshold:#只有余弦相似度高于阈值才算邻居用户
                User_Venue_User_Venue_dict[key_in_U_V_U]+=User_Venue_dict[u_id]
        User_Venue_User_Venue_dict[key_in_U_V_U]=list(set(User_Venue_User_Venue_dict[key_in_U_V_U]))#去重
    print('finish')
    return User_Venue_User_Venue_dict

