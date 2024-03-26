import subprocess
import re
from ast import literal_eval
import sys

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def _convert_table_to_dict(commandoutput: list, strings_to_number: str = True) -> dict:
    """
    Converts a table represented as a list of strings into a dictionary.

    Args:
        commandoutput (list): The list of strings representing the table.
        strings_to_number (bool, optional): Whether to convert string values to numbers. Defaults to True.

    Returns:
        dict: A dictionary representing the table, where the keys are row indices and the values are dictionaries
              representing the columns and their corresponding values.
    """
    _split_lines = commandoutput.copy()
    _split_lines = [x for x in _split_lines if x.strip()]
    _split_lines = [x for x in _split_lines if not re.match(r"^[\s_-]+$", x)]
    maxlenline = len(max(_split_lines, key=len))
    split_lines = [x.ljust(maxlenline + 1) for x in _split_lines]
    firstline = split_lines[0] + (((maxlenline + 5) * " ") + "XXXX___XXXXX")
    allspans = []
    for l in re.finditer(r"\s{1,}(?=[^\s])", firstline):
        allspans.append(list(l.span()))
    allspans[0][0] = 0
    allspans.append([maxlenline, maxlenline])
    header = []
    cutvalue_start = []
    cutvalue_end = []
    for ini in range(1, len(allspans) - 1):
        start = allspans[ini - 1][-1]
        end = allspans[ini][1]
        header.append(firstline[start:end].strip())
        cutvalue_start.append(start)
        cutvalue_end.append(end)

    resultdict = {}
    counter = 0
    for linennumber in range(1, len(split_lines) - 1):
        resultdict[counter] = {}
        for ini in range(len(cutvalue_start)):
            try:
                start = cutvalue_start[ini]
                end = cutvalue_end[ini]

                resultdict[counter][header[ini]] = split_lines[linennumber][
                    start:end
                ].strip()
                if strings_to_number:
                    try:
                        resultdict[counter][header[ini]] = literal_eval(
                            resultdict[counter][header[ini]]
                        )
                    except Exception:
                        pass
            except Exception as e:
                sys.stderr.write(str(e) + "\n")
                sys.stderr.flush()
        counter = counter + 1

    return resultdict


def execute_command(
    cmd: str, format_powershell: bool = False, cols: int = 9999999, lines: int = 1
) -> list:
    """
    A function that executes a command in the shell environment.

    Args:
        cmd (str): The command to be executed.
        format_powershell (bool): Format to: f'powershell "{cmd} | Format-Table *"'.
        cols (int): Number of columns for the console.
        lines (int): Number of lines for the console.

    Returns:
        list: A list of decoded strings representing the command output.
    """
    if format_powershell:
        cmd = f'powershell "{cmd} | Format-Table *"'
    p = subprocess.Popen(
        f"cmd.exe /w=mode con:cols={cols} lines={lines}",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        **invisibledict,
    )
    cmdbytes = cmd.encode()
    p.stdin.write(cmdbytes + b"\n")
    p.stdin.flush()
    stdo, stde = p.communicate()
    cmdlen = len(cmd)
    indexofcmd = stdo.find(cmdbytes)
    indextocut = indexofcmd + cmdlen
    stdo = stdo[indextocut:]
    assplitlines = stdo.splitlines()
    cutvalue_end = len(assplitlines)
    for q in range(len(assplitlines) - 1, 0, -1):
        if not assplitlines[q].strip():
            cutvalue_end = q
            break

    assplitlines = assplitlines[:cutvalue_end]
    return [x.decode("utf-8", "replace") for x in assplitlines if x.strip()]


def get_dict_from_command(
    cmd, convert_dtypes_with_ast=True, format_powershell=False, cols=9999999, lines=1
) -> dict:
    r"""
    Converts the output of a powershell (Get-...)/wmic command to a dict

    Args:
        cmd (str): The command to execute.
        convert_dtypes_with_ast (bool, optional): Whether to convert column data types to their appropriate types using the ast module. Defaults to True.
        format_powershell (bool, optional): Format to: f'powershell "{cmd} | Format-Table *"'. Defaults to False.
        cols (int): Number of columns for the console. Defaults to 9999999.
        lines (int): Number of lines for the console. Defaults to 1.

    Returns:
        dict: A dictionary representing the command output.

    Example:
        from wmicprocsdict import get_dict_from_command

        d1 = get_dict_from_command(
            cmd="Get-Process",
            convert_dtypes_with_ast=True,
            format_powershell=True,
            cols=9999999,
            lines=1,
        )
        d2 = get_dict_from_command(
            cmd=f'powershell "Get-Process | Format-Table *"',
            convert_dtypes_with_ast=True,
            format_powershell=False,
            cols=9999999,
            lines=1,
        )
        e1 = get_dict_from_command(
            cmd="wmic process",
            convert_dtypes_with_ast=True,
            format_powershell=False,
            cols=9999999,
            lines=1,
        )

        d3 = get_dict_from_command(
            cmd="Get-Service",
            convert_dtypes_with_ast=True,
            format_powershell=True,
            cols=9999999,
            lines=1,
        )

        d4 = get_dict_from_command(
            cmd=f'powershell "Get-Service | Format-Table *"',
            convert_dtypes_with_ast=True,
            format_powershell=False,
            cols=9999999,
            lines=1,
        )
        print(d1)
        print(d2)
        print(e1)
        print(d3)
        print(d4)

        # {0: {'Id': 56, 'PriorityClass': 'Normal', 'FileVersion': (6, 6, 0, 0), 'HandleCount': 430, 'WorkingSet': 32923648, 'PagedMemorySize': 38731776, 'PrivateMemorySize': 38731776, 'Virt...
        # {0: {'Id': 56, 'PriorityClass': 'Normal', 'FileVersion': (6, 6, 0, 0), 'HandleCount': 430, 'WorkingSet': 32923648, 'PagedMemorySize': 38731776, 'PrivateMemorySize': 38731776, 'Virt...
        # {0: {'CommandLine': '', 'CreationClassName': 'Win32_Process', 'CreationDate': '20240325180030.969217-180', 'CSCreationClassName': 'Win32_ComputerSystem', 'CSName': '...
        # {0: {'RequiredServices': {}, 'CanPauseAndContinue': False, 'CanShutdown': False, 'CanStop': False, 'DisplayName': 'Agent Activation Runtime_c5578', 'DependentServices': {}, 'Machin...
        # {0: {'RequiredServices': {}, 'CanPauseAndContinue': False, 'CanShutdown': False, 'CanStop': False, 'DisplayName': 'Agent Activation Runtime_c5578', 'DependentServices': {}, 'Machin...

    """
    assplitlines = execute_command(cmd=cmd, format_powershell=format_powershell)
    return _convert_table_to_dict(
        commandoutput=assplitlines, strings_to_number=convert_dtypes_with_ast
    )
