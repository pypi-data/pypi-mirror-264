import traceback
from pathlib import Path
from typing import Generator, Dict

from ._get_modules import _get_modules
from ._re_import import _re_import_modules


class DynamicModeExecutor:
    """A main component of dynamic execution loop.
    Creates executor file with access to local and global variables where code can be safely executed.

    for error in DynamicModeExecutor().execute(locals(), globals()):
        pass

    With each iteration modules are reloaded and the changes applied to DynamicClass instances.
    """

    def __init__(
        self,
        executor_path: Path = Path("executor.py"),
        finish_upon_success: bool = True,
        supress_print: bool = False,
    ):
        """

        :param executor_path: A path to an executor file, defaults to executor.py file parented by cwd.
        :param finish_upon_success:
            Specifies if there should be any iterations after a successful execution.
            Defaults to True if False works as an infinite loop.
        :param supress_print:
            Manages exception printing.
            If True exception is printed as if it occurred during an uncontrolled runtime.
            Exception is always yielded by loop not matter the argument.
        """
        self.executor_path = executor_path
        self.finish_upon_success = finish_upon_success
        self.supress_print = supress_print

    def execute(
        self,
        local_vars: Dict,
        global_vars: Dict,
        executor_path: Path = None,
        finish_upon_success: bool = None,
        supress_print: bool = None,
    ) -> Generator[str, None, None]:
        """Method used to override class parameters and accept local and global parameters.

        :param local_vars: local variables that can be a subject to change usually locals().
        :param global_vars: global variables that can be a subject to change usually global().
        :param executor_path: A path to an executor file, defaults to one in self.
        :param finish_upon_success:
            Specifies if there should be any iterations after a successful execution.
            Defaults to a value in self.
        :param supress_print:
            Manages exception printing.
            If True exception is printed as if it occurred during an uncontrolled runtime.
            Exception is always yielded by loop not matter the argument.
        :return: Error message if one occurred during execution. None otherwise.
        """
        if executor_path is None:
            executor_path = self.executor_path
        if supress_print is None:
            supress_print = self.supress_print
        if finish_upon_success is None:
            finish_upon_success = self.finish_upon_success

        if not executor_path.exists():
            executor_path.write_text("# Save mode executor")
            yield f"Created an executor file in {executor_path.absolute()}"
        done = False
        while True:
            try:
                compiled = compile(
                    executor_path.read_text(), executor_path.name, "exec"
                )
                exec(compiled, global_vars, local_vars)
                done = True
            except:
                if not supress_print:
                    traceback.print_exc()
                yield traceback.format_exc()
            if not finish_upon_success or not done:
                modules = _get_modules()
                _re_import_modules(modules, local_vars, global_vars)
                if done:
                    yield
            else:
                return
