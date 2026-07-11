```mermaid
graph TD
    A[Carabiner Inspection] --> B{Visual Check}
    B --> C[Gate Operation]
    C --> D[Smooth open/close?]
    D -->|Yes| E[Gate Alignment]
    D -->|No| F[REJECT - Replace]
    E --> G[Proper alignment?]
    G -->|Yes| H[Spine Integrity]
    G -->|No| F
    H --> I[No cracks/bends?]
    I -->|Yes| J[Weight Rating Visible]
    I -->|No| F
    J --> K[Rating matches use?]
    K -->|Yes| L[PASS]
    K -->|No| F
```