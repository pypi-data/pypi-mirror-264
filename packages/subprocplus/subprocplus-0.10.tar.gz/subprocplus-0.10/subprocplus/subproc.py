from __future__ import unicode_literals

from procciao import kill_proc
import collections
import ctypes
import os
import sys
import threading
from time import perf_counter
import time
from subprocplus.proc import ProcessError, Hook, MemoryRegion
from subprocplus.datatypes import windows as wintypesspec
from subprocplus.utilities import eval_number
from subprocplus.windll import kernel32 as m_k32
from subprocplus.windll import ntdll as m_ntdll
from subprocplus.windll import psapi as m_psapi
import subprocess
from copy import deepcopy

from ctypes import wintypes
import importlib
from rlogfi import PowerShellDetachedInteractive
from touchtouch import touch
import tempfile
import shutil

debug_is_enabled = True
DEFAULT = "\033[0m"
RED = "\033[91m"

windll = ctypes.LibraryLoader(ctypes.WinDLL)
kernel32 = windll.kernel32
advapi32 = windll.advapi32
user32 = windll.user32
shell32 = windll.shell32
ntdll = windll.ntdll
PROCESS_QUERY_INFROMATION = 0x1000
_GetShortPathNameW = kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD
folder = os.sep.join(__file__.split(os.sep)[:-1])


def get_tmpfile(suffix=".ps1"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def get_short_path_name(long_name):
    r"""
    Returns the short path name for the given long file name.

    Parameters:
        long_name (str): The long file name.

    Returns:
        str: The short path name if it exists, otherwise the long file name.
    """
    try:
        if os.path.exists(long_name):
            output_buf_size = 4096
            output_buf = ctypes.create_unicode_buffer(output_buf_size)
            _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
            return output_buf.value
    except Exception:
        pass
    return long_name


pse = shutil.which("powershell.exe")
workingdir = os.getcwd()
workingdirshort = get_short_path_name(workingdir)
# pse_short = get_short_path_name(pse)

try:
    np = importlib.import_module("numpy")
except Exception:
    np = None


def ctarray_to_bytes(ctarray):
    """
    Convert ctypes array into a bytes object.

    :param ctarray: The ctypes array to convert.
    :return: The converted ctypes array.
    :rtype: bytes
    """
    if np:
        if not len(ctarray):
            return np.array([], dtype=np.uint8)
        return np.ctypeslib.as_array(ctarray)
    if not len(ctarray):
        # work around a bug in v3.1 & v3.2 that results in a segfault when len(ctarray) == 0
        return bytes()
    return bytes(ctarray)  # [:]


ERROR_INVALID_HANDLE = 0x0006
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
INVALID_DWORD_VALUE = wintypes.DWORD(-1).value

DEBUG_PROCESS = 0x00000001
DEBUG_ONLY_THIS_PROCESS = 0x00000002
CREATE_SUSPENDED = 0x00000004
DETACHED_PROCESS = 0x00000008
CREATE_NEW_CONSOLE = 0x00000010
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_UNICODE_ENVIRONMENT = 0x00000400
CREATE_SEPARATE_WOW_VDM = 0x00000800
CREATE_SHARED_WOW_VDM = 0x00001000
INHERIT_PARENT_AFFINITY = 0x00010000
CREATE_PROTECTED_PROCESS = 0x00040000
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
CREATE_PRESERVE_CODE_AUTHZ_LEVEL = 0x02000000
CREATE_DEFAULT_ERROR_MODE = 0x04000000
CREATE_NO_WINDOW = 0x08000000

STARTF_USESHOWWINDOW = 0x00000001
STARTF_USESIZE = 0x00000002
STARTF_USEPOSITION = 0x00000004
STARTF_USECOUNTCHARS = 0x00000008
STARTF_USEFILLATTRIBUTE = 0x00000010
STARTF_RUNFULLSCREEN = 0x00000020
STARTF_FORCEONFEEDBACK = 0x00000040
STARTF_FORCEOFFFEEDBACK = 0x00000080
STARTF_USESTDHANDLES = 0x00000100
STARTF_USEHOTKEY = 0x00000200
STARTF_TITLEISLINKNAME = 0x00000800
STARTF_TITLEISAPPID = 0x00001000
STARTF_PREVENTPINNING = 0x00002000

SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10  # ~STARTUPINFO
SW_FORCEMINIMIZE = 11

LOGON_WITH_PROFILE = 0x00000001
LOGON_NETCREDENTIALS_ONLY = 0x00000002

STD_INPUT_HANDLE = wintypes.DWORD(-10).value
STD_OUTPUT_HANDLE = wintypes.DWORD(-11).value
STD_ERROR_HANDLE = wintypes.DWORD(-12).value


class HANDLE(wintypes.HANDLE):
    __slots__ = ("closed",)

    def __int__(self):
        return self.value or 0

    def Detach(self):
        if not getattr(self, "closed", False):
            self.closed = True
            value = int(self)
            self.value = None
            return value
        raise ValueError("already closed")

    def Close(self, CloseHandle=kernel32.CloseHandle):
        if self and not getattr(self, "closed", False):
            CloseHandle(self.Detach())

    __del__ = Close

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, int(self))


class PROCESS_INFORMATION(ctypes.Structure):
    """https://msdn.microsoft.com/en-us/library/ms684873"""

    __slots__ = "_cached_hProcess", "_cached_hThread"

    _fields_ = (
        ("_hProcess", HANDLE),
        ("_hThread", HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    )

    @property
    def hProcess(self):
        if not hasattr(self, "_cached_hProcess"):
            self._cached_hProcess = self._hProcess
        return self._cached_hProcess

    @property
    def hThread(self):
        if not hasattr(self, "_cached_hThread"):
            self._cached_hThread = self._hThread
        return self._cached_hThread

    def __del__(self):
        try:
            self.hProcess.Close()
        finally:
            self.hThread.Close()


LPPROCESS_INFORMATION = ctypes.POINTER(PROCESS_INFORMATION)

LPBYTE = ctypes.POINTER(wintypes.BYTE)


class STARTUPINFO(ctypes.Structure):
    """https://msdn.microsoft.com/en-us/library/ms686331"""

    _fields_ = (
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    )

    def __init__(self, **kwds):
        self.cb = ctypes.sizeof(self)
        super(STARTUPINFO, self).__init__(**kwds)


class PROC_THREAD_ATTRIBUTE_LIST(ctypes.Structure):
    pass


PPROC_THREAD_ATTRIBUTE_LIST = ctypes.POINTER(PROC_THREAD_ATTRIBUTE_LIST)


class STARTUPINFOEX(STARTUPINFO):
    _fields_ = (("lpAttributeList", PPROC_THREAD_ATTRIBUTE_LIST),)


LPSTARTUPINFO = ctypes.POINTER(STARTUPINFO)
LPSTARTUPINFOEX = ctypes.POINTER(STARTUPINFOEX)


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = (
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", wintypes.LPVOID),
        ("bInheritHandle", wintypes.BOOL),
    )

    def __init__(self, **kwds):
        self.nLength = ctypes.sizeof(self)
        super(SECURITY_ATTRIBUTES, self).__init__(**kwds)


LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)


class HANDLE_IHV(HANDLE):
    pass


class DWORD_IDV(wintypes.DWORD):
    pass


def _check_ihv(result, func, args):
    if result.value == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    return result.value


def _check_idv(result, func, args):
    if result.value == INVALID_DWORD_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    return result.value


def _check_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


def WIN(func, restype, *argtypes):
    func.restype = restype
    func.argtypes = argtypes
    if issubclass(restype, HANDLE_IHV):
        func.errcheck = _check_ihv
    elif issubclass(restype, DWORD_IDV):
        func.errcheck = _check_idv
    else:
        func.errcheck = _check_bool


# https://msdn.microsoft.com/en-us/library/ms724211
WIN(
    kernel32.CloseHandle,
    wintypes.BOOL,
    wintypes.HANDLE,
)  # _In_ HANDLE hObject

# https://msdn.microsoft.com/en-us/library/ms685086
WIN(
    kernel32.ResumeThread,
    DWORD_IDV,
    wintypes.HANDLE,
)  # _In_ hThread

# https://msdn.microsoft.com/en-us/library/ms682425
WIN(
    kernel32.CreateProcessW,
    wintypes.BOOL,
    wintypes.LPCWSTR,  # _In_opt_    lpApplicationName
    wintypes.LPWSTR,  # _Inout_opt_ lpCommandLine
    LPSECURITY_ATTRIBUTES,  # _In_opt_    lpProcessAttributes
    LPSECURITY_ATTRIBUTES,  # _In_opt_    lpThreadAttributes
    wintypes.BOOL,  # _In_        bInheritHandles
    wintypes.DWORD,  # _In_        dwCreationFlags
    wintypes.LPCWSTR,  # _In_opt_    lpEnvironment
    wintypes.LPCWSTR,  # _In_opt_    lpCurrentDirectory
    LPSTARTUPINFO,  # _In_        lpStartupInfo
    LPPROCESS_INFORMATION,
)  # _Out_       lpProcessInformation

# https://msdn.microsoft.com/en-us/library/ms682429
WIN(
    advapi32.CreateProcessAsUserW,
    wintypes.BOOL,
    wintypes.HANDLE,  # _In_opt_    hToken
    wintypes.LPCWSTR,  # _In_opt_    lpApplicationName
    wintypes.LPWSTR,  # _Inout_opt_ lpCommandLine
    LPSECURITY_ATTRIBUTES,  # _In_opt_    lpProcessAttributes
    LPSECURITY_ATTRIBUTES,  # _In_opt_    lpThreadAttributes
    wintypes.BOOL,  # _In_        bInheritHandles
    wintypes.DWORD,  # _In_        dwCreationFlags
    wintypes.LPCWSTR,  # _In_opt_    lpEnvironment
    wintypes.LPCWSTR,  # _In_opt_    lpCurrentDirectory
    LPSTARTUPINFO,  # _In_        lpStartupInfo
    LPPROCESS_INFORMATION,
)  # _Out_       lpProcessInformation

# https://msdn.microsoft.com/en-us/library/ms682434
WIN(
    advapi32.CreateProcessWithTokenW,
    wintypes.BOOL,
    wintypes.HANDLE,  # _In_        hToken
    wintypes.DWORD,  # _In_        dwLogonFlags
    wintypes.LPCWSTR,  # _In_opt_    lpApplicationName
    wintypes.LPWSTR,  # _Inout_opt_ lpCommandLine
    wintypes.DWORD,  # _In_        dwCreationFlags
    wintypes.LPCWSTR,  # _In_opt_    lpEnvironment
    wintypes.LPCWSTR,  # _In_opt_    lpCurrentDirectory
    LPSTARTUPINFO,  # _In_        lpStartupInfo
    LPPROCESS_INFORMATION,
)  # _Out_       lpProcessInformation

# https://msdn.microsoft.com/en-us/library/ms682431
WIN(
    advapi32.CreateProcessWithLogonW,
    wintypes.BOOL,
    wintypes.LPCWSTR,  # _In_        lpUsername
    wintypes.LPCWSTR,  # _In_opt_    lpDomain
    wintypes.LPCWSTR,  # _In_        lpPassword
    wintypes.DWORD,  # _In_        dwLogonFlags
    wintypes.LPCWSTR,  # _In_opt_    lpApplicationName
    wintypes.LPWSTR,  # _Inout_opt_ lpCommandLine
    wintypes.DWORD,  # _In_        dwCreationFlags
    wintypes.LPCWSTR,  # _In_opt_    lpEnvironment
    wintypes.LPCWSTR,  # _In_opt_    lpCurrentDirectory
    LPSTARTUPINFO,  # _In_        lpStartupInfo
    LPPROCESS_INFORMATION,
)  # _Out_       lpProcessInformation

CREATION_TYPE_NORMAL = 0
CREATION_TYPE_LOGON = 1
CREATION_TYPE_TOKEN = 2
CREATION_TYPE_USER = 3


class CREATIONINFO(object):
    __slots__ = (
        "dwCreationType",
        "lpApplicationName",
        "lpCommandLine",
        "bUseShell",
        "lpProcessAttributes",
        "lpThreadAttributes",
        "bInheritHandles",
        "dwCreationFlags",
        "lpEnvironment",
        "lpCurrentDirectory",
        "hToken",
        "lpUsername",
        "lpDomain",
        "lpPassword",
        "dwLogonFlags",
    )

    def __init__(
        self,
        dwCreationType=CREATION_TYPE_NORMAL,
        lpApplicationName=None,
        lpCommandLine=None,
        bUseShell=False,
        lpProcessAttributes=None,
        lpThreadAttributes=None,
        bInheritHandles=False,
        dwCreationFlags=0,
        lpEnvironment=None,
        lpCurrentDirectory=None,
        hToken=None,
        dwLogonFlags=0,
        lpUsername=None,
        lpDomain=None,
        lpPassword=None,
    ):
        self.dwCreationType = dwCreationType
        self.lpApplicationName = lpApplicationName
        self.lpCommandLine = lpCommandLine
        self.bUseShell = bUseShell
        self.lpProcessAttributes = lpProcessAttributes
        self.lpThreadAttributes = lpThreadAttributes
        self.bInheritHandles = bInheritHandles
        self.dwCreationFlags = dwCreationFlags
        self.lpEnvironment = lpEnvironment
        self.lpCurrentDirectory = lpCurrentDirectory
        self.hToken = hToken
        self.lpUsername = lpUsername
        self.lpDomain = lpDomain
        self.lpPassword = lpPassword
        self.dwLogonFlags = dwLogonFlags


def create_environment(environ):
    if environ is not None:
        items = ["%s=%s" % (k, environ[k]) for k in sorted(environ)]
        buf = "\x00".join(items)
        length = len(buf) + 2 if buf else 1
        return ctypes.create_unicode_buffer(buf, length)


def create_process(commandline=None, creationinfo=None, startupinfo=None):
    if creationinfo is None:
        creationinfo = CREATIONINFO()

    if startupinfo is None:
        startupinfo = STARTUPINFO()
    elif isinstance(startupinfo, subprocess.STARTUPINFO):
        startupinfo = STARTUPINFO(
            dwFlags=startupinfo.dwFlags,
            hStdInput=startupinfo.hStdInput,
            hStdOutput=startupinfo.hStdOutput,
            hStdError=startupinfo.hStdError,
            wShowWindow=startupinfo.wShowWindow,
        )

    si, ci, pi = startupinfo, creationinfo, PROCESS_INFORMATION()

    if commandline is None:
        commandline = ci.lpCommandLine

    if commandline is not None:
        if ci.bUseShell:
            si.dwFlags |= STARTF_USESHOWWINDOW
            si.wShowWindow = SW_HIDE
            comspec = os.environ.get(
                "ComSpec", os.path.join(os.environ["SystemRoot"], "System32", "cmd.exe")
            )
            commandline = '"{}" /c "{}"'.format(comspec, commandline)
        commandline = ctypes.create_unicode_buffer(commandline)

    dwCreationFlags = ci.dwCreationFlags | CREATE_UNICODE_ENVIRONMENT
    lpEnvironment = create_environment(ci.lpEnvironment)

    if dwCreationFlags & DETACHED_PROCESS and (
        (dwCreationFlags & CREATE_NEW_CONSOLE)
        or (ci.dwCreationType == CREATION_TYPE_LOGON)
        or (ci.dwCreationType == CREATION_TYPE_TOKEN)
    ):
        raise RuntimeError(
            "DETACHED_PROCESS is incompatible with "
            "CREATE_NEW_CONSOLE, which is implied for "
            "the logon and token creation types"
        )

    if ci.dwCreationType == CREATION_TYPE_NORMAL:
        kernel32.CreateProcessW(
            ci.lpApplicationName,
            commandline,
            ci.lpProcessAttributes,
            ci.lpThreadAttributes,
            ci.bInheritHandles,
            dwCreationFlags,
            lpEnvironment,
            ci.lpCurrentDirectory,
            ctypes.byref(si),
            ctypes.byref(pi),
        )

    elif ci.dwCreationType == CREATION_TYPE_LOGON:
        advapi32.CreateProcessWithLogonW(
            ci.lpUsername,
            ci.lpDomain,
            ci.lpPassword,
            ci.dwLogonFlags,
            ci.lpApplicationName,
            commandline,
            dwCreationFlags,
            lpEnvironment,
            ci.lpCurrentDirectory,
            ctypes.byref(si),
            ctypes.byref(pi),
        )

    elif ci.dwCreationType == CREATION_TYPE_TOKEN:
        advapi32.CreateProcessWithTokenW(
            ci.hToken,
            ci.dwLogonFlags,
            ci.lpApplicationName,
            commandline,
            dwCreationFlags,
            lpEnvironment,
            ci.lpCurrentDirectory,
            ctypes.byref(si),
            ctypes.byref(pi),
        )

    elif ci.dwCreationType == CREATION_TYPE_USER:
        advapi32.CreateProcessAsUserW(
            ci.hToken,
            ci.lpApplicationName,
            commandline,
            ci.lpProcessAttributes,
            ci.lpThreadAttributes,
            ci.bInheritHandles,
            dwCreationFlags,
            lpEnvironment,
            ci.lpCurrentDirectory,
            ctypes.byref(si),
            ctypes.byref(pi),
        )

    else:
        raise ValueError("invalid process creation type")

    return pi


CONSTANTS = {
    "GENERIC_READ": 0x80000000,
    "GENERIC_WRITE": 0x40000000,
    "OPEN_EXISTING": 0x03,
    "CREATE_ALWAYS": 0x02,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa366890%28v=vs.85%29.aspx
    "MEM_COMMIT": 0x00001000,
    "MEM_RESERVE": 0x00002000,
    "MEM_RESET": 0x00080000,
    "MEM_RESET_UNDO": 0x01000000,
    "MEM_LARGE_PAGES": 0x20000000,
    "MEM_PHYSICAL": 0x00400000,
    "MEM_TOP_DOWN": 0x00100000,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa366775%28v=vs.85%29.aspx
    "MEM_IMAGE": 0x01000000,
    "MEM_MAPPED": 0x00040000,
    "MEM_PRIVATE": 0x00020000,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa366894%28v=vs.85%29.aspx
    "MEM_DECOMMIT": 0x4000,
    "MEM_RELEASE": 0x8000,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa366786%28v=vs.85%29.aspx
    "PAGE_EXECUTE": 0x10,
    "PAGE_EXECUTE_READ": 0x20,
    "PAGE_EXECUTE_READWRITE": 0x40,
    "PAGE_EXECUTE_WRITECOPY": 0x80,
    "PAGE_NOACCESS": 0x01,
    "PAGE_READONLY": 0x02,
    "PAGE_READWRITE": 0x04,
    "PAGE_WRITECOPY": 0x08,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ms684880%28v=vs.85%29.aspx
    "PROCESS_CREATE_PROCESS": 0x0080,
    "PROCESS_CREATE_THREAD": 0x0002,
    "PROCESS_DUP_HANDLE": 0x0040,
    "PROCESS_QUERY_INFORMATION": 0x0400,
    "PROCESS_QUERY_LIMITED_INFORMATION": 0x1000,
    "PROCESS_SET_INFORMATION": 0x0200,
    "PROCESS_SET_QUOTA": 0x0100,
    "PROCESS_SUSPEND_RESUME": 0x0800,
    "PROCESS_TERMINATE": 0x0001,
    "PROCESS_VM_OPERATION": 0x0008,
    "PROCESS_VM_READ": 0x0010,
    "PROCESS_VM_WRITE": 0x0020,
    "SYNCHRONIZE": 0x00100000,
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa363858%28v:vs.85%29.aspx
    "FILE_SHARE_READ": 0x00000001,
    "FILE_SHARE_WRITE": 0x00000002,
    "FILE_SHARE_DELETE": 0x00000004,
    "FILE_FLAG_OVERLAPPED": 0x40000000,
}

IMAGE_DIRECTORY_ENTRY_EXPORT = 0
IMAGE_DIRECTORY_ENTRY_IMPORT = 1
IMAGE_DIRECTORY_ENTRY_RESOURCE = 2
IMAGE_DIRECTORY_ENTRY_BASERELOC = 5
IMAGE_DIRECTORY_ENTRY_DEBUG = 6
IMAGE_DIRECTORY_ENTRY_TLS = 9


class WindowsProcessError(ProcessError):
    def __init__(self, *args, **kwargs):
        self.get_last_error = None
        if "get_last_error" in kwargs:
            self.get_last_error = kwargs["get_last_error"]
            del kwargs["get_last_error"]
        ProcessError.__init__(self, *args, **kwargs)


def flags(flags):
    supported_operators = ["|", "+", "-", "^"]
    if isinstance(flags, int):
        return flags
    if flags[0] == "(" and flags[-1] == ")":
        flags = flags[1:-1]
    for sop in supported_operators:
        flags = flags.replace(sop, " " + sop + " ")
    flags = flags.split()
    parsed_flags = 0
    last_operator = None
    for part in flags:
        if part in CONSTANTS:
            part = CONSTANTS[part]
        elif part in supported_operators:
            last_operator = part
            continue
        else:
            part = eval_number(part)
        if last_operator is None:
            parsed_flags = part
        else:
            parsed_flags = eval(str(parsed_flags) + last_operator + str(part))
    return parsed_flags


def process_is_wow64(handle=None):
    """
    Determine whether the process associated with the handle is running
    in WOW64 or not.

    :param int handle: A handle to the process to check.
    :return: Whether the process is running in WOW64 or not.
    :rtype: bool
    """
    if not hasattr(m_k32, "IsWow64Process"):
        return False
    handle = handle or -1
    is_wow64 = ctypes.c_bool()
    if not m_k32.IsWow64Process(handle, ctypes.byref(is_wow64)):
        raise WindowsProcessError(
            "Error: IsWow64Process", get_last_error=m_k32.GetLastError()
        )
    return is_wow64.value


class Popen(subprocess.Popen):
    def __init__(self, *args, **kwds):
        self.oldkwargs = deepcopy(kwds)
        self.oldargs = args
        ci = self._creationinfo = kwds.pop("creationinfo", CREATIONINFO())
        self.out_dict = {}
        self.err_dict = {}
        self.print_stdout = kwds.pop("print_stdout", True)
        self.print_stderr = kwds.pop("print_stderr", True)
        self.__arch__ = "x64"
        if kwds.pop("suspended", False):
            ci.dwCreationFlags |= CREATE_SUSPENDED
        self._child_started = False
        super(Popen, self).__init__(*args, **kwds)
        self.handle = self._handle
        _name = ctypes.c_char * 0x400
        name = _name()
        if hasattr(m_psapi, "GetModuleFileNameExA"):
            m_psapi.GetModuleFileNameExA(self.handle, 0, name, ctypes.sizeof(name))
        else:
            m_k32.GetModuleFileNameExA(self.handle, 0, name, ctypes.sizeof(name))
        self.exe_file = b"".join(name).rstrip(b"\x00").decode("utf-8")
        self._installed_hooks = []

        self.t1 = threading.Thread(target=self.readstdout)
        self.t2 = threading.Thread(target=self.readstderr)
        self.t1.start()
        self.t2.start()

    def restart_proc(self, sleep_after_kill=10):
        self.close()
        time.sleep(sleep_after_kill)
        self.__init__(*self.oldargs, **self.oldkwargs)
        return self

    def readstdout(self):
        for l in iter(self.stdout.readline, b""):
            try:
                self.out_dict[perf_counter()] = l
                time.sleep(0.0000001)

                if self.print_stdout:
                    sys.stdout.write(f'{l.decode("utf-8", "backslashreplace")}')

            except Exception as e:
                print(e)
                break

    # Function to read and print stderr of the subprocess
    def readstderr(
        self,
    ):
        for l in iter(self.stderr.readline, b""):
            try:
                self.err_dict[perf_counter()] = l
                time.sleep(0.0000001)
                if self.print_stderr:
                    v = "%s%s%s" % (
                        RED,
                        f'{l.decode("utf-8", "backslashreplace")}',
                        DEFAULT,
                    )
                    sys.stderr.write(v)
            except Exception as e:
                print(e)
                break

    def sendcommand(
        self,
        cmd,
        clean_old=True,
        restart_on_fail=True,
        max_restarts=3,
        sleep_after_restart=10,
        **kwargs,
    ):
        number_of_restarts = kwargs.pop("restart_on_fail_counter", 0)
        if clean_old:
            self.out_dict.clear()
            self.err_dict.clear()
            time.sleep(0.01)
        if isinstance(cmd, str):
            cmd = cmd.encode()
        try:
            self.stdin.write(cmd + b"\n")
            self.stdin.flush()
        except Exception as e:
            if restart_on_fail:
                if number_of_restarts < max_restarts:
                    number_of_restarts += 1
                    self.restart_proc(sleep_after_kill=sleep_after_restart)
                    kwargs["restart_on_fail_counter"] = number_of_restarts
                    self.sendcommand(
                        cmd=cmd,
                        clean_old=clean_old,
                        restart_on_fail=restart_on_fail,
                        max_restarts=max_restarts,
                        sleep_after_restart=sleep_after_restart,
                        **kwargs,
                    )
                else:
                    raise e
            else:
                raise e

    def get_proc_attribute(self, attribute):
        requested_attribute = attribute
        if attribute.startswith("&"):
            attribute = attribute[1:] + "_addr"
        if hasattr(self, "_get_attr_" + attribute):
            return getattr(self, "_get_attr_" + attribute)()
        raise ProcessError("Unknown Attribute: " + requested_attribute)

    def _get_attr_peb_addr(self):
        process_basic_information = wintypesspec.PROCESS_BASIC_INFORMATION()
        return_length = wintypesspec.DWORD()
        m_ntdll.NtQueryInformationProcess(
            self.handle,
            0,
            ctypes.byref(process_basic_information),
            ctypes.sizeof(process_basic_information),
            ctypes.byref(return_length),
        )
        return process_basic_information.PebBaseAddress

    def _get_attr_peb(self):
        peb_addr = self.get_proc_attribute("peb_addr")
        peb = wintypesspec.PEB()
        m_k32.ReadProcessMemory(
            self.handle, peb_addr, ctypes.byref(peb), ctypes.sizeof(peb), 0
        )
        return peb

    def _get_attr_peb_ldr_data_addr(self):
        peb = self.get_proc_attribute("peb")
        return peb.Ldr

    def _get_attr_peb_ldr_data(self):
        peb_ldr_data_addr = self.get_proc_attribute("peb_ldr_data_addr")
        peb_ldr_data = wintypesspec.PEB_LDR_DATA()
        m_k32.ReadProcessMemory(
            self.handle,
            peb_ldr_data_addr,
            ctypes.byref(peb_ldr_data),
            ctypes.sizeof(peb_ldr_data),
            0,
        )
        return peb_ldr_data

    def _get_attr_image_dos_header_addr(self):
        return self.get_proc_attribute("peb").ImageBaseAddress

    def _get_attr_image_dos_header(self):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        image_dos_header = wintypesspec.IMAGE_DOS_HEADER()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr,
            ctypes.byref(image_dos_header),
            ctypes.sizeof(image_dos_header),
            0,
        )
        return image_dos_header

    def _get_attr_image_nt_headers_addr(self):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        image_dos_header = self.get_proc_attribute("image_dos_header")
        return image_dos_header_addr + image_dos_header.e_lfanew

    def _get_attr_image_nt_headers(self):
        if self.__arch__ == "x86":
            image_nt_headers = wintypesspec.IMAGE_NT_HEADERS32()
        else:
            raise Exception("the selected architecture is not supported")
        m_k32.ReadProcessMemory(
            self.handle,
            self.get_proc_attribute("image_nt_headers_addr"),
            ctypes.byref(image_nt_headers),
            ctypes.sizeof(image_nt_headers),
            0,
        )
        return image_nt_headers

    def _get_attr_image_import_descriptor_addr(self):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        optional_header = self.get_proc_attribute("image_nt_headers").OptionalHeader
        return (
            image_dos_header_addr
            + optional_header.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress
        )

    def _get_attr_image_import_descriptor(self):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        optional_header = self.get_proc_attribute("image_nt_headers").OptionalHeader

        import_directory = optional_header.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]
        _import_descriptors = wintypesspec.IMAGE_IMPORT_DESCRIPTOR * (
            (
                import_directory.Size
                / ctypes.sizeof(wintypesspec.IMAGE_IMPORT_DESCRIPTOR)
            )
            - 1
        )
        import_descriptors = _import_descriptors()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr + import_directory.VirtualAddress,
            ctypes.byref(import_descriptors),
            ctypes.sizeof(import_descriptors),
            0,
        )
        return import_descriptors

    def _get_attr_system_info(self):
        system_info = wintypesspec.SYSTEM_INFO()
        m_k32.GetSystemInfo(ctypes.byref(system_info))
        # m_k32.GetSystemInfo((system_info))

        return system_info

    def _get_name_for_ilt_entry(self, ilt_ent):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        _name = ctypes.c_char * 0x200
        name = _name()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr + ilt_ent + ctypes.sizeof(wintypesspec.WORD),
            ctypes.byref(name),
            ctypes.sizeof(name),
            0,
        )
        name = "".join(name)
        name = name.split("\x00")[0]
        return name

    def _get_ordinal_for_ilt_entry(self, ilt_ent):
        return ilt_ent & 0x7FFFFFFF

    def _get_name_for_image_import_descriptor(self, iid):
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        _name = ctypes.c_char * 0x400
        name = _name()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr + iid.Name,
            ctypes.byref(name),
            ctypes.sizeof(name),
            0,
        )
        name = "".join(name)
        name = name.split("\x00")[0]
        return name

    def _get_ilt_for_image_import_descriptor(self, iid):  # import lookup table
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        _ilt = ctypes.c_void_p * 0x200
        ilt = _ilt()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr + iid.OriginalFirstThunk,
            ctypes.byref(ilt),
            ctypes.sizeof(ilt),
            0,
        )
        return ilt

    def _get_iat_for_image_import_descriptor(self, iid):  # import address table
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        _iat = ctypes.c_void_p * 0x200
        iat = _iat()
        m_k32.ReadProcessMemory(
            self.handle,
            image_dos_header_addr + iid.FirstThunk,
            ctypes.byref(iat),
            ctypes.sizeof(iat),
            0,
        )
        return iat

    def _get_image_base_by_name(self, name):
        peb_ldr_data = self.get_proc_attribute("peb_ldr_data")

        firstFLink = 0
        fLink = peb_ldr_data.InLoadOrderModuleList.Flink
        while fLink != firstFLink:
            firstFLink = peb_ldr_data.InLoadOrderModuleList.Flink
            module = wintypesspec.LDR_MODULE()

            m_k32.ReadProcessMemory(
                self.handle, fLink, ctypes.byref(module), ctypes.sizeof(module), 0
            )

            _base_dll_name = ctypes.c_wchar * module.BaseDllName.MaximumLength
            base_dll_name = _base_dll_name()

            m_k32.ReadProcessMemory(
                self.handle,
                module.BaseDllName.Buffer,
                base_dll_name,
                module.BaseDllName.Length + 2,
                0,
            )
            base_dll_name = base_dll_name[: (module.BaseDllName.Length / 2)]
            if name == base_dll_name:
                return module
            fLink = module.InLoadOrderModuleList.Flink
        return None

    @property
    def maps(self):
        sys_info = self.get_proc_attribute("system_info")
        _maps = collections.deque()
        address_cursor = 0
        VirtualQueryEx = m_k32.VirtualQueryEx
        meminfo = wintypesspec.MEMORY_BASIC_INFORMATION()
        MEM_COMMIT = flags("MEM_COMMIT")
        MEM_PRIVATE = flags("MEM_PRIVATE")
        PROTECT_FLAGS = {
            0x01: "---",
            0x02: "r--",
            0x04: "rw-",
            0x08: "r--",
            0x10: "--x",
            0x20: "r-x",
            0x40: "rwx",
            0x80: "r-x",
        }
        while address_cursor < sys_info.lpMaximumApplicationAddress:
            if (
                VirtualQueryEx(
                    self.handle,
                    address_cursor,
                    ctypes.byref(meminfo),
                    ctypes.sizeof(meminfo),
                )
                == 0
            ):
                break
            address_cursor = meminfo.BaseAddress + meminfo.RegionSize
            if not meminfo.State & MEM_COMMIT:
                continue
            addr_low = meminfo.BaseAddress
            addr_high = address_cursor
            perms = PROTECT_FLAGS[meminfo.Protect & 0xFF]
            perms += "p" if meminfo.Type & MEM_PRIVATE else "s"
            _maps.append(MemoryRegion(addr_low, addr_high, perms))
        return collections.OrderedDict(
            (mr.addr_low, mr) for mr in sorted(_maps, key=lambda mr: mr.addr_low)
        )

    def install_hook(self, mod_name, new_address, name=None, ordinal=None):
        if not (bool(name) ^ bool(ordinal)):
            raise ValueError("must select either name or ordinal, not both")
        image_import_descriptors = self.get_proc_attribute("image_import_descriptor")
        image_dos_header_addr = self.get_proc_attribute("image_dos_header_addr")
        is_ordinal = lambda x: bool(x & 0x80000000)

        for iid in image_import_descriptors:
            cur_mod_name = self._get_name_for_image_import_descriptor(iid)
            if cur_mod_name.lower() != mod_name.lower():
                continue
            ilt = self._get_ilt_for_image_import_descriptor(iid)
            iat = self._get_iat_for_image_import_descriptor(iid)

            for idx in range(len(ilt)):
                if ilt[idx] is None:
                    continue
                hook_it = False
                if not is_ordinal(ilt[idx]) and name:
                    cur_func_name = self._get_name_for_ilt_entry(ilt[idx])
                    if cur_func_name == name:
                        hook_it = True
                elif is_ordinal(ilt[idx]) and ordinal:
                    cur_func_ordinal = self._get_ordinal_for_ilt_entry(ilt[idx])
                    if cur_func_ordinal == ordinal:
                        hook_it = True
                if hook_it:
                    old_address = iat[idx]

                    iat_ent_addr = image_dos_header_addr
                    iat_ent_addr += iid.FirstThunk
                    iat_ent_addr += ctypes.sizeof(ctypes.c_void_p) * idx

                    new_addr = ctypes.c_void_p()
                    new_addr.value = new_address
                    written = wintypesspec.DWORD()
                    if (
                        m_k32.WriteProcessMemory(
                            self.handle,
                            iat_ent_addr,
                            ctypes.byref(new_addr),
                            ctypes.sizeof(new_addr),
                            ctypes.byref(written),
                        )
                        == 0
                    ):
                        errno = m_k32.GetLastError()
                        if errno == 998:
                            errno = 0
                            old_permissions = wintypesspec.DWORD()
                            if (
                                m_k32.VirtualProtectEx(
                                    self.handle,
                                    iat_ent_addr,
                                    0x400,
                                    flags("PAGE_READWRITE"),
                                    ctypes.byref(old_permissions),
                                )
                                == 0
                            ):
                                raise WindowsProcessError(
                                    "Error: VirtualProtectEx",
                                    get_last_error=m_k32.GetLastError(),
                                )
                            if (
                                m_k32.WriteProcessMemory(
                                    self.handle,
                                    iat_ent_addr,
                                    ctypes.byref(new_addr),
                                    ctypes.sizeof(new_addr),
                                    ctypes.byref(written),
                                )
                                == 0
                            ):
                                errno = m_k32.GetLastError()
                            self.protect(iat_ent_addr, permissions=old_permissions)
                        if errno:
                            raise WindowsProcessError(
                                "Error: WriteProcessMemory", get_last_error=errno
                            )
                    hook = Hook("iat", iat_ent_addr, old_address, new_address)
                    self._installed_hooks.append(hook)
                    return hook
        raise ProcessError("failed to find location to install hook")

    def close(self):
        try:
            kill_proc(self.pid, kill_timeout=5, print_output=False)
        except Exception:
            pass
        try:
            self._close_my_pipes()
        except Exception:
            pass
        try:
            super().close()
        except Exception:
            pass
        try:
            m_k32.CloseHandle(self.handle)
        except Exception:
            pass
        try:
            killthread(self.t1)
        except Exception:
            pass
        try:
            killthread(self.t2)
        except Exception:
            pass
        # killthread(self.t2)
        try:
            m_k32.TerminateProcess(self.handle, 0)
        except Exception:
            pass
        self.handle = None
        self.pid = None

    def _close_my_pipes(self):
        try:
            self.stdout.close()
        except Exception:
            pass

        try:
            self.stdin.close()
        except Exception:
            pass

        try:
            self.stderr.close()
        except Exception:
            pass

    def kill(self):
        self.close()

    def load_library(self, libpath):
        libpath = os.path.abspath(libpath)
        libpath_bytes = libpath.encode("utf-8") + b"\x00"
        remote_page = m_k32.VirtualAllocEx(
            self.handle,
            None,
            len(libpath_bytes),
            flags("MEM_COMMIT"),
            flags("PAGE_EXECUTE_READWRITE"),
        )
        if not remote_page:
            raise WindowsProcessError(
                "Error: failed to allocate space for library name in the target process"
            )
        if not m_k32.WriteProcessMemory(
            self.handle, remote_page, libpath_bytes, len(libpath_bytes), None
        ):
            raise WindowsProcessError(
                "Error: failed to copy the library name to the target process"
            )
        remote_thread = m_k32.CreateRemoteThread(
            self.handle, None, 0, m_k32.LoadLibraryA.address, remote_page, 0, None
        )
        m_k32.WaitForSingleObject(remote_thread, -1)

        exitcode = wintypesspec.DWORD(0)
        m_k32.GetExitCodeThread(remote_thread, ctypes.byref(exitcode))
        m_k32.VirtualFreeEx(
            self.handle, remote_page, len(libpath_bytes), flags("MEM_RELEASE")
        )
        if exitcode.value == 0:
            raise WindowsProcessError(
                "Error: failed to load: {0}, thread exited with status: 0x{1:x}".format(
                    libpath, exitcode.value
                )
            )
        return exitcode.value

    def read_memory(self, address, size=0x400):
        _data = ctypes.c_byte * size
        data = _data()
        if (
            m_k32.ReadProcessMemory(
                self.handle, address, ctypes.byref(data), ctypes.sizeof(data), 0
            )
            == 0
        ):
            raise WindowsProcessError(
                "Error: ReadProcessMemory", get_last_error=m_k32.GetLastError()
            )
        return ctarray_to_bytes(data)

    def write_memory(self, address, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        _wr_data = ctypes.c_char * len(data)
        wr_data = _wr_data()
        wr_data.value = data
        written = wintypesspec.SIZE_T()
        if not m_k32.WriteProcessMemory(
            self.handle,
            address,
            ctypes.byref(wr_data),
            ctypes.sizeof(wr_data),
            ctypes.byref(written),
        ):
            raise WindowsProcessError(
                "Error: WriteProcessMemory", get_last_error=m_k32.GetLastError()
            )
        return

    def allocate(self, size=0x400, address=None, permissions=None):
        alloc_type = flags("MEM_COMMIT")
        permissions = flags(permissions or "PAGE_EXECUTE_READWRITE")
        result = m_k32.VirtualAllocEx(
            self.handle, address, size, alloc_type, permissions
        )
        return result

    def free(self, address):
        free_type = flags("MEM_RELEASE")
        if m_k32.VirtualFreeEx(self.handle, address, 0, free_type) == 0:
            raise WindowsProcessError(
                "Error: VirtualFreeEx", get_last_error=m_k32.GetLastError()
            )
        return

    def protect(self, address, permissions=None, size=0x400):
        permissions = flags(permissions or "PAGE_EXECUTE_READWRITE")
        old_permissions = wintypesspec.DWORD()
        if (
            m_k32.VirtualProtectEx(
                self.handle, address, size, permissions, ctypes.byref(old_permissions)
            )
            == 0
        ):
            raise WindowsProcessError(
                "Error: VirtualProtectEx", get_last_error=m_k32.GetLastError()
            )
        return

    def start_thread(self, address, targ=None):
        handle = m_k32.CreateRemoteThread(self.handle, None, 0, address, targ, 0, None)
        if handle == 0:
            raise WindowsProcessError(
                "Error: CreateRemoteThread", get_last_error=m_k32.GetLastError()
            )
        return handle

    def join_thread(self, thread_id):
        m_k32.WaitForSingleObject(thread_id, -1)
        return

    def _execute_child(
        self,
        args,
        executable,
        preexec_fn,
        close_fds,
        pass_fds,
        cwd,
        env,
        startupinfo,
        creationflags,
        shell,
        p2cread,
        p2cwrite,
        c2pread,
        c2pwrite,
        errread,
        errwrite,
        unused_restore_signals,
        unused_gid,
        unused_gids,
        unused_uid,
        unused_umask,
        unused_start_new_session,
        unused_process_group,

    ):
        """Execute program (MS Windows version)"""
        assert not pass_fds, "pass_fds not supported on Windows."
        commandline = args if isinstance(args, str) else subprocess.list2cmdline(args)
        self._common_execute_child(
            executable,
            commandline,
            shell,
            close_fds,
            creationflags,
            env,
            cwd,
            startupinfo,
            p2cread,
            c2pwrite,
            errwrite,
        )

    def _common_execute_child(
        self,
        executable,
        commandline,
        shell,
        close_fds,
        creationflags,
        env,
        cwd,
        startupinfo,
        p2cread,
        c2pwrite,
        errwrite,
        to_close=(),
    ):
        ci = self._creationinfo
        if executable is not None:
            ci.lpApplicationName = executable
        if commandline:
            ci.lpCommandLine = commandline
        if shell:
            ci.bUseShell = shell
        if not close_fds:
            ci.bInheritHandles = int(not close_fds)
        if creationflags:
            ci.dwCreationFlags |= creationflags
        if env is not None:
            ci.lpEnvironment = env
        if cwd is not None:
            ci.lpCurrentDirectory = cwd

        if startupinfo is None:
            startupinfo = STARTUPINFO()
        si = self._startupinfo = startupinfo

        default = None if sys.version_info[0] == 2 else -1
        if default not in (p2cread, c2pwrite, errwrite):
            si.dwFlags |= STARTF_USESTDHANDLES
            si.hStdInput = int(p2cread)
            si.hStdOutput = int(c2pwrite)
            si.hStdError = int(errwrite)

        try:
            pi = create_process(creationinfo=ci, startupinfo=si)
        finally:
            if sys.version_info[0] == 2:
                if p2cread is not None:
                    p2cread.Close()
                    to_close.remove(p2cread)
                if c2pwrite is not None:
                    c2pwrite.Close()
                    to_close.remove(c2pwrite)
                if errwrite is not None:
                    errwrite.Close()
                    to_close.remove(errwrite)
            else:
                if p2cread != -1:
                    p2cread.Close()
                if c2pwrite != -1:
                    c2pwrite.Close()
                if errwrite != -1:
                    errwrite.Close()
                if hasattr(self, "_devnull"):
                    os.close(self._devnull)

        if not ci.dwCreationFlags & CREATE_SUSPENDED:
            self._child_started = True

        # Retain the process handle, but close the thread handle
        # if it's no longer needed.
        self._processinfo = pi
        self._handle = pi.hProcess.Detach()
        self.pid = pi.dwProcessId
        if self._child_started:
            pi.hThread.Close()

    def start(self):
        if self._child_started and self.pid:
            raise RuntimeError("processes can only be started once")
        hThread = self._processinfo.hThread
        prev_count = kernel32.ResumeThread(hThread)
        if prev_count > 1:
            for i in range(1, prev_count):
                if kernel32.ResumeThread(hThread) <= 1:
                    break
            else:
                raise RuntimeError("cannot start the main thread")
        # The thread's previous suspend count was 0 or 1,
        # so it should be running now.
        self._child_started = True
        hThread.Close()

    def __del__(self):
        if not self._child_started:
            try:
                if hasattr(self, "_processinfo"):
                    self._processinfo.hThread.Close()
            finally:
                if hasattr(self, "_handle"):
                    self.terminate()
        super(Popen, self).__del__()

    def get_last_stdout(self, clean=True):
        lastresult = list(self.out_dict.values())
        if clean:
            self.out_dict.clear()
        return lastresult

    def get_last_stderr(self, clean=True):
        lastresult = list(self.err_dict.values())
        if clean:
            self.err_dict.clear()
        return lastresult


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

def create_new_user(new_username=None, new_password="TOPSECRET", admin=False):
    """
    Disables the internet and runs the specified executable with the given arguments.

    :param exepath: The path to the executable to run.
    :type exepath: str
    :param args: The arguments to pass to the executable (default: ()).
    :type args: tuple
    :return: A tuple containing the new username, new password, new display name 1, new display name 2, and the process ID of the executed process.
    :rtype: tuple[str, str, str, str, int]
    """

    timestampnow = str(int(time.time())).split(".")[0]
    if new_username is None:
        new_username = f"USER_{timestampnow}"
    savebafi = get_tmpfile(".ps1")
    scri = rf"""$myuserpassword="{new_password}"
$myusername="{new_username}"
$myuserpassword  = ConvertTo-SecureString $myuserpassword -AsPlainText -Force

New-LocalUser -Name $myusername -Password $myuserpassword 
$credential = New-Object System.Management.Automation.PSCredential($myusername,  $myuserpassword )


    """
    if admin:
        scri = (
            scri
            + f"""\n$CompStat = Get-WmiObject win32_computersystem;
$Localhst = $CompStat.Name;
$Computer = [ADSI]('WinNT://'+$localhst+',computer');
$accName = [ADSI]('WinNT://'+$Localhst+'/"{new_username}",user');
$group = [ADSI]('WinNT://'+$Localhst+'/Administrators,group');
$group.add($accName.path);
"""
        )

    with open(savebafi, "w", encoding="utf-8") as f:
        f.write(scri)

    interactivepwsh = PowerShellDetachedInteractive(
        executable=r"cmd.exe",
        logfolder=os.environ.get("TMP") or os.environ.get("TEMP"),
        working_dir=workingdirshort,
        execution_policy="Unrestricted",
        arguments=["echo"],
        WhatIf="",
        Verb="",
        UseNewEnvironment="",
        Wait="",
        stdinadd="",
        WindowStyle="Hidden",
    )
    time.sleep(1)
    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {savebafi}")
    try:
        time.sleep(1)
        interactivepwsh.sendcommand("exit")
        interactivepwsh.close()
    except Exception:
        pass
    return (
        new_username,
        new_password,
    )


def remove_user(username):
    savebafi = get_tmpfile(".ps1")
    scri = f'''Remove-LocalUser "{username}"'''

    with open(savebafi, "w", encoding="utf-8") as f:
        f.write(scri)
    interactivepwsh = PowerShellDetachedInteractive(
        executable=r"cmd.exe",
        logfolder=os.environ.get("TMP") or os.environ.get("TEMP"),
        working_dir=workingdirshort,
        execution_policy="Unrestricted",
        arguments=["echo"],
        WhatIf="",
        Verb="",
        UseNewEnvironment="",
        Wait="",
        stdinadd="",
        WindowStyle="Hidden",
    )

    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {savebafi}")
    try:
        interactivepwsh.sendcommand("exit")
        interactivepwsh.close()
    except Exception:
        pass


def remove_firewall_rules(rules):
    savebafi = get_tmpfile(".ps1")
    allrules=[]
    for rule in rules:
        allrules.append(f'''Remove-NetFirewallRule -DisplayName "{rule}"''')

    with open(savebafi, "w", encoding="utf-8") as f:
        f.write("\n".join(allrules))
    interactivepwsh = PowerShellDetachedInteractive(
        executable=r"cmd.exe",
        logfolder=os.environ.get("TMP") or os.environ.get("TEMP"),
        working_dir=workingdirshort,
        execution_policy="Unrestricted",
        arguments=["echo"],
        WhatIf="",
        Verb="",
        UseNewEnvironment="",
        Wait="",
        stdinadd="",
        WindowStyle="Hidden",
    )
    time.sleep(1)
    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {savebafi}")
    try:
        time.sleep(1)
        interactivepwsh.sendcommand("exit")
        interactivepwsh.close()
    except Exception:
        pass


def disable_internet_for_user(
    username, password, apps, new_display_name1=None, new_display_name2=None
):
    timestampnow = str(int(time.time())).split(".")[0]
    if new_display_name1 is None:
        new_display_name1 = f"IO_{timestampnow}"
    if new_display_name2 is None:
        new_display_name2 = f"II_{timestampnow}"
    blockedapps = ""
    createdrules = []
    for ini, app in enumerate(apps):
        appshort = get_short_path_name(app)
        blockedapp = f'''New-NetFirewallRule -DisplayName "{new_display_name1}{ini}" -LocalUser (Get-FirewallLocalUserSddl '{username}') -Direction Outbound -Action Block -Program "{appshort}"
New-NetFirewallRule -DisplayName "{new_display_name2}{ini}" -LocalUser (Get-FirewallLocalUserSddl '{username}') -Direction Inbound -Action Block -Program "{appshort}"'''
        blockedapps = blockedapps + "\n" + blockedapp
        createdrules.extend(
            [f"""{new_display_name1}{ini}""", f"""{new_display_name2}{ini}"""]
        )

    scri = rf"""$myuserpassword="{password}"
$myusername="{username}"
$myuserpassword  = ConvertTo-SecureString $myuserpassword -AsPlainText -Force

$credential = New-Object System.Management.Automation.PSCredential($myusername,  $myuserpassword )


function Get-FirewallLocalUserSddl {{
    param(
        [string[]]$UserName
    )

    $SDDL = 'D:{{0}}'

    $ACEs = foreach ($Name in $UserName) {{
        try {{
            $LocalUser = Get-LocalUser -Name $UserName -ErrorAction Stop
            '(A;;CC;;;{{0}})' -f $LocalUser.Sid.Value
        }}
        catch {{
            Write-Warning "Local user '$Username' not found"
            continue
        }}
    }}
    return $SDDL -f ($ACEs -join '')
}}

{blockedapps}

# Block NICS
# New-NetFirewallRule -Name "BlockIn"  -LocalUser (Get-FirewallLocalUserSddl '{username}') -Direction Inbound -InterfaceAlias "Ethernet 54" -Action Block
# New-NetFirewallRule -Name "BlockOut" -LocalUser (Get-FirewallLocalUserSddl '{username}') -Direction Outbound -InterfaceAlias "Ethernet 54" -Action Block


    """
    savebafi = get_tmpfile(".ps1")

    with open(savebafi, "w", encoding="utf-8") as f:
        f.write(scri)

    interactivepwsh = PowerShellDetachedInteractive(
        executable=r"cmd.exe",
        logfolder=os.environ.get("TMP") or os.environ.get("TEMP"),
        working_dir=workingdirshort,
        execution_policy="Unrestricted",
        arguments=["echo"],
        WhatIf="",
        Verb="",
        UseNewEnvironment="",
        Wait="",
        stdinadd="",
        WindowStyle="Hidden",
    )

    time.sleep(1)
    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {savebafi}")
    try:
        time.sleep(1)
        interactivepwsh.sendcommand("exit")
        interactivepwsh.close()
    except Exception:
        pass
    return createdrules

