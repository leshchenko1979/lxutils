import urllib.parse

import asyncio
import aiohttp
import time

from tqdm import tqdm

class SemaphoreWrapper():

    def __init__(self, custom_pool_size=100):
        self._stopped_time = None
        self._stopped_value = None
        self._REQUESTS_PER_SECOND = 2
        self._pool_size = custom_pool_size


    async def __aenter__(self):
        self._sem = asyncio.BoundedSemaphore(self._pool_size)
        if self._stopped_time:
            self._value = min(self._sem._bound_value, self._stopped_value + 
                int((time.monotonic() - self._stopped_time) * self._REQUESTS_PER_SECOND))
            self._stopped_time = None
            self._stopped_value = None
        self.release_task = asyncio.create_task(self._release_sem())


    async def __aexit__(self, a1, a2, a3):
        self._stopped_time = time.monotonic()
        self._stopped_value = self._sem._value
        self.release_task.cancel()


    async def _release_sem(self):
        while True:
            if self._sem._value < self._sem._bound_value - 1:
                self._sem.release()
            await asyncio.sleep(1 / self._REQUESTS_PER_SECOND)


    async def acquire(self):
        return await self._sem.acquire()

class Bitrix:
    def __init__(self, webhook, custom_pool_size = 100):
        self.webhook = webhook
        self._sw = SemaphoreWrapper(custom_pool_size)


    async def _get_paginated_list(self, method, payload_details=None, custom_start=0):
        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            results, total = await self._get_list_starting(session, custom_start, method, payload_details)
            tasks = []
            if not total or total <= 50:
                return results
            with tqdm(total=total, initial=custom_start + len(results)) as pbar:
                for start in range(custom_start + len(results), total, 50):
                    tasks.append(asyncio.create_task(self._get_list_starting(
                        session, start, method, payload_details, pbar)))
                for x in asyncio.as_completed((*tasks, self._sw.release_task)):
                    r = await x
                    results.extend(r[0])
                    if len(results) >= total: break
            results = [dict(t) for t in {tuple(d.items()) for d in results}] 
            if len(results) == total: 
                return results
#            else:
#                raise RuntimeWarning (
#                    f'Got {len(results)} entries, while expecting {total}')
        

    async def _get_list_starting(self, session, start, method, payload_details=None, pbar=None):
        url = self.webhook + method

        # log (f'Downloading list "{method}": {start}')
        payload = [('start', start)] + \
            (payload_details if payload_details else [])

        await self._sw.acquire()
        async with session.get(url, params=payload) as response:
            r = await response.json(encoding='utf-8')
        if pbar:
            pbar.update(len(r['result']))
        return r['result'], (r['total'] if 'total' in r.keys() else None)


    def get_list(self, method, payload_details=None):
        return asyncio.run(self._get_paginated_list(method, payload_details))


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))
