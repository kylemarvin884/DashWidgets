from cx_Freeze import setup, Executable

# 包含所需的包
build_exe_options = {
    "packages": ["requests", "psutil", "customtkinter"],
}

setup(
    name="ManeApp",
    version="0.1",
    description="桌面组件管理器",
    options={"build_exe": build_exe_options},
    executables=[Executable("mane.py", base="Win32GUI")],
)
