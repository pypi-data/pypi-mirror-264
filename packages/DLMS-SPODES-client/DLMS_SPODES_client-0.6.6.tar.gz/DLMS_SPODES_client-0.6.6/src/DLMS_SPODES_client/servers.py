from threading import Thread, Event
from functools import cached_property
import asyncio
from .client import Client, Errors, cdt
from . import task
from DLMS_SPODES.enums import Transmit, Application
from DLMS_SPODES import exceptions as exc
from .enums import LogLevel as logL


class Result:
    client: Client
    complete: bool
    errors: Errors
    value: cdt.CommonDataType | None

    def __init__(self, client: Client):
        self.client = client
        self.complete = False
        """complete exchange"""
        self.errors = Errors()
        self.value = None
        """response if available"""


class Results:
    __values: tuple[Result, ...]
    name: str
    tsk: task.ExTask

    def __init__(self, clients: tuple[Client],
                 tsk: task.ExTask,
                 name: str = None):
        self.__values = tuple(Result(c) for c in clients)
        self.tsk = tsk
        self.name = name
        """common operation name"""

    def __getitem__(self, item):
        return self.__values[item]

    @cached_property
    def clients(self) -> set[Client]:
        return {res.client for res in self.__values}

    @cached_property
    def ok_results(self) -> set[Result]:
        """without errors exchange clients"""
        ret = set()
        for res in self.__values:
            if all(map(lambda err_code: err_code.is_ok(), res.errors)):
                ret.add(res)
        return ret

    @cached_property
    def nok_results(self) -> set[Result]:
        """ With errors exchange clients """
        return set(self.__values).difference(self.ok_results)

    def is_complete(self) -> bool:
        return all((res.complete for res in self))


class TransactionServer:
    __t: Thread
    results: Results

    def __init__(self,
                 clients: list[Client] | tuple[Client],
                 tsk: task.ExTask,
                 name: str = None,
                 abort_timeout: int = 1):
        self.results = Results(clients, tsk, name)
        # self._tg = None
        self.__stop = Event()
        self.__t = Thread(
            target=self.__start_coro,
            args=(self.results, abort_timeout))

    def start(self):
        self.__t.start()

    def abort(self):
        self.__stop.set()

    def __start_coro(self, results, abort_timeout):
        asyncio.run(self.coro_loop(results, abort_timeout))

    async def coro_loop(self, results: Results, abort_timeout: int):
        async def check_stop(tg: asyncio.TaskGroup):
            while True:
                await asyncio.sleep(abort_timeout)
                if self.__stop.is_set():
                    print("abort")
                    tg._abort()
                    # break

        async with asyncio.TaskGroup() as tg:
            for res in results:
                tg.create_task(
                    coro=session(
                        c=res.client,
                        t=results.tsk,
                        result=res))
            tg.create_task(check_stop(tg))


async def session(c: Client,
                  t: task.ExTask,
                  result: Result,
                  is_public: bool = False):
    try:
        await c.connect(is_public)
        result.value = await t.exchange(c)
    except TimeoutError as e:
        c.set_error(Transmit.TIMEOUT, 'Таймаут при обмене')
    except exc.DLMSException as e:
        c.set_error(e.error, e.args[0])
    except ConnectionError as e:
        c.set_error(Transmit.NO_TRANSPORT, F"При соединении{e}")
    except Exception as e:
        c.log(logL.INFO, F'UNKNOWN ERROR: {e}...')
        c.set_error(Transmit.UNKNOWN, F'При обмене{e}')
    except asyncio.CancelledError as e:
        c.set_error(Transmit.ABORT, "ручная остановка")
    finally:
        result.complete = True
        result.errors = c.errors
        match c.errors:
            case {Transmit.OK: _} if len(c.errors) == 1:
                await c.close()
            case {Transmit.NO_TRANSPORT: _} | {Transmit.NO_PORT: _}:
                """ nothing need do. Port not open ... etc """
            case {Application.MISSING_OBJ: _}:
                await c.close()
            case {Transmit.TIMEOUT: _} | {Transmit.ABORT: _}:
                await c.force_disconnect()
            case {Transmit.NO_ACCESS: _} | {Application.ID_ERROR: _} | {Application.VERSION_ERROR: _}:
                await c.close()
            case _:
                await c.force_disconnect()
        return result
