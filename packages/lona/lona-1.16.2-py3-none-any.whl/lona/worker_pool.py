from concurrent.futures import ThreadPoolExecutor


class WorkerPool:
    def __init__(self, settings):
        self.settings = settings

        self._executors = {
            'worker': ThreadPoolExecutor(
                max_workers=self.settings.MAX_WORKER_THREADS,
                thread_name_prefix='LonaWorker',
            ),
            'runtime_worker': ThreadPoolExecutor(
                max_workers=self.settings.MAX_RUNTIME_THREADS,
                thread_name_prefix='LonaRuntimeWorker',
            ),
            'channel_worker': ThreadPoolExecutor(
                max_workers=(
                    self.settings.MAX_CHANNEL_TASK_WORKER_THREADS +
                    self.settings.MAX_CHANNEL_MESSAGE_BROKER_THREADS
                ),
                thread_name_prefix='LonaChannelWorker',
            ),
            'static_worker': None,
        }

        if (self.settings.MAX_STATIC_THREADS and
                self.settings.STATIC_FILES_SERVE):

            self._executors['static_worker'] = ThreadPoolExecutor(
                max_workers=self.settings.MAX_STATIC_THREADS,
                thread_name_prefix='LonaStaticWorker',
            )

    def get_executor(self, name):
        if name not in self._executors:
            raise RuntimeError(f"no executor named '{name}'")

        if not self._executors[name]:
            raise RuntimeError(f"executor '{name}' has no threads setup")

        return self._executors[name]

    def shutdown(self):
        for executor in self._executors.values():
            if not executor:
                continue

            executor.shutdown()
