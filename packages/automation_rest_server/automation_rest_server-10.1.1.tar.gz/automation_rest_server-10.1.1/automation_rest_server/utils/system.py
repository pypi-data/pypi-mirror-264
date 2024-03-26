#!/usr/bin/env python

import os
import sys
import re
import time
import socket
import yaml
import traceback
from subprocess import Popen, PIPE, STDOUT
from utils import log


def execute(cmd, cmdline=True, console=True, interrupt=True):
    """
    Execute shell command
    """
    cmd = " ".join(cmd) if isinstance(cmd, list) else cmd
    if cmdline:
        print("# {cmd}".format(cmd=cmd))

    if "linux" in sys.platform:
        proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, close_fds=True)
    else:
        proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    output = ""
    while True:
        line = proc.stdout.readline().decode("utf-8", "ignore")
        if line:
            if console:
                sys.stdout.write(line)
                sys.stdout.flush()
            output += line

        if proc.poll() is not None and line == "":
            break
    status = proc.returncode

    if status and interrupt:
        raise RuntimeError("{} failed!".format(cmd))

    return status, output


def get_ip_address():
    """Get ip address of host"""
    sock = None
    ip_address = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip_address = sock.getsockname()[0]
    finally:
        if sock:
            sock.close()
    return ip_address


def get_multi_ip_address():
    address = set()
    add_info = socket.getaddrinfo(socket.gethostname(), None)
    for item in add_info:
        if ':' not in item[4][0]:
            address.add(item[4][0])
    return address


def get_root_path():
    root_path = os.path.join(os.path.dirname(__file__), "..")
    return root_path


def get_expect_version(tool_name):
    conf = os.path.join(get_root_path(), "configuration", "version.yaml")
    with open(conf) as file_:
        cont = file_.read()
    cf_ = yaml.load(cont)
    version_ = cf_[tool_name]
    return version_


def version_check(tool):
    act_version = tool.get_version()
    exp_version = get_expect_version(tool.name)
    log.INFO("%s actual version:%s , expect version:%s", tool.name, act_version, exp_version)
    ret = True if act_version == exp_version else False
    return ret


def get_time_stamp():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))


def nexus_or_nvme_device():
    cmd = "lsblk"
    _, outs = execute(cmd)
    if "nvme" in outs:
        ret = "nvme"
    elif "nexus" in outs:
        ret = "nexus"
    else:
        ret = None
    return ret


def decorate_exception(func):
    def func_wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            print(traceback.print_exc())
            log.ERR(e)
            ret = -1
        return ret
    return func_wrapper


def decorate_exception_result(func):
    def func_wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            logs = "decorate_exception_result: {}".format(traceback.format_exc())
            ret = -1, logs
        return ret
    return func_wrapper


def get_automation_platform():
    work_path = os.environ["working_path"]
    if "test-platform" in work_path.lower():
        platform = "oakgate"
    elif "production" in work_path.lower() or "perses" in work_path.lower():
        platform = "perses"
    elif "venus" in work_path.lower():
        platform = "venus"
    elif "neuron" in work_path.lower():
        platform = "neuron"
    elif "pynvme" in work_path.lower():
        platform = "pynvme"
    else:
        platform = "none"
    return platform


@decorate_exception
def get_linux_nvme_devs():
    dev_list = list()
    cmd = "lsblk"
    _, outs = execute(cmd)
    rets = re.findall("((nexus|nvme)\w+)", outs, re.DOTALL)
    if rets:
        for item in rets:
            ret_index = re.findall("(nexus|nvme)(\d+)n", item[0])
            if ret_index:
                dev_index = ret_index[0][1]
                dev = {"index": dev_index, "name": item[0]}
                dev_list.append(dev)
    return dev_list


def get_python_interpreter():
    if "linux" in sys.platform:
        py_interpreter = "python3"
    else:
        py_interpreter = "py -3"
    return py_interpreter


def get_vendor_name(vendor_id):
    print("vendor: input {}".format(vendor_id))
    vendor_id = hex(int(vendor_id)).replace("0x", "")
    vendor_name = ""
    pci_ids_file = os.path.join(os.path.dirname(__file__), "..",  "configuration", "pci.ids")
    with open(pci_ids_file, encoding='UTF-8') as pci_file:
        while True:
            line = pci_file.readline()
            if line:
                if not line.startswith("\t"):
                    if vendor_id.lower() in line.lower():
                        vendor_name = line.split(vendor_id)[1].strip()
                        break
            else:
                break
    return vendor_name


def get_test_platform_version():
    version = 1
    root_path = os.environ["working_path"]
    folder_name = os.path.basename(root_path)
    if "test-platform2.0" in folder_name:
        version = 2
    return version


ROOT_PATH = get_root_path()
