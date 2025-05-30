import argparse
from bpj.llama_executor import LLaMAExecutor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument(
        "--exe",
        type=str,
        default="E:/test-llama/llama.cpp/build/bin/Release/llama-run.exe",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="E:/test-llama/llama.cpp/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    )
    args = parser.parse_args()

    executor = LLaMAExecutor(args.exe, args.model)
    print(executor.infer(args.prompt))


if __name__ == "__main__":
    main()
