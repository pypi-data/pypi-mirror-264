# Module for colorful printing and error handling.

## pip install exceptdrucker

### Tested against Windows 10 / Python 3.11 / Anaconda


```PY
    Module for colorful printing and error handling.
    Handle and display errors in a customizable format.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
            debug (bool): Indicates whether debugging is enabled. Defaults to True.
            symbol_top (str): Symbol to print at the top of the error message. Defaults to "╦".
            symbol_bottom (str): Symbol to print at the bottom of the error message. Defaults to "╩".
            len_top (str): Length of the top symbol line. Defaults to "60".
            len_bottom (str): Length of the bottom symbol line. Defaults to "60".
            color_top (str): Color of the top symbol line. Defaults to "YELLOW_DARK".
            color_bottom (str): Color of the bottom symbol line. Defaults to "RED_DARK".
            print_to_stderr (bool): Whether to print to stderr. Defaults to False.
            color_exception (str): Color of the exception message. Defaults to "CYAN".

    Example:
        from exceptdrucker import errwrite, config

        try:
            print("hello" / 2)
        except Exception:
            errwrite()

        try:
            print("hello" / 2)
        except Exception:
            errwrite(
                debug=True,
                symbol_top="V",
                symbol_bottom="A",
                len_top="40",
                len_bottom="40",
                color_top="YELLOW",
                color_bottom="RED",
                choosen_color="BLUE",
                print_to_stderr=False,
                color_exception="WHITE",
            )

        try:
            print("hello" / 2)
        except Exception:
            errwrite(
                debug=False,
            )

        config.debug = False
        try:
            print("hello" / 2)
        except Exception:
            print("nothing")
            errwrite()
```