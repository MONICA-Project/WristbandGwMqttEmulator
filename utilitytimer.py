import threading
import logging


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
            logging.critical('TimerRequest configure_timer Exception: {}'.format(ex))

    @staticmethod
    def action_timer() -> bool:
        try:
            TimerRequest.get_timer().start()
            TimerRequest.request_start = True
            logging.info('TimerRequest start Called')
            return True
        except Exception as ex:
            logging.critical('TimerRequest action_timer Exception: {}'.format(ex))
            return False

    @staticmethod
    def clear_timer() -> bool:
        try:
            if not TimerRequest.request_start:
                logging.info('TimerRequest clear_timer Not necessary')
                return True

            TimerRequest.get_timer().cancel()
            logging.info('TimerRequest clear_timer Called')
            return True
        except Exception as ex:
            logging.error('TimerRequest clear_timer Exception: {}'.format(ex))
            return False
