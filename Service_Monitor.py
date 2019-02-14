import smtplib
import email.mime.text
import email.mime.multipart
import time
import os
import requests
import  datetime
import queue

# 判断api失效的时间间隔，单位s
_judge_api_invalid_interval = 180
# cpu 使用率最低
_cpu_use_min = 20
# cpu 使用率最高
_cpu_use_max = 70
# cpu判断分钟间隔
_cpu_judge_interval = 5
# cpu 一定间隔判断多少次
_cpu_judge_times_in_inteval = 3
# cpu的使用率队列
_cpu_use_queue = queue.Queue(_cpu_judge_interval)


def send_email(message):
    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login("ifbuilding@intellif.com", "Admin123")
    smtp.sendmail("ifbuilding@intellif.com", "ma.haibin@intellif.com", message.as_string())
    smtp.quit()


def get_api_info_by_shell(type):
    api_count = os.popen("lsof -t /var/www/html/"+type+"/api/api.jar|wc -l").read()
    return api_count


def judge_cpu_status(allJson,msg):
    global _cpu_judge_interval
    cpuUse = allJson['cpu']['total']
    if cpuUse > _cpu_use_max or cpuUse < _cpu_use_min :
        now_time = time.time()
        if _cpu_judge_interval == 0 :
            if _cpu_use_queue.qsize()>_cpu_judge_times_in_inteval:
                print("我已经发邮件啦")
            _cpu_judge_interval = 5
            _cpu_use_queue.queue.clear()
        else:
            _cpu_use_queue.put(int(now_time))
            _cpu_judge_interval -= 1
        print(cpuUse)


def get_api_info_by_trgg():
    r = requests.get("http://192.168.11.123:61208/api/2/all")
    return r.json()


if __name__ == '__main__':
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = 'duanx'
    msg['From'] = 'ifbuilding@intellif.com'
    msg['To'] = 'ma.haibin@intellif.com'
    content = '''
    
            '''
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)
    send_email(msg)
    test_api_status = 0
    ifaas_api_status = 0
    flag = 1
    while flag == 1:
        returnJson = get_api_info_by_trgg()
        judge_cpu_status(returnJson,msg)
        time.sleep(1)

    # for processItem in processList:

        # print("--- "+processList[key])

    #     ifaas_api_count = get_api_info("ifaas")
    #     test_api_count = get_api_info("test")
    #     print("服务查看结果 = test" + str(test_api_count) + " ifaas " + str(ifaas_api_count))
    #     if ifaas_api_count == '0':
    #         ifaas_api_status += 1
    #     if test_api_count == 0:
    #         test_api_status += 1
    #     if test_api_status == _judge_api_invalid_interval:
    #         # 行定时api启动失败邮件发送
    #         print("send worning")
    #     if ifaas_api_status == _judge_api_invalid_interval:
    #         # 执行业务api的邮件发送
    #         print("send worning")
    #     time.sleep(3)
    #     print("睡眠三秒钟开始判断！"+str(test_api_status) + " ifaas "+str(ifaas_api_status))


