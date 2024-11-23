import os
import subprocess
import sys
import time

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

version_goc = ""
runBuildAll = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("=" * 66)
    print("            Building project 'ToolDriverPrinter' wizard")
    print("=" * 66)
    print("\n                [1] Build ToolDriverPrinter")
    print("\n")
    print("\n                [2] Build Fix_not_run_program")
    print("\n")
    print("\n                [3] Build All")
    print("\n")
    print("\n                [4] Install/Update request library")
    print("\n")
    print("\n                [X] Exit")
    print("\n")
    print("\n" + "=" * 66 + "\n")
    choice = input("Your choice: ").strip().upper()
    return choice

def build_tool_driver_printer(version, runBuildAll=False):
    if not runBuildAll:
        print("=" * 66)
        print("                     Build ToolDriverPrinter")
        print("=" * 66)

    if not version:
        version = input("\nEnter the program version (format n.n.n.n): ").strip()
    
    print(f"Using Version: {version}")
    print("\n>> Starting building ToolDriverPrinter...\n")
    
    cmd = (
        "nuitka "
        "ToolDriverPrinter.py "
        "--include-data-files=C:\\Users\\duyph\\Desktop\\EHD\\Certificate\\CARoot\\CA-Root.crt=CA-Root.crt "
        "--windows-uac-admin "
        "--windows-icon-from-ico=Icon\\IconProgram.ico "
        "--onefile "
        "--standalone "
        "--lto=yes "
        "--clang "
        "--follow-imports "
        "--windows-console-mode=disable "
        "--remove-output "
        "--noinclude-default-mode=error "
        "--company-name=TranPhuong319 "
        '--product-name="Easy Printer Driver Install/Uninstall Tool" '
        f"--file-version={version} "
        f"--product-version={version} "
        '--copyright="Copyright (C) 2023-2024 TranPhuong319. All rights reserved"'
    )
    
    # Dùng cmd để thực thi lệnh
    subprocess.run(
        f"cmd /c {cmd}",
    )
    
    input("\nPress Enter to return...")


def build_tools(version):
    if runBuildAll == False:
        print("=" * 66)
        print("                            Build Tools")
        print("=" * 66)
        print("\n")
    if not version:
        version = input("Enter the program version (format n.n.n.n): ").strip()
    else:
        pass
    print("\n")
    print(f"Using Version: {version}")
    print("\n>> Starting building Tools...\n")
    
    cmd = [
        "nuitka", 
        '"Tools_py\\Fix_not_run_program.py"',
        "--include-data-files=C:\\Users\\duyph\\Desktop\\EHD\\Certificate\\CARoot\\CA-Root.crt=CA-Root.crt",
        "--windows-uac-admin",
        "--onefile",
        "--standalone",
        "--lto=yes",
        "--clang",
        "--follow-imports",
        "--windows-console-mode=disable",
        "--remove-output",
        "--noinclude-default-mode=error",
        "--company-name=TranPhuong319",
        '--product-name="Fix not run Program"',
        f"--file-version={version}",
        f"--product-version={version}",
        '--copyright="Copyright (C) 2023-2024 TranPhuong319. All rights reserved"'
    ]
    cmd = " ".join(cmd)
    
    subprocess.run(f"cmd /c {cmd}")
    
    input("\nPress Enter to return...")

def build_all():
    clear_screen()
    print("=" * 66)
    print("                        Build All Components")
    print("=" * 66)
    print("\n")
    global runBuildAll
    runBuildAll = True

    # Yêu cầu nhập phiên bản cho ToolDriverPrinter
    version_tdp = input("Enter the program version for ToolDriverPrinter (format n.n.n.n): ").strip()
    print("\n")

    # Nếu người dùng không nhập phiên bản cho Tools, dùng phiên bản của ToolDriverPrinter
    version_tools = input("Enter the program version for Tools (format n.n.n.n): ").strip()
    
    # Nếu không nhập phiên bản cho Tools, sử dụng phiên bản của ToolDriverPrinter
    if not version_tools:
        version_tools = version_tdp  # Sử dụng phiên bản của ToolDriverPrinter cho Tools

    # Gọi hàm Build ToolDriverPrinter và Build Tools với các phiên bản đã nhập
    build_tool_driver_printer(version_tdp)  # Gọi hàm Build ToolDriverPrinter
    
    print("\n>> Starting building Tools with version", version_tools, "...\n")
    build_tools(version_tools)  # Gọi hàm Build Tools
    
    print("\nCompleted! Press Enter to return to the main menu.")
    runBuildAll = False
    input()

def install_update_library():
    clear_screen()
    print("=" * 66)
    print("                       Install/Update Library")
    print("=" * 66)
    print("\n>> Installing/Updating necessary libraries...\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", 
                    "wxpython", "psutil", "nuitka", "win10toast", "plyer", "pillow"])
    print("\nCompleted! Press Enter to return to the main menu.")
    input()

def exit_program():
    clear_screen()
    print("=" * 66)
    print("                            Exit Program")
    print("=" * 66)
    print("\n>> Thanks for using the program.")
    print("\n" + "=" * 66 + "\n")
    input("Press Enter to exit...")
    sys.exit()

if __name__ == "__main__":
    
    while True:
        choice = main_menu()
        if choice == "1":
            if runBuildAll == False:
                clear_screen()
                build_tool_driver_printer(version_goc)
        elif choice == "2":
            if runBuildAll == False:
                clear_screen()
                build_tools(version_goc)
        elif choice == "3":
            build_all()
        elif choice == "4":
            install_update_library()
        elif choice == "X":
            exit_program()
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)
