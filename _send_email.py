#!/usr/bin/env python3
"""栀安晨间新闻早报 · 邮件发送

用法:
  python3 _send_email.py <邮件正文文件.md>

必须配置 QQ 邮箱 SMTP 授权码:
  1. 登录 QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务
  2. 开启并获取授权码（16位字符，不是 QQ 密码）
  3. 将授权码写入 _email_config.json（格式见下方）

首次使用必须创建 _email_config.json:
  {
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "sender": "3865560266@qq.com",
    "receiver": "3865560266@qq.com",
    "auth_code": "你的QQ邮箱授权码"
  }
"""

import smtplib
import json
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "_email_config.json")


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] 配置文件不存在: {CONFIG_PATH}")
        print("请创建 _email_config.json，格式见脚本头部注释。")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def send_email(config: dict, subject: str, body: str) -> bool:
    """发送邮件，成功返回 True，失败返回 False"""
    msg = MIMEMultipart("alternative")
    msg["From"] = config["sender"]
    msg["To"] = config["receiver"]
    msg["Subject"] = Header(subject, "utf-8")

    # 纯文本 + HTML 双版本
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(body.replace("\n", "<br>"), "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], timeout=15) as s:
            s.login(config["sender"], config["auth_code"])
            s.sendmail(config["sender"], config["receiver"], msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] SMTP 认证失败 —— 授权码是否正确？注意：不是 QQ 密码，是16位授权码。")
        return False
    except Exception as e:
        print(f"[ERROR] 邮件发送失败: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 _send_email.py <邮件正文文件>")
        sys.exit(1)

    body_file = sys.argv[1]
    if not os.path.exists(body_file):
        print(f"[ERROR] 文件不存在: {body_file}")
        sys.exit(1)

    with open(body_file, "r", encoding="utf-8") as f:
        body = f.read()

    # 从正文第一行提取标题（格式: # 栀安早报 | ...）
    lines = body.strip().split("\n")
    subject = "栀安早报"
    for line in lines:
        if line.startswith("# "):
            subject = line[2:].strip()
            break

    config = load_config()
    success = send_email(config, subject, body)

    if success:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] 邮件发送成功 → {config['receiver']}")
        sys.exit(0)
    else:
        sys.exit(1)
