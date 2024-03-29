import os
import typing as t
from .command import Command
from . import input_utils

class ClearStdOut(Command):
    description = "CLEAR"
    def command(self):
        os.system("clear")

    def post_execution(self, results):
        pass

class ExitCommandCenter(Command):
    description = "EXIT"
    def command(self):
        raise KeyboardInterrupt

class CommandCenter:
    def __init__(self, commands: t.List[t.Type[Command]]):
        if not commands:
            raise ValueError("Need a list of commands")

        self.commands = commands

    def run(self):
        """
        Runs command center loop
        """
        commands: t.List[Command] = [c() for c in self.commands + [ClearStdOut, ExitCommandCenter]] 
        try:
            while True:
                command = input_utils.get_select_input(
                    question="What would you like to do?",
                    options=commands,
                    option_formatter=lambda command: command.description
                )
                command.execute()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print("Encountered exception while running command:")
            print(e)
        finally:
            print("Exiting command center...")