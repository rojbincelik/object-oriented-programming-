from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


# --------------------------------------------------------------------------- #
# 1. ABSTRACTION  - abstract class + interface                        [7][10] #
# --------------------------------------------------------------------------- #
class User(ABC):
    """Abstract base class: anyone who can log in to the shop.

    Cannot be instantiated directly - subclasses must implement get_role().
    Shared identity data lives here so Customer / future Admin don't repeat it.
    """

    def __init__(self, user_id: int, name: str, email: str) -> None:
        if "@" not in email:
            raise ValueError(f"Invalid e-mail address: {email!r}")
        self._user_id = user_id      # protected: subclasses may read
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        """Read-only view of the user's name."""
        return self._name

    @abstractmethod
    def get_role(self) -> str:
        """Every concrete user must say what kind of user it is."""

    def __str__(self) -> str:
        return f"{self.get_role()}: {self._name} <{self._email}>"


class Orderable(ABC):
    """Interface (pure abstract class): anything that can be put in an order.

    Python has no `interface` keyword; an ABC with only abstract methods
    plays the same role (Python Software Foundation, no date a).
    """

    @abstractmethod
    def get_price(self) -> float: ...

    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def reserve(self, quantity: int) -> None:
        """Take `quantity` units out of availability, or raise ValueError."""


# --------------------------------------------------------------------------- #
# 2. CONCRETE ENTITIES                                                  [2][8] #
# --------------------------------------------------------------------------- #
class Product(Orderable):
    """A physical catalogue item with limited stock."""

    def __init__(self, product_id: int, name: str, price: float, stock: int) -> None:
        # Constructor validates so an object can never start in a bad state [3]
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        self.__product_id = product_id   # private (name-mangled) - never changes
        self._name = name                # protected
        self._price = price
        self._stock = stock

    # ---- controlled access (encapsulation) -------------------------------- #
    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    # ---- Orderable implementation ----------------------------------------- #
    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return self._name

    def reserve(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > self._stock:
            raise ValueError(f"Only {self._stock} x {self._name} in stock")
        self._stock -= quantity

    def release(self, quantity: int) -> None:
        """Put units back (order cancelled)."""
        self._stock += quantity

    def __repr__(self) -> str:
        return f"Product({self.__product_id}, {self._name!r}, {self._price}, stock={self._stock})"


class GiftCard(Orderable):
    """A second Orderable with no stock concept - shows the interface's value."""

    def __init__(self, amount: float) -> None:
        self._amount = amount

    def get_price(self) -> float:
        return self._amount

    def get_description(self) -> str:
        return f"Gift card ({self._amount:.2f})"

    def reserve(self, quantity: int) -> None:
        pass  # digital item: unlimited supply, nothing to reserve


class Customer(User):
    """A registered buyer. Inherits identity from User."""              # [5]

    def __init__(self, customer_id: int, name: str, email: str) -> None:
        super().__init__(customer_id, name, email)   # reuse parent constructor
        self._orders: list[Order] = []

    def get_role(self) -> str:
        return "Customer"

    def calculate_discount(self, subtotal: float) -> float:
        """Standard customers get no discount. Overridden in PremiumCustomer."""
        return 0.0

    def add_order(self, order: Order) -> None:
        self._orders.append(order)

    @property
    def orders(self) -> tuple[Order, ...]:
        """Return an immutable view so callers cannot mutate the history."""
        return tuple(self._orders)


class PremiumCustomer(Customer):
    """Subclass: same interface as Customer, different discount behaviour."""

    DISCOUNT_RATE = 0.10          # class variable shared by all instances

    def __init__(self, customer_id: int, name: str, email: str, member_since: int) -> None:
        super().__init__(customer_id, name, email)
        self._member_since = member_since

    def get_role(self) -> str:                                          # [6]
        return "Premium Customer"

    def calculate_discount(self, subtotal: float) -> float:              # [6]
        """Override: 10 % off, +5 % more for members of 5+ years."""
        rate = self.DISCOUNT_RATE
        if datetime.now().year - self._member_since >= 5:
            rate += 0.05
        return round(subtotal * rate, 2)


# --------------------------------------------------------------------------- #
# 3. ABSTRACT DATA TYPE - ShoppingCart                                    [10] #
# --------------------------------------------------------------------------- #
class ShoppingCart:
    """ADT: a multiset of Orderable items.

    Public operations: add, remove, lines, is_empty, clear.
    The internal representation (a dict keyed by id()) is hidden and could be
    swapped for a list or a database row without changing any caller.
    """

    def __init__(self) -> None:
        self.__lines: dict[int, list] = {}      # id(item) -> [item, quantity]

    def add(self, item: Orderable, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        key = id(item)
        if key in self.__lines:
            self.__lines[key][1] += quantity
        else:
            self.__lines[key] = [item, quantity]

    def remove(self, item: Orderable) -> None:
        self.__lines.pop(id(item), None)

    def lines(self) -> list[tuple[Orderable, int]]:
        """Snapshot copy - callers cannot reach the internal dict."""
        return [(item, qty) for item, qty in self.__lines.values()]

    def is_empty(self) -> bool:
        return not self.__lines

    def clear(self) -> None:
        self.__lines.clear()


# --------------------------------------------------------------------------- #
# 4. ORDER - class vs instance variables, class methods, destructor  [3][4]  #
# --------------------------------------------------------------------------- #
class Order:
    """A confirmed or pending purchase for one customer."""

    _next_id: int = 1000          # class variable: shared counter for IDs
    _orders_created: int = 0      # class variable: statistics across all orders

    def __init__(self, customer: Customer) -> None:                    # [3]
        self._order_id = Order._next_id       # instance variable: per object
        Order._next_id += 1
        Order._orders_created += 1
        self._customer = customer
        self._items: list[tuple[Orderable, int]] = []
        self._status = "PENDING"
        self._created_at = datetime.now()

    # ---- alternative constructor -----------------------------------------#
    @classmethod
    def from_cart(cls, customer: Customer, cart: ShoppingCart) -> Order:   # [4]
        """Build an Order from a ShoppingCart ADT, then empty the cart."""
        if cart.is_empty():
            raise ValueError("Cannot create an order from an empty cart")
        order = cls(customer)
        for item, qty in cart.lines():
            order.add_item(item, qty)
        cart.clear()
        return order

    @classmethod
    def orders_created(cls) -> int:
        """Class method: reads class-level state, needs no instance."""
        return cls._orders_created

    @staticmethod
    def _format_money(amount: float) -> str:
        return f"{amount:,.2f}"

    # ---- core behaviour -------------------------------------------------- #
    def add_item(self, item: Orderable, quantity: int = 1) -> None:       # [4]
        """Reserve stock and add a line. Fails atomically if unavailable."""
        if self._status != "PENDING":
            raise RuntimeError("Cannot modify a non-pending order")
        item.reserve(quantity)            # polymorphic: Product or GiftCard
        self._items.append((item, quantity))

    def subtotal(self) -> float:
        return sum(item.get_price() * qty for item, qty in self._items)

    def total_cost(self) -> float:                                        # [4]
        """Subtotal minus whatever discount the customer type grants."""
        sub = self.subtotal()
        return round(sub - self._customer.calculate_discount(sub), 2)     # [6]

    def confirm(self) -> None:
        self._status = "CONFIRMED"
        self._customer.add_order(self)

    def cancel(self) -> None:
        """Explicit clean-up: preferred over relying on __del__."""
        if self._status == "PENDING":
            for item, qty in self._items:
                if isinstance(item, Product):
                    item.release(qty)
        self._status = "CANCELLED"

    @property
    def status(self) -> str:
        return self._status

    # ---- destructor --------------------------------------------------------#
    def __del__(self) -> None:                                            # [3]
        """Called when the garbage collector destroys the object.

        Python destructors are NOT deterministic, so this is a safety net only;
        real clean-up is done in cancel(). Used here to illustrate the concept.
        """
        if getattr(self, "_status", None) == "PENDING" and self._items:
            print(f"[GC] Order #{self._order_id} discarded while pending -> releasing stock")
            self.cancel()

    def __str__(self) -> str:
        lines = [f"Order #{self._order_id} for {self._customer.name} [{self._status}]"]
        for item, qty in self._items:
            lines.append(f"  {qty} x {item.get_description():<18} {self._format_money(item.get_price() * qty):>9}")
        lines.append(f"  Subtotal {self._format_money(self.subtotal()):>22}")
        lines.append(f"  Total    {self._format_money(self.total_cost()):>22}")
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 5. DEMO                                                                     #
# --------------------------------------------------------------------------- #
def main() -> None:
    laptop = Product(1, "Laptop", 999.00, stock=5)
    mouse = Product(2, "Mouse", 25.00, stock=50)
    card = GiftCard(50.00)

    alice = Customer(1, "Alice", "alice@example.com")
    bob = PremiumCustomer(2, "Bob", "bob@example.com", member_since=2019)

    # -- Polymorphism: same call, different behaviour per subclass ---------- #
    print("--- Polymorphism: calculate_discount(1000) ---")
    for customer in (alice, bob):
        print(f"{customer!s:45} discount = {customer.calculate_discount(1000):.2f}")

    # -- ADT + class method + interface ----------------------------------- #
    print("\n--- ShoppingCart -> Order.from_cart ---")
    cart = ShoppingCart()
    cart.add(laptop, 1)
    cart.add(mouse, 2)
    cart.add(card)
    order = Order.from_cart(bob, cart)
    order.confirm()
    print(order)
    print(f"Laptop stock after order: {laptop.stock}")

    # -- Encapsulation: invalid state is rejected ------------------------ #
    print("\n--- Data integrity ---")
    try:
        laptop.price = -1
    except ValueError as err:
        print(f"Rejected: {err}")
    try:
        Order(alice).add_item(laptop, 10)
    except ValueError as err:
        print(f"Rejected: {err}")

    # -- Destructor safety net ------------------------------------------ #
    print("\n--- Destructor ---")
    pending = Order(alice)
    pending.add_item(mouse, 3)
    print(f"Mouse stock while pending: {mouse.stock}")
    del pending                       # CPython frees it immediately -> __del__
    print(f"Mouse stock after GC:     {mouse.stock}")

    print(f"\nOrders created in total: {Order.orders_created()}")
    try:
        User(0, "x", "x@x.com")      # abstract class cannot be instantiated
    except TypeError as err:
        print(f"Abstract: {err}")


if __name__ == "__main__":
    main()
