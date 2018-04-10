import cx_Freeze

executables = [cx_Freeze.Executable("2048.py")]

cx_Freeze.setup(
    name="2048",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables

    )