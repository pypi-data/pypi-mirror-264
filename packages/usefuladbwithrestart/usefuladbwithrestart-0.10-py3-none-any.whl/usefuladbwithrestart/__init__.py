from interactiveshellsubproc import (
    SubProcessInteractiveAdb,
    RED,
    DEFAULT,
)
import subprocess
import threading
import sys
from usefuladb import AdbControl, invisibledict, get_short_path_name
import ast


class AdbWRestart(AdbControl):
    def __init__(
        self,
        adb_path,
        device_serial,
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
        *args,
        **kwargs,
    ):
        r"""
        Initializes an instance of the class.
        
        :param adb_path: The path to the ADB executable.
        :type adb_path: str
        :param device_serial: The serial number of the device to connect to.
        :type device_serial: str
        :param use_busybox: Whether to use busybox for adb commands.
        :type use_busybox: bool
        :param connect_to_device: Whether to connect to the device.
        :type connect_to_device: bool
        :param print_stdout: Whether to print stdout.
        :type print_stdout: bool
        :param print_stderr: Whether to print stderr.
        :type print_stderr: bool
        :param convert_to_83: Whether to convert the path to 8.3 format.
        :type convert_to_83: bool
        :param su: Whether to use su.
        :type su: bool
        :param commandtimeout: The timeout for commands.
        :type commandtimeout: int
        :param escape_filepath: Whether to escape the file path.
        :type escape_filepath: bool
        :param restart_when_error: Whether to restart when there is an error.
        :type restart_when_error: bool
        :param restart_tries: The number of times to try restarting.
        :type restart_tries: int
        :param sleep_after_reconnection_attempt: The time to sleep after reconnection attempt.
        :type sleep_after_reconnection_attempt: int
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        exitcommand = "xxxCOMMANDxxxDONExxx"

        super().__init__(
            adb_path=adb_path,
            device_serial=device_serial,
            use_busybox=use_busybox,
            connect_to_device=False,
            invisible=True,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            limit_stdout=None,
            limit_stderr=None,
            limit_stdin=None,
            convert_to_83=convert_to_83,
            wait_to_complete=.1,
            flush_stdout_before=True,
            flush_stdin_before=True,
            flush_stderr_before=True,
            exitcommand=exitcommand,
            capture_stdout_stderr_first=True,
            global_cmd=False,
            global_cmd_timeout=100,
            use_eval=False,
            eval_timeout=100,
        )
        self.daemon = True
        self.adbpath = adb_path
        self.device_serial = device_serial
        if convert_to_83:
            self.adb_path = get_short_path_name(adb_path)
        else:
            self.adb_path = adb_path
        if connect_to_device:
            subprocess.run([self.adb_path, "connect", device_serial], **invisibledict)
        self.device_serial = device_serial
        self.convert_to_83 = convert_to_83
        self.exitcommand = exitcommand
        self.su = su
        self.use_busybox = use_busybox
        self.adbpath = adb_path
        self.device_serial = device_serial
        if convert_to_83:
            self.adb_path = get_short_path_name(adb_path)
        else:
            self.adb_path = adb_path
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self.convert_to_83 = convert_to_83
        self.commandtimeout = commandtimeout
        self.escape_filepath = escape_filepath
        self.lockobject = threading.Lock()
        self.allcommands = []
        self.stdout = []
        self.stderr = []
        self.restart_when_error = restart_when_error
        self.restart_tries = restart_tries
        self.sleep_after_reconnection_attempt = sleep_after_reconnection_attempt
        self.get_last_adb_error = None
        self._proc_adbinstance = SubProcessInteractiveAdb(
            adb_path=self.adb_path,
            device_serial=device_serial,
            convert_to_83=convert_to_83,
            daemon=self.daemon,
            restart_when_error=restart_when_error,
            restart_tries=restart_tries,
            sleep_after_reconnection_attempt=sleep_after_reconnection_attempt,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
        )

    def execute_sh_command(self, cmd, **kwargs):
        self._correct_newlines = False
        if isinstance(cmd, str):
            try:
                stackframe = sys._getframe(1)
                for key, item in stackframe.f_locals.items():
                    if isinstance(item, bytes):
                        asstr = str(item)
                        if asstr in cmd:
                            cmd = cmd.replace(asstr, asstr[2:-1])
            except Exception as fe:
                sys.stderr.write(f"{fe}\n")
                sys.stderr.flush()

        oldvaluestdout = self.print_stdout
        oldvaluestderr = self.print_stderr

        disable_print_stdout = kwargs.get("disable_print_stdout", self.print_stdout)
        disable_print_stderr = kwargs.get("disable_print_stderr", self.print_stderr)
        su = kwargs.get("su", self.su)
        commandtimeout = kwargs.get("commandtimeout", self.commandtimeout)
        if "escape_filepath" in kwargs:
            del kwargs["escape_filepath"]

        if disable_print_stdout:
            self._proc_adbinstance.print_stdout = False
        if disable_print_stderr:
            self._proc_adbinstance.print_stderr = False

        try:
            if (cmd.startswith('b"') and cmd.endswith('"')) or (
                cmd.startswith("b'") and cmd.endswith("'")
            ):
                cmd = ast.literal_eval(str(cmd.encode("utf-8")))
        except Exception:
            pass

        if isinstance(cmd, bytes):
            if su:
                cmd = b"#!/usr/bin/env\nsu\n" + cmd
            else:
                cmd = b"#!/usr/bin/env\n" + cmd
            cmd = cmd.decode("utf-8")
        else:
            if su:
                cmd = "#!/usr/bin/env\nsu\n" + cmd
            else:
                cmd = "#!/usr/bin/env\n" + cmd

        use_busybox = kwargs.get("use_busybox", self.use_busybox)
        if use_busybox:
            cmd = "busybox " + cmd

        if commandtimeout > 0:
            stdo, stde, e = self._proc_adbinstance.sendcommand(
                cmd, timeout=commandtimeout
            )
        else:
            stdo, stde, e = self._proc_adbinstance.sendcommand(cmd)
        if e and self.print_stderr:
            print(
                "%s%s%s" % (RED, f"{e}", DEFAULT),
                end="\n",
            )
        self.get_last_adb_error = e
        self.print_stdout = oldvaluestdout
        self.print_stderr = oldvaluestderr
        return [stdo, stde]

