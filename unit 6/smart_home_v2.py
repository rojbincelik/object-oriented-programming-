from abc import ABC, abstractmethod
from datetime import datetime


# =========================================================
# COMMON INTERFACE (Target / Component)
# Every device in the system must follow this contract:
# attributes: name, power, is_on
# methods:    turn_on(), turn_off()
# =========================================================
class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class SmartLight(Device):
    """Concrete Component: a native device that already fits the interface."""

    def __init__(self, name, power=10):
        self.name = name
        self.power = power      # in watts
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


# =========================================================
# 2) ADAPTER PATTERN
# SmartFan is a third-party class (Adaptee) with an incompatible
# interface. We cannot modify its source code.
# =========================================================
class SmartFan:
    """Adaptee: third-party device with a different interface."""

    def __init__(self, model):
        self.model = model
        self.speed = 0          # 0 = off

    def start_spinning(self, speed=2):
        self.speed = speed

    def stop_spinning(self):
        self.speed = 0

    def get_speed(self):
        return self.speed


class SmartFanAdapter(Device):
    """Adapter: translates the Device interface into SmartFan calls."""

    def __init__(self, fan, name, power):
        self._fan = fan         # composition: the adapter wraps the adaptee
        self.name = name
        self.power = power

    @property
    def is_on(self):
        return self._fan.get_speed() > 0

    def turn_on(self):
        self._fan.start_spinning()

    def turn_off(self):
        self._fan.stop_spinning()


# =========================================================
# 3) DECORATOR PATTERN
# Wraps a device with an object that has the SAME interface
# and adds behavior at runtime.
# =========================================================
class DeviceDecorator(Device):
    """Base Decorator: delegates everything to the wrapped component."""

    def __init__(self, device):
        self._device = device

    # Forward the component's attributes unchanged
    @property
    def name(self):
        return self._device.name

    @property
    def power(self):
        return self._device.power

    @property
    def is_on(self):
        return self._device.is_on

    def turn_on(self):
        self._device.turn_on()

    def turn_off(self):
        self._device.turn_off()


class LoggingDecorator(DeviceDecorator):
    """Concrete Decorator: logs every operation before delegating."""

    def _log(self, action):
        print(f"[LOG {datetime.now():%H:%M:%S}] {self.name}: {action}")

    def turn_on(self):
        self._log("turn_on")
        self._device.turn_on()

    def turn_off(self):
        self._log("turn_off")
        self._device.turn_off()


class SecurityDecorator(DeviceDecorator):
    """Concrete Decorator: blocks operations while the device is locked."""

    def __init__(self, device, locked=False):
        super().__init__(device)
        self.locked = locked

    def turn_on(self):
        if self.locked:
            print(f"[SECURITY] {self.name} is locked, operation denied")
            return
        self._device.turn_on()

    def turn_off(self):
        if self.locked:
            print(f"[SECURITY] {self.name} is locked, operation denied")
            return
        self._device.turn_off()


# =========================================================
# 4) OBSERVER PATTERN
# =========================================================
class Observer(ABC):
    """Observer interface: any subscriber must implement update()."""

    @abstractmethod
    def update(self, device):
        pass


class User(Observer):
    """Concrete Observer."""

    def __init__(self, name):
        self.name = name

    def update(self, device):
        state = "ON" if device.is_on else "OFF"
        print(f"   -> {self.name} notified: {device.name} is {state}")


# =========================================================
# 5) STRATEGY PATTERN
# Each algorithm answers the same question differently:
# "Which devices should be turned off?"
# =========================================================
class EnergyStrategy(ABC):
    """Strategy interface."""

    @abstractmethod
    def select(self, devices):
        pass


class NormalMode(EnergyStrategy):
    """Concrete Strategy: turn nothing off."""

    def select(self, devices):
        return []


class EcoMode(EnergyStrategy):
    """Concrete Strategy: turn off devices above a power limit."""

    def __init__(self, limit=50):
        self.limit = limit

    def select(self, devices):
        return [d for d in devices if d.is_on and d.power > self.limit]


class NightMode(EnergyStrategy):
    """Concrete Strategy: turn off every device that is on."""

    def select(self, devices):
        return [d for d in devices if d.is_on]


# =========================================================
# 1) SINGLETON PATTERN: DeviceManager
# Also acts as the Subject (Observer pattern)
# and the Context (Strategy pattern).
# =========================================================
class DeviceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # State is initialized here, ONLY on first creation.
            # If it were in __init__, it would be reset on every DeviceManager() call.
            cls._instance._devices = {}
            cls._instance._observers = []
            cls._instance._strategy = NormalMode()
        return cls._instance

    # --- device management ---
    def add_device(self, device):
        self._devices[device.name] = device

    # --- observer management (Subject role) ---
    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def _notify(self, device):
        for obs in self._observers:
            obs.update(device)

    # --- state change: notify only if the state actually changed ---
    def _change_state(self, device, turn_on):
        before = device.is_on
        if turn_on:
            device.turn_on()
        else:
            device.turn_off()
        if device.is_on != before:
            self._notify(device)

    def turn_on(self, name):
        self._change_state(self._devices[name], True)

    def turn_off(self, name):
        self._change_state(self._devices[name], False)

    # --- strategy management (Context role) ---
    def set_strategy(self, strategy):
        self._strategy = strategy

    def apply_energy_saving(self):
        for device in self._strategy.select(list(self._devices.values())):
            self._change_state(device, False)


# =========================================================
# DEMO
# =========================================================
if __name__ == "__main__":
    print("=== 1) Singleton ===")
    m1 = DeviceManager()
    m2 = DeviceManager()
    print("Are m1 and m2 the same instance?", m1 is m2)
    manager = m1

    print("\n=== 2) Adapter + 3) Decorator: registering devices ===")
    lamp = LoggingDecorator(SmartLight("Living Room Light", power=10))
    fan = LoggingDecorator(SmartFanAdapter(SmartFan("XF-200"), "Fan", power=60))
    bedroom = SecurityDecorator(LoggingDecorator(SmartLight("Bedroom Light")), locked=True)
    for d in (lamp, fan, bedroom):
        manager.add_device(d)
    print("3 devices registered (fan via adapter, all wrapped with decorators)")

    print("\n=== 4) Observer: users subscribe ===")
    manager.subscribe(User("Alice"))
    manager.subscribe(User("Bob"))

    manager.turn_on("Living Room Light")
    manager.turn_on("Fan")
    manager.turn_on("Bedroom Light")   # locked, no notification should be sent

    print("\n=== 5) Strategy: EcoMode (turn off devices above 50W) ===")
    manager.set_strategy(EcoMode(limit=50))
    manager.apply_energy_saving()

    print("\n=== 5) Strategy: NightMode (turn everything off) ===")
    manager.set_strategy(NightMode())
    manager.apply_energy_saving()
