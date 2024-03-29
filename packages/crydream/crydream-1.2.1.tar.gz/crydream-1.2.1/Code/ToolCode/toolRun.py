import platform


class python_tool:

    def __init__(self):
        pass

    def system_platform(self):
        system_info = [
            ['Linux', 'aarch64'],  
            ['Windows', 'AMD64'],  
            ['Linux', 'X86_64']  
        ]
        system_id = platform.system()
        machine_id = platform.machine()
        if system_id == system_info[0][0] and machine_id == system_info[0][1]:
            return True
        else:
            return False
