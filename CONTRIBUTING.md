# Contributing to amazon-creators-async

Thank you for your interest in contributing! This project follows the same open-source model as `aliexpress-async-api`.

## 🛠 Prerequisites

1.  **Python 3.8+**
2.  **Amazon Associate & Creators API Credentials**: You need a `credential_id`, `credential_secret`, and `partner_tag` to run the live tests.

## 🚀 Setting Up Your Development Environment

1.  **Fork** the repository and clone your fork:
    ```bash
    git clone https://github.com/yourusername/amazon-creators-async.git
    cd amazon-creators-async
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies in editable mode**:
    ```bash
    pip install -e .
    ```

## 🧪 Testing

We use the provided `test_client.py` and `test_extra_endpoints.py` to validate API responses directly against Amazon's servers.

1.  Create a `.env` file in the root directory:
    ```ini
    AMAZON_CREDENTIAL_ID="amzn1.application-oa2-client..."
    AMAZON_CREDENTIAL_SECRET="amzn1.oa2-cs.v1..."
    AMAZON_PARTNER_TAG="yourtag-20"
    AMAZON_VERSION="3.1"
    ```
2.  Run the tests:
    ```bash
    python test_client.py
    python test_extra_endpoints.py
    ```
3.  Ensure your code doesn't produce `400 Invalid Request` or `429 TooManyRequests`.

## 📌 Coding Guidelines

*   **Asynchronous First**: All network operations must remain asynchronous using `httpx`.
*   **Pydantic Consistency**: Always map native Amazon `lowerCamelCase` responses to Pythonic `snake_case` using Pydantic `ConfigDict` and `alias_generator`. Do not leak `CamelCase` variables into the public Python signatures.
*   **Rate Limits**: Do not bypass or hardcode modifications to the `RateLimiter` unless introducing a documented generic feature (like supporting Amazon's tiered TPS).

## 📄 Pull Request Process

1.  Create a feature branch (`git checkout -b feature/awesome-new-feature`).
2.  Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
3.  Push your branch (`git push origin feature/awesome-new-feature`).
4.  Open a Pull Request on GitHub.
