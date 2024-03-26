import gc
import time
import logging
from threading import Thread


class Launcher:
    """
    A scheduled threading task manager.

    pass tasks in the form of a dictionary:

    {
        'my_task': {
            'task': MyClass,    required
            'args': (),         optional
            'kwargs': {},       optional
            'restart': True,    optional
            'delay': 600        optional
        }
    }
    """
    term = False
    task = None

    def __init__(self, tasks: dict):
        self.tasks = tasks
        self._check_keys()

    def _loop_wrapper(self, *args, **kwargs):
        """
        This is a scheduled task wrapper, pretty rad, huh?
        """
        print('#############', kwargs.keys())
        delay = kwargs.pop('delay')
        callback = kwargs.pop('callback')
        while not self.term:
            callback(*args, **kwargs)
            time.sleep(delay)
        return self

    def _check_keys(self):
        """
        This just simplifies the input requirements.
        """
        required_keys = ['args', 'kwargs', 'restart']
        defaults = [list(), dict(), False]
        for key in self.tasks:
            for required_key, default in zip(required_keys, defaults):
                if required_key not in self.tasks[key].keys():
                    self.tasks[key][required_key] = default
        return self

    def _launch_task(self, task_name: str):
        """
        Launch a specific task.
        """
        task = self.tasks[task_name]
        kwargs = {
            'args': task['args'],
            'kwargs': task['kwargs'],
            'daemon': True
        }
        if 'delay' in task.keys():
            kwargs['target'] = self._loop_wrapper
            kwargs['kwargs'].update({
                'delay': task['delay'],
                'callback': task['task']
            })
        else:
            kwargs['target'] = task['task']
        thread = Thread(**kwargs)
        thread.start()
        self.tasks[task_name].update(
            {
                'thread': thread,
                'running': True
            }
        )
        return self

    def start_tasks(self):
        """
        Launch our threaded tasks.
        """
        for key in self.tasks.keys():
            print(f'launching task: {key}')
            self._launch_task(key)
        self.task = Thread(target=self._update_tasks, daemon=True)
        self.task.start()
        return self

    def _update_tasks(self):
        """
        Ensure our tasks are operating correctly.

        Note: This works without an actual termination signal because all the threads are daemonized.
        """
        while not self.term:
            time.sleep(5)
            for key in self.tasks.keys():
                task = self.tasks[key]
                is_running = task['thread'].is_alive()
                do_restart = task['restart']
                task['running'] = is_running
                if do_restart and not is_running and not self.term:
                    logging.info(f'restarting task: {key}')
                    self._launch_task(key)

        for key in self.tasks.keys():
            logging.info(f'terminating task: {key}')
            self.tasks[key]['thread']  = None  # Drop handle.
            self.tasks[key]['running'] = False

        logging.info('threaded scheduler terminating')
        gc.collect()  # Purge orphaned handles.

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa
        self.term = True
