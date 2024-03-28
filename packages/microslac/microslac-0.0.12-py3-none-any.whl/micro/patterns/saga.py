from __future__ import annotations

from types import SimpleNamespace
from typing import Literal

__all__ = ["State", "Step", "Saga"]


class State(SimpleNamespace):
    pass


class Step:
    name: str
    saga: Saga
    state: State
    retry: int = 0

    def setup(self, saga: Saga, state: State):
        self.saga = saga
        self.state = state
        self.retry = self.retry if self.retry else self.saga.retry

    def action(self):
        pass

    def compensate(self):
        pass


class Saga:
    retry: int = 1
    state: State = State()
    status: Literal["success", "error", "fatal"]
    _steps: list[Step] = []
    current_index = 0
    error: Exception
    fatal: Exception

    def run(self):
        try:
            self.execute()
        except Exception as error:
            self.error = error
            try:
                self.rollback()
                self.status = "error"
            except Exception as fatal:
                self.fatal = fatal
                self.status = "fatal"
                self.on_fatal()
            else:
                self.on_error()
        else:
            self.status = "success"
            self.on_success()

    def execute(self):
        for index, step in enumerate(self.steps):
            self.current_index = index
            step.action()

    def rollback(self):
        for index in range(self.current_index - 1, -1, -1):
            self.current_index = index
            step = self.steps[index]
            step.compensate()

    def on_success(self):
        pass

    def on_error(self):
        raise self.error

    def on_fatal(self):
        raise self.fatal

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, values: list[Step]):
        for step in values:
            step.setup(self, self.state)
        self._steps = values

    @property
    def is_success(self):
        return self.status == "success"

    @property
    def is_rollback(self):
        return self.status == "rollback"

    @property
    def is_error(self):
        return self.status == "error"
