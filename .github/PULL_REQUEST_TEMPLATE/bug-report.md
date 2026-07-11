---
title: "Bug Report / Accessibility Concern"
description: "Report a bug or accessibility issue that needs fixing"
body:
  - type: "markdown"
    attributes:
      text: |
        Please note: This template is specifically for reporting bugs or accessibility concerns. For feature requests, use the "Feature Request" template.
  - type: "textarea"
    attributes:
      label: "Issue Description"
      description: "A clear and concise description of the bug or accessibility problem"
      placeholder: "The issue is..."
    validations:
      required: true
  - type: "textarea"
    attributes:
      label: "Reproduction Steps"
      description: "Steps to reproduce the issue"
      placeholder: "1. Go to '...'
2. Click on '...'"
      value: "1.  
2.  
3.  "
    validations:
      required: true
  - type: "textarea"
    attributes:
      label: "Current Behavior"
      description: "What happens currently (describe the bug/experience)"
      placeholder: "The page displays..."
    validations:
      required: true
  - type: "textarea"
    attributes:
      label: "Expected Behavior"
      description: "What should happen instead (describe the ideal experience)"
      placeholder: "The page should display..."
    validations:
      required: true
  - type: "textarea"
    attributes:
      label: "Steps to Reproduce (Alternative Method)"
      description: "If the issue affects navigation, provide an alternative way to access the content. Includes: What content is inaccessible, How to reach it an alternate way"
      placeholder: "Alternative: Access via '[page name]' using keyboard navigation..."
    validations:
      required: true
  - type: "textarea"
    attributes:
      label: "Supporting Files"
      description: "Add relevant screenshots or examples that can help explain your problem. Use screenshots to show the accessibility issue clearly. Optimized screenshots: <1024KB, PNG format, no text in images, screenshot with annotations where necessary. Include timestamps if relevant."
      placeholder: "Drag and drop files here or paste in this text area"
  - type: "markdown"
    attributes:
      text: |
        ## Additional Context
        
        - **Browser / Device**: (e.g., Chrome 118 on Windows 11, Safari on iPhone 14)
        - **Impact**: How this affects accessibility for: (neurodivergent users, motor impairments, visual impairments, screen reader users, low vision users, cognitive disabilities, etc.)
        - **Context**: How often this happens - on specific pages, interactive elements, particular user roles, etc.
        - **Accessibility Severity**:
          - **Critical**: Completely blocks access to content or essential functionality
          - **High**: Prevents users from completing essential tasks or understanding key information
          - **Medium**: Causes confusion or inefficiency but can work around
          - **Low**: Cosmetic or preference issue
  - type: "markdown"
    attributes:
      text: |
        ## Accessibility Standards Check
        
        - [ ] HTML validation passed
        - [ ] WCAG 2.1 AA compliance checked
        - [ ] Screen reader compatibility tested
        - [ ] Keyboard navigation tested
        - [ ] Color contrast verified
        - [ ] ARIA labels and roles correct
        - [ ] Responsive design checked
        - [ ] Language and translations verified
  - type: "textarea"
    attributes:
      label: "Testing Performed"
      description: "Any testing you did to reproduce the issue"
      value: "- [ ] Manual testing in browser
- [ ] Screen reader testing (NVDA/JAWS/VoiceOver)
- [ ] Keyboard navigation testing
- [ ] Color contrast verification
- [ ] Mobile device testing"
      validations:
        required: true