import os.path
from collections import deque
from abc import ABC, abstractmethod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

configuration_str = open(input_path).read()


class Module(ABC):
    name: str
    receiver: list[Module]

    def __init__(self, name: str, receiver: list[Module] = []) -> None:
        self.name = name
        self.receiver = receiver

    def set_receiver(self, receiver: list[Module]) -> None:
        self.receiver = receiver

    def set_state(self, state) -> None:
        self.state = state

    def info(self) -> None:
        print(f'{self.__class__.__name__}: {self.name} -> {[m.name for m in self.receiver]}')

    @abstractmethod
    def receive(self, fr: Module, pulse: int):
        pass

    @abstractmethod
    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        pass

    @abstractmethod
    def get_pulse(self, pulse: int) -> int:
        pass


class ButtonModule(Module):

    def receive(self, fr: Module, pulse: int) -> None:
        pass

    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        return [(m, self.get_pulse(pulse)) for m in self.receiver]

    def get_pulse(self, pulse: int) -> int:
        return 0


class DummyModule(Module):

    def receive(self, fr: Module, pulse: int) -> None:
        pass

    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        return []

    def get_pulse(self, pulse: int) -> int:
        return 0


class BroadcasterModule(Module):

    def receive(self, fr: Module, pulse: int) -> None:
        pass

    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        return [(m, self.get_pulse(pulse)) for m in self.receiver]

    def get_pulse(self, pulse: int) -> int:
        return pulse


class FlipFlopModule(Module):
    state: bool = False

    def receive(self, fr: Module, pulse: int) -> None:
        if pulse == 1:
            pass
        else:
            self.state = not self.state

    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        if pulse:
            return []
        return [(m, self.get_pulse(pulse)) for m in self.receiver]

    def get_pulse(self, pulse: int) -> int:
        return 1 if self.state else 0


class ConjunctionModule(Module):
    state: dict[Module, int] = {}

    def receive(self, fr: Module, pulse: int) -> None:
        self.state[fr] = pulse

    def get_next(self, pulse: int) -> list[tuple[Module, int]]:
        return [(m, self.get_pulse(pulse)) for m in self.receiver]

    def get_pulse(self, pulse: int) -> int:
        return 0 if all(s == 1 for s in self.state.values()) else 1


class ModuleConfiguration:
    modules: dict[str, Module] = {}
    button: ButtonModule = ButtonModule('button')
    low: int = 0
    high: int = 0
    is_on = False

    def __init__(self, init: str) -> None:
        conj: dict[str, set] = {}
        for line in init.splitlines():
            name, receiver_str = line.split(' -> ')
            if name == 'broadcaster':
                mod = BroadcasterModule(name)
                self.button.set_receiver([mod])
            elif name.startswith('%'):
                mod = FlipFlopModule(name[1:])
            elif name.startswith('&'):
                mod = ConjunctionModule(name[1:])
                conj[name[1:]] = set()
            else:
                raise ValueError
            self.modules[name[1:]] = mod

        for line in init.splitlines():
            name, receiver_str = line.split(' -> ')
            receiver = [self.modules[n] if n in self.modules else DummyModule(n) for n in receiver_str.split(', ')]
            mod = self.modules[name[1:]]
            mod.set_receiver(receiver)

            for r in receiver_str.split(', '):
                if r in conj:
                    conj[r].add(name[1:])

        for n, r in conj.items():
            self.modules[n].set_state({self.modules[s]: 0 for s in r})

    def info(self) -> None:
        for name, mod in self.modules.items():
            mod.info()

    def push_button(self, n=1) -> None:
        for _ in range(n):
            start = self.button.get_next(0)
            init: list[(tuple[Module, Module, int])] = [(self.button,) + start[0]]
            q = deque(init)
            while q:
                source, target, pulse = q.popleft()
                if target.name == 'rx' and pulse == 0:
                    self.is_on = True
                if pulse:
                    self.high += 1
                else:
                    self.low += 1
                # print(f'{source.name} {pulse} -> {target.name}')
                target.receive(source, pulse)
                for m, p in target.get_next(pulse):
                    q.append((target, m, p))

    def score(self) -> int:
        return self.low * self.high

    def turn_on(self) -> int:
        for i in range(1, 1000):
            self.push_button()
            if self.is_on:
                return i
        return -1


mconfig = ModuleConfiguration(configuration_str)
mconfig.push_button(1000)
print("Part 1:", mconfig.score())

mconfig = ModuleConfiguration(configuration_str)
ans = mconfig.turn_on()
print("Part 2:", ans)
