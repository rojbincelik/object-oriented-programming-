from abc import ABC, abstractmethod
from datetime import datetime


# =========================================================
# ORTAK ARAYÜZ: Sistemdeki her cihaz bu sözleşmeye uymalı
# (name, power, is_on + turn_on/turn_off)
# =========================================================
class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class SmartLight(Device):
    def __init__(self, name, power=10):
        self.name = name
        self.power = power      # watt
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


# =========================================================
# 2) ADAPTER
# SmartFan başka bir firmanın sınıfı, arayüzü bizimkine uymuyor
# ve kodunu değiştiremiyoruz.
# =========================================================
class SmartFan:
    def __init__(self, model):
        self.model = model
        self.speed = 0          # 0 = kapalı

    def start_spinning(self, speed=2):
        self.speed = speed

    def stop_spinning(self):
        self.speed = 0

    def get_speed(self):
        return self.speed


class SmartFanAdapter(Device):
    def __init__(self, fan, name, power):
        self._fan = fan
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
# 3) DECORATOR
# Cihazı aynı arayüze sahip bir nesneyle sarar, davranış ekler.
# =========================================================
class DeviceDecorator(Device):
    def __init__(self, device):
        self._device = device

    # Bilgileri içerideki cihazdan aynen ilet
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
    def _log(self, action):
        print(f"[LOG {datetime.now():%H:%M:%S}] {self.name}: {action}")

    def turn_on(self):
        self._log("turn_on")
        self._device.turn_on()

    def turn_off(self):
        self._log("turn_off")
        self._device.turn_off()


class SecurityDecorator(DeviceDecorator):
    def __init__(self, device, locked=False):
        super().__init__(device)
        self.locked = locked

    def turn_on(self):
        if self.locked:
            print(f"[GÜVENLİK] {self.name} kilitli, işlem reddedildi")
            return
        self._device.turn_on()

    def turn_off(self):
        if self.locked:
            print(f"[GÜVENLİK] {self.name} kilitli, işlem reddedildi")
            return
        self._device.turn_off()


# =========================================================
# 4) OBSERVER
# =========================================================
class Observer(ABC):
    @abstractmethod
    def update(self, device):
        pass


class User(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, device):
        state = "AÇIK" if device.is_on else "KAPALI"
        print(f"   -> {self.name} bildirimi aldı: {device.name} {state}")


# =========================================================
# 5) STRATEGY
# Her algoritma "hangi cihazlar kapatılsın?" sorusunu farklı cevaplar.
# =========================================================
class EnergyStrategy(ABC):
    @abstractmethod
    def select(self, devices):
        pass


class NormalMode(EnergyStrategy):
    def select(self, devices):
        return []                                   # hiçbir şeyi kapatma


class EcoMode(EnergyStrategy):
    def __init__(self, limit=50):
        self.limit = limit

    def select(self, devices):
        return [d for d in devices if d.is_on and d.power > self.limit]


class NightMode(EnergyStrategy):
    def select(self, devices):
        return [d for d in devices if d.is_on]      # açık olan her şeyi kapat


# =========================================================
# 1) SINGLETON: DeviceManager
# Aynı zamanda Observer'daki "subject" ve Strategy'deki "context".
# =========================================================
class DeviceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # State burada, SADECE İLK SEFERDE kuruluyor.
            # __init__ içinde kursaydık her DeviceManager() çağrısında sıfırlanırdı.
            cls._instance._devices = {}
            cls._instance._observers = []
            cls._instance._strategy = NormalMode()
        return cls._instance

    # --- cihaz yönetimi ---
    def add_device(self, device):
        self._devices[device.name] = device

    # --- observer yönetimi ---
    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def _notify(self, device):
        for obs in self._observers:
            obs.update(device)

    # --- durum değişikliği: sadece gerçekten değiştiyse bildir ---
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

    # --- strategy yönetimi ---
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
    print("m1 ile m2 aynı nesne mi?", m1 is m2)
    manager = m1

    print("\n=== 2) Adapter + 3) Decorator: cihazları ekle ===")
    lamp = LoggingDecorator(SmartLight("Salon Lambası", power=10))
    fan = LoggingDecorator(SmartFanAdapter(SmartFan("XF-200"), "Vantilatör", power=60))
    bedroom = SecurityDecorator(LoggingDecorator(SmartLight("Yatak Odası Lambası")), locked=True)
    for d in (lamp, fan, bedroom):
        manager.add_device(d)
    print("3 cihaz eklendi (fan adapter üzerinden, hepsi decorator ile sarılı)")

    print("\n=== 4) Observer: kullanıcılar abone oluyor ===")
    manager.subscribe(User("Ali"))
    manager.subscribe(User("Ayşe"))

    manager.turn_on("Salon Lambası")
    manager.turn_on("Vantilatör")
    manager.turn_on("Yatak Odası Lambası")   # kilitli, bildirim gitmemeli

    print("\n=== 5) Strategy: EcoMode (50W üstünü kapat) ===")
    manager.set_strategy(EcoMode(limit=50))
    manager.apply_energy_saving()

    print("\n=== 5) Strategy: NightMode (her şeyi kapat) ===")
    manager.set_strategy(NightMode())
    manager.apply_energy_saving()
