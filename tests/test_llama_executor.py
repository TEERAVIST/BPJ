import pytest
from bpj.llama_executor import LLaMAExecutor


def test_executable_not_found():
    with pytest.raises(FileNotFoundError):
        LLaMAExecutor("fake.exe", "model.gguf")


def test_model_not_found():
    with pytest.raises(FileNotFoundError):
        LLaMAExecutor(
            "E:/test-llama/llama.cpp/build/bin/Release/llama-run.exe", "bad_model.gguf"
        )
