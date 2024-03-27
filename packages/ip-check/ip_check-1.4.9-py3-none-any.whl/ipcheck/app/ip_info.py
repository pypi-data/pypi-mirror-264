#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class IpInfo:

    def __init__(self, ip,
                port=443,
                rtt=-1,
                loss=None,
                max_speed=-1,
                avg_speed=-1,
                loc=None,
                colo=None,
                geo_info='NG-NG(NG)',
                asn=0,
                network=None):
        self.ip = ip
        self.port = port
        self.rtt = rtt
        self.loss = loss
        self.max_speed = max_speed
        self.avg_speed = avg_speed
        self.loc = loc
        self.colo = colo
        self.geo_info = geo_info
        self.asn=asn
        self.network=network

    def __str__(self) -> str:
        return '    {}:{} {}_{} {} loss: {}% rtt: {} ms, 下载速度为(max/avg): {}/{} kB/s'.format(self.ip, self.port, self.loc, self.colo, self.geo_info, self.loss, self.rtt ,self.max_speed, self.avg_speed)

    def get_rtt_info(self) -> str:
        return '{}:{}, {}_{}, loss: {}%, rtt: {} ms'.format(self.ip, self.port, self.loc, self.colo, self.loss, self.rtt)

    def get_info(self) -> str:
        return '{}:{}, {}_{}, {} loss: {}%, rtt: {} ms, 下载速度(max/avg)为: {}/{} kB/s'.format(self.ip, self.port, self.loc, self.colo, self.geo_info, self.loss, self.rtt, self.max_speed, self.avg_speed)

    @property
    def geo_info_str(self) -> str:
        return '{} 归属: {} ASN: {} CIDR: {}'.format(self.ip, self.geo_info, self.asn, self.network)
