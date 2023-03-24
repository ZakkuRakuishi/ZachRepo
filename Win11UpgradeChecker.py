import platform
import os
import wmi

def get_system_info():
    c = wmi.WMI()
    os_info = c.Win32_OperatingSystem()[0]
    proc_info = c.Win32_Processor()[0]
    sys_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
    disk_info = c.Win32_LogicalDisk()[0]
    
    try:
        tpm_info = c.Win32_Tpm()[0] if c.Win32_Tpm() else None
        tpm_version = float(tpm_info.SpecVersion) if tpm_info else None
    except AttributeError:
        tpm_version = None

    return {
        "os_name": os_info.Caption,
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "processor": proc_info.Name,
        "ram": sys_ram,
        "storage": float(disk_info.Size) / (1024**3),  # B to GB
        "tpm_version": tpm_version,
    }

def check_windows_11_compatibility(system_info):
    if "Windows" not in system_info["os_name"]:
        return False

    if int(system_info["os_version"]) < 10:
        return False

    if system_info["architecture"] not in ("AMD64", "ARM64"):
        return False

    if system_info["ram"] < 4:
        return False

    if system_info["storage"] < 64:
        return False

    if system_info["tpm_version"] is None or system_info["tpm_version"] < 2.0:
        return False

    return True

def main():
    system_info = get_system_info()
    compatible = check_windows_11_compatibility(system_info)

    if compatible:
        print("Congratulations! Your computer is compatible with Windows 11 and can be upgraded.")
    else:
        print("Unfortunately, your computer does not meet the minimum requirements to upgrade to Windows 11.")

if __name__ == "__main__":
    main()
