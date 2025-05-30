import subprocess
from pathlib import Path


class LLaMAExecutor:
    def __init__(self, exe_path: str, model_path: str):
        self.exe = Path(exe_path)
        self.model = Path(model_path)
        if not self.exe.exists():
            raise FileNotFoundError(f"Executable not found: {self.exe}")
        if not self.model.exists():
            raise FileNotFoundError(f"Model not found: {self.model}")

    def infer(self, prompt: str, n_predict: int = 128) -> str:
        cmd = [str(self.exe), "-m", str(self.model), "-p", prompt, "-n", str(n_predict)]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Error running model: {result.stderr}")
        return result.stdout

    def tokenize(self, prompt: str) -> str:
        tokenizer = self.exe.parent / "llama-tokenize.exe"
        result = subprocess.run(
            [str(tokenizer), "-p", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
