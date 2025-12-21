import os.path
from collections import deque
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple
from math import lcm


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
    state: dict[Module, bool]

    def __init__(self, name: str) -> None:
        self.name = name
        self.state = {self: False}

    def set_receiver(self, receiver: list[Module]) -> None:
        self.receiver = receiver

    def set_state(self, state) -> None:
        self.state = state

    def send(self) -> list[Message]:
        if self.next_pulse is None:
            return []
        return [Message(self, m, self.next_pulse) for m in self.receiver]

    def receive_and_send(self, msg: Message) -> list[Message]:
        self.process(msg.sender, msg.pulse)
        return self.send()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.name} -> {[m.name for m in self.receiver]}'

    def reset(self) -> None:
        self.next_pulse = Pulse.LOW
        self.state = {m: False for m in self.state}

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

    def process(self, sender: Module, pulse: Pulse):
        if pulse == Pulse.HIGH:
            self.next_pulse = None
        else:
            self.state[self] = not self.state[self]
            self.next_pulse = Pulse.HIGH if self.state[self] else Pulse.LOW


class ConjunctionModule(Module):

    def process(self, sender: Module, pulse: Pulse):
        self.state[sender] = True if pulse == Pulse.HIGH else False
        self.next_pulse = Pulse.LOW if all(s == True for s in self.state.values()) else Pulse.HIGH


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
                raise ValueError(f'Module Identifier unknown: {name}')
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
            print(mod)

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

    def reset(self) -> None:
        for mod in self.modules.values():
            mod.reset()

    def part2(self) -> int:
        # manual inspection of input data:
        # rx is connected to a single conj (AND) module
        # that module has 4 inputs -> get cycles of those and calc lcm
        rx = self.modules['rx']
        conjs = [mod for mod in self.modules.values() if rx in mod.receiver]
        assert (len(conjs) == 1)
        conj = conjs[0]
        assert (type(conj) == ConjunctionModule)
        inputs = [mod for mod in conj.state.keys()]

        self.reset()
        cycles = {mod: [] for mod in inputs}
        for i in range(1, 10_000):
            q: deque[Message] = deque(self.modules['button'].send())

            while q:
                msg = q.popleft()
                response = msg.receiver.receive_and_send(msg)
                q.extend(response)

                if msg.pulse == Pulse.HIGH and msg.sender in cycles:
                    cycles[msg.sender].append(i)
        return lcm(*map(min, cycles.values()))


manager = ModuleManager(configuration_str)
# print(manager.info())
manager.push_button(1000)
print("Part 1:", manager.score())
print("Part 2:", manager.part2())
