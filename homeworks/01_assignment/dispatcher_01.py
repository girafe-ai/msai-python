# Write class Dispatcher with methods `register` and `get_registered_functions`
# which will store all functions decorated with method `register`


class Dispatcher:
    def register(self, func):
        """
        Register function using instance of `Dispatcher` class
        Different instances must have own registered functions scope
        Usage:
            dispatcher = Dispatcher()

            @dispatcher.register
            def func():
                return

        :param func: Decorated function
        """
        # WRITE CODE HERE
        return

    def get_registered_functions(self):
        """
        Displays list of all registered functions in order of registration
        :return: List of function  objects
        """
        # WRITE YOUR CODE HERE
        return
