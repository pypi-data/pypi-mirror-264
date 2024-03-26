# coding=utf-8
# pylint: disable=unused-variable
import subprocess
import datetime
from multiprocessing import Queue
from tool.fio.fio import Fio
from tool.fio.streams_fio import StreamsFio
from tool.iometer.iometer import IoMeter
from utils.process import MyProcess
from test_framework.state import State
from test_framework.test_case import TestCase


class TestBenchmark(object):
    def __init__(self):
        self.tool = None
        self.process_run_ = None
        self.results = list()
        self.tc = TestCase()

    def write_uart_info(self, slot=None, value=None, block_dev=None):
        if value is None:
            value = f"start benchmark step at: {datetime.datetime.now()}"
        cmd = f"python3 ./Utility/write_info_tahoe.py --slot={slot} --show_value=\"{value.upper()}\" --block_device={block_dev}"
        status = subprocess.call(cmd, shell=True)
        return status

    def _run(self, test_parameters, queue):
        try:
            tool_type = test_parameters["type"]
            tool = self.get_tool_with_type(tool_type)
            # self.tc.run("test_set_test_name.py:TestUart.test_set_name",
            #             {"test_name": "{}".format(test_parameters["test_name"])})
            self.write_uart_info(value=f"start benchmark: {test_parameters.get('test_name')}", block_dev=test_parameters['fio']['filename'])
            # perses set test case name to uart
            status, out_put, result = tool.run_benchmark(test_parameters)
            self.write_uart_info(value=f"end benchmark: {test_parameters.get('test_name')}", block_dev=test_parameters['fio']['filename'])
            ret = State.PASS if status == 0 else State.FAIL
            result = {"name": test_parameters["test_name"], "result": ret, "msg": out_put, "benchmark_result": result}
            queue.put(result)
        except Exception as e:
            print(e)
            result = None
        return result

    def run(self, test_parameters):
        queue = Queue()
        self.process_run_ = MyProcess(target=self._run, args=(test_parameters, queue, ))
        self.process_run_.start()
        self.process_run_.join()
        value = queue.get(True)
        self.results.append(value)
        return self.results

    def stop(self):
        print("TestBenchmark runner . stop")
        if self.process_run_ is not None:
            ret = self.process_run_.stop()
        else:
            ret = -1
        return ret

    def get_tool_with_type(self, tool_type):
        tool = None
        if tool_type == "fio":
            tool = Fio()
        elif tool_type == "iometer":
            tool = IoMeter()
        elif tool_type == "streams_fio":
            tool = StreamsFio()
        return tool
