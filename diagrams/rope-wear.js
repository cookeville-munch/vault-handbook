```mermaid
graph LR
    A[Rope Inspection] --> B{Sheath Check}
    B --> C[Visual: Fraying?]
    C -->|Yes| D[REJECT]
    C -->|No| E[Tactile: Soft spots?]
    E -->|Yes| D
    E -->|No| F[Core Check]
    F --> G[Flex test: Uniform?]
    G -->|Yes| H[No flat spots?]
    H -->|Yes| I[PASS]
    G -->|No| D
    H -->|No| D
```