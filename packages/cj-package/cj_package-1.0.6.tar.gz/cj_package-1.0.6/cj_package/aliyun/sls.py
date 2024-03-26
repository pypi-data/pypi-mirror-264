import os
from aliyun.log import LogClient, GetLogsRequest

def read_env():
    """
    读取环境变量获取accessKeyId和accessKey
    """
    accessKeyId = os.environ.get('ALIYUN_ACCESS_KEY_ID')
    accessKey = os.environ.get('ALIYUN_ACCESS_KEY')
    if not accessKeyId or not accessKey:
        raise Exception('请设置环境变量ALIYUN_ACCESS_KEY_ID和ALIYUN_ACCESS_KEY')
    return accessKeyId, accessKey

def hz_ingress_log(from_time, to_time, query, accessKeyId=None, accessKey=None) -> list:
    """
    查询杭州的ingress日志
    @param from_time: 开始时间戳
    @param to_time: 结束时间戳
    @param query: 查询条件
    @param accessKeyId: 阿里云accessKeyId
    @param accessKey: 阿里云accessKey
    @return: 查询结果(List类型)
    """
    chaxun_result = []
    # 日志服务的域名。更多信息，请参见服务入口。此处以杭州为例，其它地域请根据实际情况填写。
    endpoint = "cn-hangzhou.log.aliyuncs.com"
    # 判断是否传入accessKeyId和accessKey
    if not accessKeyId or not accessKey:
        accessKeyId, accessKey = read_env()
    # 创建日志服务Client
    client = LogClient(endpoint, accessKeyId, accessKey)
    # Project名称。
    project_name = "hz-k8s"
    # Logstore名称
    logstore_name = "nginx-ingress"
    request = GetLogsRequest(project_name, logstore_name, from_time, to_time, query=query)
    response = client.get_logs(request)
    for log in response.get_logs():
        chaxun_result.append(dict(log.contents))
    return chaxun_result


def us_ingress_log(from_time, to_time, query, accessKeyId=None, accessKey=None) -> list:
    """
    查询美国的ingress日志
    @param from_time: 开始时间戳
    @param to_time: 结束时间戳
    @param query: 查询条件
    @param accessKeyId: 阿里云accessKeyId
    @param accessKey: 阿里云accessKey
    @return: 查询结果(List类型)
    """
    chaxun_result = []
    # 日志服务的域名。更多信息，请参见服务入口。此处以杭州为例，其它地域请根据实际情况填写。
    endpoint = "us-west-1.log.aliyuncs.com"
    # 创建日志服务Client。
    # 判断是否传入accessKeyId和accessKey
    if not accessKeyId or not accessKey:
        accessKeyId, accessKey = read_env()
    client = LogClient(endpoint, accessKeyId, accessKey)
    # Project名称。
    project_name = "usa-k8s"
    # Logstore名称
    logstore_name = "usa-ingress"
    request = GetLogsRequest(project_name, logstore_name, from_time, to_time, query=query)
    response = client.get_logs(request)
    for log in response.get_logs():
        chaxun_result.append(dict(log.contents))
    return chaxun_result
