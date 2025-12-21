import os.path
from collections import deque
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple


class Pulse(Enum):
    LOW = False,
    HIGH = True


class Message(NamedTuple):
    sender: Module
    receiver: Module
    pulse: Pulse


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

configuration_str = open(input_path).read()


class Module(ABC):
    name: str
    receiver: list[Module] = []
    next_pulse: Pulse | None = Pulse.LOW

    def __init__(self, name: str) -> None:
        self.name = name

    def set_receiver(self, receiver: list[Module]) -> None:
        self.receiver = receiver

    def set_state(self, state) -> None:
        self.state = state

    def send(self) -> list[Message]:
        if self.next_pulse is not None:
            msg = [Message(self, m, self.next_pulse) for m in self.receiver]
            return msg
        return []

    def receive_and_send(self, msg: Message) -> list[Message]:
        self.process(msg.sender, msg.pulse)
        return self.send()

    def info(self) -> None:
        print(f'{self.__class__.__name__}: {self.name} -> {[m.name for m in self.receiver]}')

    @abstractmethod
    def process(self, sender: Module, pulse: Pulse):
        pass


class ButtonModule(Module):

    def process(self, sender: Module, pulse: Pulse):
        pass


class DummyModule(Module):

    def process(self, sender: Module, pulse: Pulse):
        pass


class BroadcasterModule(Module):

    def process(self, sender: Module, pulse: Pulse):
        self.next_pulse = pulse


class FlipFlopModule(Module):
    state: bool = False

    def process(self, sender: Module, pulse: Pulse):
        if pulse == Pulse.HIGH:
            self.next_pulse = None
        else:
            self.state = not self.state
            self.next_pulse = Pulse.HIGH if self.state else Pulse.LOW


class ConjunctionModule(Module):
    state: dict[Module, Pulse] = {}

    def process(self, sender: Module, pulse: Pulse):
        self.state[sender] = pulse
        self.next_pulse = Pulse.LOW if all(s == Pulse.HIGH for s in self.state.values()) else Pulse.HIGH


class ModuleManager:
    modules: dict[str, Module] = {}
    low: int = 0
    high: int = 0

    def __init__(self, init: str) -> None:
        conj: dict[str, set] = {}

        # create modules
        self.modules['button'] = ButtonModule('button')
        for line in init.splitlines():
            name, receiver_str = line.split(' -> ')
            if name == 'broadcaster':
                mod = BroadcasterModule(name)
                self.modules['button'].set_receiver([mod])
            elif name.startswith('%'):
                mod = FlipFlopModule(name[1:])
            elif name.startswith('&'):
                mod = ConjunctionModule(name[1:])
                conj[name[1:]] = set()
            else:
                raise ValueError
            self.modules[name[1:]] = mod

        # set receiver for every module
        for line in init.splitlines():
            name, receiver_str = line.split(' -> ')
            receiver = []
            for r in receiver_str.split(', '):
                if r in conj:
                    conj[r].add(name[1:])
                if r in self.modules:
                    receiver.append(self.modules[r])
                else:  # need dummy (rx)
                    dummy = DummyModule(r)
                    self.modules[r] = dummy
                    receiver.append(dummy)
            mod = self.modules[name[1:]]
            mod.set_receiver(receiver)

        # init state for conjunction modules
        for n, r in conj.items():
            self.modules[n].set_state({self.modules[s]: Pulse.LOW for s in r})

    def info(self) -> None:
        for name, mod in self.modules.items():
            mod.info()

    def push_button(self, n=1) -> None:
        for _ in range(n):
            q: deque[Message] = deque(self.modules['button'].send())
            while q:
                message = q.popleft()
                response = message.receiver.receive_and_send(message)
                q.extend(response)

                if message.pulse == Pulse.HIGH:
                    self.high += 1
                else:
                    self.low += 1
                # print(f'{message.sender.name} {message.pulse} -> {message.receiver.name}')

    def score(self) -> int:
        return self.low * self.high


manager = ModuleManager(configuration_str)
# print(manager.info())
manager.push_button(1000)
print("Part 1:", manager.score())
print("Part 2:",)
