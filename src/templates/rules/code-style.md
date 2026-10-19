# code-style

Property and Method Naming:
public properties and methods - only those called from the outside
_protected properties and methods - only those called within subclasses
__private properties and methods - those called strictly inside the class
method names - verbs that describe the performed action; noun naming is allowed only for properties

Class Method Ordering:
Arrange methods in a class according to Robert Martin's principles: "like a story", where called methods are placed directly below the method that invokes them

Static Methods:
Mark a method with @staticmethod when it does not access self or cls, is not overridden in parent or child classes, and is not wrapped in a decorator

Procedure and Function Naming:
Using standalone functions named with a leading underscore (e.g., _something) is prohibited
You must either use shared utilities in src/utils or implement a proper class method
Procedures and functions must strictly be public, and used only when instantiating a class for that functionality is clearly redundant

Constants:
Do not declare a module-level constant if it belongs to the scope of a single class — keep it inside the class instead (following public/_protected/__private rules)
Do not declare a constant if it is used in exactly one method (procedure/function) — a well-named local variable or named argument is sufficient

Comments:
Aim to avoid comments in code entirely — rely on self-documenting, expressive naming instead
Add a comment only in two specific scenarios:
- It is strictly required by the framework
- It explains WHY something was done a certain way, and achieving that clarity through code alone is impossible

Method Body:
Do not write one-line methods - expand them into several readable statements
Keep a single entry point and a single exit point in a method (function); use well-named variables for intermediate results
Use early returns only when they significantly improve readability and cannot be avoided
Assign the result to a variable before returning from a method (function) - it simplifies debugging
