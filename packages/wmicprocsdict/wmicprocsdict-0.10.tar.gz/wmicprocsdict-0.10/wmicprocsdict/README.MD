# Converts the output of a powershell (Get-...)/wmic command to a dict

## pip install wmicprocsdict

### Tested against Windows 10 / Python 3.11 / Anaconda

```py
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

```