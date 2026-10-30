import os
import subprocess

path = os.path.abspath("database/csv_file/csv2026-10-14 102213.csv")

# 方式 A
subprocess.Popen(f'explorer /select,"{path}"')