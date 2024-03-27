from psutil._common import shwtemp


class UsageMock:
    ru_utime = 1
    ru_stime = 1


class CpuFreqMock:
    current = 1234


class SwapMemoryMock:
    percent = 123


class PsutilMock:
    def getloadavg(self):
        return (1, 2, 3)

    def cpu_freq(self):
        return CpuFreqMock

    def cpu_percent(self, interval=None):
        return 12

    def swap_memory(self):
        return SwapMemoryMock

    def sensors_temperatures(self):
        return {
            'coretemp': [
                shwtemp(label='Package id 0', current=53.0, high=100.0, critical=100.0),
                shwtemp(label='Core 0', current=50.0, high=100.0, critical=100.0),
                shwtemp(label='Core 4', current=51.0, high=100.0, critical=100.0),
            ],
            'nvme': [
                shwtemp(label='Composite', current=32.85, high=81.85, critical=84.85),
            ],
        }
