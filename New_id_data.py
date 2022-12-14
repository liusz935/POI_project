def get_new_id_data(dataset_add):
    print('getting new_id_data')
    dataname=dataset_add[:-4]
    data= []#装所有的数据
    user_list=[]#装用户
    venue_list=[]#装地点
    venue_category_list=[]#装地点分类

    with open(dataset_add,'r',encoding='utf8')as f:

        lines=f.readlines()
        for line in lines:
            #print(line)
            line=line[:-1].split('\t')
            User_ID=int(line[0])
            Venue_ID=line[1]
            Venue_category_ID=line[2]
            #Venue_category_name=line[3]#用不到
            Latitude=line[4]
            Longitude=line[5]
            #Timezone_offset_in_minutes=line[6]#用不到
            UTC_time=line[7]
            data.append([User_ID,Venue_ID,Venue_category_ID,Latitude,Longitude,UTC_time])
            user_list.append(User_ID)
            venue_list.append(Venue_ID)
            venue_category_list.append(Venue_category_ID)
    #更新id前去重
    user_list=list(set(user_list))
    venue_list=list(set(venue_list))
    venue_category_list=list(set(venue_category_list))
    user_num=len(user_list)
    venue_num=len(venue_list)
    category_num=len(venue_category_list)
    print('用户数量：'+str(len(user_list))+'\n'+'地点数量：'+str(len(venue_list))+'\n'+'地点分类数量：'+str(len(venue_category_list))+'\n')
    #数据中的ID不能直接用，要新生成id，因为要生成用户、地点异构图，所以要统一用户和地点的ID，使其连续，地点类别不在图中，单独生成新id
    new_user_id_dict={}
    new_venue_id_list_dict={}
    new_venue_category_id_dict={}
    new_id_index=0
    for i in range(len(user_list)):
        new_user_id_dict[user_list[i]] = new_id_index
        new_id_index+=1
    for i in range(len(venue_list)):
        new_venue_id_list_dict[venue_list[i]] = new_id_index
        new_id_index+=1
    new_id_index = 0
    for i in range(len(venue_category_list)):
        new_venue_category_id_dict[venue_category_list[i]] = new_id_index
        new_id_index+=1
    #保存新旧id对应字典到文件
    file_name=dataname+'_old_user_id_to_new_user_id.csv'
    with open(file_name,'w',encoding='utf-8')as f:
        for key ,value in new_user_id_dict.items():
            s=str(key)+','+str(value)+'\n'
            f.write(s)
    file_name = dataname + '_old_venue_id_to_new_venue_id.csv'
    with open(file_name,'w',encoding='utf-8')as f:
        for key ,value in new_venue_id_list_dict.items():
            s=str(key)+','+str(value)+'\n'
            f.write(s)
    file_name = dataname + '_old_venue_category_id_to_new_venue_category_id.csv'
    with open(file_name,'w',encoding='utf-8')as f:
        for key ,value in new_venue_category_id_dict.items():
            s=str(key)+','+str(value)+'\n'
            f.write(s)
    #更新data中数据的id
    for line_id in range(len(data)):
        data[line_id][0]=new_user_id_dict[data[line_id][0]]
        data[line_id][1]=new_venue_id_list_dict[data[line_id][1]]
        data[line_id][2]=new_venue_category_id_dict[data[line_id][2]]
    #返回数据
    print('finish')
    return data,user_num,venue_num,category_num
    # 470	49bbd6c0f964a520f4531fe3	4bf58dd8d48988d127951735	Arts & Crafts Store	40.719810375488535	-74.00258103213994	-240	Tue Apr 03 18:00:09 +0000 2012
    # 1. User ID (anonymized)
    # 2. Venue ID (Foursquare)
    # 3. Venue category ID (Foursquare)
    # 4. Venue category name (Fousquare)
    # 5. Latitude
    # 6. Longitude
    # 7. Timezone offset in minutes (The offset in minutes between when this check-in occurred and the same time in UTC)
    # 8. UTC time