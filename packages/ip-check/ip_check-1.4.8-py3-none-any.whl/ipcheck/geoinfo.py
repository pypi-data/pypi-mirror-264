#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import geoip2.database
from typing import List
from ipcheck.app.ip_info import IpInfo
from ipcheck.app.utils import is_ip_address, download_file, write_file
import argparse
import configparser
import subprocess
import sys

GEO2CITY_DB_NAME = 'GeoLite2-City.mmdb'
GEO2ASN_DB_NAME = 'GeoLite2-ASN.mmdb'
GEO2CITY_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2CITY_DB_NAME)
GEO2ASN_DB_PATH = os.path.join(os.path.dirname(__file__), GEO2ASN_DB_NAME)
GEO_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'geo.ini')
GEO_DEFAULT_CONFIG = '''[common]
# asn 数据库下载地址
db_asn_url = xxxx
# city 数据库下载地址
db_city_url = yyyy
'''

def download_geo_db(url :str, path):
    print('正在下载geo database ... ...')
    res = download_file(url, path)
    result_str = '成功。' if res else '失败！'
    print('下载geo database到{} {}'.format(path, result_str))


def check_geo_loc_db():
    if os.path.exists(GEO2CITY_DB_PATH):
        return True
    else:
        print('ip 数据库不存在，请手动下载{} 到 {}'.format(GEO2CITY_DB_NAME, GEO2CITY_DB_PATH))
        return False

def check_geo_asn_db():
    if os.path.exists(GEO2ASN_DB_PATH):
        return True
    else:
        print('ip 数据库不存在，请手动下载{} 到 {}'.format(GEO2ASN_DB_NAME, GEO2ASN_DB_PATH))
        return False


def get_geo_asn(infos: List[IpInfo]) -> List[IpInfo]:
    res = []
    if check_geo_asn_db():
        with geoip2.database.Reader(GEO2ASN_DB_PATH) as reader:
            for info in infos:
                response = reader.asn(info.ip)
                info.asn = response.autonomous_system_number
                info.network = response.network
                res.append(info)
    else:
        res = infos
    return res

def handle_blank_in_str(handle_str: str):
    res = handle_str
    if handle_str:
        res = handle_str.replace(' ', '_')
    return res


# 获取位置信息与组织
def get_geo_info(infos: List[IpInfo]) -> List[IpInfo]:
    if not check_geo_loc_db() or not check_geo_asn_db():
        return infos
    res = []
    with geoip2.database.Reader(GEO2CITY_DB_PATH) as reader1, geoip2.database.Reader(GEO2ASN_DB_PATH) as reader2:
        for ipinfo in infos:
            ip = ipinfo.ip
            country, city, org = 'NG', 'NG', 'NG'
            try:
                response1 = reader1.city(remove_ipv6_mark(ip))
                country = response1.country.name
                city = response1.city.name
            except Exception:
                pass
            country = handle_blank_in_str(country)
            city = handle_blank_in_str(city)
            org, asn, network = None, None, None
            try:
                response2 = reader2.asn(remove_ipv6_mark(ip))
                org = response2.autonomous_system_organization
                asn = response2.autonomous_system_number
                network = response2.network
            except Exception:
                pass
            ipinfo.geo_info = '{}-{}({})'.format(country, city, org)
            ipinfo.asn = asn
            ipinfo.network = network
            res.append(ipinfo)
    return res

def remove_ipv6_mark(ip_str: str):
    if ip_str.startswith('[') and ip_str.endswith(']'):
        ip_str = ip_str[1: -1]
    return ip_str

def get_info():
    parser = argparse.ArgumentParser(description='geo-info 获取ip(s) 的归属地信息')
    parser.add_argument("sources", nargs="+", help="待获取归属地信息的ip(s)")
    args = parser.parse_args()
    ips = [ip_str for ip_str in args.sources if is_ip_address(remove_ipv6_mark(ip_str))]
    if ips:
        ipinfos = [IpInfo(ip) for ip in ips]
        res = get_geo_info(ipinfos)
        for r in res:
            print(r.geo_info_str)
    else:
        print('请检查是否输入了有效ip(s)')


def download_db():
    parser = argparse.ArgumentParser(description='geo-dl 升级/下载geo 数据库')
    parser.add_argument("-u", "--url", type=str, default=None, help="geo 数据库下载地址, 要求结尾包含GeoLite2-City.mmdb 或GeoLite2-ASN.mmdb")
    args = parser.parse_args()
    url = args.url
    if not args.url:
        return self_update()
    path = None
    if url.endswith(GEO2CITY_DB_NAME):
        path = GEO2CITY_DB_PATH
    if url.endswith(GEO2ASN_DB_NAME):
        path = GEO2ASN_DB_PATH
    if path:
        download_geo_db(url, path)
    else:
        print('请输入包含{} 或 {} 的url'.format(GEO2CITY_DB_NAME, GEO2ASN_DB_NAME))

def parse_geo_config():
    parser = configparser.ConfigParser()
    parser.read(GEO_CONFIG_PATH, 'utf-8')
    db_asn_url = parser.get('common', 'db_asn_url')
    db_city_url = parser.get('common', 'db_city_url')
    return db_asn_url, db_city_url

def check_or_gen_def_config():
    if not os.path.exists(GEO_CONFIG_PATH):
        print('警告: 配置文件不存在，正在生成默认配置... ...')
        write_file(GEO_DEFAULT_CONFIG, GEO_CONFIG_PATH)
        print('配置文件已生成位于 {}, 请按需要修改！'.format(GEO_CONFIG_PATH))

def config_edit():
    parser = argparse.ArgumentParser(description='geo-cfg 编辑geo config')
    _ = parser.parse_args()
    check_or_gen_def_config()
    print('编辑配置文件 {}'.format(GEO_CONFIG_PATH))
    platform = sys.platform
    if platform.startswith('win'):
        subprocess.run(['notepad.exe', GEO_CONFIG_PATH])
    elif platform.startswith('linux'):
        subprocess.run(['vim', GEO_CONFIG_PATH])
    else:
        print('未知的操作系统，请尝试手动修改{}！'.format(GEO_CONFIG_PATH))


def self_update():
    check_or_gen_def_config()
    db_asn_url, db_city_url = parse_geo_config()
    print('ASN 数据库下载地址:', db_asn_url)
    download_geo_db(db_asn_url, GEO2ASN_DB_PATH)
    print('CITY 数据库下载地址:', db_city_url)
    download_geo_db(db_city_url, GEO2CITY_DB_PATH)


if __name__ == '__main__':
    get_info()
