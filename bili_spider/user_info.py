import time

user_config = {
    'name': "//span[@id='h-name']/text()",
    'gender': "//span[@id='h-gender']/@class",
    'level': "//a[@class='h-level m-level']/@lvl",
    'register_time': "//div[@class='item regtime']/span[@class='text']/text()",
    'location': "//div[@class='item geo']/span[@class='text']/text()"
}

extend_config = {
    'head_img': "//div[@class='h-avatar']/img/@src",
    'sign': "//div[@class='h-sign']/text()",
    'birthday': "//div[@class='item birthday']/span[@class='text']/text()",
    'follow_num': "//a[@href='#!/fans/follow']/p[@class='n-data-v space-attention']/text()",
    'fans_num': "//a[@href='#!/fans/fans']/p[@class='n-data-v space-fans']/text()"
}


def deal_api_data(data):
    info = {}
    extend_info = {}
    try:
        info['name'] = data['name']
        if data['sex'] == '男':
            info['gender'] = 1
        else:
            if data['sex'] == '女':
                info['gender'] = 0
            else:
                info['gender'] = -1
        info['location'] = data['place'] or '未填写'
        info['register_time'] = data['regtime']
        info['level'] = data['level_info']['current_level']
        extend_info['fans_num'] = data['fans']
        extend_info['follow_num'] = data['friend']
        extend_info['sign'] = data['sign'].replace('\'', '#')
        extend_info['birthday'] = data['birthday'][5:]
        extend_info['head_img'] = data['face']
        return info, extend_info
    except:
        return {}, {}


def deal_user_info(data):
    for key in data.keys():
        try:
            func = "deal_" + str(key)
            data[key] = eval(func)(str(data[key]).replace('\'', '#') or '')
        except Exception as e:
            print(key, e)
    return data


def deal_name(name):
    if name and (name != "哔哩哔哩"):
        return name
    else:
        return ''


def deal_gender(gender):
    if gender == 'icon gender male':
        return 1
    else:
        if gender == 'icon gender female':
            return 0
        else:
            return -1


def deal_level(level):
    if level.isdigit():
        return int(level)
    else:
        return 0


def deal_register_time(register_time):
    try:
        date_structs = str(register_time).replace("注册于 ", "").split('-')
        date_structs = map(int, date_structs)
        date_structs = tuple(date_structs) + (0, 0, 0, 0, 0, 0)
        return time.mktime(date_structs)
    except Exception as e:
        return 0


def deal_head_img(head_img):
    return head_img


def deal_sign(sign):
    return str(sign + ' ')


def deal_birthday(birthday):
    return birthday


def deal_follow_num(follow_num):
    if follow_num.isdigit():
        return int(follow_num)
    else:
        return 0


def deal_fans_num(fans_num: str):
    if fans_num.isdigit():
        return int(fans_num)
    else:
        num = fans_num.rstrip('万').rstrip(' ').lstrip(' ')
        if len(num) < len(fans_num):
            return float(num) * 10000
        else:
            return 0


def deal_location(location):
    return location or ''

