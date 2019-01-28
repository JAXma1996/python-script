import re

# 定义两个字典用于存放数据
capture_map = {}
hit_map = {}


def find_device_upload_info_count():
    with open("E:\\intellif.log", "r", encoding='utf-8') as file:
        for line in file:
            # 正则表达式 匹配ip=xxx.xx.xx.xxx某某某某某的日志
            hit_match_obj = re.search(r'ip=((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))(.){6}', line)
            if hit_match_obj:
                hit_string = hit_match_obj.group()
                # 根据字符串切割获取ip
                ip_key = hit_match_obj.group()[1: hit_match_obj.group().index("回")]
                if hit_string.find('识别') != -1:
                    if ip_key not in hit_map.keys():
                        hit_map[ip_key] = 1
                    else:
                        hit_map[ip_key] += 1
                if hit_string.find('抓拍') !=-1:
                    if ip_key not in capture_map.keys():
                        capture_map[ip_key] = 1
                    else:
                        capture_map[ip_key] += 1


if __name__ == '__main__':
    find_device_upload_info_count()
    print(capture_map)
    print(hit_map)
    print('在该日志中有'+str(capture_map.keys().__len__())+'盒子回调抓拍接口')
    print('在该日志中有'+str(hit_map.keys().__len__())+'盒子回调识别接口')

