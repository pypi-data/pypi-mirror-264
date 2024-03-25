#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================

import http.client
import os
import json
import time
import urllib.parse
from html.parser import HTMLParser

from . import logger_config
from .download_util import CONFIG_INST, DOWNLOAD_INST, CheckHash
from .download_util import calc_sha256, get_arch, get_specified_python, CH, DownloadCheckError, UrlOpenError

LOG = logger_config.LOG


class SimpleIndexParser(HTMLParser):
    """
    解析simple index
    """

    def __init__(self):
        super().__init__()
        self.index = {}
        self.tmp_attrs = None

    def get_index(self):
        """
        get_index  获取解析到的软件包的索引

        :return:  索引
        """
        return self.index

    def handle_starttag(self, tag, attrs):
        """
        handle_starttag  解析tag开始
        """
        if tag == 'a':
            self.tmp_attrs = attrs

    def handle_data(self, data):
        """
        handle_starttag  解析tag中的数据
        """
        if self.tmp_attrs is not None:
            self.index[data] = self.tmp_attrs[0][1]


class MyPip(object):
    """
    downloader for pip
    """

    def __init__(self):
        self.cache = {}
        self.downloaded = []
        # 读取配置
        script = os.path.realpath(__file__)
        self.pypi_url = CONFIG_INST.get_pypi_url()
        self.require_file = os.path.join(os.path.dirname(script), 'requirements.txt')
        self.obs_resources_file = os.path.join(os.path.dirname(script), 'obs_resources.json')
        self.repo_path = os.path.join(os.path.dirname(script), '../resources/pylibs')

    @staticmethod
    def file_download(url, dest):
        """
        file_download

        :param url:  待下载文件的url
        :param dest: 下载时本地文件名,带路径
        :return:
        """
        if os.path.exists(dest):
            LOG.info('[{0}] exist'.format(os.path.basename(dest)))
            os.remove(dest)
            LOG.info('[{0}] deleted'.format(os.path.basename(dest)))
        DOWNLOAD_INST.download(url, dest)

    @staticmethod
    def is_wheel_match(full_name, version, platform, implement):
        """
        is_wheel_match

        :param full_name:
        :param version:
        :param platform:
        :param implement:
        :return:
        """
        try:
            elements = full_name.split('-')
            wheel_version = elements[1]
            wheel_impl = elements[2]
            wheel_platform = elements[4].split('.')[0]
            if wheel_version != version:
                return False

            if wheel_impl not in ('py3', 'py2.py3', implement):
                return False

            if wheel_platform not in ('any', platform):
                return False

        except IndexError as err:
            print(err)
            LOG.error(err)
            return False
        finally:
            pass

        return True

    @staticmethod
    def source_filter(index, version):
        """
        source_filter

        :param index:
        :param version:
        :return:
        """
        pkg = ''
        url = ''
        for name, href in index.items():
            if 'tar' in name or 'zip' in name:
                if version in name:
                    pkg = name
                    url = href
            else:
                continue
        return pkg, url

    @staticmethod
    def need_download_again(dst_file, url_with_hash):
        """
        need_download_again
        校验目的文件的hash值与url中的hash值是否相等，来决定是否重新下载

        :param dst_file: 目的文件
        :param url_with_hash:  带hash值的URL
        :return:
        """
        if url_with_hash is None or len(url_with_hash) == 0:
            return True
        if not os.path.exists(dst_file):
            return True

        return not CheckHash.check_download_hash(dst_file, url_with_hash)

    def get_simple_index(self, distribution):
        """
        get_simple_index

        :param distribution:
        :return:
        """
        if distribution in self.cache.keys():
            index = self.cache.get(distribution)
        else:
            url = '{0}/{1}/'.format(self.pypi_url, distribution.lower())
            LOG.info('pypi URL = [{0}]'.format(url))
            index = DOWNLOAD_INST.urlopen(url)
            self.cache[distribution] = index

        parser = SimpleIndexParser()
        parser.feed(index.decode())
        idx = parser.get_index()
        return idx

    def wheel_filter(self, index, version, platform, implement):
        """
        wheel_filter

        :param index:
        :param version:
        :param platform:
        :param implement:
        :return:
        """
        pkg = ''
        url = ''
        for name, href in index.items():
            if 'whl' in name:
                if self.is_wheel_match(name, version, platform, implement):
                    pkg = name
                    url = href
            else:
                continue
        return pkg, url

    def get_url_from_obs(self, name, platform, implement):
        if platform == 'none':
            return "", ""
        distribution, version = name.split('==')
        with open(self.obs_resources_file) as file_content:
            index = json.load(file_content)
            for file_name, href in index.items():
                elements = file_name.split('-')
                try:
                    wheel_name = elements[0]
                    wheel_version = elements[1].split('+')[0]
                    wheel_impl = elements[2]
                    wheel_platform = elements[4].split('.')[0]
                except IndexError as err:
                    print(err)
                    LOG.error(err)
                if wheel_name != distribution:
                    continue
                if wheel_version != version:
                    continue
                if wheel_impl not in ('py3', 'py2.py3', implement):
                    continue
                if wheel_platform not in ('any', platform):
                    continue
                return file_name, href
            return "", ""

    def download_wheel(self, name, platform, implement, dest_path):
        """
        下载软件包
        """
        # get url from pypi
        distribution, version = name.split('==')
        index = self.get_simple_index(distribution)
        file_name, url = self.wheel_filter(index, version, platform, implement)
        if len(url) == 0:
            # get url from obs
            file_name, download_url = self.get_url_from_obs(name, platform, implement)
            if not download_url:
                LOG.info('can not find {0} for {1} {2}'.format(name, platform, implement))
                return False
        else:
            download_url = '{0}/{1}/{2}'.format(self.pypi_url, distribution, url)

        if file_name in self.downloaded:
            return True
        LOG.info("Download {0} from [{1}]".format(file_name, download_url))
        file_path = os.path.join(dest_path, file_name)
        if not self.need_download_again(file_path, download_url):
            print(file_name.ljust(60), "exists")
            LOG.info('{0} no need download again'.format(file_name))
            self.downloaded.append(file_name)
            return True
        self.file_download(download_url, file_path)
        if not CH.check_download_hash(file_path, download_url):
            LOG.info('the downloaded file：{} hash is not equal to the hash in the url'.format(file_path))
            raise DownloadCheckError(f"file_path: {file_path}, download_url: {download_url}")
        print(file_name.ljust(60), "download success")
        self.downloaded.append(file_name)
        return True

    def download_source(self, name, dest_path):
        """
        下载源码包
        """
        distribution, version = name.split('==')
        index = self.get_simple_index(distribution)
        file_name, url = self.source_filter(index, version)
        if len(url) == 0:
            return False
        if file_name in self.downloaded:
            return True
        download_url = '{0}/{1}/{2}'.format(self.pypi_url, distribution, url)
        LOG.info("Download {0} from [{1}]".format(file_name, download_url))
        file_path = os.path.join(dest_path, file_name)
        if not self.need_download_again(file_path, url):
            print(file_name.ljust(60), "exists")
            LOG.info('{0} no need download again'.format(file_name))
            self.downloaded.append(file_name)
            return True
        self.file_download(download_url, file_path)
        if not CH.check_download_hash(file_path, url):
            LOG.info('the downloaded file：{} hash is not equal to the hash in the url'.format(file_path))
            raise DownloadCheckError(file_path)
        print(file_name.ljust(60), "download success")
        self.downloaded.append(file_name)
        return True

    def download_x86(self, name, implement_flag, dest_path):
        """
        download_x86

        :param name:
        :param implement_flag:
        :param dest_path:
        :return:
        """
        platform_list = ('linux_x86_64', 'manylinux1_x86_64', 'manylinux2010_x86_64',
                         'manylinux2014_x86_64')
        for platform in platform_list:
            if self.download_wheel(name, platform, implement_flag, dest_path):
                return True
        return False

    def download_arm(self, name, implement_flag, dest_path):
        """
        download_arm

        :param name:
        :param implement_flag:
        :param dest_path:
        :return:
        """
        platform_list = ('linux_aarch64', 'manylinux_2_17_aarch64', 'manylinux2014_aarch64')
        for platform in platform_list:
            if self.download_wheel(name, platform, implement_flag, dest_path):
                return True
        return False

    def download(self, name, dest_path, arch):
        """
        download

        :param name:
        :param dest_path:
        :return:
        """
        try:
            specified_python = get_specified_python()
            if "Python-3.7" in specified_python:
                implement_flag = "cp37"
            if "Python-3.8" in specified_python:
                implement_flag = "cp38"
            if "Python-3.9" in specified_python:
                implement_flag = "cp39"

            if not os.path.exists(dest_path):
                os.makedirs(dest_path, mode=0o750, exist_ok=True)

            if self.download_wheel(name, "none", implement_flag, dest_path):
                return True

            if "x86_64" in arch and not self.download_x86(name, implement_flag, dest_path):
                self.download_source(name, dest_path)

            if "aarch64" in arch and not self.download_arm(name, implement_flag, dest_path):
                self.download_source(name, dest_path)
            return True
        except Exception:
            print(name.ljust(60), "download failed")
            raise
        finally:
            pass


my_pip = MyPip()


def download(os_list, res_dir):
    """
    按软件列表下载其他部分
    """
    if os_list is None:
        os_list = []
    arch = get_arch(os_list)
    repo_path = os.path.join(res_dir, 'pylibs')
    LOG.info('pip arch is {0}'.format(arch))

    results = {'ok': [], 'failed': []}
    with open(my_pip.require_file) as file_content:
        for line in file_content:
            LOG.info('[{0}]'.format(line.strip()))
            if my_pip.download(line.strip(), repo_path, arch):
                results.get('ok', []).append(line.strip())
                continue
            results.get('failed', []).append(line.strip())
    return results
