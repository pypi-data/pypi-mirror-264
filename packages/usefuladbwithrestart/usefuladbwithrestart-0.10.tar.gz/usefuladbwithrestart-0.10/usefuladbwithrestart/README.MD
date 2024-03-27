# usefuladb with restart


### A version of https://github.com/hansalemaos/usefuladb that automatically reconnects if it gets disconnected

### pip install usefuladbwithrestart


```py
from usefuladbwithrestart import AdbWRestart

adb = AdbWRestart(
    adb_path=r"C:\ProgramData\chocolatey\lib\adb\tools\platform-tools\adb.exe",
    device_serial="127.0.0.1:5845",
    use_busybox=False,
    connect_to_device=True,
    print_stdout=False,
    print_stderr=False,
    convert_to_83=True,
    su=False,
    commandtimeout=30,
    escape_filepath=True,
    restart_when_error=True,
    restart_tries=10,
    sleep_after_reconnection_attempt=5,
)
```