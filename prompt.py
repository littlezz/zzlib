import threading
from .decorators import threading_lock, clear_output
__author__ = 'zz'






class Error:
    _error_lock = threading.Lock()

    def __init__(self, connect_fail_prompt_bound=3):
        self._connect_fail = 0
        self.connect_fail_prompt_bound = connect_fail_prompt_bound

    @threading_lock(_error_lock)
    @clear_output
    def reconnect(self, try_times):
        print('连接断开,正在尝试第{}次重连'.format(try_times))
        self._connect_fail += 1

        if self._connect_fail > self.connect_fail_prompt_bound:
            print('当前连接通道不稳定! 请检查网路状况....')
            self._connect_fail = 0