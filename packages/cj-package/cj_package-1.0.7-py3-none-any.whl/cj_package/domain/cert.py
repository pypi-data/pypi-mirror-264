import ssl
import socket
import dns.resolver
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pendulum

def convert_utc_to_eastern_8(utc_time):
    """
    将日期时间字符串转换为东八区时间
    """
    # 将字符串转换为 Pendulum 对象
    utc_time = pendulum.parse(str(utc_time))

    # 将时区从 UTC 转换为东八区（北京时间）
    eastern_time = utc_time.in_timezone("Asia/Shanghai")

    return eastern_time

def counting_days(after_time):
    """
    计算两个日期时间之间的天数差异
    """
    # 获取当前时间,时区为东八区
    before_time = pendulum.now('Asia/Shanghai')
    after_time = pendulum.parse(str(after_time))

    # 计算天数差异
    days_diff = after_time.diff(before_time).days
    return days_diff

def get_cert_details(domain, dns_server='114.114.114.114') ->dict:
    """
    获取域名的证书信息,并返回证书的过期时间和剩余有效天数

    参数:
    domain (str): 域名
    dns_server (str): DNS 服务器地址，默认为 114.114.114.114

    返回:
    dict: 包含证书过期时间和剩余有效天数的字典
    """
    result = {
        'stats': True,
        'msg': '获取域名证书成功🍺🍺🍺🍺🍺',
        'data': ''
    }
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [dns_server]
        try:
            ips = resolver.resolve(domain, 'A')
        except Exception:
            raise Exception('解析域名失败,没有获取解析的ip')

        if len(ips) > 1:
            # 获取解析的所有ip
            ips = [str(ip) for ip in ips]
            result['data'] = dict(resolve_ips=ips)
            raise Exception('解析域名成功,但存在多个ip,请手动验证')
        ip = ips[0].to_text()
        # 建立连接并获取服务器证书
        with socket.create_connection((ip, 443)) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=domain) as ssock:
                der_cert = ssock.getpeercert(True)

        # 解析证书
        cert = x509.load_der_x509_certificate(der_cert, default_backend())

        # 计算过期剩余天数
        not_valid_before = convert_utc_to_eastern_8(cert.not_valid_before)
        not_valid_after = convert_utc_to_eastern_8(cert.not_valid_after)
        remaining_days = counting_days(not_valid_after)

        result['data'] = {
            'version': cert.version,
            'subject': cert.subject.rfc4514_string(),
            'issuer': cert.issuer.rfc4514_string(),
            'resolve_ip': ip,
            'not_valid_before': not_valid_before,
            'not_valid_after': not_valid_after,
            'expiration_days': remaining_days
        }
    except Exception as e:
        result['stats'] = False
        result['msg'] = str(e)

    return result

# if __name__ == "__main__":
#     details = get_cert_details('www.cjdropshipping.com')
# #     # if details:
# #     #     print("Certificate details:")
# #     #     for key, value in details.items():
# #     #         print(f"{key}: {value}")
# #     # else:
# #     #     print("Failed to retrieve certificate details.")
#     for k,v in details['data'].items():
#         print(k,v)
