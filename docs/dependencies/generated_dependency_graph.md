# Module Dependency Graph

```mermaid
flowchart TD
    01-orientation-consent[["01\norientation\nconsent\nFoundational"]]
    style 01-orientation-consent fill:#4CAF50,color:white
    02-session-techniques[["02\nsession\ntechniques\nFoundational"]]
    style 02-session-techniques fill:#4CAF50,color:white
    03-special-populations[["03\nspecial\npopulations\nIntermediate"]]
    style 03-special-populations fill:#FF9800,color:white
    04-advanced-topics[["04\nadvanced\ntopics\nAdvanced"]]
    style 04-advanced-topics fill:#F44336,color:white
    05-assessment-evaluation[["05\nassessment\nevaluation\nIntermediate"]]
    style 05-assessment-evaluation fill:#FF9800,color:white
    06-digital-fetish-tools-technology-safety[["06\ndigital\nfetish\ntools\ntechnology\nsafety\nIntermediate"]]
    style 06-digital-fetish-tools-technology-safety fill:#FF9800,color:white
    07-online-kink-community-moderation-safety[["07\nonline\nkink\ncommunity\nmoderation\nsafety\nIntermediate"]]
    style 07-online-kink-community-moderation-safety fill:#FF9800,color:white
    08-financial-accessibility-economic-justice-in-education[["08\nfinancial\naccessibility\neconomic\njustice\nin\neducation\nFoundational"]]
    style 08-financial-accessibility-economic-justice-in-education fill:#4CAF50,color:white
    09-aging-elder-lifespan-education[["09\naging\nelder\nlifespan\neducation\nFoundational"]]
    style 09-aging-elder-lifespan-education fill:#4CAF50,color:white
    10-electrical-play[["10\nelectrical\nplay\nAdvanced"]]
    style 10-electrical-play fill:#F44336,color:white

    02-session-techniques --> 01-orientation-consent
    01-orientation-consent --> 02-session-techniques
    04-advanced-topics --> 02-session-techniques
    01-orientation-consent --> 03-special-populations
    01-orientation-consent --> 04-advanced-topics
    02-session-techniques --> 04-advanced-topics
    01-orientation-consent --> 05-assessment-evaluation
    01-orientation-consent --> 06-digital-fetish-tools-technology-safety
    01-orientation-consent --> 07-online-kink-community-moderation-safety
    01-orientation-consent --> 08-financial-accessibility-economic-justice-in-education
    01-orientation-consent --> 09-aging-elder-lifespan-education
```
