# SDK Interface – CosmoEmbeddings

This document defines the structure and functionality of the core SDK for interacting with the CosmoEmbeddings network.

---

## 🔹 Purpose

The SDK enables developers and agents to:

- Generate and sign knowledge blocks.
- Validate blocks (including cosmic signature).
- Interact with other nodes via the sync protocol.
- Integrate easily into AI pipelines.

---

## 🔹 Core Modules

### 1. `BlockBuilder`

```python
BlockBuilder.create(
    input_data: Union[str, bytes],
    input_type: str,
    model: str,
    location: Tuple[float, float],
    timestamp: Optional[datetime] = None,
    tags: List[str] = [],
    linked_blocks: List[str] = []
) -> dict
```

- Generates embedding
- Computes input hash
- Collects astronomical data
- Returns complete, unsigned block (dict)

---

### 2. `Signer`

```python
Signer.sign_block(
    block: dict,
    private_key: str
) -> dict
```

- Signs block fields and adds `signature` field

---

### 3. `Validator`

```python
Validator.validate(
    block: dict,
    public_key: str
) -> bool
```

- Verifies:
  - Signature
  - Hash match
  - Timestamp format
  - Cosmo signature (via sky data lookup)

---

### 4. `SyncClient`

```python
SyncClient.push_block(block: dict) -> bool
SyncClient.get_block(block_id: str) -> dict
SyncClient.search_blocks(tag: str) -> List[dict]
```

- HTTP-based client to interact with other nodes

---

## 🔹 Configuration

- Support for `.env` file or config object:
  - `NODE_ID`
  - `PRIVATE_KEY`
  - `API_ENDPOINT`
  - `DEFAULT_MODEL`
  - `DEFAULT_LOCATION`

---

## 🔹 Dependencies

- Embedding provider (`openai`, `transformers`, etc.)
- Astronomical library (`skyfield`)
- Cryptography (`ed25519`)
- HTTP client (`requests` or `httpx`)
