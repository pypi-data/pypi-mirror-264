import subprocess
import os
import tempfile
import re
from rlogfi import (
    PowerShellDetachedInteractive,
    escapecmdlist,
    invisibledict,
    touch,
    get_short_path_name,
    errwrite,
)
import shutil
import time
import os

enablefirewallcmd = "netsh", "advfirewall", "set", "currentprofile", "state", "on"
disablefirewallcmd = "netsh", "advfirewall", "set", "currentprofile", "state", "off"


def get_tmpfile(suffix=".bat"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def check_firewall_status():
    p = subprocess.run(
        ["netsh", "advfirewall", "show", "currentprofile"],
        capture_output=True,
        **invisibledict,
    )

    stdo, stde = p.stdout.splitlines(), p.stderr.splitlines()
    stode = [
        h.strip().split(maxsplit=1)[-1].lower() for h in stdo if h.startswith(b"State")
    ]
    allok = [h for h in stode if h == b"on"]
    allnotok = [h for h in stode if h != b"on"]
    firewalloff = False
    if allnotok or not allok:
        firewalloff = True
    return firewalloff


def disable_internet_and_run(
    exepath: str, args: tuple = ()
) -> tuple[str, str, str, str, int]:
    """
    Disables the internet and runs the specified executable with the given arguments.

    :param exepath: The path to the executable to run.
    :type exepath: str
    :param args: The arguments to pass to the executable (default: ()).
    :type args: tuple
    :return: A tuple containing the new username, new password, new display name 1, new display name 2, and the process ID of the executed process.
    :rtype: tuple[str, str, str, str, int]
    """

    firewalloff = check_firewall_status()
    if firewalloff:
        subprocess.run(enablefirewallcmd, **invisibledict)

    timestampnow = str(int(time.time())).split(".")[0]
    new_username = f"NO_{timestampnow}"
    new_password = "NOINTERNET"
    new_display_name1 = f"IO_{timestampnow}"
    new_display_name2 = f"II_{timestampnow}"

    args = []
    savebafi = get_tmpfile(".ps1")
    piddata = get_tmpfile(".txt")
    pse = shutil.which("powershell.exe")
    workingdir = os.sep.join(re.split(r"[\\/]+", exepath)[:-1])
    exepathshort = get_short_path_name(exepath)
    workingdirshort = get_short_path_name(workingdir)
    observerscriptmp = get_tmpfile(suffix=".ps1")
    observerscriptmpshort = get_short_path_name(observerscriptmp)

    if args:
        argsstring = " -ArgumentList " + escapecmdlist(args) + " "
    else:
        argsstring = " "
    scri = rf"""$myuserpassword="{new_password}"
$myusername="{new_username}"
$myuserpassword  = ConvertTo-SecureString $myuserpassword -AsPlainText -Force

New-LocalUser -Name $myusername -Password $myuserpassword 
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

New-NetFirewallRule -DisplayName "{new_display_name1}" -LocalUser (Get-FirewallLocalUserSddl '{new_username}') -Direction Outbound -Action Block -Program "{exepathshort}"
New-NetFirewallRule -DisplayName "{new_display_name2}" -LocalUser (Get-FirewallLocalUserSddl '{new_username}') -Direction Inbound -Action Block -Program "{exepathshort}"


    """

    with open(savebafi, "w", encoding="utf-8") as f:
        f.write(scri)

    pse_short = get_short_path_name(pse)
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

    startproc = get_tmpfile(".ps1")
    os.remove(piddata)
    time.sleep(2)
    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {savebafi}")
    tmpfilestdout = get_tmpfile(".txt")
    tmpfilestderr = get_tmpfile(".txt")
    tmpfilestdout_short = get_short_path_name(tmpfilestdout)
    tmpfilestderr_short = get_short_path_name(tmpfilestderr)

    with open(startproc, "w", encoding="utf-8") as f:
        f.write(
            f"""$myuserpassword="{new_password}"
    $myusername="{new_username}"
    $myuserpassword  = ConvertTo-SecureString $myuserpassword -AsPlainText -Force

    New-LocalUser -Name $myusername -Password $myuserpassword 
    $credential = New-Object System.Management.Automation.PSCredential($myusername,  $myuserpassword )
    Start-Process -FilePath "{exepathshort}" -Credential $credential  -RedirectStandardOutput {tmpfilestdout_short} -RedirectStandardError {tmpfilestderr_short} -WorkingDirectory "{workingdirshort}"{argsstring}-PassThru -WindowStyle Normal | Format-List"""
        )
    stdout, stderr = interactivepwsh.sendcommand(f"{pse} {startproc} > {piddata}")

    while not os.path.exists(piddata):
        time.sleep(1)
    time.sleep(2)
    while True:
        try:
            os.rename(piddata, piddata)
            break
        except Exception:
            time.sleep(3)
    while True:
        try:
            with open(piddata, "r", encoding="utf-8") as f:
                pidda = f.read()
                break
        except Exception:
            time.sleep(3)
    processfound = False
    if re.findall(r"\bId\s+:", pidda):
        processfound = True
    pidofproc = 0
    if processfound:
        pidofproc = re.split(r"Id\s+:\s*", pidda)[-1].split()[0]
        checktime = 5
        adddisablefirewall = " ".join(disablefirewallcmd) if firewalloff else ""
        observerscript = rf"""$pidToMonitor = {pidofproc}  
    while ($true) {{
        $process = Get-Process -Id $pidToMonitor -ErrorAction SilentlyContinue

        if (-not $process) {{
            Remove-NetFirewallRule -DisplayName "{new_display_name1}"
            Remove-NetFirewallRule -DisplayName "{new_display_name2}"

            Remove-LocalUser "{new_username}"
            {adddisablefirewall}
            break  # Exit the loop once the script has been executed
        }}

        Start-Sleep -Seconds {checktime}
    }}

        """

        with open(observerscriptmp, "w", encoding="utf-8") as f:
            f.write(observerscript)

        interactivepwsh.sendcommand(
            f"{pse_short} -File {observerscriptmp} -WindowStyle Hidden"
        )
        time.sleep(5)

    interactivepwsh.stdout_stoptrigger[0] = True
    interactivepwsh.stderr_stoptrigger[0] = True
    time.sleep(5)
    interactivepwsh.thread_being_executed.killthread()
    time.sleep(5)
    try:
        interactivepwsh._proc.stdin.close()
    except Exception as ef:
        errwrite(ef)
    try:
        interactivepwsh._proc.stdout.close()
    except Exception as ef:
        errwrite(ef)

    try:
        interactivepwsh._proc.stderr.close()
    except Exception as ef:
        errwrite(ef)
    try:
        interactivepwsh._proc.wait(timeout=1)
    except Exception as ef:
        errwrite(ef)
    try:
        interactivepwsh._proc.terminate()
    except Exception as ef:
        errwrite(ef)
    return (
        new_username,
        new_password,
        new_display_name1,
        new_display_name2,
        int(pidofproc),
    )
