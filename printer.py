import pandas as pd
from typing import Union

class Printer:
    def printer(self, message: Union[str, list, dict], output_type: str = "plain") -> None:
            """
            Print messages in different formats.
            
            Args:
                message: The message/data to print
                output_type: Format type ("plain", "table", "json", "info", "warning", "error")
            """
            types = {
                "plain": lambda msg: print(msg),
                "table": lambda msg: print(pd.DataFrame(msg) if isinstance(msg, (list, dict)) else msg),
                "json": lambda msg: print(pd.DataFrame(msg).to_json(indent=2) if isinstance(msg, (list, dict)) else msg),
                "info": lambda msg: print(f"{msg}"),
                "warning": lambda msg: print(f"\033[93m[WARNING] {msg}\033[0m"),
                "error": lambda msg: print(f"\033[91m[ERROR] {msg}\033[0m")
            }
            
            if output_type in types:
                types[output_type](message)
            else:
                print(f"Unknown format '{output_type}'. Using plain format.")
                print(message)