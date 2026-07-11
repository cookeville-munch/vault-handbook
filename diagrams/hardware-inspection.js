```mermaid
flowchart TD
    A[Hardware Inspection] --> B[Anchor Points]
    B --> C[Rated for 10x expected load?]
    C -->|Yes| D[No corrosion/cracks]
    C -->|No| E[REJECT]
    D -->|Yes| F[Mounting hardware secure?]
    D -->|No| E
    F -->|Yes| G[Connection Hardware]
    F -->|No| E
    G --> H[Quick-links: Threads clean?]
    H -->|Yes| I[Rings: No deformation?]
    I -->|Yes| J[Swivels: Rotate freely?]
    J -->|Yes| K[PASS]
    H -->|No| E
    I -->|No| E
    J -->|No| E
```