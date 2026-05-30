# ITDR_ISPM-Engine

This is a prototype for Identity threat detection and security posture management engine. It takes uncompressed messy cloud trail log streams, then normalizes it and uses deterministic logic filters to reduce token usage, then it prepares structured LLM reasoning layers to instantly output validated, least-privilege remediation configs.

## Core Architecture

The platform is explicitly divided into independent files to preserve strict data contracts so it can support further scaling and prevent code dependencies:

### File Definitions
* **`models.py`**: It defines a rigorous system schema using **Pydantic V2**. It defines a strict structural output contract (`ComprehensiveAuditReport`) so that the LLM's payload works well with deterministic backend Python objects.
* **`data_generator.py`**: It acts as the data abstraction layer. It establishes corporate access profiles which provides static granted permissions with 90-day activity histories to mock real-world AWS infrastructure footprints.
* **`normalizer.py`**: It is the local preprocessing pipeline. It processes the complex, multi-structured cloud audit logs and clears out the unwanted information (noise) locally before sending it to the API for further processing. 
* **`auditor.py`**: It is the orchestration core. It performs initial deterministic structural checks, sets the required execution steps and validates using the `google-genai` SDK with `gemini-2.5-flash`.
* **`app.py`**: A low-latency dashboard made with Streamlit, it has an interactive file-uploading feature with other required system metrics.

Directly sending raw logging files to the LLM model can cause context window exhaustion and would increase the token usage that would inflate the API cost. The processing pipeline inside `normalizer.py` resolves this by executing structured filtering locally, which reduces the footprints by up to 80% while getting all the required critical threat signals.

LLM's genrally output texts with conversational fillers which are of no use to us, to avoid this we used `model_validate_json()` to structure the output by binding Pydantic validations directly to the core inference layer, which ensures 100% reliable system outputs. 

---

## Further Advancements 

### 1. Semantic Log Embedding Filters (RAG)
Currently, the deterministic filter checks for exact strings like AWS_AdministratorAccess etc. But in general the permission tags are custom and unique for every enterprise. For solving this, we can build a RAG vector scanner, which performs a sililarity checkup before directly sending it to gemini with all unknown tags. Which ultimately would save a lot of computation and execution expenses. 

### 2. Using Boto3 to get live cloud trails directly 
To get it production ready, instead of working with a harcoded list from data-generator.py we would like to get into the enterprise's live AWS control panel to get the library logs directly. We can do it by using an official library boto3, built by Amazon. 

---

## Local Setup

### Prerequisites
* Python 3.10 or higher
* A valid Gemini API Key
* Install libraries: google-genai streamlit pydantic dotenv pandas 
