from tqdm import tqdm
def get_U_P_C_P_dict(User_Venue_dict,Venue_Category_dict,Category_Venue_dict,Venue_Venue_threshold_tensor,user_num):
    U_P_C_P_dict = {}
    print('getting U_P_C_P_dict')
    for key ,value in tqdm(User_Venue_dict.items()):#key:用户id valuie:[地点id，地点id]
        U_P_C_P_dict[key]=[]
        for element in value:#地点id
            for category_id in Venue_Category_dict[element]:#{地点id：[地点分类id，地点分类id]...}
                for venue_id in Category_Venue_dict[category_id]:#{地点分类id：[地点id，地点id]...}
                    if Venue_Venue_threshold_tensor[element-user_num][venue_id-user_num]:#算出地点id对应到threshold_tensor中的索引
                        if venue_id not in U_P_C_P_dict[key]:
                            U_P_C_P_dict[key].append(venue_id)
    print('finish')
    return U_P_C_P_dict