```mermaid
graph TB
    subgraph Scene_Setup[Scene Setup Zone]
        A1[Primary Impact Tools]
        A2[Backup Tools]
        A3[Safety Shears]
        A4[First Aid Kit]
        A5[Water/Blankets]
    end
    
    subgraph Inspection_Zone[Inspection Zone]
        B1[Carabiners x4]
        B2[Rope 30ft x2]
        B3[Quick-links x6]
        B4[Anchor Verification]
    end
    
    subgraph Emergency_Zone[Emergency Access]
        C1[Phone/911 Access]
        C2[Emergency Release Tools]
        C3[Exit Path Clear]
    end
    
    Inspection_Zone -->|Verified| Scene_Setup
    Scene_Setup --> Emergency_Zone
```