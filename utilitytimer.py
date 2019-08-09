import threading


class TimerRequest:
    timer_set = None
    request_start = False

    @staticmethod
    def get_timer() -> threading.Timer:
        if not TimerRequest.timer_set:
            raise Exception('NO TIMER SET')
        return TimerRequest.timer_set

    @staticmethod
    def configure_timer(func, timeout):
        try:
            TimerRequest.timer_set = threading.Timer(interval=timeout, function=func)
        except Exception as ex:
            print('TimerRequest configure_timer Exception: {}'.format(ex))

    @staticmethod
    def action_timer() -> bool:
        try:
            TimerRequest.get_timer().start()
            TimerRequest.request_start = True
            print('TimerRequest start Called')
        except Exception as ex:
            print('TimerRequest action_timer Exception: {}'.format(ex))

    @staticmethod
    def clear_timer() -> bool:
        try:
            if not TimerRequest.request_start:
                print('TimerRequest clear_timer Not necessary')
                return True

            TimerRequest.get_timer().cancel()
            print('TimerRequest clear_timer Called')
            return True
        except Exception as ex:
            print('TimerRequest clear_timer Exception: {}'.format(ex))
            return False
