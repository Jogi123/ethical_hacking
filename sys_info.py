#!/bin/python

import platform
import psutil
import GPUtil


def convert_units(size):
    factor = 1024
    for i in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size > factor:
            size = size / factor
        else:
            return f'{size} {i}'


uname = platform.uname()
print('-' * 40, 'System', '-' * 40)
print(f'OS: {uname.system}')
print(f'PC Name: {uname.node}')
print(f'OS Release: {uname.release}')
print(f'OS Version: {uname.version}')
print(f'Architecture: {uname.machine}')

print('\n')
print('-' * 40, 'CPU', '-' * 40)
print(f'Physical Cores: {psutil.cpu_count(logical=False)}')
print(f'Logical Cores: {psutil.cpu_count(logical=True)}')
print(f'CPU Frequency Max: {psutil.cpu_freq().max} Mhz')
print(f'CPU Frequency Current: {psutil.cpu_freq().current} Mhz')
print(f'CPU usage: {psutil.cpu_percent()}%')
print(f'CPU Temperature: {psutil.sensors_temperatures()}')

print('\n')
print('-' * 40, 'RAM', '-' * 40)
mem = psutil.virtual_memory()
print(f'Total Memory: {convert_units(mem.total)}')
print(f'Used Memory: {convert_units(mem.used)}')
print(f'Available Memory: {convert_units(mem.available)}')

print('\n')
print('-' * 40, 'Partitions', '-' * 40)
partitions = psutil.disk_partitions()
for p in partitions:
    print(f'Device: {p.device}')
    print(f'\tMountpoint: {p.mountpoint}')
    print(f'\tFilesystemtype: {p.fstype}')
    try:
        usage = psutil.disk_usage(p.mountpoint)
    except PermissionError:
        continue
    print(f'\tTotal Size: {convert_units(usage.total)}')
    print(f'\tUsed: {convert_units(usage.used)}')
    print(f'\tFree: {convert_units(usage.free)}')
    print(f'\tPercentage: {usage.percent}')
    print('\n')

disk_io = psutil.disk_io_counters()
print(f'Read since boot: {convert_units(disk_io.read_bytes)}')
print(f'Written since boot: {convert_units(disk_io.write_bytes)}')

print('\n')
print('-' * 40, 'GPU', '-' * 40)
gpus = GPUtil.getGPUs()
for gpu in gpus:
    print(f'Name: {gpu.name}')
    print(f'Load: {gpu.load * 100}%')
    print(f'Total Memory: {convert_units(gpu.memoryTotal)}')
    print(f'Free Memory: {convert_units(gpu.memoryFree)}')
    print(f'Used Memory: {convert_units(gpu.memoryUsed)}')
    print(f'GPU Temperature: {gpu.temperature}°C')
