# Llama GGUF Env Setup

## Prerequisites
1. Install Visual C++ Build Tools at: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Check the box for "Desktop development with C++" - this is the main one you need
3. **Restart your terminal/command prompt after installation**

## Environment Setup
1. Create and activate conda environment (or env manager of your choice):
```bash
conda create -n local_llama python=3.11
conda activate local_llama
```

2. Install OpenBLAS via conda:
```bash
conda install -c conda-forge openblas
```

3. Build llama-cpp-python with optimizations:
```bash
set CMAKE_ARGS=-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS -DBLAS_LIBRARIES="%CONDA_PREFIX%\Library\lib\openblas.lib" -DBLAS_INCLUDE_DIRS="%CONDA_PREFIX%\Library\include\openblas"

pip install llama-cpp-python
```

4. Install other requirements:
```bash
pip install -r requirements.txt
```

## Verify Installation
```bash
python -c "from llama_cpp import Llama; print('✅ Success!')"
```

## Testing Transformers - SmolLM3 Integration

The `testing_transformers.ipynb` notebook demonstrates how to:

### Features
- **Load SmolLM3-3B model** using HuggingFace Transformers
- **Create custom LangChain wrapper** (`SmolLM3LLM`) for seamless integration
- **Basic chat functionality** with conversation memory
- **Structured output** using Pydantic models and JSON parsing
- **GPU acceleration** with CUDA support

### Model Details
- **Model**: `HuggingFaceTB/SmolLM3-3B`
- **Size**: 3B parameters
- **Local caching**: Models downloaded to `./models/SmolLM3-3B-transformers/`
- **Device**: Automatically uses CUDA if available, falls back to CPU

### Key Components

#### Custom LangChain Chat Model
The notebook implements `SmolLM3LLM` class that:
- Extends LangChain's `BaseChatModel`
- Supports conversation history
- Provides token counting and timing metadata
- Handles structured output parsing

#### Structured Output Example
```python
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(default=None, description="How funny the joke is, from 1 to 10")

structured_llm = llm.with_structured_output(Joke)
response = structured_llm.invoke([HumanMessage(content="Tell me a joke")])
```