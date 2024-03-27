from init_interp import run


def entry_shell():
    while True:
        text = input('>> ')
        if text.strip() == "": continue
        result, error = run('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            print(result)
            #if len(result.elements) == 1:
             #   print(repr(result.elements[0]))
           # else:
            #    print(repr(result))
