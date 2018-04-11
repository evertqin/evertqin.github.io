---
title: A Guide to Python Decorator
date: 04/16/2015
tags: 
- Python
---

In this blog, I am going to walk you through python decorator, which will make your code more concise and more professional.

Lets start by creating the simplest possible decorator

<!--more-->

~~~~{python}
def simplest_decorator(func):
    print "Entering decorator: simplest_decorator"
    return func

@simplest_decorator
def no_arguments():
    print "processing function without arguments"

if __name__ == '__main__':
     no_arguments()
~~~~

The program above only does one thing: print a message before actually calling the function itself, this is similar to the following (but you will see the difference later):

~~~~{python}
wrapped_function = simplest_decorator(no_arguments)
wrapped_function()
# or like the following
simplest_decorator(no_arguments)()
# what about the following form? Why it does not work?
simplest_decorator(no_arguments())
~~~~

Ok, the example above is quite simple but it is useless since we are not really "decorating" the function passed in per se. We just returned it as is. So we need to do more:

~~~~{python}
def still_simple_decorator(func):
    print "Entering decorator: still_simple_decorator"

    def wrapper(*args, **kwargs):
        print 'Entering inner function wrapper'
        print args, kwargs
        func(*args, **kwargs)
        print 'Finished calling original function'

    return wrapper

@still_simple_decorator
def with_arguments(arg1, kwarg1):
    """
    Some document goes here
    """
    print "processing function with arguments"
~~~~

Now our decorator becomes a little bit more complicated but it is still not hard to figure out what it is doing. Instead of returning the original function as is, we create a inner function taking position and keyword arguments. 

Now we are more flexible, we can truly wrap our function inside. Think about the following use case: we need to time the run time of a function, this involves starting the timer at the top of the function then stop and calculate the time difference at the end of the function. With decorator, you can do it more elegantly without having to plug in code not related to the logic of the function itself

~~~~{python}
from time import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        print time() - start_time

    return wrapper

@time_it
def test_time_it():
    '''
    Okay! We are testing the time
    '''
    print 'something'

if __name__ == '__main__':
    test_time_it()
~~~~

THe above is useful, whenever we want to profile a function, the only thing we need to do is to decorate the function with @time_it decorator, and you will find the run time!

However, above still have a problem. Sometimes, we need to use function properties, such as `__name__` or `__doc__` if we do it on the wrapped function:

~~~~{python}
print test_time_it.__name__
print test_time_it.__doc__
~~~~

The print out is not what we expect, for name is should be `test_time_it` instead of `wrapper`! To solve this problem, we need to use another decorator for functools library, just decorate your wrapper with @wraps(func) like bellow

~~~~{python}
from functools import wraps

def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        print time() - start_time

    return wrapper
~~~~

Try the print we just did, it should work now.


Well, we have tried decorator on functions, and I bet you already know that decorator is merely a syntax sugar that helps you wrap your function object into another function. This another function can also take arguments like all other functions

~~~~{python}

from functools import wraps

def decorator_takes_arguments(*decorator_arguments):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print decorator_arguments
            return func(*args, **kwargs)

        return wrapper
    return decorator


@decorator_takes_arguments('something', 1)
def test_decorator_with_arguments():
    print "in test_decorator_with_arguements"
~~~~

This is a little bit more complicated, now our decorator becomes a function that takes arbitrary number of position arguments. To use these arguments, we create a closure. The function `decorator` and its inner function wrapper resemble our previous decorators: it takes the function as argument. Since everything is within the closure formed by `decorator_takes_arguments`, we can use its argument freely.

You can wrap as many level as you like but how about using a class as decorator, since decorator is only a function that takes function as argument.


~~~~{python}

from functools import wraps

class DecoratorClass(object):
    @classmethod
    def test(cls, func):
        print "in test"
        return func

    @classmethod
    def test_with_arguments(cls, *expected_args, **expected_kwargs):
        print 'in test_with_arguments', cls, expected_args, expected_kwargs

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwrags):
                print expected_args, expected_kwargs
                return func(*args, **kwrags)
            return wrapper

        return decorator

@DecoratorClass.test
def test_class_decorator():
    print "In test_class_decorator"

@DecoratorClass.test_with_arguments(0.1, length=4)
def test_class_decorator_with_arguments():
    print 'In test_class_decorator_with_arguments'

~~~~

Above is fancier, but the concept is the same. The beauty of using class to create decorator is that you can easily create a decorator library with nice structural syntax.

That's it for today, I will add more topic about decorator in the future
