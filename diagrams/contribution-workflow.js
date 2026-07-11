graph TD
    A[Open Issue] --> B[Community Vote & Prioritize]
    B --> C[Check Shared Need Evidence]
    C --> D[Create Feature PR]
    
    subgraph "PR Review Cycle"
        D --> E[Initial Screening]
        E --> F[Owner Assignment]
        F --> G[Peer Review]
        G --> H[CI/CD Pipeline]
        H --> I[Accessibility Check]
        I --> J[Community Validation]
    end
    
    J --> K{Meets Criteria?}
    K -->|Yes| L[Merge to Master]
    K -->|No| M[Iterate & Revise]
    M --> D
    
    L --> N[Release Build]
    N --> O[Update Documentation]
    O --> P[Community Notification]
    
    style A fill:#FF9999,stroke:#333,stroke-width:2px
    style C fill:#99FF99,stroke:#333,stroke-width:2px
    style M fill:#FFCC99,stroke:#333,stroke-width:2px
    style L fill:#99CCFF,stroke:#333,stroke-width:2px
    style P fill:#CC99FF,stroke:#333,stroke-width:2px
    
    linkStyle 0 stroke:#333,stroke-width:2px
    linkStyle 1 stroke:#333,stroke-width:2px
    linkStyle 2 stroke:#333,stroke-width:2px
    linkStyle 3 stroke:#333,stroke-width:2px