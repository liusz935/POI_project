# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    data= {}#{用户：【地点，时间】}
    poi_lat_long={}
    user_list=[]
    venue_list=[]
    venue_category_list=[]

    with open('dataset_tsmc2014/dataset_TSMC2014_TKY.txt','r',encoding='utf8')as f:

        lines=f.readlines()
        for line in lines:
            print(line)
            line=line[:-1].split('\t')
            User_ID=int(line[0])
            Venue_ID=line[1]
            Venue_category_ID=line[2]
            Venue_category_name=line[3]#用不到
            Latitude=line[4]
            Longitude=line[5]
            Timezone_offset_in_minutes=line[6]#用不到
            UTC_time=line[7]

    # 在下面的代码行中使用断点来调试脚本。
    # 1. User ID (anonymized)
    # 2. Venue ID (Foursquare)
    # 3. Venue category ID (Foursquare)
    # 4. Venue category name (Fousquare)
    # 5. Latitude
    # 6. Longitude
    # 7. Timezone offset in minutes (The offset in minutes between when this check-in occurred and the same time in UTC)
    # 8. UTC time
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
