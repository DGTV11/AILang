import AILang

def shell(strict_mode=True):
    print(f'Official AILang Shell (Python Implementation) ({"" if not strict_mode else "strict mode"})')
    while True:
        text = input('SHELL > ')
        if text.strip() == '': continue
        result, error = AILang.run('<stdin>', text, is_strict=strict_mode)

        if error: print(error.as_str())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))