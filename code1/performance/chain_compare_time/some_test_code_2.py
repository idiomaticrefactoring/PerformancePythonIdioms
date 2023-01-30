class Independencies(object):
    """
    Base class for independencies.
    independencies class represents a set of Conditional Independence
    assertions (eg: "X is independent of Y given Z" where X, Y and Z
    are random variables) or Independence assertions (eg: "X is
    independent of Y" where X and Y are random variables).
    Initialize the independencies Class with Conditional Independence
    assertions or Independence assertions.
    Parameters
    ----------
    assertions: Lists or Tuples
            Each assertion is a list or tuple of the form: [event1,
            event2 and event3]
            eg: assertion ['X', 'Y', 'Z'] would be X is independent
            of Y given Z.
    Examples
    --------
    Creating an independencies object with one independence assertion:
    Random Variable X is independent of Y
    >>> independencies = independencies(['X', 'Y'])
    Creating an independencies object with three conditional
    independence assertions:
    First assertion is Random Variable X is independent of Y given Z.
    >>> independencies = independencies(['X', 'Y', 'Z'],
    ...             ['a', ['b', 'c'], 'd'],
    ...             ['l', ['m', 'n'], 'o'])
    Public Methods
    --------------
    add_assertions
    get_assertions
    get_factorized_product
    closure
    entails
    is_equivalent
    """

    def __init__(self, *assertions):
        self.independencies = []
        self.add_assertions(*assertions)

    def __str__(self):
        string = "\n".join([str(assertion) for assertion in self.independencies])
        return string

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Independencies):
            return False
        return all(
            independency in other.get_assertions()
            for independency in self.get_assertions()
        ) and all(
            independency in self.get_assertions()
            for independency in other.get_assertions()
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def contains(self, assertion):
        """
        Returns `True` if `assertion` is contained in this `Independencies`-object,
        otherwise `False`.
        Parameters
        ----------
        assertion: IndependenceAssertion()-object
        Examples
        --------
        >>> from pgmpy.independencies import Independencies, IndependenceAssertion
        >>> ind = Independencies(['A', 'B', ['C', 'D']])
        >>> IndependenceAssertion('A', 'B', ['C', 'D']) in ind
        True
        >>> # does not depend on variable order:
        >>> IndependenceAssertion('B', 'A', ['D', 'C']) in ind
        True
        >>> # but does not check entailment:
        >>> IndependenceAssertion('X', 'Y', 'Z') in Independencies(['X', 'Y'])
        False
        """
        if not isinstance(assertion, IndependenceAssertion):
            raise TypeError(
                f"' in <Independencies()>' requires IndependenceAssertion as left operand, not {type(assertion)}"
            )

        return assertion in self.get_assertions()

    __contains__ = contains

    def get_all_variables(self):
        """
        Returns a set of all the variables in all the independence assertions.
        """
        return frozenset().union(*[ind.all_vars for ind in self.independencies])

    def get_assertions(self):
        """
        Returns the independencies object which is a set of IndependenceAssertion objects.
        Examples
        --------
        >>> from pgmpy.independencies import Independencies
        >>> independencies = Independencies(['X', 'Y', 'Z'])
        >>> independencies.get_assertions()
        """
        return self.independencies

    def add_assertions(self, *assertions):
        """
        Adds assertions to independencies.
        Parameters
        ----------
        assertions: Lists or Tuples
                Each assertion is a list or tuple of variable, independent_of and given.
        Examples
        --------
        >>> from pgmpy.independencies import Independencies
        >>> independencies = Independencies()
        >>> independencies.add_assertions(['X', 'Y', 'Z'])
        >>> independencies.add_assertions(['a', ['b', 'c'], 'd'])
        """
        for assertion in assertions:
            if isinstance(assertion, IndependenceAssertion):
                self.independencies.append(assertion)
            else:
                try:
                    self.independencies.append(
                        IndependenceAssertion(assertion[0], assertion[1], assertion[2])
                    )
                except IndexError:
                    self.independencies.append(
                        IndependenceAssertion(assertion[0], assertion[1])
                    )

    def closure(self):
        """
        Returns a new `Independencies()`-object that additionally contains those `IndependenceAssertions`
        that are implied by the the current independencies (using with the `semi-graphoid axioms
        <https://en.wikipedia.org/w/index.php?title=Conditional_independence&oldid=708760689#Rules_of_conditional_independence>`_;
        see (Pearl, 1989, `Conditional Independence and its representations
        <http://www.cs.technion.ac.il/~dang/journal_papers/pearl1989conditional.pdf>`_)).
        Might be very slow if more than six variables are involved.
        Examples
        --------
        >>> from pgmpy.independencies import Independencies
        >>> ind1 = Independencies(('A', ['B', 'C'], 'D'))
        >>> ind1.closure()
        (A \u27C2 B | D, C)
        (A \u27C2 B, C | D)
        (A \u27C2 B | D)
        (A \u27C2 C | D, B)
        (A \u27C2 C | D)
        >>> ind2 = Independencies(('W', ['X', 'Y', 'Z']))
        >>> ind2.closure()
        (W \u27C2 Y)
        (W \u27C2 Y | X)
        (W \u27C2 Z | Y)
        (W \u27C2 Z, X, Y)
        (W \u27C2 Z)
        (W \u27C2 Z, X)
        (W \u27C2 X, Y)
        (W \u27C2 Z | X)
        (W \u27C2 Z, Y | X)
        [..]
        """

        def single_var(var):
            "Checks if var represents a single variable"
            if not hasattr(var, "__iter__"):
                return True
            else:
                return len(var) == 1