# package: TimeMyCode

The goal of this package is to time the execution of differents parts of a Python code.

## 1. Initiate the global timer
The package **TimeMyCode** depends of the built-in packages **contextlib** and **time**.

The design of the class **TimeMyCode** is based on the Singleton pattern.
So all new instance inside the code refer finally to the same object. 

Just need to import the package:

```
> from timemycode import TimeMyCode as TMC
```

To use it, just call the class to get the object:

```
> with TMC().tag("test 1"):
>    ...
```

## 2. Use the global timer in your code
As this package uses a context manager, we have to use it with the statement "with".
To time a new part of code, we have to use a new tag.

```
> with TMC().tag("This is my new tag"):
>     ...
```

The same tag could be use in different parts inside your code.

## 3. Print the time log
At the end of the process you want to time, you could display the global time log by calling the method **summary()**.

**Note**: the method **summary()** reinitiate the timer.

```
> print(TMC().summary())

Time log:
  - This is my new tag ....... 6.01s ->  1 it [6.0100 s/it]

Total time: 6.02s
```

Details:
- the tag name
- the total execution time for this tag
- the number of iterations (number of calls of this tag)
- the time per iteration


## 4. Example with a For loop

```
> for i in range(5):
>     with TMC().tag('for 1'):
>         sleep(0.5)
> 
>         for i in range(15):
>             with TMC().tag('  for 2'):
>                 sleep(0.1)
> 
> print(TMC().summary())

Time log:
  - for 1 ..... 10.02s ->  5 it [2.0034 s/it]
  -   for 2 ...  7.51s -> 75 it [0.1002 s/it]

Total time: 10.02s
```