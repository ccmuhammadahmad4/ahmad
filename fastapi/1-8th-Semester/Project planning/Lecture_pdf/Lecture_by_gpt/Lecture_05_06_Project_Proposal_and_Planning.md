# Lectures 5 & 6: Project Proposal & Planning

## 📋 Table of Contents
1. [Financial Metrics for Project Selection](#financial-metrics-for-project-selection)
2. [Project Proposal](#project-proposal)
3. [Project Planning](#project-planning)
4. [Creating a Good Project Management Plan](#creating-a-good-project-management-plan)
5. [Key Takeaways](#key-takeaways)
6. [Problem-Solving Hierarchy](#problem-solving-hierarchy)

---

## Financial Metrics for Project Selection

### 1. Benefit/Cost Ratio (BCR)

**Definition**: Ratio between present value of benefits and present value of costs.

**Formula**:
```
BCR = Present Value of Benefits / Present Value of Costs
```

**Decision Rule**:
- BCR > 1 → Project creates more value than cost (ACCEPT)
- BCR < 1 → Project costs more than benefits (REJECT)
- BCR = 1 → Break-even (INDIFFERENT)

**Example**:
```
Project Investment: $100,000
Expected Benefits (present value): $150,000

BCR = 150,000 / 100,000 = 1.5

Interpretation: For every $1 invested, get $1.50 back ✅
```

**Usage**: Projects with higher BCR are generally preferred.

---

### 2. Scoring Model

**Definition**: Objective technique where selection committee lists criteria, assigns weights, scores projects, and chooses highest total.

**Process**:
1. List relevant criteria
2. Weight criteria by importance (total = 100%)
3. Score each project (1-5 or 1-10 scale)
4. Calculate weighted score
5. Select highest scoring project

**Already covered in detail in Lecture 4.**

---

### 3. Payback Period

**Definition**: Time needed to recover the original investment.

**Formula**:
```
Payback Period = Total Investment / Average Annual Cash Flow
```

**Example**:
```
Investment: $200,000
Annual Return: $50,000

Payback Period = 200,000 / 50,000 = 4 years
```

**Decision Rule**: Shorter payback period preferred.

**Limitations**:
- ❌ Doesn't consider time value of money
- ❌ Ignores benefits after payback
- ❌ Ignores project risks
- ❌ Focuses on liquidity, not profitability

**Best for**: Organizations focused on quick returns or high-risk industries.

---

### 4. Net Present Value (NPV)

**Definition**: Difference between present value of cash inflows and present value of cash outflows.

**Why Important**: Future money is worth less than today's money (time value).

**Example - Jane's Flowers**:
```
Project: Expand into dried flower business
Initial Investment: $8,000
Expected Cash Flow: $1,000/year for 10 years
Discount Rate (Cost of Capital): 10%

Calculate Present Value:
Year 1: $1,000 / (1.1)^1 = $909.09
Year 2: $1,000 / (1.1)^2 = $826.45
Year 3: $1,000 / (1.1)^3 = $751.31
...continue for 10 years...

Total PV of cash flows = $6,144.57
Initial Investment = -$8,000

NPV = $6,144.57 - $8,000 = -$1,855.43 ❌

Decision: REJECT (NPV is negative - project loses money!)
```

**Decision Rule**:
- NPV > 0 → ACCEPT (creates value)
- NPV < 0 → REJECT (destroys value)
- NPV = 0 → Indifferent

**Advantages**:
- ✅ Considers time value of money
- ✅ Considers all cash flows
- ✅ Shows absolute value creation

**Limitations**:
- ❌ Requires accurate forecasts
- ❌ Choosing discount rate can be subjective
- ❌ Doesn't show percentage return

---

### 5. Discounted Cash Flow (DCF)

**Definition**: Method to estimate value of investment adjusted for time value of money.

**Core Principle**: 
> "$1 today is worth more than $1 tomorrow because you can invest it today."

**Example**:
```
With 5% annual interest:
- $1 today → $1.05 in one year
- $1 payment delayed one year → Present value is $0.95
```

**Formula**:
```
DCF = Σ [Cash Flow in Period t / (1 + Discount Rate)^t]
```

**Application**: 
DCF is the foundation for NPV calculations. It allows you to compare cash flows occurring at different times on an equal basis.

---

### 6. Internal Rate of Return (IRR)

**Definition**: The discount rate at which NPV equals zero. The "break-even" interest rate.

**Interpretation**: 
IRR is the annualized effective compounded return rate of the project.

**Decision Rule**:
- IRR > Required Return → ACCEPT
- IRR < Required Return → REJECT
- Higher IRR = Better Project

**Example**:
```
Company's Required Return: 10%

Project A: IRR = 15% ✅ (Acceptable, 5% above required)
Project B: IRR = 8% ❌ (Reject, below required return)
```

**Comparison with NPV**:
- IRR shows percentage return
- NPV shows absolute dollar value

**Important Note**:
> "When IRR and NPV give different rankings, trust NPV. NPV tells you actual value creation."

**Limitation**: 
A project with lower IRR might have higher NPV if it's much larger. Always consider NPV for final decision.

---

### 7. Opportunity Cost

**Definition**: Cost of giving up the next best alternative when making a choice.

**Example**:
```
You have $100,000 and three options:

Option A: Invest in Project X (expected return: 15%)
Option B: Invest in Project Y (expected return: 12%)
Option C: Put in bank (guaranteed return: 5%)

If you choose Project X:
- Direct benefit: 15% return
- Opportunity cost: Missing out on 12% from Project Y
- Net benefit: 15% - 12% = 3% better than next best option
```

**Why It Matters**:
Every choice has a hidden cost - what you could have gained from the alternative.

**Application in Project Selection**:
```
Project A: NPV = $50,000
Project B: NPV = $45,000

If you select A:
- Gain: $50,000
- Opportunity cost: $45,000 (what you gave up)
- Net advantage: $5,000
```

**Best Practice**: Always consider what you're giving up, not just what you're gaining.

---

### DCF vs NPV

**Relationship**:
- **DCF**: General approach to value any investment based on discounted future cash flows
- **NPV**: Specific metric using DCF, subtracting initial investment

**Think of it this way**:
```
DCF = Method (How to calculate)
NPV = Result (The actual answer)

DCF tells you present value of all future cash
NPV tells you if you should invest (after subtracting cost)
```

**Example**:
```
Using DCF: Future cash flows worth $120,000 today
Investment needed: $100,000

NPV = $120,000 (DCF result) - $100,000 (investment) = +$20,000 ✅
```

---

## Project Proposal

### What is a Project Proposal?

**Definition**: 
A document describing a proposed project including purpose, outcomes, and steps to complete it.

**Purpose**:
- Communicate how you plan to approach the project
- Persuade decision-makers to approve and fund
- Allow comparison between different vendors
- Set initial expectations

**NOT a Contract**: It's a preliminary document, not a legal agreement.

---

### Key Elements of a Project Proposal

#### 1. **Project Background**
- What problems exist?
- What challenges need solving?
- What opportunities are available?
- Why is this project needed NOW?

**Example**:
> "Our customer service response time has increased to 48 hours (from 24 hours last year), leading to 25% decrease in customer satisfaction. Competitors respond within 12 hours."

#### 2. **Objectives**
- What are the intended outcomes?
- What will be different after the project?
- Measurable goals

**Example**:
> "Reduce customer service response time to under 12 hours and increase customer satisfaction score from 75% to 90% within 6 months."

#### 3. **Project Scope**
- What are the steps/stages?
- What elements are included?
- What elements are EXCLUDED? (Important!)
- How will objectives be reached?

**Example - Included**:
- New ticketing system
- Staff training
- Integration with email
- Mobile app

**Example - Excluded**:
- Social media integration (Phase 2)
- Voice call system (separate project)

#### 4. **Deliverables**
- What tangible outputs will be produced?
- What will you hand over at the end?

**Example**:
- Functional ticketing system
- User documentation
- Training materials
- 3 months of support

#### 5. **Timeline**
- Project duration
- Major milestones
- Key deadlines

**Example**:
- Month 1-2: System selection and setup
- Month 3-4: Customization and integration
- Month 5: Training and testing
- Month 6: Go-live and stabilization

#### 6. **Budget**
- Total cost estimate
- Breakdown by category
- Payment terms

**Example**:
- Software license: $20,000
- Implementation: $30,000
- Training: $5,000
- Support (3 months): $5,000
- **Total: $60,000**

#### 7. **Team & Resources**
- Who will work on this?
- What are their roles?
- What qualifications do they have?

**Example**:
- Project Manager: John (10 years PM experience)
- System Architect: Sarah (5 years)
- 2 Developers: Certified in platform
- 1 Trainer: Customer service background

#### 8. **Risks & Mitigation**
- What could go wrong?
- How will you handle it?

**Example**:
- Risk: Staff resistance to new system
- Mitigation: Early involvement, comprehensive training, change champions

#### 9. **Success Criteria**
- How will you measure success?
- What defines "done"?

**Example**:
- System uptime: 99.5%
- Response time: < 12 hours (95% of tickets)
- User satisfaction: > 85%
- All staff trained and certified

---

### Why is a Project Proposal Important?

#### 1. **Improved Vendor Comparison**
- Compare multiple vendors objectively
- Understand price differences
- See different approaches
- Make informed choice

**Example**:
```
Vendor A: $60,000, 6 months, basic features
Vendor B: $80,000, 8 months, advanced features + AI
Vendor C: $50,000, 5 months, limited support

Decision: Choose based on needs, not just price
```

#### 2. **Project Understanding**
- Both parties agree on scope
- Reduces misunderstandings
- Establishes shared vision
- Builds trust

**Before Proposal**: 
- Client thinks: "I want a simple website"
- Vendor thinks: "They want e-commerce with payment"
- **Mismatch!** ❌

**After Proposal**: 
- Both agree: "5-page informational website, no e-commerce"
- **Alignment!** ✅

#### 3. **Establish Credibility**
- Shows you understand the problem
- Demonstrates expertise
- Proves capability
- Builds confidence

**Good Proposal Says**:
> "We've done 20 similar projects, here's our approach based on proven methods..."

#### 4. **Propose Timeline & Budget**
- Realistic estimates
- Helps client planning
- Sets expectations
- Enables resource allocation

**Not a Final Contract**, but close enough for decision-making.

#### 5. **Set Expectations**
- Clear deliverables
- Defined timeline
- Agreed budget
- Communication plan
- Change process

**Prevents**:
- Scope creep
- Budget overruns
- Misunderstandings
- Conflicts

#### 6. **Inform Project Planning**
- Once approved, becomes foundation
- Used to create detailed project plan
- Basis for contract
- Reference throughout project

---

## Project Planning

### What is a Project Plan?

**Definition**: 
Formal document containing all planning decisions, approved scope, and costs.

**Difference from Proposal**:
- **Proposal**: Selling the idea (before approval)
- **Plan**: How to execute (after approval)

---

### What is Project Planning?

**Definition**: 
Process of defining scope, objectives, and ways to achieve them.

**When It Happens**: 
BEFORE actual work starts. Planning precedes execution.

**Output**: 
The Project Plan document.

---

### Project Plan Purpose

A well-prepared plan answers these questions:

#### 1. **Why?**
- Reasons for sponsoring project
- Problem being addressed
- Business case
- Expected benefits

#### 2. **What?**
- Scope of work
- Tasks and activities
- Deliverables
- Success criteria

#### 3. **Who?**
- People involved
- Roles and responsibilities
- Organizational structure
- Reporting relationships

#### 4. **When?**
- Project schedule/timeline
- Milestones
- Deadlines
- Dependencies

#### 5. **Where?**
- Project location
- Geographic considerations
- Facility requirements
- Remote/on-site work

#### 6. **How?**
- Methodology/approach
- Steps to complete tasks
- Tools and techniques
- Quality processes

---

### What Should a Project Plan Include?

#### 1. **Vision (Executive Summary)**
- Brief description
- All goals and objectives
- High-level overview

**Example**:
> "This project will implement a Learning Management System enabling 5,000 students to access courses online, complete assignments, and receive grades electronically, replacing the current manual process. Project duration: 9 months. Budget: $150,000. Expected benefits: 50% reduction in administrative work, 24/7 student access, improved tracking."

#### 2. **Context Details**
- Is it a new project?
- Does it build on previous work?
- Lessons from similar past projects
- Related initiatives

#### 3. **Target Audience**
- Who will use the output?
- Their needs and expectations
- Unique selling point (USP)

**Example**:
- Primary users: Students (undergrad and grad)
- Secondary users: Faculty
- Administrators
- USP: Mobile-first design, offline access

#### 4. **Roles and Responsibilities**
- All individuals involved
- Their specific roles
- Authority levels
- RACI matrix

**RACI Matrix Example**:
```
Task: Design Database

R (Responsible): Database Admin - Does the work
A (Accountable): IT Manager - Final approval
C (Consulted): App Developer - Provides input
I (Informed): Project Sponsor - Kept updated
```

#### 5. **Communication Strategy**
- How will team communicate?
- Meeting schedule
- Reporting format
- Communication tools

**Example**:
- Daily: 15-min standup (team)
- Weekly: Status report (to sponsor)
- Bi-weekly: Steering committee meeting
- Tools: Slack, Email, Jira, Zoom

#### 6. **Project Timeline**
- Tasks in logical order
- Start and end dates
- Milestones
- Dependencies

**Example (Gantt Chart)**:
```
Task 1: Requirements (Week 1-2)
Task 2: Design (Week 3-4) - depends on Task 1
Task 3: Development (Week 5-10) - depends on Task 2
Task 4: Testing (Week 11-12) - depends on Task 3
Task 5: Deployment (Week 13)
```

#### 7. **Core Tasks and Deliverables**
- What needs to be done
- What will be produced
- Acceptance criteria

**Example**:
| Task | Deliverable | Acceptance Criteria |
|------|-------------|---------------------|
| Requirements gathering | Requirements document | Approved by stakeholders |
| Database design | ER diagram + schema | Technical review passed |
| Development | Working code | Passes all unit tests |
| User training | Training materials + sessions | 90% attendance, 85% pass quiz |

#### 8. **Resources**
- People needed
- Tools and software
- Hardware/infrastructure
- Materials

**Example**:
- **People**: 4 developers, 1 designer, 1 QA, 1 PM
- **Tools**: Visual Studio, Git, Jira, AWS
- **Hardware**: Development servers, test environment
- **Materials**: Training room, documentation tools

#### 9. **Budget and Costs**
- Detailed cost breakdown
- Cost categories
- Contingency reserve
- Payment schedule

**Example Budget**:
```
Personnel: $80,000
Software licenses: $20,000
Infrastructure: $15,000
Training: $5,000
Contingency (10%): $12,000
──────────────────
Total: $132,000
```

#### 10. **Contingency Plan (Risk Management)**
- Identified risks
- Risk assessment (probability × impact)
- Mitigation strategies
- Contingency reserves

**Example**:
```
Risk: Key developer leaves

Probability: Medium (30%)
Impact: High
Mitigation:
- Cross-training team members
- Comprehensive documentation
- Backup resource identified
Contingency: Budget for contractor if needed
```

#### 11. **Document Management System**
- How documents will be stored
- Version control
- Access permissions
- Naming conventions

**Example**:
- All docs in SharePoint
- Version format: ProjectName_Document_v1.0.docx
- Access: Team has edit, stakeholders have view
- Retention: 5 years after project closure

#### 12. **Legacy**
- Intended lasting impact
- Sustainability plan
- Knowledge transfer
- Ongoing support

**Example**:
> "After project completion, system will be maintained by IT department. All source code and documentation transferred. Two team members will transition to support roles for 6 months."

---

### Subsidiary Management Plans

For complex projects, create specialized plans:

#### 1. **Schedule Management Plan**
- How schedule will be developed
- How changes will be controlled
- Review and update process

#### 2. **Scope Management Plan**
- How scope will be defined
- How to handle scope changes
- Scope verification process

#### 3. **Resource Management Plan**
- How resources will be acquired
- How resources will be managed
- Resource leveling approach

#### 4. **Quality Management Plan**
- Quality standards
- Quality assurance activities
- Quality control procedures

#### 5. **Cost Management Plan**
- How budget will be managed
- Cost estimation methods
- Cost control procedures

#### 6. **Communications Management Plan**
- Who needs what information
- When and how to communicate
- Communication responsibility matrix

#### 7. **Risk Management Plan**
- Risk identification process
- Risk analysis methods
- Risk response strategies

#### 8. **Change Management Plan**
- How changes will be requested
- Change evaluation process
- Change approval authority

#### 9. **Stakeholder Engagement Plan**
- Stakeholder analysis
- Engagement strategies
- Management approaches

#### 10. **Procurement Management Plan**
- What needs to be procured
- Procurement process
- Vendor management

**How Many Do You Need?**
Depends on project complexity and organizational requirements.

**Minimum**: Schedule, Scope, Resource, and Communication plans
**Maximum**: All 10 for very complex projects

---

### Project Plan vs Project Management Plan

**Often confused, but they're different!**

#### Project Plan (Higher-Level)
- **Focus**: WHAT needs to be done
- **Detail Level**: Low to medium
- **Nature**: Visionary document
- **Audience**: Stakeholders, sponsors
- **Purpose**: Communicate the vision

**Example Content**:
- We will build an e-commerce website
- It will have these main features
- It will take 6 months
- It will cost $100,000

#### Project Management Plan (Execution-Level)
- **Focus**: HOW it will be done
- **Detail Level**: High, detailed
- **Nature**: Execution document
- **Audience**: Project team
- **Purpose**: Guide daily work

**Example Content**:
- Database will use PostgreSQL 13
- Sprint duration: 2 weeks
- Code review required before merge
- Testing protocol: automated + manual
- Deployment: Every Friday at 6 PM

#### Relationship:
```
Project Plan (The Vision)
    ↓
Guides creation of
    ↓
Project Management Plan (The Execution)
```

#### When to Merge:
- **Small projects**: Can combine into one document
- **Large projects**: Keep separate for clarity

---

## Creating a Good Project Management Plan

### 7 Steps to Create Your Plan

#### Step 1: Communicate

**What to do**:
- Talk to your team about goals
- Identify participants
- Discuss tasks
- Stay in touch constantly

**Why Important**:
> "80% of employees spend half their workweek on 'rework' caused by poor communication." - Project Management Institute

**Activities**:
1. Kickoff meeting with all stakeholders
2. One-on-one with each team member
3. Establish communication norms
4. Set up communication channels

**Questions to Answer**:
- Who needs to know what?
- How often will we communicate?
- What tools will we use?
- What's the escalation process?

---

#### Step 2: Identify Stakeholders & Determine Goals

**Stakeholders Can Be**:

1. **Sponsor**
   - Funds the project
   - Approves major decisions
   - Provides organizational support

2. **Project Manager**
   - Creates and executes plan
   - Controls daily operations
   - Manages team

3. **Project Team**
   - Creates end product
   - Handles development, quality, design

4. **End Users**
   - Will use the final product
   - Provide requirements
   - Test and validate

5. **Others**:
   - Risk analysts
   - Procurement specialists
   - Legal/compliance
   - Vendors

**How to Identify**:
1. List everyone affected by project
2. Categorize: Direct vs Indirect influence
3. Assess their interest and power
4. Prioritize high-power, high-interest stakeholders

**Determine Goals Using SMART**:

**S**pecific: Clearly defined, not vague
**M**easurable: Can track progress
**A**chievable: Realistic and attainable
**R**elevant: Aligns with business objectives
**T**imely: Has a deadline

**Example**:
- ❌ Vague: "Improve customer service"
- ✅ SMART: "Reduce average customer service response time from 48 hours to 12 hours by June 30, 2026, measured through ticketing system reports"

**Conduct Interviews**:
- Understand stakeholder requirements
- Clarify goals
- Identify constraints
- Build relationships

**This answers the WHY question**: Why is this project sponsored?

---

#### Step 3: Define Project Scope

**Most Important Stage!**

**What to Define**:

1. **Justification**: Why are we doing this?
2. **Product Description**: What are we building?
3. **Acceptance Criteria**: How do we know it's done?
4. **Objectives/Deliverables**: What will be produced?
5. **Exclusions**: What's NOT included?
6. **Constraints**: What limitations exist?
7. **Assumptions**: What are we assuming?
8. **Cost Estimates**: How much will it cost?

**Output**: Project Scope Statement

**Importance**:
- Establishes shared understanding
- Prevents scope creep
- Reduces risks of misunderstanding
- Basis for all future decisions

**This answers the WHAT question**: What will we do?

**Example Scope Statement**:
```
PROJECT: University Mobile App

IN SCOPE:
✅ Student information lookup
✅ Course schedule viewing
✅ Grade checking
✅ Campus map
✅ Event calendar
✅ Push notifications
✅ iOS and Android apps

OUT OF SCOPE:
❌ Online course registration (future phase)
❌ Payment processing (separate system)
❌ Social networking features
❌ Desktop version

CONSTRAINTS:
- Must integrate with existing student database
- Must complete by August 2026 (before fall semester)
- Budget: $75,000

ASSUMPTIONS:
- Student database API will be available
- 2 developers allocated full-time
- University will provide beta testers
```

---

#### Step 4: Define Roles and Responsibilities

**What to do**:
- Assign tasks to team members
- Define each person's role
- Set clear responsibilities
- Ensure no task is unassigned

**Create RACI Matrix**:

| Task/Deliverable | Project Manager | Developer | Designer | Tester | Sponsor |
|------------------|-----------------|-----------|----------|--------|---------|
| Requirements | A | C | C | C | I |
| Design | C | R | A | C | I |
| Development | A | R | C | C | I |
| Testing | C | C | C | R/A | I |
| Deployment | R/A | C | - | C | I |

**Legend**:
- **R** (Responsible): Does the work
- **A** (Accountable): Final approval, owns outcome
- **C** (Consulted): Provides input
- **I** (Informed): Kept updated

**This answers the WHO question**: Who does what?

---

#### Step 5: Schedule the Project

**What to do**:
- Set work duration for each task
- Define start and end dates
- Identify dependencies
- Set milestones
- Find critical path

**This answers the WHEN question**.

**Tools**:
- Gantt charts
- Network diagrams
- Critical path method (CPM)
- PERT charts

**Key Concepts**:

**Milestones**: Significant events
- Example: "Requirements Approved", "Design Complete", "Beta Launch"
- Zero duration
- Mark important achievements

**Critical Path**: Longest path through project
- Determines minimum project duration
- Any delay on critical path delays entire project
- Must be monitored closely

**Dependencies**:
- Finish-to-Start: B can't start until A finishes (most common)
- Start-to-Start: B can't start until A starts
- Finish-to-Finish: B can't finish until A finishes
- Start-to-Finish: B can't finish until A starts (rare)

---

#### Step 6: Visualize with Gantt Chart

**What is Gantt Chart?**
- Visual representation of project schedule
- Shows tasks, durations, dependencies
- Easy to understand timeline

**Benefits**:
- ✅ Create tasks and assign to team members
- ✅ Set duration with start/end dates
- ✅ Set dependencies between tasks
- ✅ Track progress of each task
- ✅ Identify resource needs
- ✅ Define cost per resource
- ✅ Collaborate with team
- ✅ Follow milestones
- ✅ Enable critical path view

**Tools**: GanttPRO, MS Project, Asana, Monday.com, Smartsheet

**Example**:
```
Task                    |Jan |Feb |Mar |Apr |May |Jun
─────────────────────────────────────────────────────
Requirements (2 weeks)  |████|    |    |    |    |
Design (3 weeks)        | ██████ |    |    |    |
Development (8 weeks)   |    | ████████████████ |
Testing (3 weeks)       |    |    |    | ████████
Deployment (1 week)     |    |    |    |    | ██

Milestones:
▼ Requirements Done (End Jan)
▼ Design Done (Mid Feb)
▼ Beta Release (End Apr)
▼ Go Live (Early May)
```

---

#### Step 7: Manage Risks

**What to do**:
- Define what can go wrong
- Assess probability and impact
- Create mitigation plans
- Assign risk owners
- Monitor throughout project

**Common Risks**:
1. **Too optimistic expectations** (time and cost)
2. **Unclear requirements** and needs
3. **Unclear roles** and responsibilities
4. **Changes in requirements**
5. **New requirements** added
6. **Budget cuts**
7. **Poor communication**
8. **Resource unavailability**
9. **Technical challenges**
10. **Stakeholder conflicts**

**Risk Management Process**:

```
1. IDENTIFY risks
   └─ Brainstorm what can go wrong
   
2. ANALYZE risks
   └─ Assess probability (Low/Medium/High)
   └─ Assess impact (Low/Medium/High)
   └─ Calculate risk score
   
3. PLAN responses
   └─ Avoid: Change plan to eliminate risk
   └─ Mitigate: Reduce probability or impact
   └─ Transfer: Insurance, outsourcing
   └─ Accept: For low-priority risks
   
4. IMPLEMENT responses
   └─ Execute the risk response plan
   
5. MONITOR continuously
   └─ Track identified risks
   └─ Identify new risks
   └─ Review effectiveness of responses
```

**Example Risk Register**:

| Risk ID | Description | Probability | Impact | Score | Response Strategy | Owner |
|---------|-------------|-------------|--------|-------|-------------------|-------|
| R-001 | Key developer leaves | Medium | High | 8 | Mitigate: Cross-training, documentation | PM |
| R-002 | Requirements change | High | Medium | 7 | Accept: Change control process | PM |
| R-003 | Integration issues | Medium | Medium | 5 | Mitigate: Early testing, POC | Tech Lead |
| R-004 | Budget overrun | Low | High | 6 | Mitigate: Weekly budget tracking | PM |

---

### Stick With It!

**Reality Check**:
- No two projects are identical
- One can be perfect, another can fail (same team, same conditions)
- Plans WILL change
- Risks WILL occur

**What Helps**:
- ✅ Detailed project scope
- ✅ Realistic schedule
- ✅ Good teamwork
- ✅ Assessed risks
- ✅ Flexibility to adapt

**Attitude**:
> "Even challenging projects can bring fun and joy with proper planning!"

---

## Key Takeaways

### Financial Metrics Summary

| Metric | What it Shows | Decision Rule | Best Use |
|--------|---------------|---------------|----------|
| **BCR** | Benefit per cost dollar | BCR > 1 → Accept | Simple comparisons |
| **Payback** | Recovery time | Shorter → Better | Liquidity focus |
| **NPV** | Absolute value creation | NPV > 0 → Accept | Most accurate |
| **IRR** | Percentage return | IRR > Required → Accept | Easy communication |
| **Opportunity Cost** | What you're giving up | Minimize | Choosing between options |

### Project Proposal vs Plan

| Aspect | Proposal | Plan |
|--------|----------|------|
| **Timing** | Before approval | After approval |
| **Purpose** | Sell the idea | Guide execution |
| **Audience** | Decision-makers | Project team |
| **Detail** | High-level | Detailed |
| **Focus** | WHAT and WHY | HOW and WHEN |

### Planning Essentials

**Remember the 6 Questions**:
1. WHY? - Justification and business case
2. WHAT? - Scope and deliverables
3. WHO? - Roles and responsibilities
4. WHEN? - Schedule and timeline
5. WHERE? - Location and logistics
6. HOW? - Methodology and approach

### Success Formula

```
Good Plan = Communication + Clear Scope + Defined Roles + 
            Realistic Schedule + Identified Risks + 
            Stakeholder Buy-in + Flexibility
```

---

## Problem-Solving Hierarchy

### 🎯 Complete Planning Process

#### **Phase 1: Pre-Planning (Before You Start)**

**Step 1: Get Project Approved**
```
1. Create business case
2. Write project proposal
3. Present to decision-makers
4. Get approval and funding
5. Secure project sponsor
```

**Step 2: Assemble Planning Team**
```
1. Identify project manager
2. Select key team members
3. Identify subject matter experts
4. Confirm availability
5. Get commitments
```

---

#### **Phase 2: Core Planning (Create the Plan)**

**Week 1: Initiation & Communication**

**Day 1-2: Kickoff**
```
□ Project kickoff meeting
  └─ Introduce team
  └─ Share project vision
  └─ Discuss high-level goals
  └─ Set expectations
  
□ Establish communication norms
  └─ Meeting schedules
  └─ Communication tools
  └─ Response time expectations
  └─ Escalation procedures
```

**Day 3-5: Stakeholder Analysis**
```
□ Identify all stakeholders
  └─ Create stakeholder register
  └─ Categorize (power vs interest)
  └─ Prioritize key stakeholders
  
□ Conduct stakeholder interviews
  └─ Understand their expectations
  └─ Identify their concerns
  └─ Gather requirements
  └─ Build relationships
```

**Week 2: Scope Definition**

**Day 6-8: Requirements Gathering**
```
□ Collect requirements from stakeholders
□ Document functional requirements
□ Document non-functional requirements
□ Identify constraints
□ Document assumptions
□ Clarify exclusions
```

**Day 9-10: Scope Statement**
```
□ Write project scope statement
  └─ Justification
  └─ Product description
  └─ Deliverables
  └─ Acceptance criteria
  └─ Constraints
  └─ Assumptions
  └─ Exclusions
  
□ Get stakeholder approval
□ Baseline the scope
```

**Week 3: WBS & Scheduling**

**Day 11-13: Work Breakdown Structure**
```
□ Break project into phases
□ Break phases into deliverables
□ Break deliverables into work packages
□ Assign IDs to all elements
□ Create WBS dictionary
□ Review with team
```

**Day 14-15: Initial Schedule**
```
□ Estimate duration for each work package
□ Identify dependencies
□ Create network diagram
□ Identify critical path
□ Set milestones
□ Create Gantt chart
□ Add buffer time
```

**Week 4: Resources & Budget**

**Day 16-17: Resource Planning**
```
□ Identify resource needs
  └─ People (skills and quantity)
  └─ Equipment
  └─ Materials
  └─ Facilities
  
□ Check resource availability
□ Assign resources to tasks
□ Level resources (resolve conflicts)
□ Create resource calendar
```

**Day 18-20: Budget Development**
```
□ Estimate costs for each work package
  └─ Labor costs
  └─ Material costs
  └─ Equipment costs
  └─ Other costs
  
□ Add contingency reserve (10-20%)
□ Add management reserve
□ Create budget breakdown
□ Get budget approval
```

**Week 5: Risk & Quality Planning**

**Day 21-22: Risk Management**
```
□ Brainstorm risks with team
□ Document risks in risk register
□ Analyze each risk
  └─ Probability (1-5)
  └─ Impact (1-5)
  └─ Risk score (P × I)
  
□ Prioritize top 10 risks
□ Develop response strategies
□ Assign risk owners
□ Calculate contingency needs
```

**Day 23-25: Quality & Other Plans**
```
□ Define quality standards
□ Plan quality assurance activities
□ Plan quality control procedures
□ Develop communication plan
□ Develop change management process
□ Create procurement plan (if needed)
```

**Week 6: Documentation & Approval**

**Day 26-28: Finalize Plan**
```
□ Compile all sections into one document
□ Create executive summary
□ Add appendices
  └─ Detailed schedules
  └─ Budget breakdown
  └─ Risk register
  └─ Resource calendar
  
□ Review with team
□ Make revisions
□ Proofread
```

**Day 29-30: Get Approval**
```
□ Present plan to sponsor
□ Present to steering committee
□ Address questions and concerns
□ Make final adjustments
□ Get formal sign-off
□ Distribute to all stakeholders
□ BASELINE THE PLAN
```

---

#### **Phase 3: Plan Validation (Before Execution)**

**Validation Checklist:**

```
COMPLETENESS CHECK:
□ All 6 questions answered? (Why, What, Who, When, Where, How)
□ All subsidiary plans created?
□ All stakeholders identified?
□ All risks assessed?
□ Budget realistic?
□ Schedule realistic?
□ Resources confirmed?
□ Quality criteria defined?
□ Communication plan clear?
□ Change process defined?

QUALITY CHECK:
□ SMART goals?
□ Clear acceptance criteria?
□ No ambiguous language?
□ Dependencies identified?
□ Critical path defined?
□ Baseline established?
□ All stakeholders buy-in?
□ Plan easy to understand?

RISK CHECK:
□ Major risks identified?
□ Risk responses planned?
□ Contingency budgeted?
□ Risk owners assigned?
□ Monitoring process defined?
```

If ALL checked → PROCEED TO EXECUTION! ✅

If ANY missing → FIX BEFORE STARTING! ❌

---

#### **Phase 4: Common Planning Problems & Solutions**

**Problem 1: Stakeholders Can't Agree on Requirements**

**Symptoms**:
- Conflicting requirements
- Endless requirement meetings
- No sign-off on scope

**Solution**:
```
1. Escalate to sponsor
2. Conduct facilitated workshop
3. Use MoSCoW method:
   M - Must have
   S - Should have
   C - Could have
   W - Won't have (this time)
4. Get sponsor to prioritize
5. Document trade-offs
6. Get formal approval
```

---

**Problem 2: Schedule Seems Unrealistic**

**Symptoms**:
- Team says "impossible"
- Too aggressive deadlines
- No buffer time

**Solution**:
```
1. Review estimates with team
2. Use three-point estimation:
   - Optimistic
   - Most likely
   - Pessimistic
3. Add buffer (15-20%)
4. Identify what can be parallel
5. Look for fast-tracking opportunities
6. If still too tight, negotiate with sponsor
7. Consider phased delivery
```

---

**Problem 3: Budget Not Approved**

**Symptoms**:
- Budget cut by management
- Need to reduce costs
- Scope vs budget mismatch

**Solution**:
```
1. Review and optimize costs
2. Challenge all assumptions
3. Look for cost-saving alternatives
4. Consider phased approach
5. Present scope-cost trade-off
6. Show business case again
7. If still not approved:
   - Reduce scope
   - Extend timeline (reduce resource load)
   - Increase quality risk (not recommended)
```

---

**Problem 4: Key Resources Not Available**

**Symptoms**:
- Assigned resources pulled to other projects
- Skills not available in-house
- Resource conflicts

**Solution**:
```
1. Negotiate with resource managers
2. Escalate to sponsor if needed
3. Consider alternatives:
   - Hire contractors
   - Outsource parts
   - Train existing staff
   - Adjust schedule
4. Update resource plan
5. Revise budget if needed
```

---

**Problem 5: Too Many Risks**

**Symptoms**:
- Risk register has 50+ risks
- Team overwhelmed
- Analysis paralysis

**Solution**:
```
1. Focus on top 10-15 risks (80/20 rule)
2. Ignore low probability + low impact
3. Group related risks
4. Accept some risks (can't mitigate everything)
5. Set risk thresholds
6. Review risks monthly, not daily
```

---

### 📊 Real-World Planning Scenario

**Scenario**: You're assigned to manage development of a Customer Portal for a bank.

**Given Information**:
- Budget: $200,000
- Timeline: 9 months
- Team: 5 developers, 1 designer, 1 QA
- Stakeholders: IT Head, Marketing Head, Operations Head, 2,000 customers

**Apply Complete Planning Process**:

**Week 1: Communication & Stakeholders**

**Actions**:
1. Kickoff meeting with 3 department heads
2. Interviewed 10 representative customers
3. Met with each team member
4. Set up Slack for communication
5. Scheduled weekly steering committee meetings

**Output**:
- Stakeholder register (12 stakeholders identified)
- Communication plan
- SMART Goal: "Launch customer portal with account summary, bill payment, and transaction history features by September 30, 2026, achieving 70% customer adoption within 3 months."

**Week 2: Scope**

**Actions**:
1. Documented requirements from interviews
2. Created feature list (35 features)
3. Prioritized using MoSCoW
4. Defined what's out of scope
5. Got scope approved by steering committee

**Output**:
- Scope statement (5 pages)
- Must-have: 15 features
- Should-have: 10 features  
- Could-have: 10 features
- Won't have (this phase): Investments, loans (separate project)

**Week 3: WBS & Schedule**

**Actions**:
1. Created 3-level WBS
2. 45 work packages identified
3. Estimated each work package (team input)
4. Created network diagram
5. Identified critical path (database + payment integration)
6. Built Gantt chart

**Output**:
- WBS document
- 9-month schedule with 6 milestones
- Critical path: 7 months (2 months buffer)
- Sprint-based (2-week sprints, 18 sprints total)

**Week 4: Resources & Budget**

**Actions**:
1. Assigned developers to modules
2. Reserved design time
3. Allocated QA throughout
4. Identified need for security audit (external)
5. Calculated all costs

**Output**:
```
BUDGET BREAKDOWN:

Personnel (7 people × 9 months):
- 5 Developers: $120,000
- 1 Designer: $25,000
- 1 QA: $20,000

External Services:
- Security audit: $15,000
- Penetration testing: $8,000

Infrastructure:
- Dev/Test/Prod environments: $7,000

Software & Tools:
- Licenses: $3,000

Contingency (15%): $30,000

────────────────────────────
Total: $228,000

ISSUE: Over budget by $28,000!

SOLUTION:
- Reduce designer to 0.5 FTE: Save $12,500
- Use in-house testing: Save $8,000
- Optimize infrastructure: Save $2,000
- Reduce contingency to 10%: Save $9,000
────────────────────────────
Revised Total: $198,000 ✅ Under budget!
```

**Week 5: Risks & Quality**

**Actions**:
1. Risk brainstorming session (team + stakeholders)
2. Identified 28 risks
3. Analyzed and prioritized
4. Focused on top 10
5. Created response plans

**Top 3 Risks**:
```
Risk 1: Payment gateway integration issues
- Probability: High (60%)
- Impact: High
- Score: 9/10
- Response: Proof of concept in Sprint 2, backup vendor identified

Risk 2: Security vulnerabilities
- Probability: Medium (40%)
- Impact: Critical
- Score: 8/10
- Response: Security review every sprint, external audit before launch

Risk 3: Customer adoption lower than expected
- Probability: Medium (50%)
- Impact: Medium
- Score: 6/10
- Response: Marketing campaign, user training videos, incentives
```

**Week 6: Finalize & Approve**

**Actions**:
1. Compiled 45-page project management plan
2. Created 5-page executive summary
3. Presented to steering committee
4. Answered questions
5. Made minor revisions

**Final Approval Meeting**:
- IT Head: ✅ Approved (technical approach sound)
- Marketing Head: ✅ Approved (meets customer needs)
- Operations Head: ✅ Approved (realistic timeline)
- Sponsor: ✅ Approved (within budget)

**PLAN BASELINED! Ready to execute! 🚀**

---

**Lessons from This Example**:
1. Systematic process works
2. Stakeholder involvement is key
3. Budget constraints are real (had to adjust)
4. Risk planning pays off
5. Getting buy-in takes time but worth it
6. Comprehensive planning enables smooth execution

---

## Summary

**Project Planning is THE most critical phase**. It determines project success more than any other phase.

**Golden Rules of Planning**:

1. **Involve stakeholders early** - Their buy-in is crucial
2. **Be realistic** - Optimistic plans fail
3. **Plan for risks** - They WILL happen
4. **Document everything** - Memory fails
5. **Get formal approval** - Avoid scope creep
6. **Communicate constantly** - Information is power
7. **Be flexible** - Plans change, adapt
8. **Use proven tools** - Gantt charts, RACI, WBS
9. **Don't over-plan** - Balance detail vs progress
10. **Celebrate milestones** - Keep team motivated

**Remember**: 
> "Hours spent in planning save days in execution!"

**Next Lecture**: We'll explore **Project Conception & Feasibility Studies** - how to evaluate if a project is even worth doing! 🚀

---

*End of Lectures 5 & 6*
