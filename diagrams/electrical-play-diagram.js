```mermaid
flowchart LD
    A[Violet Wand] --> B{Safe Distance}
    B -->|<18"| C[Skin Surface]
    B -->|<32kHz| D[Thyroid Avoided]
    D --> E[Electrode Placement]

classDef "safe" fill:#4CAF50
classDef "caution" fill:#FFC107
classDef "danger" fill:#F44336

class A safe
class C safe
class D caution
class E danger
```