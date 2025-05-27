#!/usr/bin/env python
import os
import subprocess
import sys

def generate_ssl_certs():
    """
    자체 서명된 SSL 인증서를 생성합니다.
    """
    print("SSL 인증서 생성 중...")
    
    # 이미 인증서가 있는지 확인
    if os.path.exists("cert.pem") and os.path.exists("key.pem"):
        print("인증서가 이미 존재합니다. 다시 생성하려면 cert.pem과 key.pem 파일을 삭제하세요.")
        return
    
    try:
        # OpenSSL 명령어 실행
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes", 
            "-out", "cert.pem", "-keyout", "key.pem", "-days", "365",
            "-subj", "/CN=localhost"
        ], check=True)
        print("인증서가 성공적으로 생성되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"인증서 생성 중 오류가 발생했습니다: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("OpenSSL이 설치되어 있지 않습니다. OpenSSL을 설치한 후 다시 시도하세요.")
        sys.exit(1)

if __name__ == "__main__":
    generate_ssl_certs()