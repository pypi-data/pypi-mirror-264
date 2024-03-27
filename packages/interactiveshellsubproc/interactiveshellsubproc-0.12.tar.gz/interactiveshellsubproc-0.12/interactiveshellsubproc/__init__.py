import subprocess
import sys
import threading
import ctypes
import re
from ctypes import wintypes
from time import sleep
import os
from math import floor
from exceptdrucker import errwrite, config
from procciao import kill_proc

RED = "\033[91m"
DEFAULT = "\033[0m"
config.debug = True

def sleep2(secs):
    r"""
    Sleeps for a given number of seconds.

    Parameters:
        secs (int): The number of seconds to sleep.

    Returns:
        None

    This function takes an integer `secs` as a parameter and sleeps for that many seconds. If `secs` is 0, the function returns immediately without sleeping. The function first calculates the maximum range based on `secs` and checks if it is an instance of float. If it is, it calculates the number of seconds to sleep (`sleeplittle`) by converting `maxrange` to an integer and subtracting a fraction of `maxrange` divided by 50. Then, it sleeps for the calculated fraction of a second. Next, it checks if `maxrange` is greater than 0. If it is, it enters a loop and sleeps for 0.016 seconds for `maxrange` iterations.

    Note:
        This function uses the `sleep` function from the `time` module to pause the execution for the specified number of seconds.

    Example:
        >>> sleep2(3)
        # Sleeps for 3 seconds.

        >>> sleep2(0)
        # Does not sleep.

        >>> sleep2(2.5)
        # Sleeps for 2 seconds and 250 milliseconds.
    """
    if secs == 0:
        return
    maxrange = 50 * secs
    if isinstance(maxrange, float):
        sleeplittle = floor(maxrange)
        sleep((maxrange - sleeplittle) / 50)
        maxrange = int(sleeplittle)
    if maxrange > 0:
        for _ in range(maxrange):
            sleep(0.016)




startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}

windll = ctypes.LibraryLoader(ctypes.WinDLL)
user32 = windll.user32
kernel32 = windll.kernel32
GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
CloseHandle = windll.kernel32.CloseHandle
GetExitCodeProcess.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_ulong),
]
CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
GetExitCodeProcess.restype = ctypes.c_int
CloseHandle.restype = ctypes.c_int

GetWindowRect = user32.GetWindowRect
GetClientRect = user32.GetClientRect
_GetShortPathNameW = kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD


def send_ctrl_commands(
    pid, protect_myself=True,*args,**kwargs
):
    """
    A function to send control commands to a specified process.

    Args:
        pid (int): The process ID of the target process.
        command (int, optional): The control command to send. Defaults to 0.
        protect_myself (bool, optional): Flag to protect the own process of accidentally KeyboardInterrupts. Defaults to True.
        powershell_or_python (str, optional): The choice of using powershell or python. Defaults to "powershell".
    """
    kill_proc(
    pid=pid,
    kill_timeout=5,    protect_myself=protect_myself,  # important, protect_myselfis False, you might kill the whole python process you are in.
    winkill_sigint_dll=True,  # dll first
    winkill_sigbreak_dll=True,
    winkill_sigint=True,  # exe from outside
    winkill_sigbreak=True,
    powershell_sigint=True,
    powershell_sigbreak=True,
    powershell_close=True,
    multi_children_kill=True,  # try to kill each child one by one
    multi_children_always_ignore_pids=(0, 4),  # ignore system processes
    print_output=False,
    taskkill_as_last_option=True,  # this always works, but it is not gracefully anymore
)


def killthread(threadobject):
    """
    Kill the specified thread by sending it a SystemExit exception.

    Args:
        threadobject: The thread object to be terminated.

    Returns:
        bool: True if the thread was successfully terminated, False otherwise.
    """
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


def tkill(pid):
    """
    A function to terminate a process with the given process ID.
    """
    _ = subprocess.run(f"taskkill /F /PID {pid} /T", **invisibledict)


def get_short_path_name(long_name):
    """
    Returns the short path name for a given long file path.

    Parameters:
        long_name (str): The long file path.

    Returns:
        str: The short file path. If an exception occurs, the long file path is returned.
    """
    try:
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        errwrite(e)
    return long_name


class SubProcessInteractive:
    def __init__(self, *args, **kwargs):
        """
        Initializes the object with the given arguments and keyword arguments.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Keyword arguments.
                daemon (bool): Specifies whether the thread should be a daemon thread. Default is True.
                finish_command (str or bytes): The command to be executed when the process finishes. Default is "echo XXXXCOMMANDFINISHXXXX".
                finish_command_output (bytes): The expected output of the finish command. Default is b"XXXXCOMMANDFINISHXXXX".
                restart_when_error (bool): Specifies whether to restart the process when an error occurs. Default is True.
                restart_tries (int): The number of times to attempt to restart the process. Default is 3.
                sleep_after_reconnection_attempt (int): The number of seconds to sleep after a reconnection attempt. Default is 5.
                print_stdout (bool): Specifies whether to print the standard output. Default is True.
                print_stderr (bool): Specifies whether to print the standard error. Default is True.

        Raises:
            Exception: If the finish_command is not set.

        Attention:
            If you want to create your own subclasses, have a look at SubProcessInteractivePowerShell, SubProcessInteractiveAdb, SubProcessInteractiveCmd, SubProcessInteractiveBash do unterstand what you have to do
        Returns:
            None
        """
        self.is_rebooting = False
        self.args2 = args
        self.kwargs2 = kwargs.copy()
        self.daemon = kwargs.get("daemon", True)
        if "daemon" in kwargs:
            del kwargs["daemon"]
        self.finish_command = kwargs.get(
            "finish_command",
            r"""echo XXXXCOMMANDFINISHXXXX""",
        )
        if isinstance(self.finish_command, str):
            self.finish_command_bytes = self.finish_command.encode()
        else:
            self.finish_command_bytes = self.finish_command
            self.finish_command = self.finish_command_bytes.decode()
        if "finish_command" in kwargs:
            del kwargs["finish_command"]
        else:
            raise Exception("finish_command not set")
        self.finish_command_output = kwargs.get(
            "finish_command_output", b"XXXXCOMMANDFINISHXXXX"
        )
        if "finish_command_output" in kwargs:
            del kwargs["finish_command_output"]

        self.restart_when_error = kwargs.get("restart_when_error", True)
        if "restart_when_error" in kwargs:
            del kwargs["restart_when_error"]
        self.restart_tries = kwargs.get("restart_tries", 3)
        if "restart_tries" in kwargs:
            del kwargs["restart_tries"]

        self.sleep_after_reconnection_attempt = kwargs.get(
            "sleep_after_reconnection_attempt", 5
        )
        if "sleep_after_reconnection_attempt" in kwargs:
            del kwargs["sleep_after_reconnection_attempt"]
        self.print_stdout = kwargs.get("print_stdout", True)
        if "print_stdout" in kwargs:
            del kwargs["print_stdout"]

        self.print_stderr = kwargs.get("print_stderr", True)
        if "print_stderr" in kwargs:
            del kwargs["print_stderr"]
        self.args = args
        self.kwargs = kwargs
        self.kwargs.update(invisibledict)
        self.kwargs.update(
            {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "stdin": subprocess.PIPE,
            }
        )
        self._proc = subprocess.Popen(*self.args, **self.kwargs)
        self.t3 = None
        self.t1 = threading.Thread(target=self.readstdout)
        self.t2 = threading.Thread(target=self.readstderr)
        self.t1.daemon = self.daemon
        self.t2.daemon = self.daemon
        self.t1.start()
        self.t2.start()

    def __str__(self):
        return str(self._proc)

    def __repr__(self):
        return repr(self._proc)

    def __getattr__(self, key):
        if hasattr(self._proc, key):
            return getattr(self._proc, key)

    def readstdout(self):
        """
        Reads the output from the standard output of the process and yields each line.
        This function reads the output from the standard output of the process and yields each line. It uses the `iter`
        function to iterate over the lines read from the standard output, stopping when an empty byte string is encountered.
        If the `print_stdout` flag is set to `True`, each line is printed to the standard output.
        If an exception occurs during the reading process, it is caught and the exception is written
        to the standard error using the `errwrite` function.
        Yields:
            bytes: Each line of the standard output of the process.
        Raises:
            Exception: If an error occurs during the reading process.
        """
        try:
            for l in iter(self._proc.stdout.readline, b""):
                if self.print_stdout:
                    print(
                        f"{l.decode('utf-8', 'backslashreplace')}",
                        end="",
                    )

                yield l
        except Exception as e:
            errwrite(e)

    def readstderr(self):
        """
        Reads the stderr output of the process and yields each line.

        This function reads the stderr output of the process and yields each line.
        It uses the `iter()` function to iterate over the lines of stderr output,
        until it reaches the end of the output (indicated by an empty byte string).
        If `print_stderr` is `True`, it prints each line of stderr output to the console
        after decoding it from bytes to a string using the 'utf-8' encoding and
        replacing any invalid characters with backslashes.

        Parameters:
            None

        Returns:
            A generator that yields each line of stderr output as a byte string.

        Raises:
            Exception: If an error occurs while reading the stderr output.

        """
        try:
            for l in iter(self._proc.stderr.readline, b""):
                if self.print_stderr:
                    print(
                        "%s%s%s"
                        % (RED, (f"{l.decode('utf-8', 'backslashreplace')}"), DEFAULT),
                        end="",
                    )
                yield l
        except Exception as e:
            errwrite(e)

    def _restart_everything(self, **kwargs):
        """
        Restarts the entire process by terminating the current process and starting a new one.

        Parameters:
            close3 (bool): If True, closes thread 3 before restarting the process. Default is True.

        Returns:
            None
        """
        close3=kwargs.pop("close3", True)
        self.is_rebooting = True

        try:
            send_ctrl_commands(self._proc.pid)
            sleep2(2)
        except Exception:
            pass
        except KeyboardInterrupt:
            try:
                sleep(1)
            except:
                pass
        try:
            tkill(self._proc.pid)
        except Exception:
            pass
        try:
            self._proc.stdin.flush()
            self._proc.stdin.close()
        except Exception:
            pass
        try:
            self._proc.stdout.flush()
            self._proc.stdout.close()
        except Exception:
            pass

        try:
            self._proc.stderr.flush()
            self._proc.stderr.close()
        except Exception:
            pass
        try:
            self._proc.wait(timeout=1)
        except Exception:
            pass
        try:
            self._proc.terminate()
        except Exception:
            pass
        isclosed1 = killthread(self.t1)
        isclosed2 = killthread(self.t2)
        if close3:
            if self.t3 is not None:
                isclosed3 = killthread(self.t3)
        ismyproc = False
        try:
            di = get_all_procs()
            _procdata = di.get(self._proc.pid, None)
            if _procdata:
                if isinstance(self._proc.args, str):
                    ismyproc = _procdata["CommandLine"] == self._proc.args
                else:
                    ismyproc = _procdata["CommandLine"] == " ".join(self._proc.args)
        except Exception:
            pass

        if ismyproc:
            try:
                tkill(self._proc.pid)
                sleep(self.sleep_after_reconnection_attempt)
            except Exception:
                pass

        self._proc = subprocess.Popen(*self.args, **self.kwargs)
        sleep(self.sleep_after_reconnection_attempt)
        self.t1 = threading.Thread(target=self.readstdout)
        self.t2 = threading.Thread(target=self.readstderr)
        self.t1.start()
        self.t2.start()
        self.is_rebooting = False

    # Function to send a command to the subprocess
    def sendcommand(self, cmd, **kwargs):
        """
        Sends a command to the stdin and flushes the stdin buffer to avoid deadlocks

        Args:
            cmd: The command to be sent.
            **kwargs: Additional keyword arguments:
                timeout (float): The timeout period.

        Returns:
            tuple: A tuple containing stdoutlist, stderrlist, and an exception.
        """

        def timeoutkill():
            try:
                timeoutnow = kwargs.get("timeout", 0)
                if timeoutnow > 0:
                    maxrange = 50 * timeoutnow
                    if isinstance(maxrange, float):
                        sleeplittle = floor(maxrange)
                        sleep((maxrange - sleeplittle) / 50)
                        maxrange = int(sleeplittle)
                    if maxrange > 0:
                        for _ in range(maxrange):
                            sleep(0.016)
                            if keepproc and not execution_running:
                                return True
                    if keepproc and not execution_running:
                        return True
                    try:
                        send_ctrl_commands(self._proc.pid)
                    except KeyboardInterrupt:
                        try:
                            sleep(1)
                        except:
                            pass
                    return False

                return True
            except Exception as e:
                errwrite(e)
                return True

        try:
            keepproc = True
            execution_running = True
            self.t3 = threading.Thread(target=timeoutkill)
            self.t3.daemon = self.daemon
            self.t3.start()
            try:
                self._proc.stdin.flush()
            except Exception:
                while self.is_rebooting:
                    sleep(0.1)
            if isinstance(cmd, str):
                self._proc.stdin.write((cmd + f"\n{self.finish_command}\n").encode())
            else:
                self._proc.stdin.write(cmd + b"\n" + self.finish_command_bytes + b"\n")
            self._proc.stdin.flush()
        except Exception as e:
            errwrite(e)
            print("Restarting ...")
            self._restart_everything()
            if "restart_count" not in kwargs:
                kwargs["restart_count"] = 0
            if kwargs.get("restart_count", 10000000) > self.restart_tries:
                raise TimeoutError(
                    f"Restart count is {kwargs.get('restart_count',sys.maxsize)}"
                )
            else:
                kwargs["restart_count"] += 1
            return self.sendcommand(cmd, **kwargs)
        stdoutlist = []
        stderrlist = []
        try:
            lineiterstdout = self.readstdout()
            lineiterstderr = self.readstderr()

            while True:
                line_stdout = next(lineiterstdout)
                stdoutlist.append(line_stdout)
                if self.finish_command_output in line_stdout:
                    break

            while True:
                line_stderr = next(lineiterstderr)
                stderrlist.append(line_stderr)
                if self.finish_command_output in line_stderr:
                    break
            execution_running = False
            return stdoutlist, stderrlist, None
        except Exception as e:
            errwrite(e)
            execution_running = False
            return [stdoutlist, stderrlist, e]


def get_all_procs():
    dax = subprocess.run(
        "wmic process list FULL", capture_output=True, **invisibledict
    ).stdout
    procdata = re.split(r"[\r\n]+CommandLine=", dax.decode("utf-8", "backslashreplace"))

    procdata = ["CommandLine=" + x for x in procdata if x.strip()]
    procdata = [
        [(g.strip() + " ").split("=", maxsplit=1) for g in x.strip().splitlines()]
        for x in procdata
    ]
    procdata = [
        {x[0].strip(): x[1].strip() for x in q if len(x) == 2} for q in procdata
    ]
    procdatafiltered = {}
    for pr in procdata:
        try:
            procdatafiltered[int(pr["ProcessId"])] = pr
        except Exception as era:
            errwrite(era)
    return procdatafiltered


class SubProcessInteractivePowerShell(SubProcessInteractive):
    def __init__(self, *args, **kwargs):
        finish_command = r"""$encodedString = 'WFhYWENPTU1BTkRGSU5JU0hYWFhY'
[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($encodedString))
$decodedString = [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($encodedString))
[Console]::Error.WriteLine($decodedString)"""
        self._startcommand = r"""$encodedString = 'WFhYWENPTU1BTkRTVEFSVFhYWFg='
[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($encodedString))
$decodedString = [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($encodedString))
[Console]::Error.WriteLine($decodedString)"""
        self._startcommand_bytes = self._startcommand.encode()
        finish_command_output = b"XXXXCOMMANDFINISHXXXX"
        kwargs.update(
            {
                "finish_command": finish_command,
                "finish_command_output": finish_command_output,
            }
        )
        self.return_error = kwargs.get("return_error", True)
        for kwarg in ["return_error"]:
            if kwarg in kwargs:
                del kwargs[kwarg]
        self._inoutput_finished = b"XXXXCOMMANDFINISHXXXX\r\n"
        self._inoutput_start = b"XXXXCOMMANDSTARTXXXX\r\n"
        super().__init__(["powershell.exe"], *args, **kwargs)

    def sendcommand(self, cmd, **kwargs):
        def format_stdout(executedcommand):
            try:
                finishindex = (
                    len(executedcommand)
                    - list(reversed(executedcommand)).index(self._inoutput_finished)
                    - 3
                )
            except Exception:
                finishindex = len(executedcommand)
            try:
                startindex = (executedcommand).index(self._inoutput_start) + 4
            except Exception:
                startindex = 0
            executedcommand_finished = executedcommand[startindex:finishindex]
            try:
                while True:
                    if executedcommand_finished[0] in [b"\r\n", b"\n"]:
                        executedcommand_finished.pop(0)
                    else:
                        break
            except Exception:
                pass
            return executedcommand_finished

        def format_stderr(executedcommand):
            try:
                finishindex = (
                    len(executedcommand)
                    - list(reversed(executedcommand)).index(self._inoutput_finished)
                    - 1
                )
            except Exception:
                finishindex = len(executedcommand)
            try:
                startindex = (executedcommand).index(self._inoutput_start) + 1
            except Exception:
                startindex = 0
            executedcommand_finished = executedcommand[startindex:finishindex]
            try:
                while True:
                    if executedcommand_finished[0] in [b"\r\n", b"\n"]:
                        executedcommand_finished.pop(0)
                    else:
                        break
            except Exception:
                pass
            return executedcommand_finished

        if isinstance(cmd, str):
            cmd = self._startcommand + "\n" + cmd
        else:
            cmd = self._startcommand + b"\n" + cmd
        stdoutlist, stderrlist, e = super().sendcommand(cmd, **kwargs)
        if not e:
            stdoutlist = format_stdout(stdoutlist)
            stderrlist = format_stderr(stderrlist)
        if self.return_error:
            return [stdoutlist, stderrlist, e]
        else:
            return [stdoutlist, stderrlist]


class SubProcessInteractiveAdb(SubProcessInteractive):
    def __init__(self, *args, **kwargs):
        finish_command = r"""
encodedString='eHh4Q09NTUFORHh4eERPTkV4eHg='
n1=$(base64 -d <<< $(echo -n "$encodedString"))
echo -e "$n1" >&1
echo -e "$n1" >&2"""

        self._startcommand = r"""
encodedString='WFhYWENPTU1BTkRTVEFSVFhYWFg='
n1=$(base64 -d <<< $(echo -n "$encodedString"))
echo -e -n "$n1" >&1
echo -e -n "$n1" >&2"""
        self._startcommand_bytes = self._startcommand.encode()

        finish_command_output = b"xxxCOMMANDxxxDONExxx"
        kwargs.update(
            {
                "finish_command": finish_command,
                "finish_command_output": finish_command_output,
            }
        )
        adb_path = kwargs.get("adb_path", "adb.exe")
        if kwargs.get("convert_to_83", True):
            adb_path = get_short_path_name(adb_path)
        devserial = kwargs.get("device_serial", "")
        self.return_error = kwargs.get("return_error", True)
        if devserial:
            devserial = f"-s {devserial}"
        for kwarg in ["adb_path", "device_serial", "convert_to_83", "return_error"]:
            if kwarg in kwargs:
                del kwargs[kwarg]
        cmd = " ".join([adb_path, devserial, "shell"])
        self._inoutput_start = b"XXXXCOMMANDSTARTXXXX"
        super().__init__(cmd, *args, **kwargs)

    def sendcommand(self, cmd, **kwargs):
        if isinstance(cmd, str):
            cmd = self._startcommand + "\n" + cmd
        else:
            cmd = self._startcommand + b"\n" + cmd
        stdoutlist, stderrlist, e = super().sendcommand(cmd, **kwargs)
        stdoutlistfiltered, stderrlistfiltered = [], []
        counter = 0
        if not e:
            for resultlists in [stdoutlist, stderrlist]:
                try:
                    for i in range(len(resultlists), 0, -1):
                        if i == 0:
                            break
                        if (
                            self.finish_command_output
                            in resultlists[len(resultlists) - 1]
                        ):
                            resultlists[len(resultlists) - 1] = resultlists[
                                len(resultlists) - 1
                            ].split(self.finish_command_output)[0]
                            if not resultlists[len(resultlists) - 1]:
                                resultlists.pop(-1)
                            break
                        else:
                            resultlists.pop(-1)
                except Exception:
                    pass
                try:
                    for i in range(0, len(resultlists)):
                        if self._inoutput_start in resultlists[0]:
                            resultlists[0] = resultlists[0].split(self._inoutput_start)[
                                -1
                            ]
                            break
                        else:
                            resultlists.pop(0)
                except Exception as err:
                    errwrite(err)
                    pass
                if counter == 0:
                    stdoutlistfiltered.extend(resultlists)
                    counter += 1
                else:
                    stderrlistfiltered.extend(resultlists)
            stdoutlist, stderrlist = stdoutlistfiltered, stderrlistfiltered
        stdoutlist = [x.replace(b"\r\n", b"\n") for x in stdoutlist]
        stderrlist = [x.replace(b"\r\n", b"\n") for x in stderrlist]
        if self.return_error:
            return [stdoutlist, stderrlist, e]
        else:
            return [stdoutlist, stderrlist]


class SubProcessInteractiveCmd(SubProcessInteractive):
    def __init__(self, *args, **kwargs):
        self._startcommand = r"""set startstrxxx=XXXXCOMMANDSTARTYYYY
call set startstrxxx=%startstrxxx:YYYY=%XXXX
echo %startstrxxx%
echo %startstrxxx% 1>&2
"""
        finish_command = r"""set endstrxxx=XXXXCOMMANDFINISHYYYY
call set endstrxxx=%endstrxxx:YYYY=%XXXX
echo %endstrxxx%
echo %endstrxxx% 1>&2
"""
        self._startcommand_bytes = self._startcommand.encode()
        finish_command_output = b"XXXXCOMMANDFINISHXXXX"
        kwargs.update(
            {
                "finish_command": finish_command,
                "finish_command_output": finish_command_output,
            }
        )
        self.return_error = kwargs.get("return_error", True)
        for kwarg in ["return_error"]:
            if kwarg in kwargs:
                del kwargs[kwarg]
        self._inoutput_finished = b"XXXXCOMMANDFINISHXXXX"
        self._inoutput_start = b"XXXXCOMMANDSTARTXXXX"
        variationoutputadd = [
            rb"\r\n",
            b"\r\n",
            rb" \r\n",
            b" \r\n",
            rb" \n",
            b" \n",
            rb"\n",
            b"\n",
        ]
        self._outputvariations_finished = [
            self._inoutput_finished + variationoutputadd[i]
            for i in range(len(variationoutputadd))
        ]
        self._outputvariations_start = [
            self._inoutput_start + variationoutputadd[i]
            for i in range(len(variationoutputadd))
        ]
        comspec = os.environ.get("ComSpec")
        if not comspec:
            system_root = os.environ.get("SystemRoot", "")
            comspec = os.path.join(system_root, "System32", "cmd.exe")
            if not os.path.isabs(comspec):
                comspec = "cmd.exe"
            executable = comspec
        if os.path.isabs(comspec):
            executable = comspec
        super().__init__([executable], *args, **kwargs)

    def sendcommand(self, cmd, **kwargs):
        if isinstance(cmd, str):
            cmd = self._startcommand + "\n" + cmd
        else:
            cmd = self._startcommand + b"\n" + cmd
        stdoutlist, stderrlist, e = super().sendcommand(cmd, **kwargs)
        stdoutlistfiltered, stderrlistfiltered = [], []
        if not e:
            counter = 0
            for resultlists in [stdoutlist.copy(), stderrlist.copy()]:
                try:
                    for i in range(len(resultlists), 0, -1):
                        if i == 0:
                            break
                        if resultlists[len(resultlists) - 1].startswith(
                            self._inoutput_finished
                        ):
                            resultlists.pop(-1)
                            if set(self._outputvariations_finished).intersection(
                                set(resultlists)
                            ):
                                continue
                            break
                        else:
                            resultlists.pop(-1)
                except Exception:
                    pass
                try:
                    for i in range(0, len(resultlists)):
                        if resultlists[0].startswith(self._inoutput_start):
                            resultlists.pop(0)

                            if set(self._outputvariations_start).intersection(
                                set(resultlists)
                            ):
                                continue
                            else:
                                break
                        else:
                            resultlists.pop(0)
                except Exception as err:
                    errwrite(err)
                try:
                    while True:
                        if resultlists[0] in [b"\r\n", b"\n"]:
                            resultlists.pop(0)
                        else:
                            break
                except Exception:
                    pass
                if counter == 0:
                    stdoutlistfiltered.extend(resultlists)
                    counter += 1
                else:
                    stderrlistfiltered.extend(resultlists)
            stdoutlist, stderrlist = stdoutlistfiltered, stderrlistfiltered
        try:
            stdoutlist = stdoutlist[4:-5]
        except Exception as err:
            errwrite(err)
        if self.return_error:
            return [stdoutlist, stderrlist, e]
        else:
            return [stdoutlist, stderrlist]


class SubProcessInteractiveBash(SubProcessInteractive):
    def __init__(self, *args, **kwargs):
        finish_command = r"""
encodedString='WFhYWENPTU1BTkRGSU5JU0hYWFhY'
n1=$(base64 -d <<< $(echo -n "$encodedString"))
echo "$n1" >&1
echo "$n1" >&2
"""

        self._startcommand = r"""
encodedString='WFhYWENPTU1BTkRTVEFSVFhYWFg'
n1=$(base64 -d <<< $(echo -n "$encodedString"))
echo "$n1" >&1
echo "$n1" >&2
"""
        self._startcommand_bytes = self._startcommand.encode()

        finish_command_output = b"XXXXCOMMANDFINISHXXXX\n"
        kwargs.update(
            {
                "finish_command": finish_command,
                "finish_command_output": finish_command_output,
            }
        )
        bash_path = kwargs.get("bash_path", "bash.exe")
        if kwargs.get("convert_to_83", True):
            bash_path = get_short_path_name(bash_path)
        self.return_error = kwargs.get("return_error", True)
        for kwarg in ["bash_path", "convert_to_83", "return_error"]:
            if kwarg in kwargs:
                del kwargs[kwarg]
        cmd = bash_path
        self._inoutput_start = b"XXXXCOMMANDSTARTXXXX\n"
        super().__init__(cmd, *args, **kwargs)

    def sendcommand(self, cmd, **kwargs):
        if isinstance(cmd, str):
            cmd = self._startcommand + "\n" + cmd
        else:
            cmd = self._startcommand + b"\n" + cmd
        stdoutlist, stderrlist, e = super().sendcommand(cmd, **kwargs)
        stdoutlistfiltered, stderrlistfiltered = [], []
        counter = 0
        if not e:
            for resultlists in [stdoutlist, stderrlist]:
                try:
                    for i in range(len(resultlists), 0, -1):
                        if i == 0:
                            break
                        if resultlists[len(resultlists) - 1].startswith(
                            self.finish_command_output
                        ):
                            resultlists.pop(-1)
                            break
                        else:
                            resultlists.pop(-1)
                except Exception:
                    pass
                try:
                    for i in range(0, len(resultlists)):
                        if resultlists[0].startswith(self._inoutput_start):
                            resultlists.pop(0)
                            break
                        else:
                            resultlists.pop(0)
                except Exception as err:
                    errwrite(err)
                if counter == 0:
                    stdoutlistfiltered.extend(resultlists)
                    counter += 1
                else:
                    stderrlistfiltered.extend(resultlists)
            stdoutlist, stderrlist = stdoutlistfiltered, stderrlistfiltered
        if self.return_error:
            return [stdoutlist, stderrlist, e]
        else:
            return [stdoutlist, stderrlist]
