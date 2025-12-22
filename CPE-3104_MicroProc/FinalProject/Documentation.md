# Complete Teaching Guide for 8086 Classroom Power Control System

## Document Purpose
This document provides comprehensive context for an AI tutor to teach a student about their 8086-based microprocessor project. The student has provided their assembly code and needs help understanding the entire system - from basic concepts to advanced implementation details.

---

## Table of Contents
1. [Student Profile and Context](#student-profile-and-context)
2. [Project Overview](#project-overview)
3. [Critical Setup Information](#critical-setup-information)
4. [Hardware Architecture](#hardware-architecture)
5. [Detailed Port Address Map](#detailed-port-address-map)
6. [Address Decoding System](#address-decoding-system)
7. [8086 Microprocessor Fundamentals](#8086-microprocessor-fundamentals)
8. [8255A Programmable Peripheral Interface](#8255a-programmable-peripheral-interface)
9. [LCD Display Interface](#lcd-display-interface)
10. [Keypad Interface](#keypad-interface)
11. [Relay Control System](#relay-control-system)
12. [Software Architecture](#software-architecture)
13. [Password Security System](#password-security-system)
14. [Timer Safety System](#timer-safety-system)
15. [Common Programming Patterns](#common-programming-patterns)
16. [Troubleshooting Guide](#troubleshooting-guide)
17. [Study Questions and Exercises](#study-questions-and-exercises)

---

## Student Profile and Context

### Student Information
- **Username**: cedvtan13
- **Course**: CPE-3104 Microprocessor Systems (Third Year)
- **Repository**: cedvtan13/3rdYR (Information Engineering Codes)
- **Project Name**:  Classroom Power Control System
- **Learning Stage**: First-time microprocessor and assembly language student
- **Development Environment**: Proteus 8. 11 simulator with MASM32 assembler
- **Project Status**: Code is complete and functional

### Student's Learning Style
The student learns best through:
- **Step-by-step explanations** with clear cause-and-effect relationships
- **Visual analogies** (comparing circuits to everyday objects)
- **Practical examples** from their actual code
- **"Why" explanations** not just "what" or "how"
- **Building up** from fundamentals to complex concepts
- **Real-world context** for abstract concepts

### Common Confusion Points
Be prepared to clarify:
- Why memory and I/O are separate address spaces
- Why transistors are needed for relay control (current amplification)
- Why address decoding is needed for I/O but not memory in Proteus
- How the multiplexed address/data bus works
- When to use IN/OUT vs.  MOV instructions
- Read-modify-write pattern for partial port updates
- Why passwords are stored as ASCII instead of binary

---

## Project Overview

### What the System Does

**Classroom Power Control System** - A password-protected embedded system that manages three electrical power branches in a classroom: 

1. **AC Units** - Climate control systems
2. **Power Outlets** - Student/faculty device charging, projector power
3. **Lights** - Classroom lighting

### Key Features Implemented

#### Security Features
- 4-digit numeric password (0-9)
- No default password - mandatory first-time setup
- Double-entry confirmation (prevents typos)
- Password stored as ASCII characters for comparison
- Lock function - press # to require re-authentication
- Masked display (shows **** instead of actual digits)
- Unlimited login attempts (educational system)

#### Control Features
- Individual device toggle (turn each device ON/OFF independently)
- Shutdown all function (emergency cutoff)
- Real-time status display (shows current state of all devices)
- Closed-loop control (feedback verification via PORTB2)

#### Safety Features
- **Shutdown delay timer**:  0-9 minutes before power cuts
  - Purpose: Allows LCD projectors to cool down
  - Purpose: Gives time for safe classroom exit with lights on
  - Cancellable: Hardware button or # key aborts
- **Relay feedback verification**: Confirms relays actually switched
- **Default safe state**: All devices OFF on power-up/reset

#### User Interface
- 20×4 LCD display for all interactions
- 4×4 matrix keypad for input
- Visual countdown during timer operation
- Clear status indicators (1. AC: ON, 2.PWR: OFF, etc.)

---

## Critical Setup Information

### Proteus Configuration (MUST KNOW!)

#### Virtual Memory Setting - CRITICAL! 
**Before simulation, MUST set 8086 properties:**
