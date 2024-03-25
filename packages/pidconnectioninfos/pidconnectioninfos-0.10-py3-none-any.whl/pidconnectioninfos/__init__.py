import subprocess
import re
from flatten_any_dict_iterable_or_whatsoever import fla_tu
import ctypes
from ctypes import wintypes
import os


procmatch1regex = re.compile(rb"^[\s-]*$")
procmatch2regex = re.compile(rb"^\s*$")

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
ntdll = windll.ntdll
kernel32 = windll.kernel32
_GetShortPathNameW = kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD
GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
CloseHandle = windll.kernel32.CloseHandle
GetExitCodeProcess.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_ulong),
]
CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
GetExitCodeProcess.restype = ctypes.c_int
CloseHandle.restype = ctypes.c_int
NTSTATUS = wintypes.LONG

INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
FILE_READ_ATTRIBUTES = 0x80
FILE_SHARE_READ = 1
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

FILE_INFORMATION_CLASS = wintypes.ULONG
FileProcessIdsUsingFileInformation = 47

LPSECURITY_ATTRIBUTES = wintypes.LPVOID
ULONG_PTR = wintypes.WPARAM


kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.CreateFileW.argtypes = (
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    LPSECURITY_ATTRIBUTES,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
)


class IO_STATUS_BLOCK(ctypes.Structure):
    class _STATUS(ctypes.Union):
        _fields_ = (("Status", NTSTATUS), ("Pointer", wintypes.LPVOID))

    _anonymous_ = ("_Status",)
    _fields_ = (("_Status", _STATUS), ("Information", ULONG_PTR))


iosb = IO_STATUS_BLOCK()


class FILE_PROCESS_IDS_USING_FILE_INFORMATION(ctypes.Structure):
    _fields_ = (
        ("NumberOfProcessIdsInList", wintypes.LARGE_INTEGER),
        ("ProcessIdList", wintypes.LARGE_INTEGER * 64),
    )


info = FILE_PROCESS_IDS_USING_FILE_INFORMATION()

PIO_STATUS_BLOCK = ctypes.POINTER(IO_STATUS_BLOCK)
ntdll.NtQueryInformationFile.restype = NTSTATUS
ntdll.NtQueryInformationFile.argtypes = (
    wintypes.HANDLE,
    PIO_STATUS_BLOCK,
    wintypes.LPVOID,
    wintypes.ULONG,
    FILE_INFORMATION_CLASS,
)


def get_short_path_name(long_name):
    try:
        if os.path.exists(long_name):
            output_buf_size = 4096
            output_buf = ctypes.create_unicode_buffer(output_buf_size)
            _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
            return output_buf.value
    except Exception:
        pass
    return long_name


def get_procs_with_open_file_pids_only(path):
    """
    Get the list of process IDs that have an open file at the specified path.

    Args:
        path (str): The path of the file.

    Returns:
        list: A list of process IDs that have the file open.
    """
    if not os.path.exists(path):
        return []
    shortpath = get_short_path_name(path)
    hFile = kernel32.CreateFileW(
        shortpath,
        FILE_READ_ATTRIBUTES,
        FILE_SHARE_READ,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        None,
    )
    if hFile == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())

    status = ntdll.NtQueryInformationFile(
        hFile,
        ctypes.byref(iosb),
        ctypes.byref(info),
        ctypes.sizeof(info),
        FileProcessIdsUsingFileInformation,
    )
    pidList = info.ProcessIdList[0 : info.NumberOfProcessIdsInList]
    CloseHandle(hFile)
    return pidList


def get_children_pids(pid: int):
    """
    A function to retrieve the process IDs of children processes based on the parent process ID.
    Parameters:
        pid (int): The parent process ID for which children process IDs will be retrieved.
    Returns:
        tuple: A tuple containing two lists, the first list with stdout lines and the second list with stderr lines.
    """
    pr = subprocess.run(
        f"""wmic process where (ParentProcessId={pid}) get Caption,ProcessId,CommandLine""",
        shell=False,
        capture_output=True,
        **invisibledict,
    )
    return pr.stdout.splitlines(), pr.stderr.splitlines()


def get_processes_and_pids():
    """
    Retrieves a list of processes and their corresponding process IDs (PIDs) using the `wmic` command.

    Returns:
        A tuple containing the stdout and stderr output of the `wmic` command.
    """
    pr = subprocess.run(
        """wmic process get Caption,ProcessId,CommandLine""",
        shell=False,
        capture_output=True,
        **invisibledict,
    )
    return pr.stdout, pr.stderr


def get_all_pids_from_main_processes():
    """
    Get all process IDs from the main processes and return a list of integers.
    """
    pr = subprocess.run(
        "wmic process get ProcessId",
        shell=False,
        capture_output=True,
        **invisibledict,
    )
    resus = []
    allp = pr.stdout.strip().splitlines()
    for q in allp:
        try:
            resus.append(int(q.strip()))
        except Exception:
            pass
    return resus


def is_process_alive(pid: int):
    """
    A function that checks if a process with a given Process ID is alive.
    Parameters:
        - pid: int, the Process ID of the process to check.
    Returns:
        - tuple: (bool, tuple) where the boolean indicates if the process is alive, and the tuple contains information about the process.
    """
    pr = subprocess.run(
        f"wmic process where (ProcessId={pid}) get Caption,ProcessId,CommandLine",
        shell=False,
        capture_output=True,
        **invisibledict,
    )
    outs, errs = pr.stdout, pr.stderr
    resultall2 = []
    for po in outs.splitlines():
        try:
            if not procmatch1regex.match(po):
                po = po.decode("utf-8", "backslashreplace")
                l1, l2 = po.strip().split(maxsplit=1)
                l2, l3 = l2.strip().rsplit(maxsplit=1)
                allnums = (l1, l2, int(l3))
                resultall2.append(allnums)
        except Exception:
            continue
    try:
        return True, resultall2[0]
    except Exception:
        return False, (None, None, None)


def get_all_children_this_python_process():
    """
    Returns all the children processes of the current Python process.

    :return: A list of Process objects representing the children processes.
    :rtype: List[Process]
    """
    return get_processes_and_children(pids_to_search=[os.getpid()])


def get_all_children_parents_this_python_process():
    """
    Returns all the children and parents of the current Python process.

    :return: A dictionary containing the children and parents of the current Python process.
             The dictionary has the following structure:
             {
                 "children": [list of child process IDs],
                 "parents": [list of parent process IDs]
             }
    :rtype: dict
    """
    return get_processes_and_children(pids_to_search=[os.getppid()])


def get_processes_and_children(
    pids_to_search: list | tuple | int | None = None, always_ignore: tuple = (0, 4)
):
    """
    Get the processes and their children based on the provided process IDs to search and the processes to always ignore.
    If no IDs are provided, it will default to searching through a range of 65536 IDs.
    The function returns two dictionaries: `resultchildren` containing the children of each process as a "family tree", and `resultchildren_flat` containing a flattened version of the children relationship.
    """
    if not pids_to_search:
        interesspids = list(range(65536))
    else:
        if isinstance(pids_to_search, (list, tuple)):
            interesspids = [int(q) for q in pids_to_search]
        else:
            interesspids = [int(pids_to_search)]
    interesspids = sorted(set(interesspids) - set(always_ignore))
    outs, errs = get_processes_and_pids()
    resultall2 = []
    for po in outs.splitlines():
        try:
            if not procmatch1regex.match(po):
                po = po.decode("utf-8", "backslashreplace")
                l1, l2 = po.strip().split(maxsplit=1)
                l2, l3 = l2.strip().rsplit(maxsplit=1)
                allnums = (l1, l2, int(l3))
                resultall2.append(allnums)
        except Exception:
            continue

    resultall = []
    for po in resultall2:
        if po[2] in interesspids:
            resultall.append(po)

    resultchildren = {}

    def get_all_kids(resultc, pname, ppath, p_id, resultc_before=None):
        didi = resultc.setdefault((pname, ppath, p_id), {})
        so, se = get_children_pids(p_id)
        so = [
            po.decode("utf-8", "backslashreplace")
            for po in so
            if not procmatch2regex.match(po)
        ]
        if not so:
            resultc[(pname, ppath, p_id)] = -1
        resultscounter = 0
        for po in so:
            try:
                l1, l2 = po.strip().split(maxsplit=1)
                l2, l3 = l2.strip().rsplit(maxsplit=1)
                try:
                    l3 = int(l3)
                except Exception:
                    continue
                if (pname, ppath, p_id) == (l1, l2, int(l3)):
                    continue

                resultscounter += 1
                get_all_kids(
                    didi,
                    l1,
                    l2,
                    int(l3),
                    resultc_before,
                )
            except Exception:
                continue
        if resultscounter == 0:
            resultc[(pname, ppath, p_id)] = -1

    for pname, ppath, p_id in resultall:
        try:
            get_all_kids(resultchildren, pname, ppath, p_id)
        except Exception:
            continue

    resultchildren_flat = {}
    for parent, child in resultchildren.items():
        dupliset = set()
        for q in fla_tu(child):
            for qq in q[1:]:
                cou = 0

                for qqq in qq:
                    # resultchildren_flat.setdefault(qq,set()).add(parent)
                    newture = resultchildren_flat.setdefault(parent, [])
                    if qqq not in dupliset:
                        dupliset.add(qqq)
                        newture.append((cou,) + qqq)
                        cou += 1

    return resultchildren, resultchildren_flat


def is_subprocess_alive(cmp: subprocess.Popen):
    """
    Check if a subprocess is still alive.

    Parameters:
        cmp (subprocess.Popen): The subprocess to check.

    Returns:
        bool: True if the subprocess is still alive, False otherwise.
    """
    resupid = is_process_alive(cmp.pid)
    strargs = ""
    listargs = []
    if resupid[0]:
        if isinstance(cmp.args, (list)):
            strargs = " ".join(cmp.args)
            listargs = cmp.args
        else:
            strargs = cmp.args
            listargs = cmp.args.split()
    else:
        return False
    foundproc = False
    if strargs:
        if strargs.strip() in resupid[1][1]:
            foundproc = True
        elif resupid[1][1] in strargs.strip():
            foundproc = True
        elif (
            re.sub(r"\s+", " ", strargs).strip().lower()
            in re.sub(r"\s+", " ", str(resupid[1][1])).strip().lower()
        ):
            foundproc = True
        elif (
            re.sub(r"\s+", " ", str(resupid[1][1])).strip().lower()
            in re.sub(r"\s+", " ", str(strargs)).strip().lower()
        ):
            foundproc = True
        elif listargs[0].lower() in [str(b).lower() for b in resupid[1][:2]]:
            foundproc = True
        elif listargs[0].lower() in str(resupid[1][1]):
            foundproc = True
    if foundproc:
        return True
    return False


def get_information_from_all_procs_with_connections():
    """
    This function runs the 'netstat -bnoa' command using subprocess and captures the output. It then processes the output to extract information about processes with connections, including the PID, protocol, local address, foreign address, and state. The function returns a list of tuples containing this information.
    """
    pproc2 = subprocess.run(["netstat", "-bnoa"], capture_output=True, **invisibledict)
    trigger = False
    goodata = []
    for o in pproc2.stdout.splitlines():
        o = o.strip()
        if not o.endswith(b"PID") and not trigger:
            continue
        if o.endswith(b"PID"):
            trigger = True
            continue
        else:
            if re.findall(rb"\d+$", o):
                ospli = o.decode("utf-8", "backslashreplace").split()
                if len(ospli) >= 4:
                    try:
                        ospli[-1] = int(ospli[-1])
                    except Exception:
                        continue
                    goodata.append(tuple(ospli))
    return goodata


def get_all_imagenames_and_pid():
    """
    Get all image names and their corresponding process IDs.
    """
    pr = subprocess.run(
        "wmic process get Caption,ProcessId",
        shell=False,
        capture_output=True,
        **invisibledict,
    )
    out, errs = (
        pr.stdout.strip().decode("utf-8", "backslashreplace").splitlines(),
        pr.stderr.strip().decode("utf-8", "backslashreplace").splitlines(),
    )
    out2 = [g.rsplit(maxsplit=1) for x in out if (g := x.strip())]
    out3 = []
    for x in out2:
        if len(x) == 2:
            try:
                out3.append([x[0].strip(), int(x[1])])
            except Exception:
                pass

    return out3


def get_all_pids_from_image(imagefile: str = "chrome.exe"):
    """
    Get all process IDs associated with a specific image file.

    :param imagefile: The name of the image file to search for process IDs (default is "chrome.exe")
    :type imagefile: str
    :return: A list of process IDs associated with the specified image file
    :rtype: list
    """
    allexeandpid = get_all_imagenames_and_pid()

    imagefilelower = imagefile.lower()
    return [x[1] for x in allexeandpid if x[0].lower() == imagefilelower]


def get_processes_and_children_and_netstat(
    pids_to_search: list | tuple | int | None = None, always_ignore: tuple = (0, 4)
):
    """
    Retrieves a tree of processes, their children, and netstat connection information.

    Args:
        pids_to_search (Optional[List[int]]): A list of process IDs to search for. Defaults to None.
        always_ignore (Tuple[int]): A tuple of process IDs to always ignore. Defaults to (0, 4).

    Returns:
        Tuple[Dict[int, Dict[str, Any]], List[Dict[str, Any]], Dict[int, List[List[str]]], Dict[int, List[List[str]]]]:
            - A tree of processes and their children, represented as a dictionary.
            - A flat list of processes and their children, represented as a list of dictionaries.
            - A dictionary of established connections, with the process ID as the key and a list of connection information as the value.
            - A dictionary of all connection data, with the process ID as the key and a list of connection information as the value.
    """
    children_tree, children_flat = get_processes_and_children(
        pids_to_search=pids_to_search, always_ignore=always_ignore
    )
    connectiondataall = get_information_from_all_procs_with_connections()
    connectiondataalldict = {}
    for con in connectiondataall:
        connectiondataalldict.setdefault(con[-1], []).append(con)
    establishedconnections = {}

    for item, keys in fla_tu(children_tree):
        for k in keys:
            try:
                establishedconnections.setdefault(k, set()).update(
                    connectiondataalldict.get(k[-1]), {}
                )
            except Exception:
                pass
    allconnectionresultsfiltered = {
        k: sorted(v, key=lambda x: x[-1])
        for k, v in establishedconnections.items()
        if v
    }
    return (
        children_tree,
        children_flat,
        allconnectionresultsfiltered,
        connectiondataalldict,
    )


def get_network_connections_from_process(ports, always_ignore=(0, 4)):
    """
    Retrieves network connections associated with the specified ports from the process.

    Args:
        ports (list): A list of ports to retrieve network connections for.
        always_ignore (tuple, optional): A tuple of process IDs to ignore. Defaults to (0, 4).

    Returns:
        dict: A dictionary containing network connections grouped by process ID.
    """
    px = subprocess.run("netstat -ano", capture_output=True, **invisibledict)
    allps = [("(:" + str(x) + "\\b\\s+)").encode() for x in ports]
    allipsstr = b"(" + b"|".join(allps) + b")"
    reports = re.compile(allipsstr, flags=re.I)
    dad1 = [
        [
            q,
            list(
                [
                    r[0].strip(b": ")
                    for r in fla_tu(
                        [[z[0] for z in fla_tu(y)] for y in reports.findall(q)]
                    )
                ]
            ),
        ]
        for q in px.stdout.strip().splitlines()
    ]
    allpidsforcon = set()

    def toint(x):
        try:
            return int(x)
        except Exception:
            return None

    dad2 = []
    lookupdict = {}
    lookupdict2 = {}
    for ax in dad1:
        ax[-1] = sorted(set([u for u in ax[-1] if u and re.match(rb"^\d+$", u)]))
        ax[-1] = [toint(x) for x in ax[-1]]
        ax[-1] = [x for x in ax[-1] if x is not None]
        if ax[-1]:
            intpid = int(ax[0].strip().rsplit(maxsplit=1)[-1])
            if intpid in always_ignore:
                continue
            dad2.append([ax[0].decode("utf-8", "backslashreplace"), intpid, ax[-1]])
            allpidsforcon.add(dad2[-1][-2])
            lookupdict.setdefault(intpid, set()).update(dad2[-1][-1])
            for po in dad2[-1][-1]:
                lookupdict2.setdefault(po, set()).add(intpid)

    connectiondict = {}
    for keyp, prodi in (lookupdict).items():
        a1, b1 = get_processes_and_children(keyp)
        connectiondict[keyp] = {
            "family_tree": a1,
            "flat_tree": b1,
            "found_ports": prodi,
        }

    return connectiondict
