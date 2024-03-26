import ssl
import socket
import dns.resolver
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pytz
from datetime import datetime, timezone, timedelta

def convert_utc_to_eastern_8(utc_time):
    # 将字符串转换为 datetime 对象（带时区信息）
    original_time = datetime.fromisoformat(str(utc_time))

    # 获取东八区的时区信息
    eastern_time_zone = timezone(timedelta(hours=8))

    # 将原始时间转换为东八区的时间
    eastern_time = original_time.astimezone(eastern_time_zone)

    return eastern_time

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
        not_valid_before = convert_utc_to_eastern_8(cert.not_valid_before_utc)
        not_valid_after = convert_utc_to_eastern_8(cert.not_valid_after_utc)
        tz = pytz.timezone('Asia/Shanghai')
        current_time = datetime.now(tz)
        remaining_days = (not_valid_after - current_time).days

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
#     details = get_cert_details('www.softbrews.com')
#     # if details:
#     #     print("Certificate details:")
#     #     for key, value in details.items():
#     #         print(f"{key}: {value}")
#     # else:
#     #     print("Failed to retrieve certificate details.")
#     print(details)

