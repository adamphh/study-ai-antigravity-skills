# Magento 2 Agent Skills Template

This document defines a **ready-to-use agent skills specification** for building Magento 2 modules using an Agentic AI architecture (Planner – Executor – Critic).

Use this file as:
- Context for AI IDEs (Cursor, Claude, ChatGPT, etc.)
- A shared contract between human devs and AI agents
- A guardrail to prevent Magento anti-patterns

---

## 🎯 Goal

Enable an AI agent to **create, extend, and review Magento 2 modules safely**, following Magento conventions and real-world best practices.

---

## 🧠 Agent Roles

### Planner - Tech lead trong đầu AI - Nghĩ trước khi làm - không code
- Understands the business goal
- Chooses Magento patterns (plugin, observer, UI component, etc.)
- Breaks work into executable steps

### Executor - Dev thực hiện - code chính
- Creates files
- Writes code
- Modifies XML and PHP
- Call API
- Execute shell command
- Run Test
- Commit

### Critic - Review code
- Reviews architecture
- Detects Magento anti-patterns
- Validates conventions and performance risks
- Validates output
- review performance

---
Planner → Executor → Critic
              ↑        ↓
              ←── fix ──

---

## 📖 Understanding Skills (Planner)

### read_magento_version
**Purpose**: Detect Magento version & edition  
**Reads**: composer.json  
**Output**:
```json
{ "version": "2.4.x", "edition": "commerce|opensource" }
```

---

### summarize_existing_modules
**Purpose**: Detect related or conflicting modules  
**Scope**: app/code, vendor/*  
**Read-only**

---

### detect_module_pattern
**Purpose**: Decide correct Magento pattern  
**Output**:
- plugin
- observer
- ui_component
- cron
- api
- graphql

---

## 🏗️ Module Initialization Skills (Executor)

### create_magento_module_skeleton
**Input**:
```json
{
  "vendor": "MW",
  "module": "PromotionQR",
  "areas": ["frontend", "adminhtml"]
}
```

**Creates**:
- registration.php
- etc/module.xml
- composer.json

**Guards**:
- No overwrite if module exists
- PSR-4 compliant

---

### register_module
**Purpose**: Validate and register module.xml  
**Idempotent**

---

## ⚙️ Configuration Skills (XML)

### add_di_configuration
**Purpose**: Add DI plugin or preference  
**Files**:
- etc/di.xml
- etc/frontend/di.xml
- etc/adminhtml/di.xml

**Guard**:
- Respect existing plugins
- Avoid unnecessary around plugins

---

### add_routes
**Purpose**: Declare frontend/admin routes  
**Guard**:
- Prevent route collision

---

### add_acl_resource
**Purpose**: Add admin ACL  
**Guard**:
- No override of core ACL
- Correct tree hierarchy

---

## 🧩 Business Logic Skills

### create_controller
**Purpose**: Generate controller  
**Rules**:
- No heavy logic
- Use services via DI

---

### create_plugin
**Purpose**: Create before/after/around plugin  
**Rules**:
- Avoid around unless required
- Never swallow exceptions

---

### create_observer
**Purpose**: Create event observer  
**Rules**:
- Validate event exists
- Minimal logic only

---

## 🗄️ Database / Setup Skills

### create_schema_patch
**Purpose**: Create DB schema patch  
**Rules**:
- No InstallSchema
- Must be reversible

---

### add_index
**Purpose**: Add DB index  
**Rules**:
- Validate index usefulness
- Skip if exists

---

## 🖥️ Admin / UI Skills

### create_admin_grid
**Purpose**: Create UI Component grid  
**Rules**:
- Separate data provider
- No SQL in XML

---

### add_system_config
**Purpose**: Add system.xml config  
**Rules**:
- Default value required
- Clear scope

---

## 🔍 Validation & Review Skills (Critic)

### validate_magento_convention
**Checks**:
- Folder structure
- XML schema
- DI usage
- Naming conventions

---

### run_magento_compile
**Purpose**: Run di:compile (report only)

---

### review_module_design
**Detects**:
- God classes
- Service locator usage
- Plugin abuse
- Observer overuse

---

## 🧠 Composite Skill

### generate_magento_module
**Purpose**: From business goal → working module  
**Flow**:
1. Planner selects pattern
2. Executor builds module
3. Critic reviews output

**Restrictions**:
- Never deploy
- Never enable module automatically

---

## 🚫 Hard Guardrails

- No direct core hacks
- No production DB access
- No auto deploy
- No main branch push

---

## ✅ Usage Tip

Provide this file as context and say:

> "Follow magento_agent_skills.md strictly. Do not violate guardrails."

This turns the AI from a code generator into a **Magento-aware engineering agent**.

---

## 🧠 Final Note

Magento is hard because it is **distributed complexity**.

Agent skills turn that chaos into a controlled system.

