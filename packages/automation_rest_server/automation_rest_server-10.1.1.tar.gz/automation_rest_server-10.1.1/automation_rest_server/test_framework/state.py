
class State(object):
    NONE = -1
    FAIL = 0
    PASS = 1
    NOT_START = 2
    RUNNING = 3
    ABORT = 4

    BLOCK = 10
    ERROR_NOT_FOUND = 11
    ERROR_BASE_EXCEPTION = 12
    ERROR_TIMEOUT = 13
    ERROR_CONNECTION = 14
    ERROR_ABNORMAL_END = 15
    ERROR_UNHEALTHY = 16

    verdicts_map = {
        NONE: "NONE",
        FAIL: "FAIL",
        PASS: "PASS",
        NOT_START: "NOT_START",
        RUNNING: "RUNNING",
        ABORT: "ABORT",
        BLOCK: "BLOCK",
        ERROR_NOT_FOUND: "ERROR_NOT_FOUND",
        ERROR_BASE_EXCEPTION: "ERROR_BASE_EXCEPTION",
        ERROR_TIMEOUT: "ERROR_TIMEOUT",
        ERROR_CONNECTION: "ERROR_CONNECTION",
        ERROR_ABNORMAL_END: "ERROR_ABNORMAL_END",
        ERROR_UNHEALTHY: "ERROR_UNHEALTHY"
    }

    def __init__(self):
        pass


class TestType(object):

    TestCase = 1
    TestSuite = 2
    TestBenchmark = 3
    TestBenchmarkGroup = 4
    TestRebootHandle = 5
    UPGRADE = 10
    BuildFirmware = 11
    url_map = {
        TestCase: "test",
        TestSuite: "test",
        TestBenchmark: "test",
        TestBenchmarkGroup: "test",
        TestRebootHandle: "test",
        UPGRADE: "download",
        BuildFirmware: "build"
    }

    def __init__(self):
        pass


class NodeState(object):
    Online = 1
    Offline = 2
    Running = 3
    Idle = 4
    verdicts_map = {
        Online: "online",
        Offline: "offline",
        Running: "running",
        Idle: "idle",
    }


class DownloadType(object):

    NVMe = 0
    two_step_download = 1
    logic_fw = 2


class SlotState(object):
    Idle = 0
    Standby = 1
    Build = 2
    Download = 3
    Testing = 4
    Lost = 5
    verdicts_map = {
        Idle: "Idle",
        Standby: "Standby",
        Build: "Build",
        Download: "Download",
        Testing: "Testing",
        Lost: "Lost",
    }


class UpgradeType(object):

    NVMe = (0, "nvme")
    TwoStepDownload = (1, "two step download")
    LogicFw = (2, "logic fw")


