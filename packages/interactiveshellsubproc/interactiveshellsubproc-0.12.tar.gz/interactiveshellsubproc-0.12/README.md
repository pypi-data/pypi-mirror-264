# Interactive subprocess Instances for cmd.exe, powershell.exe, adb.exe, bash.exe without deadlocks - pure Python, no dependencies

## Easy, bidirectional communication with various subprocesses such as PowerShell, ADB, Command Prompt (Cmd), and Bash.

### pip install interactiveshellsubproc

### Tested against MSYS2 / powershell/cmd.dexe -> Windows 10 / Bluestacks / Python 3.11 / Windows 10

## Advantages

### Interactivity:
Allows bidirectional communication with subprocesses, enabling command execution and retrieval of outputs.

### Versatility:
Supports various subprocess types, including PowerShell, ADB, Cmd, and Bash, catering to different use cases and environments. New classes for any other shell can be easily derived from the base class.

### Error Handling:
Implements error handling mechanisms such as automatic process restart when stdin breaks (BrokenPipe) and configurable restart policies, enhancing robustness.

### configurability:
Offers a range of configurable options such as daemon mode, output printing settings, and restart behavior, providing flexibility in usage.

### Ease of Use:
Provides a straightforward interface for sending commands to subprocesses and retrieving outputs, simplifying interaction with external processes.

### Very low (almost no) deadlock danger: It very rarely deadlocks.
If you are sending normal shell commands, your instance will probably never deadlock. However, when you write, for example, a shell script and forget a curly brace or a bracket at the end and execute the half-backed command, or you open AWK or cat, and they start reading from stdin and not from a file or a PIPE because you didn't pass it, then chances are very high that the console will deadlock.

```py
from interactiveshellsubproc import (
    SubProcessInteractivePowerShell,
    SubProcessInteractiveAdb,
    SubProcessInteractiveCmd,
    SubProcessInteractiveBash,
)

if __name__ == "__main__":
    powershellinstance = SubProcessInteractivePowerShell(
        daemon=True,
        restart_when_error=True,
        restart_tries=5,
        sleep_after_reconnection_attempt=5,
        print_stderr=False,
        print_stdout=False,
        return_error=True,
    )

    stdout, stderr, exception = powershellinstance.sendcommand("ls")
    # Out[10]: [b"lsbabababa : The term 'lsbabababa' is not recognized as the name of a cmdlet, function,....
    stdout, stderr, exception = powershellinstance.sendcommand("lsbabababa")
    # [b"lsbabababa : The term 'lsbabababa' is not recognized as the name of a cmdlet, function, script

    adbinstance = SubProcessInteractiveAdb(
        adb_path=r"C:\ProgramData\chocolatey\lib\adb\tools\platform-tools\adb.exe",
        device_serial="127.0.0.1:5845",
        convert_to_83=True,
        daemon=True,
        restart_when_error=True,
        restart_tries=5,
        sleep_after_reconnection_attempt=5,
        print_stderr=False,
        print_stdout=False,
        return_error=True,
    )
    # In [1]: adbinstance.sendcommand("ls")
    # Out[1]: [[b'acct\n', b'apex\n', b'bin\n', b'boot\n', b'bugreports\n', b...

    # In [2]: adbinstance.stdin.close() # closing the pipe to simulate a problem

    # In [3]: adbinstance.sendcommand("ls")
    # ------------------------------------------
    # Traceback (most recent call last):
    #   File "C:\ProgramData\anaconda3\envs\a0\checkpowers.py", line 411, in sendcommand
    #     self._proc.stdin.write((cmd + f"\n{self.finish_command}\n").encode())
    # ValueError: write to closed file
    # ------------------------------------------
    # Restarting ...
    # Out[3]: [[], [], None] # the output of the first command after the restart is mostly not complete

    # In [4]: adbinstance.sendcommand("ls") # After the first one, everything is like before
    # Out[4]: [[b'acct\n', b'apex\n', b'bin\n', b'boot\n', b'bugreports\n'...

    cmdinstance = SubProcessInteractiveCmd(
        daemon=True,
        restart_when_error=True,
        restart_tries=5,
        sleep_after_reconnection_attempt=5,
        print_stderr=False,
        print_stdout=False,
        return_error=True,
    )
    # In [6]: cmdinstance.sendcommand("ls")
    # Out[6]: [[b'Code.VisualElementsManifest.xml\n', b'Code.exe\n', b'LICENSES.chromium.html\n',

    # In [7]:  cmdinstance.stdin.close() # provoking a broken pipe

    # All subclasses of SubProcessInteractive reconnect automatically
    # In [8]: cmdinstance.sendcommand("ls")
    # ------------------------------------------
    # Traceback (most recent call last):
    #   File "C:\ProgramData\anaconda3\envs\a0\checkpowers.py", line 411, in sendcommand
    #     self._proc.stdin.write((cmd + f"\n{self.finish_command}\n").encode())
    # ValueError: write to closed file
    # ------------------------------------------
    # Restarting ...
    # Out[8]: [[], [], None]

    # In [9]: cmdinstance.sendcommand("ls")
    # Out[9]: [[b'Code.VisualElementsManifest.xml\n', b'Code.exe\n',

    bashinstance = SubProcessInteractiveBash(
        bash_path=r"C:\msys64\usr\bin\bash.exe",
        convert_to_83=True,
        daemon=True,
        restart_when_error=True,
        restart_tries=5,
        sleep_after_reconnection_attempt=5,
        print_stderr=False,
        print_stdout=False,
        return_error=True,
    )
    # In [13]: bashinstance.sendcommand("exit")
    # ------------------------------------------
    # Traceback (most recent call last):
    #   File "C:\ProgramData\anaconda3\envs\a0\checkpowers.py", line 435, in sendcommand
    #     while True:

    # StopIteration
    # ------------------------------------------
    # Out[13]: [[b'XXXXCOMMANDSTARTXXXX\n'], [], StopIteration()]

    # In [14]: bashinstance.sendcommand("ls")
    # ------------------------------------------
    # Traceback (most recent call last):
    #   File "C:\ProgramData\anaconda3\envs\a0\checkpowers.py", line 414, in sendcommand
    #     self._proc.stdin.write(cmd + b"\n" + self.finish_command_bytes + b"\n")
    #     ^^^^^^^^^^^^^^^^^^^^^^^^
    # OSError: [Errno 22] Invalid argument
    # ------------------------------------------
    # Restarting ...
    # Out[14]: [[], [], None]

    # In [15]: bashinstance.sendcommand("ls")
    # Out[15]: [[b'Code.VisualElementsManifest.xml\n', b'Code.exe\n', b'L
    #
    so1, se1, error = powershellinstance.sendcommand("ls")
    so2, se2, error = adbinstance.sendcommand("ls")
    so3, se3, error = cmdinstance.sendcommand("ls")

    print(f"{so1,so2,so3=}")
    print(f"{se1,se2,se3=}")

    so1, se1, error = powershellinstance.sendcommand("lsxx")
    so2, se2, error = adbinstance.sendcommand("lsxx")
    so3, se3, error = cmdinstance.sendcommand("lsxx")

    print(f"{so1,so2,so3=}")
    print(f"{se1,se2,se3=}")

    so3, se3, error = bashinstance.sendcommand("ls")
    print(f"{so3, se3, error=}")

    psout, pserr, pserror = powershellinstance.sendcommand(
        "Get-Process | Format-Table *"
    )
    print(psout)
```