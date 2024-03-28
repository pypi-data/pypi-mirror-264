import inspect
import os
from thompcoUtils.log_utils import get_logger
import psutil
from sys import platform
import time
from netifaces import interfaces, ifaddresses, AF_INET


class UnhandledOs(Exception):
    pass


def _list_zones(walk_dir):
    d = {"timezones": []}
    files = os.listdir(walk_dir)
    for f in files:
        if os.path.isdir(os.path.join(walk_dir, f)):
            d[f] = _list_zones(os.path.join(walk_dir, f))
        else:
            d["timezones"].append(f)
    return d


def list_timezones():
    ost = os_type()
    if ost == "windows":
        time_zones = _list_zones("d:/temp/zoneinfo")
        time_zones["current_timezone"] = get_timezone()
        return time_zones
    elif ost == "linux" or ost == "osx":
        time_zones = _list_zones("/usr/share/zoneinfo")
        time_zones["current_timezone"] = get_timezone()
        return time_zones
    else:
        raise UnhandledOs("{} os not supported".format(ost))


def get_timezone():
    ost = os_type()
    if ost == "linux":
        with open("/etc/timezone") as f:
            return f.read().strip()
    elif ost == "windows" or ost == "osx":
        return time.tzname[0]
    else:
        raise UnhandledOs("{} os not supported".format(ost))


def list_all_processes():
    processes = []
    for process in psutil.process_iter():
        processes.append(process)
    return processes


def find_processes(process_name):
    processes = []
    for process in psutil.process_iter():
        if process_name == process.name():
            processes.append(process)
    return processes


def list_child_processes(pid):
    processes = []
    for process in psutil.process_iter():
        if process.ppid() == pid:
            processes.append(process)
    return processes


def kill_process(process):
    logger = get_logger()
    killed = False
    try:
        process.kill()
        if not process._is_running():
            logger.debug('Killed "{}" process'.format(process.name()))
            killed = True
    except Exception as e:
        logger.debug(e)
    if not killed:
        logger.debug("Could not kill pid {}/process name {}".format(process.pid, process.name()))


def kill_all_processes_by_name(process_name):
    logger = get_logger()
    killed = False
    for process in psutil.process_iter():
        if process_name in process.name():
            # noinspection PyBroadException
            try:
                print(process.ppid)
                process.kill()
                if not process.is_running():
                    logger.debug('Killed "{}" process'.format(process.name()))
                    killed = True
            except Exception as e:
                logger.debug(e)
    if not killed:
        logger.error('Could kill process name "{}"'.format(process_name))


def is_running(name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python.exe' or proc.info['name'] == 'pythonw.exe':
                for info in proc.info['cmdline']:
                    if info.endswith(name):
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def script_is_running(obj: object) -> bool:
    """
    Checks if a python script is running
    :param obj: the name of the python object (generally the filename without the extension)
    :return: True if running, else False
    """
    # noinspection PyTypeChecker
    script_name = inspect.getfile(object=obj)

    if not script_name.endswith('.py'):
        raise RuntimeError(f'script_name {script_name} must end in .py')

    if os_type() == OSType.WINDOWS:
        extension = '.exe'
    else:
        extension = ''

    for proc in psutil.process_iter():
        try:
            # noinspection PyUnresolvedReferences, PyProtectedMember
            cmd_line = proc.cmdline()

            if len(cmd_line) > 0 and f'python{extension}' in cmd_line[0]:
                for s in cmd_line:
                    if script_name in s:
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


class OSType(enumerate):
    Linux = "Linux"
    OSX = "OSX"
    WINDOWS = "Windows"


class OSName(enumerate):
    Arm = 'Arm'
    X86 = 'X86'


def os_name():
    if os.uname()[4][:3] == 'arm':
        return OSName.Arm
    elif os.uname()[4][:3] == 'x86':
        return OSName.X86
    else:
        raise UnhandledOs("Unknown system")


def os_type() -> OSType:
    if platform == "linux" or platform == "linux2":
        return OSType.Linux
    elif platform == "darwin":
        return OSType.OSX
    elif platform == "win32":
        return OSType.WINDOWS
    else:
        raise UnhandledOs("Unknown system")


def get_ip_addresses():
    addresses = None
    for interface_name in interfaces():
        addresses = [i['addr'] for i in ifaddresses(interface_name).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
    return addresses


def main():
    chrome_processes = find_processes("Google Chrome")
    for process in chrome_processes:
        child_processes = list_child_processes(process.pid)
        if len(child_processes) < 7:
            kill_process(process)
    pass


if __name__ == '__main__':
    main()
