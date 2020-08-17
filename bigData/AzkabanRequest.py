import json
import os
import re
import time

# 配置项
USER_NAME = ""
PASSWORD = "3775448903b6a141ffcdeb83e942d710"
HOST = "https://azkaban.jpushoa.com"
START = 0
EXEC_LENGTH = 1
HOST_MANAGER = "https://azkaban.jpushoa.com/manager"

OFFSET = 0
LOG_LENGTH = 99999999
HOST_EXECUTOR = "https://azkaban.jpushoa.com/executor"

HIVE_QUERY_ID_URL = 'http://yarn-tools.dp.jpushoa.com/api/v1/application/logs/?hive_query_id='
APPLICATION_ID_URL = 'http://yarn-tools.dp.jpushoa.com/api/v1/application/logs/?application_id='


def get_session_id():
    """申请 session_id"""
    time.sleep(10)
    login_req = 'curl -s -k -X POST --data "action=login&username={user_name}&password={password}" {host}'\
        .format(host=HOST, user_name=USER_NAME, password=PASSWORD)
    print("cmd =", login_req)
    login_resp = os.popen(login_req).read()
    data = json.loads(login_resp)
    if "session.id" in data:
        session_id = data["session.id"]
    else:
        raise Exception("session.id获取失败!!!")
    return session_id


def get_execid(session_id, project, flow):
    """获取execid"""
    time.sleep(10)
    execid_req = 'curl -k --get --data "session.id={session_id}&ajax=fetchFlowExecutions&project={project}&flow={flow}&start={start}&length={length}" {host_manager}'\
        .format(session_id=session_id, project=project, flow=flow, start=START, length=EXEC_LENGTH, host_manager=HOST_MANAGER)
    print("cmd =", execid_req)
    execid_resp = os.popen(execid_req).read()
    data = json.loads(execid_resp)
    if "executions" in data:
        executions = data["executions"][0]
        if "execId" in executions:
            execid = executions["execId"]
        else:
            raise Exception("executions中不存在execId！！！")
    else:
        raise Exception("executions获取失败！！！")
    return execid


def get_log(session_id, execid, jobid):
    """获取log，抓取queryIds"""
    time.sleep(10)
    log_req = 'curl -k --data "session.id={session_id}&ajax=fetchExecJobLogs&execid={execid}&jobId={jobid}&offset={offset}&length={length}" {host_executor}' \
        .format(session_id=session_id, execid=execid, jobid=jobid, offset=OFFSET, length=LOG_LENGTH,
                host_executor=HOST_EXECUTOR)
    print("cmd =", log_req)
    log_resp = os.popen(log_req).read()
    return log_resp



def hive_process(log_resp):
    """处理抓取的数据结果"""
    time.sleep(300)
    queryids = set(re.findall(r'hive_\d{14}[\w\-]+', log_resp))
    print("queryids", queryids)
    if len(queryids) == 0:
        return


def spark_process(log_resp):
    """处理抓取的数据结果"""
    time.sleep(300)
    applicationids = set(q.strip() for q in re.findall(r' application_[\d_]+', log_resp))
    print("queryids", applicationids)
    if len(applicationids) == 0:
        return

def main():
    # 配置项：项目 flow job
    jobs = [["icredit", "test_log_view", "test_log"]]
    for project, flow, jobid in jobs:
        print("当前执行任务：", project, flow, jobid)
        # 获取session_id
        session_id = get_session_id()
        # 获取execid
        execid = get_execid(session_id, project, flow)
        # 获取log
        log_resp = get_log(session_id, execid, jobid)
        # 打印统计结果
        print("部分job_log:", log_resp[-999:])
        hive_process(log_resp)
        spark_process(log_resp)


if __name__ == "__main__":
    main()
