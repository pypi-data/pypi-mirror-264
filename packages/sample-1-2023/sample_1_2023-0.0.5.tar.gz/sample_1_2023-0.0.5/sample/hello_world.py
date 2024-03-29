import pandas as pd


class HelloWorld:
    def __init__(self) -> None:
        pass

    def say_hello(self):
        data = {
            'Name': ['John', 'Alice', 'Bob'],
            'Age': [30, 25, 35],
            'Salary': [50000.50, 60000.75, 70000.80]
        }

        df = pd.DataFrame(data)

        pd.set_option('display.float_format', '${:,.2f}'.format)
        print(df)

        return "Hello World!!!"


HelloWorld().say_hello()
