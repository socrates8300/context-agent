from pathlib import Path
from typing import Dict, List
from trae_agent.utils.cli_console import CLIConsole

class ContextGatherer:
    def __init__(self, cli_console: CLIConsole | None = None):
        self.cli_console = cli_console

    def gather_context_from_files(self, file_paths: List[str]) -> Dict[str, str]:
        context = {}
        for file_path_str in file_paths:
            file_path = Path(file_path_str)
            if file_path.is_absolute():
                absolute_path = file_path
            else:
                # Assuming paths are relative to the project root for now
                # This needs to be more robust in a real scenario, perhaps by passing project_root
                absolute_path = Path.cwd() / file_path

            if absolute_path.exists() and absolute_path.is_file():
                try:
                    content = absolute_path.read_text()
                    context[str(absolute_path)] = content
                except Exception as e:
                    error_msg = f"Error reading file {absolute_path}: {e}"
                    context[str(absolute_path)] = error_msg
                    if self.cli_console:
                        self.cli_console.print_error(error_msg)
            else:
                error_msg = f"File not found or is a directory: {absolute_path}"
                context[str(absolute_path)] = error_msg
                if self.cli_console:
                    self.cli_console.print_warning(error_msg)
        return context

if __name__ == '__main__':
    # Example Usage (requires creating dummy files for testing)
    # Create some dummy files
    Path("test_file1.txt").write_text("Content of test file 1.")
    Path("test_file2.txt").write_text("Content of test file 2.")
    Path("non_existent_file.txt").unlink(missing_ok=True)

    # Dummy CLIConsole for testing
    class DummyCLIConsole:
        def print_error(self, message: str, bold: bool = False): print(f"ERROR: {message}")
        def print_warning(self, message: str, bold: bool = False): print(f"WARNING: {message}")

    gatherer = ContextGatherer(DummyCLIConsole())
    files_to_read = [
        "test_file1.txt",
        "/Volumes/Everything/Development/context-agent/test_file2.txt", # Absolute path example
        "non_existent_file.txt"
    ]

    gathered_context = gatherer.gather_context_from_files(files_to_read)

    import json
    print(json.dumps(gathered_context, indent=2))

    # Clean up dummy files
    Path("test_file1.txt").unlink()
    Path("test_file2.txt").unlink()
