from OpenSSL import crypto
import os
from app.core.config import settings

def generate_self_signed_cert():
    """
    HTTPS 서버를 위한 자체 서명 인증서를 생성합니다.
    """
    # 인증서 디렉토리 확인
    cert_dir = os.path.dirname(settings.CERT_FILE)
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)

    # 키 생성
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # 인증서 생성
    cert = crypto.X509()
    cert.get_subject().C = "KR"
    cert.get_subject().ST = "Seoul"
    cert.get_subject().L = "Seoul"
    cert.get_subject().O = "MCP Server"
    cert.get_subject().OU = "Development"
    cert.get_subject().CN = settings.HOST
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1년
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # 인증서 및 키 파일 저장
    with open(settings.CERT_FILE, "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(settings.KEY_FILE, "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    print(f"자체 서명 인증서 생성 완료: {settings.CERT_FILE}, {settings.KEY_FILE}")