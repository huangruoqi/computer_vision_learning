import inspect

def debug(*variables):
    if variables:
        frame = inspect.currentframe().f_back
        calling_globals = frame.f_globals
        calling_locals = frame.f_locals

        arg_names = []
        for arg in variables:
            arg_name = None
            for name, var_value in calling_globals.items():
                if var_value is arg and name not in arg_names:
                    arg_name = name
                    break
            for name, var_value in calling_locals.items():
                if var_value is arg and name not in arg_names:
                    arg_name = name
                    break
            arg_names.append(arg_name)

        for i, (arg_name, arg_value) in enumerate(zip(arg_names, variables)):
            print(f"<{arg_name}>: {arg_value}")

    user_input = "_"
    while len(user_input.strip())>0:
        try:
            user_input = input(">>> ")
            try:
                result = eval(user_input)
                if result is not None:
                    print(result)
            except SyntaxError:
                exec(user_input)
        except Exception as e:
            print(f"Error: {e}")
