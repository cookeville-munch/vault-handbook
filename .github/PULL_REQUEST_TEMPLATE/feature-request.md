---
title: "Feature Request: Community-Empowering & Self-Service Oriented"
description: "Propose a feature that enables self-sovereignty, reduces dependency on others, or solves shared community needs"
body:
  - type: "markdown"
    attributes:
      text: |
        # Feature Request: Community-Empowering & Self-Service Oriented

        **Purpose:** This template ensures feature requests align with our mission to empower community members to self-serve and create shared value. All requests must demonstrate mechanisms for either:
        - Direct benefits to multiple users
        - Scalable solutions that others can replicate
        - Tools that reduce burden on limited resources

        **Instructions:** Fill out all sections thoughtfully. The community prioritizes proposals that foster collaboration, self-reliance, or address systemic barriers.
  - type: "textarea"
    id: "feature-summary"
    attributes:
      label: "Feature Summary"
      description: "One-sentence summary of the proposed feature and its primary community benefit"
      placeholder: "A self-guided safety checklist generator that helps newcomers create personalized negotiation frameworks without requiring experienced partners to guide them"
      validations:
        required: true
  - type: "textarea"
    id: "problem-context"
    attributes:
      label: "Problem Context & Community Impact"
      description: "Describe the specific need, pain point, or barrier this addresses. Explain how this affects multiple people in the community, not just you."
      placeholder: |
        Currently, newcomers to negotiation often rely entirely on experienced partners to guide them through safety discussions. This creates:
        1. Bottleneck on experienced partners' time
        2. Inconsistent safety coverage based on partner knowledge
        3. Barrier to entry for people without access to mentors
        4. Risk of skipped safety steps when excitement overrides caution
        
        This affects: new community members, people in areas without local communities, neurodivergent folks who struggle with verbal negotiation, and anyone without trusted mentors.
      validations:
        required: true
  - type: "textarea"
    id: "self-service-mechanism"
    attributes:
      label: "Self-Service Mechanism"
      description: "How does this feature enable someone to meet their own needs without requiring another person's active time/attention?"
      placeholder: |
        The checklist generator would:
        - Provide guided questions with contextual help tooltips
        - Output a personalized, printable/shareable negotiation document
        - Include risk-awareness education embedded in the flow
        - Allow saving/loading profiles for different partners/scenarios
        - Work completely offline after initial load (PWA)
        - Require zero backend infrastructure or moderator approval
      validations:
        required: true
  - type: "textarea"
    id: "shared-need-evidence"
    attributes:
      label: "Evidence of Shared Need"
      description: "What indicates this isn't just your personal preference? Cite community discussions, recurring questions, support requests, or patterns you've observed."
      placeholder: |
        - #1234: "Newbie safety checklist?" (47 upvotes, 23 comments)
        - Discord #newbie-help: 3-5 questions/week about "what should I negotiate?"
        - Survey 2023: 68% of respondents <6 months experience felt unprepared for first negotiation
        - Mentor program waitlist: 40+ people waiting for negotiation guidance
        - Common pattern: Experienced partners burn out from repeating basics
      validations:
        required: true
  - type: "textarea"
    id: "reduces-burden"
    attributes:
      label: "How This Reduces Burden on Community Resources"
      description: "Explain specifically how this decreases demand on: mentor time, moderator attention, experienced partner emotional labor, documentation maintenance, or other scarce resources."
      placeholder: |
        - Eliminates need for mentors to walk through basics (saves ~30 min/person)
        - Reduces moderator interventions for incomplete negotiations
        - Decreases repeat questions in help channels by estimated 40%
        - Allows experienced partners to focus on nuanced dynamics rather than basics
        - Creates reusable artifact (the checklist) that persists beyond conversations
      validations:
        required: true
  - type: "textarea"
    id: "replicability"
    attributes:
      label: "Replicability & Extensibility"
      description: "How can others adapt/extend this for their specific needs without requiring core team changes? Include technical and social extensibility."
      placeholder: |
        Technical:
        - JSON schema for checklist sections allows community contributions
        - Plugin architecture for domain-specific modules (rope, impact, power exchange, etc.)
        - Export format compatible with existing negotiation apps
        - Open-source core with clear contribution guide
        
        Social:
        - Template library where community shares specialized checklists
        - "Remix" culture encouraged with attribution
        - Multilingual support built into architecture
        - Accessibility-first design for neurodivergent users
      validations:
        required: true
  - type: "textarea"
    id: "implementation-contribution"
    attributes:
      label: "Your Implementation Contribution Plan"
      description: "What parts of this can YOU build, test, document, or support? Be specific about skills, time, and willingness to maintain."
      placeholder: |
        I can contribute:
        - UX research & user testing with 5+ newcomers (2 weeks)
        - Content architecture for negotiation domains (1 week)
        - Accessibility testing with screen readers & cognitive walkthroughs
        - Documentation writing for contributor onboarding
        - Ongoing: Moderate community template submissions (2 hrs/week)
        
        I need help with:
        - Frontend development (React/Vue - I can pair program)
        - PWA/offline architecture
        - Schema validation library
      validations:
        required: true
  - type: "textarea"
    id: "validation-approach"
    attributes:
      label: "Community Validation Approach"
      description: "How will you validate this serves the community before/after building? Include measurable criteria."
      placeholder: |
        Pre-build:
        - Survey 20+ newcomers on current pain points
        - Co-design session with 3 neurodivergent community members
        - Prototype testing with 10 users (task completion rate target: 80%)
        
        Post-launch metrics (3 months):
        - 500+ unique users generating checklists
        - 30% reduction in #newbie-help negotiation questions
        - 15+ community-contributed template variations
        - 4.5+ star satisfaction rating
        - Zero critical accessibility issues
      validations:
        required: true
  - type: "textarea"
    id: "documentation-commitment"
    attributes:
      label: "Documentation & Knowledge Transfer Commitment"
      description: "What documentation will you create/maintain so others can use, extend, and troubleshoot this without you?"
      placeholder: |
        - User guide: "Creating Your First Safety Checklist" (screenshots, video)
        - Contributor guide: "Adding New Negotiation Domains" (code + content)
        - Accessibility statement with testing checklist
        - FAQ based on beta testing questions
        - Architecture decision records (ADRs) for key technical choices
        - Migration guide for future schema versions
        - All docs in Markdown, versioned with code, screen-reader accessible
      validations:
        required: true
  - type: "markdown"
    attributes:
      text: |
        ---
        **Review Criteria (for community reference):**
        
        ✅ **High Priority** if: Enables self-service for underserved group + reduces mentor burden + clear community demand + contributor commits to maintenance
        
        🔄 **Iterate** if: Good concept but needs refinement on accessibility/replicability/scope
        
        ❌ **Decline** if: Only serves individual need, requires ongoing core-team maintenance, duplicates existing tools, or lacks validation plan
        
        ---
        *Remember: The goal isn't just "build my feature" — it's "build something that helps the community help itself."*
  - type: "checkboxes"
    id: "community-alignment"
    attributes:
      label: "Community Alignment Confirmation"
      description: "Confirm these principles align with your proposal"
      options:
        - label: "This feature primarily serves a shared community need, not just my personal preference"
          required: true
        - label: "I've searched existing issues/discussions and this doesn't duplicate current work"
          required: true
        - label: "I'm willing to iterate based on community feedback before/during implementation"
          required: true
        - label: "I'll document this so others can use/extend it without my ongoing involvement"
          required: true
        - label: "I've considered accessibility from the start (not as an afterthought)"
          required: true
        - label: "This reduces rather than increases dependency on limited community resources"
          required: true