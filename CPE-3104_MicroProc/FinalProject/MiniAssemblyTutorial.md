# Learning Guide:  Classroom Power Control System

Don't worry!  Let's break down everything step by step. I'll explain what everything is and how it all works together.

---

## Part 1: What is a Microprocessor System? 

### Think of it like this: 
Imagine your classroom power control system as a **simple robot brain**: 
- **Brain (8086)**: Makes decisions, does math, follows instructions
- **Hands (8255A chips)**: Actually turns things on/off, reads buttons
- **Eyes (Keypad & Sensors)**: Sees what buttons you press
- **Mouth (LCD)**:  Tells you what's happening

### The 8086 Microprocessor
- It's a **16-bit CPU** (Central Processing Unit) from the 1970s
- Reads instructions one at a time from your assembly code
- Can only understand **machine language** (numbers like 10110101)
- We write **assembly language** (like MOV, ADD) which is easier for humans

---

## Part 2: Understanding Assembly Language Basics

### What is Assembly Language? 
Assembly is **one step above machine code**. Each line does ONE simple thing. 

### Basic Concepts: 

#### 1. **Registers** (Think:  Tiny Storage Boxes)
The 8086 has small storage locations called registers: 

```
AX, BX, CX, DX = General purpose (do math, store values)
SI, DI = Pointers (remember locations)
```

**Example:**
```assembly
MOV AL, 5       ; Put number 5 into register AL
ADD AL, 3       ; Add 3 to AL (now AL = 8)
```

#### 2. **Instructions** (Commands)
Basic instructions you'll see:

| Instruction | What it does | Example |
|-------------|--------------|---------|
| `MOV` | Copy/Move data | `MOV AL, 10` (put 10 in AL) |
| `ADD` | Add numbers | `ADD AL, 5` (add 5 to AL) |
| `SUB` | Subtract | `SUB AL, 2` (subtract 2 from AL) |
| `CMP` | Compare | `CMP AL, 10` (is AL equal to 10?) |
| `JMP` | Go to another line | `JMP START` (jump to label START) |
| `JE` | Jump if equal | `JE LABEL` (jump if comparison was equal) |
| `CALL` | Run a subroutine | `CALL DELAY` (run the DELAY function) |
| `RET` | Return from subroutine | `RET` (go back) |
| `IN` | Read from port | `IN AL, DX` (read port into AL) |
| `OUT` | Write to port | `OUT DX, AL` (write AL to port) |

#### 3. **Ports** (Doors to the Outside World)
Ports are addresses where you can talk to hardware:

```assembly
MOV DX, 0F0h        ; DX = port address 0xF0 (LCD data)
MOV AL, 'A'         ; AL = character 'A'
OUT DX, AL          ; Send 'A' to the LCD
```

Think of it like mailing a letter: 
- **DX** = the mailbox address
- **AL** = the letter
- **OUT** = putting the letter in the mailbox

---

## Part 3: Your Hardware Components Explained

### The 8255A Chip (Your "Hands")
This chip gives the 8086 **ports** to control things. 

**Each 8255A has 3 ports:**
- **Port A**: 8 pins (can be input or output)
- **Port B**: 8 pins (can be input or output)  
- **Port C**: 8 pins (can be input or output)

**You have THREE 8255A chips:**

#### **8255A #1** - LCD and Keypad
```
Port A (0xF0h) = LCD data lines D0-D7
Port B (0xF2h) = LCD control (RS, E)
Port C (0xF4h) = Keypad input
```

#### **8255A #2** - Power Control
```
Port A (0xE0h) = Turn relays ON/OFF
Port B (0xE2h) = Read if relays are ON/OFF
Port C (0xE4h) = Cancel button
```

#### **8255A #3** - Extra (not really used)
```
Port A (0xC0h) = Reserved for future
Ports B & C = Grounded (not used)
```

---

## Part 4: How the LCD Works

The **LM044L** is your 20x4 LCD (20 characters wide, 4 lines tall).

### LCD Connections:
```
8086 → 8255A #1 → LCD
        Port A (8 bits) → D0-D7 (data pins)
        Port B bit 0 → RS (Register Select)
        Port B bit 1 → E (Enable)
```

### How to Write to LCD: 

#### Step 1: Choose Instruction or Data
- **RS = 0**: You're sending a command (like "clear screen")
- **RS = 1**: You're sending a character (like 'A')

#### Step 2: Put data on Port A
```assembly
MOV DX, 0F0h        ; Port A address
MOV AL, 'A'         ; Character to display
OUT DX, AL          ; Put 'A' on the data lines
```

#### Step 3: Pulse the Enable (E) pin
```assembly
MOV DX, 0F2h        ; Port B address
MOV AL, 00000001b   ; RS=1 (data), E=0
OUT DX, AL          

MOV AL, 00000011b   ; RS=1, E=1 (pulse high)
OUT DX, AL

MOV AL, 00000001b   ; RS=1, E=0 (pulse low - LCD reads it!)
OUT DX, AL
```

The **falling edge** (E going from 1→0) makes the LCD read the data.

### LCD Commands:
```assembly
0x01 = Clear screen
0x38 = Set to 2-line mode
0x0E = Turn display on, cursor on
0x80 = Go to line 1, column 0
0xC0 = Go to line 2, column 0
```

---

## Part 5: How the Keypad Works

The **MM74C922** is a smart chip that reads your 4x4 keypad.

### How it works: 
```
You press '5' → MM74C922 scans and finds it
                ↓
        Outputs:  ABCD = 0101 (binary for 5)
                 DA = 1 (data available)
                ↓
        8086 reads Port C (0xF4h)
```

### Reading a Key:
```assembly
MOV DX, 0F4h        ; Port C address
IN AL, DX           ; Read the port
TEST AL, 00010000b  ; Check bit 4 (DA)
JZ NO_KEY           ; If 0, no key pressed

AND AL, 00001111b   ; Get bits 0-3 (ABCD = key code)
; Now AL has the key number (0-15)
```

### Key Codes:
```
Key '1' = 0x0
Key '2' = 0x1
Key '3' = 0x2
Key '*' = 0xC
Key '0' = 0xD
Key '#' = 0xE
```

---

## Part 6: How the Relays Work

**Relays** are electromagnetic switches that control high-voltage power.

### Why use relays?
- Your 8086 outputs 5V (low voltage, low current)
- Classroom AC power is 220V (high voltage, high current)
- **Relays bridge the gap safely! **

### How it works:
```
8086 → Port A2 bit 0 = 1 (5V signal)
       ↓
  Relay driver (2N2222 transistor)
       ↓
  Relay coil energizes
       ↓
  Relay contacts close
       ↓
  220V AC power flows to AC Units
```

### Control Example:
```assembly
; Turn ON AC Units
MOV DX, 0E0h        ; Port A2 (relay control)
MOV AL, 00000001b   ; Bit 0 = 1 (AC on)
OUT DX, AL          ; Send command

; Check if it really turned on
MOV DX, 0E2h        ; Port B2 (relay feedback)
IN AL, DX           ; Read actual relay state
TEST AL, 00000001b  ; Check bit 0
JNZ AC_IS_ON        ; If bit set, AC confirmed on
```

---

## Part 7: Understanding Your Code Flow

Let's trace what happens when you run your program:

### 1. **Startup (INIT_DEVICES)**
```assembly
START:
    MOV AX, DATA
    MOV DS, AX          ; Set up data segment
    
    XOR AX, AX          ; Clear all registers
    XOR BX, BX
    ; ... (starting fresh)
    
INIT_DEVICES:
    MOV DX, COM_REG     ; 8255A #1 control
    MOV AL, 89h         ; Configure ports
    OUT DX, AL          ; Port A=out, B=out, C=in
    
    ; Turn off all relays (safety!)
    MOV DX, PORTA2
    MOV AL, 00h
    OUT DX, AL
    
    CALL INIT_LCD       ; Set up the LCD
```

**What's happening:**
1. Clear all registers (start clean)
2. Tell each 8255A which ports are input/output
3. Turn off all power (relays OFF)
4. Initialize the LCD

---

### 2. **Password Setup (SET_PASSWORD_MODE)**
```assembly
SET_PASSWORD_MODE:
    CALL CLS            ; Clear LCD screen
    
    MOV AL, 080h        ; LCD line 1 address
    CALL INST_CTRL      ; Send to LCD
    LEA SI, SET_MODE    ; "SET NEW PASSWORD:"
    CALL PRINT_STRING   ; Display it
    
    XOR CX, CX          ; CX = counter (0)
    MOV SI, OFFSET PASS_BUF  ; SI points to password buffer
    
ENTER_NEW_PASS:
    CALL WAIT_FOR_KEYPRESS_FIXED  ; Wait for key
    
    ; Key code now in AL
    CMP AL, 0Dh         ; Is it '0'?
    JNE NOT_ZERO1
    MOV AL, '0'         ; Convert to ASCII '0'
    JMP STORE_DIGIT1
    
NOT_ZERO1:
    ADD AL, '0'         ; Convert 1-9 to ASCII
    
STORE_DIGIT1:
    MOV [SI], AL        ; Save digit
    INC SI              ; Next position
    INC CX              ; Count++
    
    ; Display asterisk
    MOV AL, 0C0h        ; LCD line 2
    ADD AL, CL
    DEC AL
    CALL INST_CTRL
    MOV AL, '*'
    CALL DATA_CTRL      ; Show '*' on screen
    
    CMP CX, 04h         ; Got 4 digits?
    JL ENTER_NEW_PASS   ; No, keep going
```

**What's happening:**
1. Display "SET NEW PASSWORD:"
2. Wait for keypad press
3. Convert key code (0-9) to ASCII character ('0'-'9')
4. Save it in password buffer
5. Show asterisk (*) on screen
6. Repeat until 4 digits entered

---

### 3. **Login (SEC_SYS_START)**
```assembly
SEC_SYS_START:
    CALL CLS
    MOV AL, 080h
    CALL INST_CTRL
    LEA SI, SEC_START   ; "ENTER PASSWORD:"
    CALL PRINT_STRING
    
    XOR CX, CX
    MOV DI, OFFSET CONFIRM_BUF
    
GET_PASSWORD_DIGITS:
    CALL WAIT_FOR_KEYPRESS_FIXED
    ; ...  (similar to password setup)
    
    ; After 4 digits, verify: 
    MOV CX, 04h
    MOV SI, OFFSET NEW_PASS      ; Correct password
    MOV DI, OFFSET CONFIRM_BUF   ; Entered password
    
CHECK_PASSWORD:
    MOV AL, [SI]        ; Get correct digit
    MOV BL, [DI]        ; Get entered digit
    CMP AL, BL          ; Compare
    JNE ACCESS_DENIED   ; Not equal?  Denied! 
    INC SI
    INC DI
    LOOP CHECK_PASSWORD ; Check all 4 digits
    
    JMP MENU_STARTUP    ; All match!  Access granted
```

**What's happening:**
1. Ask for password
2. User enters 4 digits
3. Compare each digit with saved password
4. If all match → go to main menu
5. If any don't match → show "ACCESS DENIED"

---

### 4. **Main Menu (MENU_STARTUP)**
```assembly
MENU_STARTUP: 
    CALL CLS
    
    ; Display "PRESS # TO LOCK"
    MOV AL, 080h
    CALL INST_CTRL
    LEA SI, LOCK_PROMPT
    CALL PRINT_STRING
    
CHECK_STATUS_AC:
    MOV AL, 0C0h        ; Line 2
    CALL INST_CTRL
    
    MOV DX, PORTB2      ; Read relay feedback
    IN AL, DX
    AND AL, 001b        ; Check bit 0 (AC)
    JNZ CHECK_AC_ON     ; If bit set, AC is ON
    CALL AC_L           ; Display "AC:  OFF"
    JMP CHECK_STATUS_PO
    
CHECK_AC_ON: 
    CALL AC_H           ; Display "AC: ON"
    JMP CHECK_STATUS_PO
    
; ... (similar for Power Outlets and Lights)
```

**What's happening:**
1. Clear screen
2. Display lock prompt
3. Read Port B2 to see which relays are ON
4. Display status: 
   ```
   PRESS # TO LOCK
   1. AC: ON    2.PWR: OFF
   3.LIGHTS: ON
   4.SHUTDOWN ALL
   ```

---

### 5. **Control Relays (RELAY_CONTROL)**
```assembly
RELAY_CONTROL: 
    CALL WAIT_FOR_KEYPRESS_FIXED  ; Wait for key
    
    CMP AL, 00h         ; Button 1? 
    JE CHECK_AC_STATUS
    
    CMP AL, 01h         ; Button 2?
    JE CHECK_PO_STATUS
    
    CMP AL, 02h         ; Button 3?
    JE CHECK_LI_STATUS
    
    CMP AL, 04h         ; Button 4? 
    JE SHUTDOWN_ALL
    
    CMP AL, 0Eh         ; Button #? 
    JE LOCK_SYSTEM
    
    JMP RELAY_CONTROL   ; Invalid key, wait again

CHECK_AC_STATUS:
    MOV DX, PORTB2      ; Read current state
    IN AL, DX
    AND AL, 01h         ; Check AC bit
    JZ TURN_AC_ON       ; If 0, turn it ON
    JMP TURN_AC_OFF     ; If 1, turn it OFF
    
TURN_AC_ON:
    MOV DX, PORTA2      ; Control port
    IN AL, DX           ; Read current output
    OR AL, 001b         ; Set bit 0
    OUT DX, AL          ; Turn ON relay
    JMP MENU_STARTUP    ; Back to menu
```

**What's happening:**
1. Wait for button press
2. Check which button (1, 2, 3, 4, or #)
3. For devices (1-3):
   - Read current state from Port B2
   - If OFF → turn ON
   - If ON → turn OFF (with timer option)
4. Update Port A2 to control relay
5. Go back to menu

---

### 6. **Timer (TIMER)**
```assembly
TIMER:
    CALL CLS
    LEA SI, TMR         ; "SET TIMER:"
    CALL PRINT_STRING
    
TIMER_INPUT_LOOP:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    CMP AL, 00H         ; Key '1'?
    JE M1               ; Set 1 minute
    
    CMP AL, 0DH         ; Key '0'?
    JE M0               ; Set 0 minutes (immediate)
    
    CMP AL, 0CH         ; Key '*'?
    JE TIMER_START      ; Start countdown
    
    ; ... (handle other keys)

M1:
    MOV AL, 094h        ; Line 3
    CALL INST_CTRL
    LEA SI, MIN1        ; "01 MINUTE"
    CALL PRINT_STRING
    MOV MINS_FLAG, 1    ; Save selection
    JMP TIMER_INPUT_LOOP

TIMER_START:
    ; Check MINS_FLAG and countdown
    ; When timer expires, turn off selected device
```

**What's happening:**
1. Show "SET TIMER:"
2. User presses 0-9 for minutes
3. Display selected time
4. User presses * to start
5. Countdown begins
6. When time's up, turn off the device

---

## Part 8: Important Subroutines

### WAIT_FOR_KEYPRESS_FIXED
This is the **heart of keypad reading**: 

```assembly
WAIT_FOR_KEYPRESS_FIXED: 
    PUSH DX
    PUSH BX
    
    ; Wait for NO key
WAIT_NO_KEY:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h        ; Check DA (bit 4)
    JNZ WAIT_NO_KEY     ; If DA=1, key still pressed
    
    CALL DEBOUNCE_DELAY ; Wait 20ms
    
    ; Wait for key press
WAIT_KEY_PRESS:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h        ; Check DA
    JZ WAIT_KEY_PRESS   ; If DA=0, no key yet
    
    CALL DEBOUNCE_DELAY ; Wait 20ms
    
    ; Get key value
    AND AL, 0Fh         ; Mask to get ABCD (bits 0-3)
    MOV BL, AL          ; Save it
    
    ; Wait for release
WAIT_KEY_RELEASE:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h
    JNZ WAIT_KEY_RELEASE
    
    CALL DEBOUNCE_DELAY
    
    MOV AL, BL          ; Return key value
    POP BX
    POP DX
    RET
```

**What's happening:**
1. Wait until no key is pressed (DA=0)
2. Wait 20ms (debounce - prevent false reads)
3. Wait for key press (DA=1)
4. Wait 20ms again
5. Read key code (ABCD bits)
6. Wait for key release
7. Return key code in AL

**Why debounce?** When you press a button, it "bounces" (makes/breaks contact rapidly). Waiting 20ms lets it settle. 

---

### INIT_LCD
Sets up the LCD for use:

```assembly
INIT_LCD:
    ; Send 0x38 (function set:  2-line, 5x7 font)
    MOV AL, 038h
    CALL INST_CTRL
    
    ; Send 0x0E (display on, cursor on)
    MOV AL, 00Eh
    CALL INST_CTRL
    
    ; Send 0x01 (clear display)
    MOV AL, 001h
    CALL INST_CTRL
    
    ; Send 0x06 (entry mode:  increment cursor)
    MOV AL, 006h
    CALL INST_CTRL
    
    RET
```

---

### INST_CTRL (Send instruction to LCD)
```assembly
INST_CTRL:
    PUSH DX
    
    MOV DX, PORTA       ; Data port
    OUT DX, AL          ; Put instruction on D0-D7
    
    MOV DX, PORTB       ; Control port
    MOV AL, 00000000b   ; RS=0, E=0
    OUT DX, AL
    
    MOV AL, 00000010b   ; RS=0, E=1
    OUT DX, AL
    
    CALL DELAY_LCD      ; Hold
    
    MOV AL, 00000000b   ; RS=0, E=0 (falling edge)
    OUT DX, AL
    
    CALL DELAY_LCD      ; Wait for execution
    
    POP DX
    RET
```

---

### DATA_CTRL (Send character to LCD)
```assembly
DATA_CTRL:
    PUSH DX
    
    MOV DX, PORTA       ; Data port
    OUT DX, AL          ; Put character on D0-D7
    
    MOV DX, PORTB       ; Control port
    MOV AL, 00000001b   ; RS=1, E=0
    OUT DX, AL
    
    MOV AL, 00000011b   ; RS=1, E=1
    OUT DX, AL
    
    CALL DELAY_LCD      ; Hold
    
    MOV AL, 00000001b   ; RS=1, E=0 (falling edge)
    OUT DX, AL
    
    CALL DELAY_LCD
    
    POP DX
    RET
```

---

## Part 9: Proteus Simulation Tips

### Setting Up in Proteus: 

#### 1. **Place Components**
- Search for "8086" and place it
- Add three "8255" chips
- Add "LM044L" for LCD
- Add "MM74C922" for keypad
- Add "RELAY-SPDT" for relays

#### 2. **Wire Connections**

**8255A #1 to LCD:**
```
PA0-PA7 → LCD D0-D7
PB0 → LCD RS
PB1 → LCD E
LCD RW → Ground
```

**8255A #1 to Keypad:**
```
PC0-PC3 → MM74C922 ABCD (output pins)
PC4 → MM74C922 DA (data available)
```

**8255A #2 to Relays:**
```
PA0 → Relay 1 coil (through 2N2222)
PA1 → Relay 2 coil (through 2N2222)
PA2 → Relay 3 coil (through 2N2222)

PB0 ← Relay 1 contact feedback
PB1 ← Relay 2 contact feedback
PB2 ← Relay 3 contact feedback
```

#### 3. **Address Decoding**
Use 74LS138 to decode addresses:
```
A7-A5 → 74LS138 inputs
74LS138 outputs → 8255A chip select pins
```

#### 4. **Load Your Code**
- Right-click 8086 → Edit Properties
- Program File → Browse to your . HEX file
- Click OK

#### 5. **Run Simulation**
- Press Play button
- LCD should show "SET NEW PASSWORD:"
- Click keypad buttons to interact

### Common Proteus Issues:

| Problem | Solution |
|---------|----------|
| LCD shows squares | Check contrast (V0 pin, use 1kΩ resistor to ground) |
| Keypad doesn't work | Verify MM74C922 OSC capacitor (100nF) |
| Program doesn't start | Check 8086 clock crystal (typically 5-8MHz) |
| Relays don't switch | Add base resistors (1kΩ) to 2N2222 transistors |
| "Address error" | Verify 74LS138 address decoder connections |

---

## Part 10: Quick Reference

### Binary/Hex Cheat Sheet:
```
Binary      Hex    Decimal
0000        0x0    0
0001        0x1    1
0010        0x2    2
0011        0x3    3
0100        0x4    4
0101        0x5    5
0110        0x6    6
0111        0x7    7
1000        0x8    8
1001        0x9    9
1010        0xA    10
1011        0xB    11
1100        0xC    12
1101        0xD    13
1110        0xE    14
1111        0xF    15
```

### Port Address Summary:
```
LCD Data:      0xF0 (Port A, 8255A #1)
LCD Control:  0xF2 (Port B, 8255A #1)
Keypad Input: 0xF4 (Port C, 8255A #1)

Relay Control:    0xE0 (Port A, 8255A #2)
Relay Feedback:  0xE2 (Port B, 8255A #2)
Cancel Button:   0xE4 (Port C, 8255A #2)
```

### Key Instructions:
```assembly
MOV dest, src   ; Copy src to dest
IN AL, DX       ; Read port DX into AL
OUT DX, AL      ; Write AL to port DX
CALL label      ; Call subroutine
RET             ; Return from subroutine
CMP val1, val2  ; Compare values
JE label        ; Jump if equal
JNE label       ; Jump if not equal
AND AL, mask    ; Bitwise AND
OR AL, mask     ; Bitwise OR
```

---

## Practice Exercises

Try these to learn: 

### Exercise 1: Turn on LED
```assembly
; Turn on an LED connected to Port A bit 0
MOV DX, 0E0h        ; Port A address
MOV AL, 00000001b   ; Bit 0 = 1
OUT DX, AL          ; Turn on LED
```

### Exercise 2: Read a button
```assembly
; Read a button on Port C bit 0
MOV DX, 0E4h        ; Port C address
IN AL, DX           ; Read port
AND AL, 00000001b   ; Check bit 0
JZ BUTTON_OFF       ; If 0, button not pressed
; Button is pressed! 
```

### Exercise 3: Display character on LCD
```assembly
; Display 'H' on LCD
MOV AL, 080h        ; Line 1, column 0
CALL INST_CTRL      ; Set position

MOV AL, 'H'         ; Character to display
CALL DATA_CTRL      ; Send to LCD
```

---

## Summary

Your classroom power control system: 
1. **Starts** by setting up all hardware
2. **Asks instructor** to set a password
3. **Asks user** to log in
4. **Shows menu** with power branch status
5. **Reads keypad** to see what button you press
6. **Controls relays** to turn power ON/OFF
7. **Uses timer** for safe shutdown delays

The **8086** is the brain, the **8255As** are the hands, the **MM74C922** reads your keypad, and the **LM044L** displays information. 

**Assembly language** is just telling the 8086 what to do, one step at a time, by moving data, checking conditions, and jumping to different parts of code.

---

Does this help?  What specific part would you like me to explain more?  😊