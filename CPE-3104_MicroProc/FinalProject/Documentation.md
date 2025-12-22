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
```
Right-click 8086 → Edit Properties
→ Internal Memory Size:  0x10000 (65536 bytes = 64KB)
```

**Why this matters:**
- Proteus 8086 model includes **virtual memory** inside the chip
- This eliminates need for external RAM/ROM chips
- Size 0x10000 = 64KB (sufficient for this project)
- Without this setting, program won't load or will crash

#### What Virtual Memory Contains
```
Memory Space (0x00000 - 0x0FFFF):
├─ Program code (~3-4 KB)
├─ Data segment (strings, variables, buffers ~1 KB)
├─ Stack (128 bytes)
└─ Unused space (~59 KB free)

This is SEPARATE from I/O space!
```

### Two Separate Address Spaces - KEY CONCEPT! 

#### Memory Space (Virtual - Inside 8086)
```
Access with:    MOV, PUSH, POP, CALL, JMP, LEA
Address range:   0x00000 - 0x0FFFF (64KB)
Signal:         M/IO = HIGH (1)
Location:       Inside Proteus 8086 model (virtual)
Purpose:        Store program code, data, stack
```

**Example instructions:**
```assembly
MOV AL, [SI]        ; Read from memory
MOV [DI], BL        ; Write to memory
LEA SI, STRING      ; Load memory address
CALL SUBROUTINE     ; Jump to code in memory
```

#### I/O Space (Physical - External Hardware)
```
Access with:   IN, OUT (ONLY these!)
Address range: 0x0000 - 0xFFFF (16-bit I/O addresses)
Signal:        M/IO = LOW (0)
Location:      External chips (8255A, 8253A)
Purpose:       Control hardware devices
```

**Example instructions:**
```assembly
IN AL, DX           ; Read from I/O port
OUT DX, AL          ; Write to I/O port
```

**NEVER use MOV with I/O ports!**
```assembly
❌ WRONG:  MOV AL, [0F0h]     ; This accesses MEMORY, not I/O! 
✓ RIGHT: IN AL, DX           ; DX = 0xF0, reads I/O port
```

---

## Hardware Architecture

### Complete Component List

#### Microprocessor
- **8086 CPU**:  16-bit processor, main controller
  - Clock:  5-10 MHz
  - Mode:  Minimum mode (MN/MX = 1)
  - 20-bit address bus (1MB addressable)
  - 16-bit data bus (multiplexed with lower address)

#### Peripheral Interface Chips (PPIs)
1. **8255A #1** @ 0xF0: LCD and Keypad Interface
2. **8255A #2** @ 0xE0: Relay Control and Feedback
3. **8255A #3** @ 0xC0: Auxiliary (delay generation)
4. **8253A Timer** @ 0xD0: Configured but minimally used

#### Address Decoding
- **74LS138**:  3-to-8 decoder (I/O address decoding ONLY)
- **74LS373**:  Octal latch (demultiplexes address/data bus)

#### Input Devices
- **MM74C922**: 16-key encoder chip for 4×4 matrix keypad
  - Hardware debouncing built-in
  - Outputs 4-bit key code (ABCD)
  - Data Available flag (DA)
- **LM044L**: 20×4 character LCD (HD44780 compatible)
  - 20 characters per line, 4 lines
  - 8-bit parallel interface

#### Output Devices
- **3× SPDT Relays**: Control high-voltage (220V AC) circuits
  - Relay 1: AC Units
  - Relay 2: Power Outlets
  - Relay 3: Lights

#### Relay Driver Circuit Components
- **2N2222 NPN Transistor** (3 units): Current amplifier
  - Why needed: 8255A outputs ~2mA, relay needs ~100mA
  - Function: Amplifies control signal
  - Current gain (β): 50-200×
- **1kΩ Resistor** (3 units): Base current limiter
  - Limits base current to safe level (~4mA)
  - Protects 8255A from overcurrent
- **Flyback Diode** (3 units): Surge protection
  - Protects transistor from inductive kickback
  - Clamps voltage spikes when relay turns off

#### Support Components
- Crystal oscillator (5-10 MHz)
- Decoupling capacitors (0.1µF)
- Pull-up/pull-down resistors
- Power supply (+5V, GND)

---

## Detailed Port Address Map

### 8255A #1 - LCD and Keypad Interface (Base 0xF0)

| PORT NAME | ADDRESS | DIRECTION | BITS USED | CONNECTION |
|-----------|---------|-----------|-----------|------------|
| PORTA | 0xF0 | OUTPUT | 0-7 | LCD D0-D7 (data lines) |
| PORTB | 0xF2 | OUTPUT | 0-1 | LCD RS (bit 0), E (bit 1) |
| PORTC | 0xF4 | INPUT | 0-4 | Keypad ABCD (0-3), DA (4) |
| COM_REG | 0xF6 | WRITE | - | Control register (0x89) |

**Configuration Word 0x89 (10001001b):**
```
Bit 7: 1 = Mode set
Bits 6-5: 00 = Mode 0 (basic I/O)
Bit 4: 0 = Port A OUTPUT (LCD data)
Bit 3: 1 = Port C upper INPUT (keypad DA)
Bit 2: 0 = Mode 0
Bit 1: 0 = Port B OUTPUT (LCD control)
Bit 0: 1 = Port C lower INPUT (keypad ABCD)
```

**Physical connections:**
```
LCD Side: 
PA0 → LCD D0 (pin 7)    PB0 → LCD RS (pin 4)
PA1 → LCD D1 (pin 8)    PB1 → LCD E  (pin 6)
PA2 → LCD D2 (pin 9)    LCD RW (pin 5) → GND
PA3 → LCD D3 (pin 10)
PA4 → LCD D4 (pin 11)   Keypad Side:
PA5 → LCD D5 (pin 12)   PC0 ← MM74C922 A (LSB)
PA6 → LCD D6 (pin 13)   PC1 ← MM74C922 B
PA7 → LCD D7 (pin 14)   PC2 ← MM74C922 C
                        PC3 ← MM74C922 D (MSB)
                        PC4 ← MM74C922 DA (flag)
```

### 8255A #2 - Relay Control (Base 0xE0)

| PORT NAME | ADDRESS | DIRECTION | BITS USED | CONNECTION |
|-----------|---------|-----------|-----------|------------|
| PORTA2 | 0xE0 | OUTPUT | 0-2 | Relay drivers |
| PORTB2 | 0xE2 | INPUT | 0-2 | Relay feedback sensors |
| PORTC2 | 0xE4 | INPUT | 0 | Timer cancel button |
| COM_REG2 | 0xE6 | WRITE | - | Control register (0x89) |

**Port A2 Bit Assignment (Relay Control):**
```
Bit 0: AC Units relay control (1=ON, 0=OFF)
Bit 1: Power Outlets relay control (1=ON, 0=OFF)
Bit 2: Lights relay control (1=ON, 0=OFF)
Bits 3-7: Unused
```

**Port B2 Bit Assignment (Relay Feedback):**
```
Bit 0: AC Units relay actual state
Bit 1: Power Outlets relay actual state
Bit 2: Lights relay actual state
Purpose: Verify relay actually switched (closed-loop control)
```

### 8255A #3 - Auxiliary (Base 0xC0)

| PORT NAME | ADDRESS | DIRECTION | CONNECTION |
|-----------|---------|-----------|------------|
| PORTA3 | 0xC0 | OUTPUT | Delay generation |
| PORTB3 | 0xC2 | - | Grounded (unused) |
| PORTC3 | 0xC4 | - | Grounded (unused) |
| COM_REG3 | 0xC6 | WRITE | Control register |

### 8253A Timer (Base 0xD0)

| REGISTER | ADDRESS | PURPOSE |
|----------|---------|---------|
| Counter 0 | 0xD0 | Not actively used |
| Counter 1 | 0xD2 | Not actively used |
| Counter 2 | 0xD4 | Not actively used |
| COMT | 0xD6 | Control register (0x37) |

---

## Address Decoding System

### Why Address Decoding is Needed

**The Problem:**
You have 4 I/O devices (three 8255As + one 8253A). Without decoding, all would respond to the same addresses simultaneously → **BUS CONFLICT** → data corruption, system crash. 

**The Solution:**
74LS138 decoder ensures **only ONE device is active at a time**. 

### 74LS138 Configuration

#### Input Connections
```
74LS138 Input Pins:
A ← Address bit 3 (A3)
B ← Address bit 4 (A4)
C ← Address bit 5 (A5)

These 3 bits create 8 possible combinations (Y0-Y7 outputs)
```

#### Enable Connections (All must be satisfied)
```
E1 ← Address bit 6 (A6)         [Active HIGH - must be 1]
E2 ← M/IO signal                [Active LOW - must be 0]
E3 ← NOT A7 (inverted A7)       [Active LOW - must be 0, so A7 must be 1]

Combined requirement: 
- A7 = 1 (bit 7 set)
- A6 = 1 (bit 6 set)
- M/IO = 0 (I/O operation, not memory)

Result:  Decoder only activates for I/O operations in range 0xC0-0xFF
```

#### Why M/IO is Connected to E2
**This is the KEY to separating memory from I/O! **

```
When executing:  MOV AL, [1000h]  (memory access)
- M/IO = 1 (HIGH)
- E2 not satisfied (needs LOW)
- 74LS138 disabled
- I/O devices don't respond
- Only virtual memory responds ✓

When executing: IN AL, DX  (I/O access, DX = 0xF0)
- M/IO = 0 (LOW)
- E2 satisfied ✓
- A7=1, A6=1 also satisfied
- 74LS138 enabled
- Decodes A5A4A3 to select device ✓
```

### Output Mapping

| A5 A4 A3 | CBA | Output | Address | Device Selected |
|----------|-----|--------|---------|-----------------|
| 0 0 0 | 000 | Y0 | 0xC0 | 8255A #3 (Auxiliary) |
| 0 0 1 | 001 | Y1 | 0xC8 | Not used |
| 0 1 0 | 010 | Y2 | 0xD0 | 8253A Timer |
| 0 1 1 | 011 | Y3 | 0xD8 | Not used |
| 1 0 0 | 100 | Y4 | 0xE0 | 8255A #2 (Relays) |
| 1 0 1 | 101 | Y5 | 0xE8 | Not used |
| 1 1 0 | 110 | Y6 | 0xF0 | 8255A #1 (LCD/Keypad) |
| 1 1 1 | 111 | Y7 | 0xF8 | Not used |

### Example:  How Address 0xF0 is Decoded

```
Address 0xF0 = 11110000 binary

Bit 7: 1 → A7 = 1 → Inverted = 0 → E3 satisfied ✓
Bit 6: 1 → A6 = 1 → E1 satisfied ✓
M/IO:  0 → (I/O operation) → E2 satisfied ✓

All enables active → Decoder works! 

Bit 5: 1 → C = 1
Bit 4: 1 → B = 1
Bit 3: 0 → A = 0

CBA = 110 → Output Y6 activates (goes LOW)

Y6 connected to 8255A #1 CS (Chip Select)
CS goes LOW → 8255A #1 selected
Other chips remain disabled (CS HIGH)

Bits 1-0: 00 → Selects Port A within 8255A #1

Result: Access to 8255A #1 Port A (LCD data) ✓
```

---

## 8086 Microprocessor Fundamentals

### Register Set Overview

#### General Purpose Registers (16-bit, splittable)

**AX (Accumulator) = AH + AL**
```
Primary uses:
- Arithmetic operations
- I/O operations (IN AL, DX / OUT DX, AL)
- Function return values

In your code:
- Holds LCD commands/data before output
- Receives keypad input
- Stores characters for display
```

**BX (Base) = BH + BL**
```
Primary uses:
- Base address pointer
- General storage
- Counter in loops

In your code:
- Delay loop counters (DELAY_1MS)
- Temporary storage for key codes
```

**CX (Count) = CH + CL**
```
Primary uses:
- Loop counter (LOOP instruction)
- String/array operations
- Repetition count

In your code:
- Password digit counter (CX = 4 for 4 digits)
- Comparison loop counter
- Delay loop iterations

Special:  LOOP instruction auto-decrements CX and jumps if CX ≠ 0
```

**DX (Data) = DH + DL**
```
Primary uses:
- MUST be used for I/O port addresses
- Extended arithmetic operations

In your code:
- Always holds port address for IN/OUT
- Example: MOV DX, 0xF0 / OUT DX, AL

Why DX for ports?
IN AL, port - only works for ports 0-255
IN AL, DX - works for all ports 0-65535
All your ports (0xC0-0xFF) require DX
```

#### Index and Pointer Registers (16-bit only)

**SI (Source Index)**
```
Purpose: Points to source data when reading

Usage pattern:
LEA SI, STRING      ; SI = address of string
MOV AL, [SI]        ; Read byte at address SI
INC SI              ; Move to next byte

In your code:
- Points to strings for PRINT_STRING
- Points to password buffers for reading
- Iterates through character arrays
```

**DI (Destination Index)**
```
Purpose: Points to destination when writing

Usage pattern:
LEA DI, BUFFER      ; DI = address of buffer
MOV [DI], AL        ; Write byte to address DI
INC DI              ; Move to next position

In your code:
- Points to password buffers for writing
- Destination for copying passwords
```

**SP (Stack Pointer)**
```
Purpose: Points to top of stack
Automatically managed: 
- PUSH decrements SP, stores value
- POP loads value, increments SP
- CALL pushes return address
- RET pops return address
```

#### Segment Registers (16-bit)

**DS (Data Segment) - MUST BE INITIALIZED! **
```
Points to:  Data variables, strings, buffers
MUST BE INITIALIZED: 

START:
    MOV AX, DATA    ; Get DATA segment address
    MOV DS, AX      ; Set DS register

Without this: 
- LEA SI, STRING won't find string
- MOV AL, [variable] accesses wrong memory
- Program crashes or behaves erratically
```

#### Special Registers

**IP (Instruction Pointer)**
```
Function: Points to next instruction to execute
Modified by: 
- JMP:  Changes IP to jump target
- CALL: Pushes current IP, loads new IP
- RET:  Pops IP from stack
- Sequential:  Auto-increments after each instruction
```

**FLAGS (Status Register)**
```
Important flags in your project: 

ZF (Zero Flag):
- Set (1) when result = 0
- Used by:  JE, JZ (jump if zero)
- Example: CMP AL, BL → if equal, ZF=1

Flags are set automatically by: 
- Arithmetic:  ADD, SUB, INC, DEC
- Logic: AND, OR, XOR, TEST
- Comparison: CMP

Flags are checked by:
- Conditional jumps:  JE, JNE, JZ, JNZ, JL, JG, etc.
```

### Essential Assembly Instructions

#### Data Movement

**MOV dest, source** - Copy data
```assembly
MOV AL, 5          ; AL = 5 (immediate)
MOV AL, BL         ; AL = BL (register)
MOV AL, [SI]       ; AL = byte at memory address SI
MOV [DI], AL       ; Memory at DI = AL

Rules:
- Cannot MOV [SI], [DI] (memory to memory)
- Must be same size (AL to BL ok, AL to BX not ok)
- Source unchanged
```

**LEA reg, memory** - Load Effective Address
```assembly
LEA SI, STRING     ; SI = address of STRING
; Equivalent to:  MOV SI, OFFSET STRING

Use LEA when you want the ADDRESS
Use MOV when you want the VALUE at that address
```

**IN AL, DX / OUT DX, AL** - I/O operations
```assembly
MOV DX, 0xF4       ; Port address
IN AL, DX          ; Read byte from port into AL

MOV DX, 0xF0       ; Port address
MOV AL, 'A'        ; Data to write
OUT DX, AL         ; Write AL to port
```

#### Arithmetic

**ADD dest, source** - Addition
```assembly
ADD AL, 5          ; AL = AL + 5
ADD AL, BL         ; AL = AL + BL
```

**INC reg/mem** - Increment by 1
```assembly
INC SI             ; SI = SI + 1
INC CX             ; CX = CX + 1
Faster than ADD reg, 1
```

#### Logical Operations

**AND dest, source** - Bitwise AND
```assembly
AND AL, 0Fh        ; Keep lower 4 bits, clear upper 4

Example: 
AL = 11010101b
AND AL, 00001111b
Result: 00000101b (masked to lower nibble)

Use:  Extract specific bits, clear bits
```

**OR dest, source** - Bitwise OR
```assembly
OR AL, 01h         ; Set bit 0

Example:
AL = 00000100b
OR AL, 00000001b
Result: 00000101b (bit 0 now set)

Use: Set specific bits
```

**TEST dest, source** - Bitwise AND without modifying
```assembly
TEST AL, 10h       ; Check if bit 4 is set
JZ BIT_CLEAR       ; Jump if bit 4 = 0
JNZ BIT_SET        ; Jump if bit 4 = 1

Advantage: Sets flags but doesn't change AL
```

#### Comparison and Jumps

**CMP value1, value2** - Compare
```assembly
CMP AL, 5          ; Compare AL with 5
JE EQUAL           ; Jump if AL = 5
JNE NOT_EQUAL      ; Jump if AL ≠ 5

How it works:
- Internally does: value1 - value2
- Sets flags based on result
- Doesn't store result (values unchanged)
- If result = 0 → ZF=1 (they're equal)
```

**Conditional Jumps:**
```assembly
JE  label          ; Jump if Equal (ZF=1)
JNE label          ; Jump if Not Equal (ZF=0)
JZ  label          ; Jump if Zero (ZF=1)
JNZ label          ; Jump if Not Zero (ZF=0)
JL  label          ; Jump if Less (signed)
JG  label          ; Jump if Greater (signed)
```

**CALL / RET** - Subroutine control
```assembly
CALL INIT_LCD      ; Jump to INIT_LCD, save return address

INIT_LCD:
    ; ...  do initialization ...
    RET            ; Pop return address, jump back
```

**LOOP label** - Loop with CX counter
```assembly
    MOV CX, 4          ; Loop 4 times
REPEAT:
    ; ... body ...
    LOOP REPEAT        ; CX--, jump if CX≠0
```

---

## 8255A Programmable Peripheral Interface

### What It Does
8255A is an **I/O expander**:
- Gives 8086 **24 additional I/O pins** (3 ports × 8 bits)
- Each port independently configurable as input or output
- Simple programming interface (just write to ports)
- Industry standard chip (since 1970s)

### Control Register (COM_REG) - MUST CONFIGURE!

**Before using 8255A, MUST write control word:**

#### Control Word Format (Mode 0)
```
Bit 7:    1 = Mode Set flag (MUST BE 1!)
Bits 6-5: 00 = Mode 0 (basic I/O)
Bit 4:    Port A direction (0=OUT, 1=IN)
Bit 3:    Port C upper direction (0=OUT, 1=IN)
Bit 2:    0 = Mode 0 for Group B
Bit 1:    Port B direction (0=OUT, 1=IN)
Bit 0:    Port C lower direction (0=OUT, 1=IN)

Direction:  0 = OUTPUT, 1 = INPUT
```

#### Common Configuration:  0x89
```
0x89 = 10001001b

Bit 7: 1 (Mode set) ✓
Bit 4: 0 (Port A = OUTPUT) ✓
Bit 3: 1 (Port C upper = INPUT) ✓
Bit 1: 0 (Port B = OUTPUT) ✓
Bit 0: 1 (Port C lower = INPUT) ✓

Result: 
- Port A: 8 outputs (LCD data)
- Port B: 8 outputs (LCD control)
- Port C: 8 inputs (keypad)
```

**Your initialization code:**
```assembly
INIT_DEVICES:
    MOV DX, COM_REG        ; 0xF6
    MOV AL, 89h            ; Configuration word
    OUT DX, AL             ; Configure 8255A #1
```

### Read-Modify-Write Pattern - CRITICAL!

**The Problem:**
Writing to a port **overwrites all 8 bits**.  If you want to change one bit, you'll accidentally change others.

**Solution:  Read-Modify-Write**
```assembly
✓ CORRECT: 
MOV DX, PORTA2
IN AL, DX              ; Read current state
OR AL, 001b            ; Set bit 0
OUT DX, AL             ; Write back (preserves other bits)
```

**To turn OFF (clear bit):**
```assembly
MOV DX, PORTA2
IN AL, DX              ; Read current state
AND AL, 11111110b      ; Clear bit 0 (mask:  all 1s except bit 0)
OUT DX, AL             ; Write back
```

---

## LCD Display Interface

### Display Specifications
- **Size**: 20 characters × 4 lines = 80 characters total
- **Controller**: HD44780 (industry standard)
- **Interface**: 8-bit parallel (D0-D7)

### Control Signals Explained

#### RS - Register Select (Port B bit 0)
```
RS = 0: Instruction/Command mode
       - Sending commands to LCD
       - Examples: clear screen, set cursor, configure

RS = 1: Data/Character mode
       - Sending characters to display
       - Examples: 'A', '1', '*', etc.
```

#### E - Enable (Port B bit 1)
```
Function: Strobe signal that tells LCD to read data

Timing sequence:
1. Put data on D0-D7 (Port A)
2. Set E = 1 (HIGH)
3. Wait (minimum 450ns)
4. Set E = 0 (LOW)
5. Falling edge (HIGH→LOW) triggers LCD to latch data
```

#### RW - Read/Write (Tied to GND)
```
Your circuit: RW permanently grounded (always 0)

Why?  Simplification:
- Write-only mode
- Can't read busy flag from LCD
- Must use delays instead
- Simpler hardware
```

### LCD Memory Map (DDRAM Addresses)

| LINE | COLUMNS | DDRAM ADDRESS | COMMAND TO SET CURSOR |
|------|---------|---------------|----------------------|
| 1 | 0-19 | 0x00-0x13 | 0x80 + column |
| 2 | 0-19 | 0x40-0x53 | 0xC0 + column |
| 3 | 0-19 | 0x14-0x27 | 0x94 + column |
| 4 | 0-19 | 0x54-0x67 | 0xD4 + column |

### Common LCD Commands

| COMMAND | HEX | FUNCTION |
|---------|-----|----------|
| Clear | 0x01 | Clear display, cursor home |
| Entry | 0x06 | Increment cursor, no shift |
| Display | 0x0C | Display ON, cursor OFF |
| Function | 0x38 | 8-bit, 2-line, 5×7 font |
| SetAddr | 0x80+ | Set cursor position |

### Initialization Sequence (CRITICAL!)

```assembly
INIT_LCD: 
    MOV AL, 38h             ; Function Set:  8-bit, 2-line, 5×7
    CALL INST_CTRL
    
    MOV AL, 08h             ; Display off temporarily
    CALL INST_CTRL
    
    MOV AL, 01h             ; Clear display
    CALL INST_CTRL
    
    MOV AL, 06h             ; Entry mode: increment cursor
    CALL INST_CTRL
    
    MOV AL, 0Ch             ; Display on, cursor off
    CALL INST_CTRL
    
    RET
```

### INST_CTRL Routine (Send Command)

```assembly
INST_CTRL:
    PUSH AX
    
    MOV DX, PORTA           ; Output command to data lines
    OUT DX, AL
    
    MOV DX, PORTB           ; Set RS=0, E=1
    MOV AL, 02h
    OUT DX, AL
    
    CALL DELAY1             ; Hold enable high
    
    MOV DX, PORTB           ; Set RS=0, E=0 (falling edge)
    MOV AL, 00h
    OUT DX, AL
    
    POP AX
    RET
```

### DATA_CTRL Routine (Send Character)

```assembly
DATA_CTRL:
    PUSH AX
    
    MOV DX, PORTA           ; Output character
    OUT DX, AL
    
    MOV DX, PORTB           ; Set RS=1, E=1
    MOV AL, 03h
    OUT DX, AL
    
    CALL DELAY1
    
    MOV DX, PORTB           ; Set RS=1, E=0 (falling edge)
    MOV AL, 01h
    OUT DX, AL
    
    POP AX
    RET
```

### PRINT_STRING Routine

```assembly
PRINT_STRING:
    MOV AL, [SI]            ; Get character
    CMP AL, "$"             ; Check terminator
    JE PS_DONE
    
    CALL DATA_CTRL          ; Display character
    INC SI                  ; Next character
    JMP PRINT_STRING
    
PS_DONE:
    RET
```

---

## Keypad Interface

### MM74C922 Keypad Encoder

**What it does:**
- Scans 4×4 matrix keypad automatically
- Provides hardware debouncing (10-50ms)
- Outputs 4-bit encoded key value (ABCD)
- Provides Data Available flag (DA)

### Physical Connection to 8255A #1 Port C

```
MM74C922 OUTPUT → 8255A #1 PORT C
────────────────────────────────
A (LSB) → PC0
B       → PC1
C       → PC2
D (MSB) → PC3
DA      → PC4
```

### Key Encoding Table

| KEY | ABCD | HEX | FUNCTION |
|-----|------|-----|----------|
| 1 | 0000 | 0x0 | AC Units toggle |
| 2 | 0001 | 0x1 | Power Outlets toggle |
| 3 | 0010 | 0x2 | Lights toggle |
| 4 | 0100 | 0x4 | Shutdown All |
| 5 | 0101 | 0x5 | Timer 5 minutes |
| 6 | 0110 | 0x6 | Timer 6 minutes |
| 7 | 1000 | 0x8 | Timer 7 minutes |
| 8 | 1001 | 0x9 | Timer 8 minutes |
| 9 | 1010 | 0xA | Timer 9 minutes |
| * | 1100 | 0xC | Enter/Confirm |
| 0 | 1101 | 0xD | Zero/Timer 0 min |
| # | 1110 | 0xE | Back/Cancel/Lock |

### Reading the Keypad

```assembly
; Read Port C
MOV DX, PORTC
IN AL, DX           ; AL = PCxxxxDADCBA

; Check Data Available flag (bit 4)
TEST AL, 10h        ; Check if bit 4 is set
JZ NO_KEY           ; If 0, no key pressed

; Get key code (bits 0-3)
AND AL, 0Fh         ; Mask to get lower 4 bits
; Now AL contains key code (0x0 to 0xF)
```

### Debouncing Strategy

#### Hardware Debouncing (MM74C922)
- Built-in RC circuit debounces mechanical bounce
- Typical debounce time: 10-50ms

#### Software Debouncing (Your Code)
```
WAIT_FOR_KEYPRESS_FIXED routine:
1. Wait for DA=0 (no key)
2. Delay 20ms
3. Wait for DA=1 (key pressed)
4. Delay 20ms (verify stable)
5. Read key code
6. Wait for DA=0 (key released)
7. Delay 20ms
8. Return key code

Why both? 
- MM74C922: Handles mechanical bounce
- Software: Handles electrical noise
- Combined: Extremely robust
```

---

## Relay Control System

### What Relays Do

**Relay** = Electromagnetically controlled switch

**Purpose**: Allow low-voltage, low-current signals to control high-voltage, high-current circuits safely. 

```
Control side:              Load side:
5V, 2mA from 8086         220V AC, 10A to device
     ↓                          ↑
[8255A] → [Transistor] → [Relay Coil] → [Relay Contacts]
```

### Why Transistor is Needed - Current Amplification

**The Problem:**
```
8255A can provide:     ~2 mA
Relay coil needs:    ~100 mA
────────────────────────────
Shortfall:             -98 mA  NOT ENOUGH! 
```

**The Solution:  2N2222 NPN Transistor**

```
Function: Current amplifier

Small base current (2-4 mA) →
Transistor amplifies →
Large collector current (100 mA) →
Relay coil energizes ✓

Current gain (β): 50-200×
Example: 4 mA × 50 = 200 mA (more than enough!)
```

### Complete Relay Driver Circuit

```
                    +5V
                     │
                 [Relay Coil]
                     │
              ┌──────┴──────┐
              │             │
          [Flyback      Collector
           Diode]           │
              │         ┌───┴───┐
             GND        │ 2N2222│
                        │       │
              ┌─────────┤ Base  │
              │         └───┬───┘
           [1kΩ]           │
         Resistor      Emitter
              │            │
8255A PA0 ────┴────────────┴──── GND
```

### Component Functions

**1kΩ Base Resistor:**
```
Purpose: Limit base current to safe level

Calculation: 
Voltage = 5V - 0.7V = 4.3V (Vbe drop)
Current = 4.3V / 1kΩ = 4.3 mA

This is safe for 8255A (under 10 mA max)
And provides enough current to saturate transistor
```

**Flyback Diode:**
```
Purpose: Protect transistor from voltage spikes

When relay turns OFF:
- Coil is an inductor
- Current suddenly stops
- Inductor generates large voltage spike (100V+)
- Spike can destroy transistor

Diode solution:
- Provides path for current to circulate
- Clamps voltage to safe level (~0.7V)
- Energy dissipates harmlessly
- Transistor protected ✓
```

### Operation States

**Relay OFF (8255A output = 0V):**
```
8255A PA0 = 0V →
Base current = 0 →
Transistor OFF (open switch) →
No collector current →
Relay coil = NO CURRENT →
Relay contacts = OPEN →
Device = OFF
```

**Relay ON (8255A output = 5V):**
```
8255A PA0 = 5V →
Base current = 4.3 mA →
Transistor ON (closed switch) →
Collector current = 100+ mA →
Relay coil = ENERGIZED →
Relay contacts = CLOSED →
Device = ON
```

### Control vs.  Feedback (Closed-Loop Control)

**PORTA2 - Control Output:**
```
Bit 0: Command to AC relay (1=turn on, 0=turn off)
Bit 1: Command to Outlet relay
Bit 2: Command to Lights relay
```

**PORTB2 - Feedback Input:**
```
Bit 0: Actual AC relay state (1=confirmed on)
Bit 1: Actual Outlet relay state
Bit 2: Actual Lights relay state
```

**Why Feedback Matters:**
- Verifies relay actually switched
- Detects stuck relays or driver failures
- Provides accurate status display
- Enables closed-loop control

### Control Example from Your Code

```assembly
; Turn ON AC relay
MOV DX, PORTA2
IN AL, DX              ; Read current state
OR AL, 001b            ; Set bit 0
OUT DX, AL             ; Send command

; Verify it turned on
MOV DX, PORTB2
IN AL, DX              ; Read feedback
AND AL, 01h            ; Check bit 0
JNZ AC_ON_CONFIRMED    ; If set, relay is on
```

---

## Software Architecture

### Program Flow Overview

```
1. START
   ├─ Initialize data segment
   ├─ Clear all registers
   └─ Jump to INIT_DEVICES

2. INIT_DEVICES
   ├─ Configure 8255A #1 (0x89)
   ├─ Configure 8255A #2 (0x89)
   ├─ Configure 8253A (0x37)
   ├─ Turn off all relays (safety)
   ├─ Initialize LCD (INIT_LCD)
   └─ Jump to SET_PASSWORD_MODE

3. SET_PASSWORD_MODE (First-time setup)
   ├─ Display "SET NEW PASSWORD:"
   ├─ User enters 4 digits → PASS_BUF
   ├─ Display asterisks for security
   ├─ Display "CONFIRM PASSWORD:"
   ├─ User re-enters → CONFIRM_BUF
   ├─ Compare buffers byte-by-byte
   ├─ If match:  Copy to NEW_PASS, set flag
   ├─ If mismatch: Show error, restart
   └─ Jump to SEC_SYS_START

4. SEC_SYS_START (Login)
   ├─ Display "ENTER PASSWORD:"
   ├─ User enters 4 digits → CONFIRM_BUF
   ├─ Compare with NEW_PASS
   ├─ If correct: Jump to MENU_STARTUP
   └─ If incorrect: "ACCESS DENIED", retry

5. MENU_STARTUP (Main menu)
   ├─ Clear screen
   ├─ Display "PRESS # TO LOCK"
   ├─ Read PORTB2 (relay feedback)
   ├─ Display device states: 
   │   Line 1: Lock prompt
   │   Line 2: AC status, Outlet status
   │   Line 3: Lights status
   │   Line 4: Shutdown all option
   └─ Jump to RELAY_CONTROL

6. RELAY_CONTROL (Process input)
   ├─ Wait for keypress
   ├─ Key 1: Toggle AC
   ├─ Key 2: Toggle Outlet
   ├─ Key 3: Toggle Lights
   ├─ Key 4: Shutdown all
   ├─ Key #: Lock system
   └─ Invalid:  Ignore, wait again

7. Device Toggle Logic
   ├─ Read PORTB2 to check current state
   ├─ If OFF: Turn ON
   ├─ If ON:  Enter TIMER mode
   └─ Return to MENU_STARTUP

8. TIMER (Shutdown delay)
   ├─ Display "SET TIMER:  0-9 MIN"
   ├─ User selects minutes
   ├─ Press * to start countdown
   ├─ Press # to cancel
   ├─ Visual countdown
   ├─ Check cancel button
   └─ Execute shutdown when expires
```

### Key Subroutines

**WAIT_FOR_KEYPRESS_FIXED:**
```
Purpose: Read one key with debouncing
Process:
1. Wait for no key (DA=0)
2. Debounce delay (20ms)
3. Wait for key press (DA=1)
4. Debounce delay (20ms)
5. Read key code (PORTC bits 0-3)
6. Wait for release (DA=0)
7. Debounce delay (20ms)
8. Return key code in AL
```

**INIT_LCD:**
```
Purpose: Initialize LCD for use
Sequence:
1. Send 0x38 (8-bit, 2-line, 5×7 font)
2. Send 0x08 (display off)
3. Send 0x01 (clear display)
4. Send 0x06 (entry mode: increment)
5. Send 0x0C (display on, cursor off)
```

**PRINT_STRING:**
```
Purpose: Display null-terminated string
Process:
1. Read character from [SI]
2. If '$' terminator, done
3. Call DATA_CTRL to display
4. Increment SI
5. Loop to step 1
```

**CLS (Clear Screen):**
```
Purpose: Clear all 4 LCD lines
Process:
1. Set cursor to line 1 (0x80)
2. Print 20 spaces
3. Repeat for lines 2-4
```

---

## Password Security System

### Storage Format

**Passwords stored as 4 ASCII characters, not binary:**
```
Key code '1' (0x01) → Stored as ASCII '1' (0x31)
Key code '5' (0x05) → Stored as ASCII '5' (0x35)
```

### Conversion Process

```assembly
; Convert key code to ASCII
CMP AL, 0Dh         ; Is it key 0? 
JNE NOT_ZERO
MOV AL, '0'         ; ASCII '0' (0x30)
JMP STORE

NOT_ZERO:
ADD AL, '0'         ; Convert 1-9: add 0x30
                    ; Example: 5 (0x05) + '0' (0x30) = '5' (0x35)
```

### Password Buffers

```
PASS_BUF:      Temporary during password entry
CONFIRM_BUF:   Temporary during confirmation
NEW_PASS:     Permanent storage (4 ASCII chars + '$')
```

### Comparison Algorithm

```assembly
; Compare two passwords
MOV CX, 04h                 ; 4 characters
MOV SI, OFFSET PASS_BUF
MOV DI, OFFSET CONFIRM_BUF

COMPARE_LOOP:
    MOV AL, [SI]            ; Get char from buffer 1
    MOV BL, [DI]            ; Get char from buffer 2
    CMP AL, BL              ; Compare
    JNE DIFFERENT           ; Not equal
    INC SI
    INC DI
    LOOP COMPARE_LOOP       ; Repeat 4 times

; If here, all 4 characters matched
```

### Security Features
1. **Masked display**: Shows **** instead of digits
2. **Double-entry**: Must enter twice to confirm
3. **No default password**: Forces custom setup
4. **Lock function**: Press # to require re-authentication
5. **Unlimited retries**: No lockout (educational)

---

## Timer Safety System

### Purpose of Shutdown Delay

**Equipment Protection:**
- LCD projectors need cooling time
- Computers should shut down gracefully
- Lights stay on for safe classroom exit

**Operation:**
1. User selects 0-9 minutes
2. Visual countdown on LCD
3. Can cancel anytime (# key or hardware button)
4. Power cuts after timer expires

### Timer Implementation

**Minute Selection:**
```assembly
TIMER: 
    CALL CLS
    ; Display "SET TIMER: 0-9 MIN"
    
TIMER_INPUT_LOOP:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    CMP AL, 0Dh         ; Key 0?
    JE M0               ; Set 0 minutes
    
    CMP AL, 05h         ; Key 5? 
    JE M5               ; Set 5 minutes
    
    CMP AL, 0Ch         ; Key *?
    JE TIMER_START      ; Start countdown
    
    CMP AL, 0Eh         ; Key #?
    JE MENU_STARTUP     ; Cancel, go back
```

**Countdown Loop:**
```assembly
TIMER_SECONDS:
    MOV DX, 05h         ; 5 iterations per minute
    
SEC_DELAY:
    PUSH DX
    MOV DX, PORTC2      ; Check cancel button
    IN AL, DX
    CMP AL, 00h
    JE CANCEL           ; If pressed, cancel timer
    POP DX
    
    CALL DELAY          ; Wait
    DEC DX
    CMP DX, 00h
    JE DONE
    JMP SEC_DELAY
    
DONE:
    RET
```

### Cancel Function

**Two ways to cancel:**
1. Press # key on keypad
2. Press hardware cancel button (PORTC2 bit 0)

```assembly
CANCEL: 
    CALL CLS
    ; Display "ACTION STOPPED"
    CALL DELAY_RELAY
    JMP MENU_STARTUP
```

---

## Common Programming Patterns

### Bit Manipulation

**Set a bit (turn ON):**
```assembly
OR AL, 00000100b    ; Set bit 2
```

**Clear a bit (turn OFF):**
```assembly
AND AL, 11111011b   ; Clear bit 2 (all 1s except target)
```

**Toggle a bit:**
```assembly
XOR AL, 00000100b   ; Flip bit 2
```

**Test a bit:**
```assembly
TEST AL, 00000100b  ; Check bit 2
JZ BIT_WAS_ZERO
JNZ BIT_WAS_ONE
```

### Delay Generation

**Software delay:**
```assembly
DELAY_1MS:
    MOV DX, PORTA3      ; I/O operations take time
    MOV AL, 0CFH
    OUT DX, AL
    MOV AL, 07H
    OUT DX, AL
    DEC BX              ; Counter
    JNZ DELAY_1MS
    RET
```

### Cursor Positioning

```assembly
; Display at Line 2, Column 5
MOV AL, 0C0h        ; Line 2 base
ADD AL, 05h         ; Add column
CALL INST_CTRL      ; Set cursor

; Write character
MOV AL, '*'
CALL DATA_CTRL
```

### String Display

```assembly
; Position cursor
MOV AL, 80h         ; Line 1, column 0
CALL INST_CTRL

; Display string
LEA SI, MESSAGE
CALL PRINT_STRING
```

---

## Troubleshooting Guide

### Common Proteus Issues

#### LCD Shows Garbage
**Causes:**
- Not initialized properly
- Contrast voltage wrong
- Timing too fast

**Solutions:**
- Ensure INIT_LCD called at startup
- Adjust V0 contrast (0.5V-1V)
- Increase delay values

#### Keypad Not Responding
**Causes:**
- MM74C922 not powered
- DA signal not connected
- Oscillator capacitor missing

**Solutions:**
- Check VCC connection
- Verify DA to PC4
- Add 100nF capacitor on OSC pin

#### Relays Don't Switch
**Causes:**
- No base resistor on transistor
- Wrong port address
- Flyback diode orientation

**Solutions:**
- Add 1kΩ base resistor
- Verify PORTA2 = 0xE0
- Check diode cathode to +5V

#### Memory/Simulation Errors
**Causes:**
- Internal memory size not set
- Wrong HEX file
- Clock not running

**Solutions:**
- Set memory to 0x10000
- Recompile and reload
- Check clock source

### Debug Tools in Proteus
- **Logic Probes**: Monitor signals (HIGH/LOW)
- **Logic Analyzer**: View timing
- **Oscilloscope**: Check waveforms
- **Memory Viewer**: Right-click 8086 → View Memory
- **Step Mode**: Execute one instruction at a time

---

## Study Questions and Exercises

### Conceptual Questions

1. **Why are memory and I/O separate address spaces?**
   - Hint: Think about M/IO signal and 74LS138 E2 connection

2. **What would happen if you forgot to set DS at startup?**
   - Hint:  Consider LEA SI, STRING and where it would look

3. **Why must passwords be stored as ASCII instead of binary?**
   - Hint: Think about keypad output (0x0-0xF) vs display needs

4. **How does read-modify-write prevent turning off other relays?**
   - Hint: Compare OR vs direct write

5. **What's the difference between INST_CTRL and DATA_CTRL?**
   - Hint: Look at RS signal

### Practical Questions

1. **How would you modify code for 6-digit passwords?**
   - Change CX counters
   - Adjust buffer sizes
   - Update comparison loops

2. **What changes needed to add 4th power branch (projector)?**
   - Use PORTA2 bit 3
   - Add relay driver circuit
   - Update menu display
   - Add toggle logic

3. **How to use 8253A for real-time clock display?**
   - Configure counter for 1Hz output
   - Read counter periodically
   - Update LCD seconds display

4. **What's needed for EEPROM password storage?**
   - Add 24C02 chip (I2C)
   - Write password on setup
   - Read password at startup
   - Requires I2C protocol code

5. **How to implement 3-wrong-password lockout?**
   - Add counter variable
   - Increment on wrong password
   - Check if >= 3
   - Implement timeout delay

### Debugging Scenarios

1. **LCD displays but shows wrong characters**
   - Check contrast (V0)
   - Verify initialization sequence
   - Check data line connections
   - Test with single character

2. **Keypad always reads 0xF**
   - Check MM74C922 power
   - Verify DA connection
   - Check oscillator capacitor
   - Test with multimeter

3. **Relays turn on but feedback shows OFF**
   - Check feedback sensor wiring
   - Verify PORTB2 input configuration
   - Test relay contacts with meter
   - Check for stuck contacts

4. **Password always fails with correct entry**
   - Check ASCII conversion (ADD AL, '0')
   - Verify comparison loop (4 iterations)
   - Print password bytes to LCD for debug
   - Check SI/DI pointers

5. **System crashes after timer start**
   - Check stack size (adequate?)
   - Verify CALL/RET balance
   - Check for infinite loops
   - Monitor SP in memory viewer

### Code Tracing Exercise

**Trace this code execution:**
```assembly
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h
    JZ NO_KEY
    AND AL, 0Fh
    ; What's in AL if key '5' is pressed?
```

**Answer:**
1. Read PORTC:  AL = 00010101b (DA=1, ABCD=0101)
2. TEST checks bit 4: DA=1, so ZF=0
3. JZ not taken (ZF=0)
4. AND AL, 0Fh: AL = 00000101b (value 5)
5. Result: AL = 0x05 (key code for '5')

---

## Teaching Strategies for AI Tutor

### Explanation Approaches

**For Hardware Concepts:**
1. Start with "why it's needed"
2. Use real-world analogies
3. Show signal flow diagrams
4. Explain component by component
5. Show complete circuit
6. Trace example operation

**For Software Concepts:**
1. Show high-level purpose
2. Break into steps
3. Show code snippet
4. Trace execution with values
5. Show common mistakes
6. Give practice exercises

**For Debugging:**
1. Describe symptom
2. List possible causes
3. Show diagnostic steps
4. Explain how to test each
5. Show correct solution
6. Explain why it works

### When Student Asks Questions

**If about hardware:**
- Explain component function first
- Show how it connects
- Trace signal path
- Give voltage/current values
- Show timing if relevant

**If about code:**
- Show relevant code section
- Explain line by line
- Show register/variable values
- Trace through execution
- Show alternative approaches

**If about errors:**
- Ask for symptom description
- Guide through diagnosis
- Don't just give answer
- Help them understand root cause
- Show prevention strategies

### Key Points to Emphasize

1. **Virtual memory ≠ I/O space** (most common confusion)
2. **Always configure 8255A before use** (COM_REG)
3. **Read-modify-write for partial updates** (don't overwrite)
4. **RS signal determines LCD mode** (command vs data)
5. **Transistor amplifies current** (not voltage)
6. **Debouncing needs both HW and SW** (reliability)
7. **ASCII storage for passwords** (comparison needs)
8. **Feedback verifies commands** (closed-loop)

---

## Quick Reference Summary

### Essential Port Addresses
```
8255A #1 (LCD/Keypad): 0xF0-0xF6
8255A #2 (Relays):     0xE0-0xE6
8255A #3 (Auxiliary):  0xC0-0xC6
8253A Timer:           0xD0-0xD6
```

### Key Configuration Values
```
8255A Control:   0x89 (PA=OUT, PB=OUT, PC=IN)
8253A Control:  0x37 (Square wave mode)
LCD Function:   0x38 (8-bit, 2-line)
LCD Display:    0x0C (ON, cursor OFF)
```

### Critical Hardware Values
```
Virtual Memory:  0x10000 (64KB)
Base Resistor:   1kΩ (transistor)
Relay Current:   100 mA
8255A Current:  2 mA max per pin
Debounce Time:  20 ms (software)
```

### Common Instructions
```
IN AL, DX      - Read I/O port
OUT DX, AL     - Write I/O port
MOV AL, [SI]   - Read memory
MOV [DI], AL   - Write memory
CMP AL, value  - Compare
JE label       - Jump if equal
CALL label     - Call subroutine
RET            - Return
```

---

## End of Teaching Guide

This comprehensive guide provides everything an AI tutor needs to help the student understand their 8086 classroom power control system. It covers hardware, software, debugging, and includes teaching strategies for effective learning.

The student should be able to:
- Understand how each component works
- Trace program execution
- Debug hardware and software issues
- Modify code for enhancements
- Explain design decisions
- Apply concepts to new projects

**Remember:  The student learns best through:**
- Step-by-step explanations
- Real-world analogies
- Cause-and-effect relationships
- Practical examples from their code
- Understanding "why" not just "how"

Good luck with your studies! 🎓
