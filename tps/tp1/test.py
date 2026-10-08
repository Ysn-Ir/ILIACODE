"""Verify ML/AI library installations. Run: python check_install.py"""
import importlib
import importlib.metadata as md
import sys

# (import name, pip name)
GROUPS = {
    "Core": [
        ("numpy", "numpy"), ("pandas", "pandas"), ("matplotlib", "matplotlib"),
        ("scipy", "scipy"), ("sklearn", "scikit-learn"), ("xgboost", "xgboost"),
        ("lightgbm", "lightgbm"), ("catboost", "catboost"), ("seaborn", "seaborn"),
    ],
    "Deep learning": [
        ("torch", "torch"), ("torchvision", "torchvision"), ("torchaudio", "torchaudio"),
        ("tensorflow", "tensorflow"), ("keras", "keras"),
    ],
    "RL": [
        ("gymnasium", "gymnasium"), ("stable_baselines3", "stable-baselines3"),
    ],
    "NLP": [
        ("nltk", "nltk"), ("spacy", "spacy"), ("gensim", "gensim"),
        ("sentencepiece", "sentencepiece"), ("tokenizers", "tokenizers"),
    ],
    "LLM / Hugging Face": [
        ("transformers", "transformers"), ("datasets", "datasets"),
        ("accelerate", "accelerate"), ("huggingface_hub", "huggingface_hub"),
        ("safetensors", "safetensors"), ("evaluate", "evaluate"),
    ],
    "Fine-tuning / quantization": [
        ("peft", "peft"), ("trl", "trl"), ("bitsandbytes", "bitsandbytes"),
        ("optimum", "optimum"), ("llama_cpp", "llama-cpp-python"),
        ("onnx", "onnx"), ("onnxruntime", "onnxruntime"),
    ],
    "RAG / vector DBs": [
        ("langchain", "langchain"), ("llama_index", "llama-index"),
        ("sentence_transformers", "sentence-transformers"), ("faiss", "faiss-cpu"),
        ("chromadb", "chromadb"), ("qdrant_client", "qdrant-client"),
    ],
    "Agents / APIs": [
        ("langgraph", "langgraph"), ("crewai", "crewai"), ("openai", "openai"),
        ("anthropic", "anthropic"), ("pydantic", "pydantic"), ("mcp", "mcp"),
    ],
    "Web / serving": [
        ("requests", "requests"), ("httpx", "httpx"), ("bs4", "beautifulsoup4"),
        ("playwright", "playwright"), ("selenium", "selenium"),
        ("fastapi", "fastapi"), ("uvicorn", "uvicorn"),
        ("gradio", "gradio"), ("streamlit", "streamlit"),
    ],
    "Tooling": [
        ("jupyterlab", "jupyterlab"), ("wandb", "wandb"), ("mlflow", "mlflow"),
        ("dotenv", "python-dotenv"), ("tqdm", "tqdm"), ("rich", "rich"),
    ],
}


def version_of(import_name, pip_name):
    try:
        return md.version(pip_name)
    except Exception:
        mod = sys.modules.get(import_name)
        return getattr(mod, "__version__", "?")


def main():
    print(f"Python {sys.version.split()[0]} at {sys.executable}\n")
    ok, missing, broken = [], [], []

    for group, libs in GROUPS.items():
        print(f"== {group} ==")
        for imp, pip_name in libs:
            try:
                importlib.import_module(imp)
                v = version_of(imp, pip_name)
                print(f"  [OK]      {pip_name:<24} {v}")
                ok.append(pip_name)
            except ModuleNotFoundError:
                print(f"  [MISSING] {pip_name}")
                missing.append(pip_name)
            except Exception as e:  # installed but fails to import
                print(f"  [BROKEN]  {pip_name:<24} {type(e).__name__}: {str(e)[:70]}")
                broken.append(pip_name)
        print()

    print("== GPU checks ==")
    try:
        import torch
        print(f"  PyTorch {torch.__version__} | CUDA build: {torch.version.cuda} "
              f"| GPU available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"  PyTorch: not usable ({type(e).__name__})")
    try:
        import tensorflow as tf
        print(f"  TensorFlow GPUs: {tf.config.list_physical_devices('GPU')}")
    except Exception as e:
        print(f"  TensorFlow: not usable ({type(e).__name__})")

    print("\n== Quick functional test ==")
    try:
        import torch
        x = torch.randn(3, 3)
        lstm = torch.nn.LSTM(4, 8, batch_first=True)
        out, _ = lstm(torch.randn(2, 5, 4))
        print(f"  PyTorch LSTM output shape: {tuple(out.shape)}  (expected (2, 5, 8))")
    except Exception as e:
        print(f"  PyTorch test failed: {e}")
    try:
        import gymnasium as gym
        env = gym.make("CartPole-v1")
        obs, _ = env.reset()
        print(f"  Gymnasium CartPole obs shape: {obs.shape}")
    except Exception as e:
        print(f"  Gymnasium test failed: {e}")
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("  spaCy model en_core_web_sm: loaded")
    except Exception:
        print("  spaCy model missing -> run: python -m spacy download en_core_web_sm")

    print(f"\nSummary: {len(ok)} OK, {len(missing)} missing, {len(broken)} broken")
    if missing:
        print("Missing:", ", ".join(missing))
    if broken:
        print("Broken (installed, import fails):", ", ".join(broken))


if __name__ == "__main__":
    main()