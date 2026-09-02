# Vodcast script - Online Shopping System

Speaker notes per slide (also embedded in the .pptx as notes). Target: 5-10 minutes total.


## Slide 1 (97 words)

Good morning. This presentation walks through the design of a small Online Shopping System in Python that manages products, customers and orders. It was built to show core object-oriented principles in practice. I will move through the concepts in the order they build on each other - classes and objects, the object life-cycle, inheritance and polymorphism, abstraction, encapsulation and abstract data types - and on each slide I point out one design decision and its trade-off. I finish with a critical evaluation. The full source file is submitted with the slides and every snippet comes from it.


## Slide 2 (116 words)

Three classes mirror the three nouns in the brief: Product, Customer and Order. A class is only a blueprint; the last three lines create real objects, each with its own state, so two Products can hold different stock while sharing behaviour. The key decision is that an Order does not copy product data. It holds references to Product objects plus a quantity, which gives a single source of truth: a price change is visible to every pending order, and stock is decremented on the real object. The trade-off is coupling - the Order depends on the Product instance staying alive, which is fine in memory but would become an ID reference once a database is introduced.


## Slide 3 (120 words)

Constructors and destructors bracket an object's life. The constructor __init__ validates every argument before storing it, so a Product can never exist with a negative price or stock - the first line of defence for data integrity. The destructor __del__ runs when the garbage collector frees the object; in Order it releases reserved stock if the order was abandoned while pending, and the output shows the mouse stock going back up. Critically, this is a safety net, not the design. CPython frees most objects immediately by reference counting, but objects in a cycle wait for the cyclic collector, so timing is not guaranteed. That is why Order has an explicit cancel() method, which is what production code should rely on.


## Slide 4 (130 words)

Two kinds of state live in Order. Instance variables such as the item list and status are unique to each order. The class variable _next_id is shared by the whole class and incremented in the constructor, giving every order a unique ID without an external counter. from_cart is a @classmethod: it receives the class, not an instance, and acts as an alternative constructor that builds an Order from a ShoppingCart. add_item calls reserve first and only appends the line if that succeeds, so asking for more stock than exists leaves the order unchanged. total_cost asks the customer object for its discount instead of checking its type - the hook for polymorphism on slide 6. Trade-off: stock is committed at add time, so a real shop would add a reservation timeout.


## Slide 5 (119 words)

Inheritance models an is-a relationship. The diagram shows the chain: User is abstract, Customer is the concrete buyer, PremiumCustomer specialises Customer. In the code PremiumCustomer calls super().__init__, so e-mail validation and the order list come from the parents; the subclass only adds the membership year and a discount rate. Because it keeps the parent's interface, an Order can hold either type without knowing which. I chose inheritance because a premium customer really is a customer in every respect except pricing. My evaluation is that this stops scaling if pricing rules multiply, since every tier becomes a subclass. The alternative is the Strategy pattern, where the discount rule is a separate object - I return to that in the conclusion.


## Slide 6 (129 words)

PremiumCustomer overrides two inherited methods: get_role and calculate_discount. The override keeps the same signature but changes behaviour - ten percent off plus a loyalty bonus after five years. Polymorphism is what makes this useful: the loop calls the same method on two objects and gets two results, Alice with no discount and Bob with 150. More importantly, Order calls calculate_discount through the base type and never checks which subclass it has, so a new customer tier is one new class and no changes elsewhere - the open/closed principle in practice. One limitation: Python resolves the override at run time and has no override keyword, so a typo would silently create a new method. In Java the compiler would flag it; here I rely on tests or a type checker.


## Slide 7 (123 words)

Abstraction separates what an object does from how. User is an abstract base class: it holds the identity fields and the shared __str__ but marks get_role as abstract, so a bare User cannot be instantiated - the demo raises a TypeError. Orderable plays the role of an interface. Python has no interface keyword, so an ABC containing only abstract methods is the idiomatic equivalent: three methods any item in an order must provide. The diagram shows two implementations, Product with stock and GiftCard without, and Order can hold either. The modern alternative is typing.Protocol, which defines the contract structurally. I chose the ABC because the failure is immediate and loud; for a library consumed by third parties the Protocol would be less intrusive.


## Slide 8 (126 words)

Python has no public, protected or private keywords; it uses the naming conventions in the table. A single underscore marks an attribute as internal; a double underscore triggers name mangling, so __product_id is stored as _Product__product_id and cannot be reached by accident. In the code, price is a protected attribute exposed through a property: reading is free, but writing goes through a setter that rejects negative values, and the output shows both the rejected write and the mangled attribute. The honest evaluation is that none of this is enforced by the compiler; a determined caller can still reach the mangled name. What the conventions give you is protection from mistakes, so data integrity rests on the properties - every state change passes through one validated path.


## Slide 9 (120 words)

Encapsulation and information hiding are related but distinct. Encapsulation means data and its operations are bundled in one class: ShoppingCart keeps the dictionary of lines and the rule that quantities must be positive together, so they cannot drift apart. Information hiding is about what callers may depend on. Nothing outside ShoppingCart knows it uses a dictionary; it could switch to a list or a database table and Order.from_cart would not change, because it only calls lines(). Customer.orders follows the same idea by returning a tuple, so nobody can append to the history from outside. The cost is a copy on every read - negligible for a cart, but for thousands of orders I would use a read-only proxy or paginate.


## Slide 10 (128 words)

This is the full class diagram: the inheritance chain on the left, the Orderable interface at the top with its two implementations, and Order and ShoppingCart at the bottom holding items through that interface. ShoppingCart is the abstract data type. An ADT is specified by what you can do with it - add, remove, list, check emptiness, clear - and how those operations behave together, not by how data is stored. That is exactly what lets the representation change. Orderable is what makes the design flexible: because Order only calls get_price, get_description and reserve, a gift card without stock and a physical product go through identical code. The reuse test is simple - adding a new item type or customer tier means one new class and nothing else.


## Slide 11 (137 words)

To recap: each pillar solved a concrete requirement. Classes and objects gave a domain model whose constructors make invalid state impossible. Inheritance and polymorphism let a premium customer change pricing without touching Order. Encapsulation, through validated properties and a hidden cart representation, delivers the data integrity the brief asks for. Abstraction, through User and Orderable, keeps the design open to future enhancements. Evaluating honestly: the strengths are correctness and extensibility. The limitations are real - float is the wrong type for money and should be Decimal; stock release relies on cancellation or garbage collection; and everything lives in memory. To scale it I would introduce the Strategy pattern for discounts, dataclasses to cut boilerplate, and a repository layer over a database with reservation timeouts. The abstractions chosen now are what make those changes local rather than system-wide.


## Slide 12 (41 words)

That concludes the presentation. Questions I have prepared for: why an ABC rather than a Protocol for Orderable, why stock is reserved at add time rather than checkout, and how discounts would move to a Strategy object. Thank you for listening.


## Slide 13 (21 words)

Sources for the concepts and language features, in Harvard format. The code is original; only the documented language mechanisms are cited.


---
Total: 1407 words - about 9.4 min at 150 wpm, 10.8 min at 130 wpm.
