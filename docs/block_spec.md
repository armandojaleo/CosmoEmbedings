# Block Specification – CosmoEmbeddings

This document defines the structure and required fields of a **knowledge block** in the CosmoEmbeddings network.

Each block represents a unit of machine-interpretable knowledge (typically an embedding) and contains metadata to ensure traceability, interoperability, and validation integrity.

---

## 🔹 Core Structure

```json
{
  "id": "block-uuid",
  "embedding": [0.123, -0.872, ...],
  "embedding_format": "openai/text-embedding-3",
  "input_type": "text", // or "image", "audio", "embedding"
  "input_reference": {
    "hash": "sha256(input)",
    "origin": "https://..." // optional URI or filename
  },
  "timestamp": "2025-04-06T18:43:00Z",
  "observer_location": {
    "lat": 40.4168,
    "lon": -3.7038
  },
  "cosmo_signature": "Orion-127.5-Angle",
  "created_by": "agent_XYZ",
  "signature": "ed25519(...)",
  "version": 1,
  "tags": ["biology", "genetics"],
  "linked_blocks": ["block-abc", "block-def"]
}
```

---

## 🔹 Field Descriptions

- **id**: Globally unique identifier for the block.
- **embedding**: The actual vectorized representation of the knowledge.
- **embedding_format**: Indicates which model or method produced the embedding (important for compatibility).
- **input_type**: Specifies the original data type.
- **input_reference**:
  - `hash`: Digest of the raw input.
  - `origin`: (optional) Link or label of the source.
- **timestamp**: When the block was generated.
- **observer_location**: Geolocation of the agent or sensor that created the cosmo signature.
- **cosmo_signature**: A unique representation derived from astronomical conditions at a specific place and time.
- **created_by**: ID of the agent that created the block.
- **signature**: Digital signature over the full content.
- **version**: Version of the block structure.
- **tags**: Semantic labels to help categorize or retrieve blocks.
- **linked_blocks**: Array of block IDs semantically related to this one.

---

## 🔹 Validation Process

1. **Hash Verification**: The hash in `input_reference` must match the original input (if available).
2. **Cosmo Validation**: The `cosmo_signature` must match the observed astronomical data at the timestamp and location.
3. **Signature Check**: The block’s contents must be signed by the agent and verifiable by its public key.
4. **Optional Rule Sets**: Communities may apply custom rules for accepting or rejecting blocks (e.g., based on tags or reputation).

---

This format is designed to be extendable. Any field not listed above must be namespaced.
