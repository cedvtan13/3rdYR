# Classroom Automation System - Documentation

## Overview
This is an 8086 assembly language-based classroom automation and security system with password protection, designed to control multiple electrical devices through relays.  The system uses a 20x4 LCD display for user interface and a keypad for input.

## Hardware Components

### Microprocessor & Memory
- **2N2222** - NPN Transistor (for switching/driving)
- **74LS04** - Hex Inverter
- **74LS138** - 3-to-8 Line Decoder
- **74LS245** - Octal Bus Transceiver
- **74LS373** - Octal D-Type Latch
- **74S04** - Hex Inverter (Schottky)
- **8086** - Main Microprocessor
- **8253A** - Programmable Interval Timer
- **8255A** - Programmable Peripheral Interface (3 instances)
- **8259** - Programmable Interrupt Controller

### Input/Output Devices
- **BUTTON** - Physical push buttons (including timer cancel button)
- **KEYPAD-PHONE** - 4x4 Matrix Keypad (0-9, *, #)
- **LCD (20x4)** - 20 characters × 4 lines display (LM044L)

### Power & Control Components
- **CAPACITOR** - Filtering/decoupling capacitors
- **DIODE** - Protection diodes
- **FUSE** - Circuit protection
- **LAMP** - Visual indicators/controlled devices
- **LED** - Status indicators
- **LM044L** - LCD Controller (20x4)
- **LOGICSTATE** - Logic level indicators
- **MM74C922** - 16-Key Encoder IC
- **RELAY** - Electromagnetic switches for device control (3x)
- **RES (Resistor)** - Pull-up/pull-down resistors
- **VSINE** - AC power source simulation

## System Architecture

### Port Configuration

#### 8255A #1 (LCD & Keypad Interface)
- **PORTA (0xF0h)** - LCD Data Bus
  - Bits 0-7: Connected to LCD D0-D7 (LM044L data pins)
  
- **PORTB (0xF2h)** - LCD Control Lines
  - Bit 0: RS (Register Select) - 0=Instruction, 1=Data
  - Bit 1: E (Enable) - Falling edge triggers LCD operation
  - Bits 2-7: Unused
  
- **PORTC (0xF4h)** - Keypad Interface (MM74C922)
  - Bits 0-3: ABCD inputs from MM74C922 (encoded key value)
  - Bit 4: DA (Data Available) from MM74C922
    - Also inverted and connected to $\overline{OE}$ (Output Enable, active low)
  - Bits 5-7: Unused
  
- **COM_REG (0xF6h)** - Control Register
  - Mode: **89h** (10001001b)
    - Port A: Output (LCD data)
    - Port B: Output (LCD control)
    - Port C: Input (keypad)

#### 8255A #2 (Device Control & Feedback)
- **PORTA2 (0xE0h)** - Relay Control (OUTPUT)
  - Bit 0: Air Conditioner (AC) relay control
  - Bit 1: Power Outlet (PO) relay control
  - Bit 2: Lights (LI) relay control
  - Bits 3-7: Unused
  
- **PORTB2 (0xE2h)** - Relay Status Feedback (INPUT)
  - Bit 0: AC relay state (reads back actual relay position)
  - Bit 1: Power Outlet relay state
  - Bit 2: Lights relay state
  - Bits 3-7: Unused
  
- **PORTC2 (0xE4h)** - Timer Cancel Button
  - Bit 0: Timer cancel button input
  - Bits 1-7: Unused
  
- **COM_REG2 (0xE6h)** - Control Register
  - Mode: **89h** (10001001b)
    - Port A: Output (relay control)
    - Port B: Output initially configured, but reads relay feedback
    - Port C: Input (cancel button)

#### 8255A #3 (Auxiliary/Reserved)
- **PORTA3 (0xC0h)** - Auxiliary Output
  - Bit 0: Output (purpose defined by hardware design)
  - Bits 1-7: Grounded
  
- **PORTB3 (0xC2h)** - All grounded (unused)
  
- **PORTC3 (0xC4h)** - All grounded (unused)
  
- **COM_REG3 (0xC6h)** - Control Register
  - Mode:  Configured but minimally used

#### 8253A Timer
- **COMT (0xD6h)** - Timer Control Register
  - Mode: **37h** - Square wave generator
  - Used for timing operations

### Hardware Signal Flow

#### LCD Interface (LM044L)
```
8086 → 8255A #1 PORTA [D0-D7] → LM044L Data Bus
8086 → 8255A #1 PORTB [RS, E] → LM044L Control
```

**LCD Write Operation:**
1. Place data/instruction on PORTA (D0-D7)
2. Set RS (PORTB bit 0): 0 for instruction, 1 for data
3. Set E high (PORTB bit 1)
4. Set E low (falling edge latches data into LCD)

#### Keypad Interface (MM74C922)
```
Keypad Matrix → MM74C922 [Row/Col scan] → Encoded Output
MM74C922 [ABCD] → 8255A #1 PORTC [0-3]
MM74C922 [DA] → 8255A #1 PORTC [4] (direct)
MM74C922 [DA] → NOT gate → MM74C922 [$OE] (inverted)
```

**Keypad Read Operation:**
1. MM74C922 continuously scans 4x4 matrix
2. On key press: 
   - DA (Data Available) goes high
   - DA inverted to $\overline{OE}$ goes low (enables output)
   - ABCD outputs 4-bit encoded key value
3. Software reads PORTC: 
   - Bit 4 (DA) = 1 indicates key available
   - Bits 0-3 (ABCD) = key code (0x0-0xF)

#### Relay Control System
```
8086 → 8255A #2 PORTA2 [bits 0-2] → Relay Driver → Relays → Devices
Relays → Feedback Sensors → 8255A #2 PORTB2 [bits 0-2] → 8086
```

**Control Flow:**
- **PORTA2 (Output)**: Commands sent to relay drivers
- **PORTB2 (Input)**: Actual relay position feedback
  - Allows verification that relay actually switched
  - Provides real-time device status for display

### Relay Control Bit Mapping
| Bit | Device | PORTA2 (Control) | PORTB2 (Feedback) |
|-----|--------|------------------|-------------------|
| 0 | Air Conditioner | Write to switch | Read actual state |
| 1 | Power Outlet | Write to switch | Read actual state |
| 2 | Lights | Write to switch | Read actual state |

**Example:**
```assembly
; Turn on AC (bit 0)
MOV DX, PORTA2
IN AL, DX           ; Read current state
OR AL, 001b         ; Set bit 0
OUT DX, AL          ; Send command

; Verify AC turned on
MOV DX, PORTB2
IN AL, DX           ; Read feedback
AND AL, 001b        ; Check bit 0
JNZ AC_IS_ON        ; If bit 0 set, AC confirmed on
```

## Features

### 1. Security System
- **Password Protection**: 4-digit password required for access
- **First-Time Setup**: Mandatory password creation on first boot
- **Password Confirmation**: Double-entry verification to prevent typos
- **Access Control**: Lock/unlock system with # key
- **No Default Password**: Forces user to set custom password for security

### 2. Device Control
The system controls three independent devices: 

1. **Air Conditioner (AC)** - Button 1
2. **Power Outlet (PO)** - Button 2
3. **Lights (LI)** - Button 3
4. **Shutdown All** - Button 4

Each device can be toggled ON/OFF individually or all at once.

### 3. Timer Function
- **Delayed Shutdown**: Set 0-9 minute timer before turning off devices
- **Immediate Action**: Select 0 minutes for instant shutdown
- **Cancellable**: Press # to cancel timer and return to menu
- **Hardware Cancel Button**:  PORTC2 bit 0 provides physical cancel button
- **Visual Feedback**: Countdown display on LCD

### 4. User Interface (20x4 LCD - LM044L)

#### Display Layout
- **Line 1 (0x80)**: System prompts/titles
- **Line 2 (0xC0)**: Input feedback/device status
- **Line 3 (0x94)**: Device status continued
- **Line 4 (0xD4)**: Additional options/instructions

#### Key Messages
- Password setup screens
- Device status indicators (ON/OFF)
- Timer settings
- Action confirmations

## Keypad Layout & Encoding

### Physical Layout
```
[1] [2] [3] [A]
[4] [5] [6] [B]
[7] [8] [9] [C]
[*] [0] [#] [D]
```

### MM74C922 Encoding
The MM74C922 encodes the 16-key matrix into a 4-bit value (ABCD):

| Key | ABCD (Hex) | PORTC [3:0] | Function |
|-----|------------|-------------|----------|
| 1 | 0x0 | 0000b | Device 1 (AC) |
| 2 | 0x1 | 0001b | Device 2 (Outlet) |
| 3 | 0x2 | 0010b | Device 3 (Lights) |
| A | 0x3 | 0011b | Not used |
| 4 | 0x4 | 0100b | Device 4 (Shutdown) |
| 5 | 0x5 | 0101b | Timer:  5 min |
| 6 | 0x6 | 0110b | Timer: 6 min |
| B | 0x7 | 0111b | Not used |
| 7 | 0x8 | 1000b | Timer: 7 min |
| 8 | 0x9 | 1001b | Timer: 8 min |
| 9 | 0xA | 1010b | Timer: 9 min |
| C | 0xB | 1011b | Not used |
| * | 0xC | 1100b | Enter/Confirm |
| 0 | 0xD | 1101b | Zero/Timer:  0 min |
| # | 0xE | 1110b | Back/Cancel/Lock |
| D | 0xF | 1111b | Not used |

### Data Available (DA) Signal
- **PORTC bit 4**: Direct connection from MM74C922 DA pin
- **DA = 1**: Valid key data available on ABCD
- **DA = 0**: No key pressed
- **Inverted DA → $\overline{OE}$**: Automatically enables MM74C922 output when key pressed

## Operation Flow

### Startup Sequence
1. **Initialize Devices**
   - Configure 8255A #1 ports (LCD output, keypad input)
   - Configure 8255A #2 ports (relay control output, feedback input)
   - Configure 8255A #3 ports (auxiliary)
   - Set 8253A timer mode
   - Turn off all relays via PORTA2
   - Initialize LCD display via PORTA/PORTB

2. **Password Setup** (First Boot)
   - Display "SET NEW PASSWORD:" on LCD
   - User enters 4-digit password via keypad (displays as ****)
   - Display "CONFIRM PASSWORD:"
   - User re-enters password
   - If match: "PASSWORD SET!" → Continue to main menu
   - If mismatch: "NOT MATCHED!" → Restart setup

### Normal Operation

1. **Login Screen**
   - Display "ENTER PASSWORD:"
   - User enters 4-digit password via keypad
   - If correct: Access granted → Main menu
   - If incorrect: "ACCESS DENIED" → Retry after 3-second delay

2. **Main Menu**
   - Read relay feedback from PORTB2
   - Display "PRESS # TO LOCK" (Line 1)
   - Show real-time device status from PORTB2 (Lines 2-4):
     ```
     1.AC:  ON/OFF    2.PWR: ON/OFF
     3.LIGHTS: ON/OFF
     4.SHUTDOWN ALL
     ```

3. **Device Control**
   - Press 1-3 to toggle individual devices
   - Write to PORTA2, verify with PORTB2
   - Press 4 for shutdown all
   - Press # to lock system (return to login)

4. **Timer Mode** (when turning off device)
   - Display "SET TIMER:"
   - Display "SELECT 0-9 MIN"
   - Show current selection (updates as user presses keys)
   - Press * to start countdown
   - Press # or cancel button (PORTC2 bit 0) to abort
   - Timer counts down and executes shutdown

## Debouncing Implementation

### Hardware Debouncing (MM74C922)
The MM74C922 provides built-in debouncing: 
- **Internal oscillator**:  Scans key matrix
- **Debounce circuit**: Typically 10-50ms delay
- **DA signal**: Only asserts when stable key detected
- **Key rollover**: Handles 2-key rollover

### Software Debouncing Strategy
Additional software debouncing ensures reliability: 

```assembly
WAIT_FOR_KEYPRESS_FIXED:
1. Wait for PORTC bit 4 (DA) = 0 (no key)
2. Debounce delay (~20ms)
3. Wait for PORTC bit 4 (DA) = 1 (key pressed)
4. Debounce delay (~20ms)
5. Verify DA still high (reject glitches)
6. Read PORTC bits 0-3 (key value)
7. Wait for DA = 0 (key released)
8. Debounce delay (~20ms)
9.  Verify DA still low
10. Return key value
```

**Why Both Hardware and Software? **
- **MM74C922**: Handles mechanical bounce (<1ms transients)
- **Software**: Handles electrical noise and ensures clean state transitions
- **Combined**: Extremely robust input with no false triggers

## LCD Control Details

### LM044L Command Set

#### Instruction Mode (RS=0)
| Command | Hex | Function |
|---------|-----|----------|
| Clear Display | 0x01 | Clear screen, cursor home |
| Return Home | 0x02 | Cursor to 0,0 |
| Entry Mode | 0x06 | Increment cursor, no shift |
| Display ON | 0x0E | Display on, cursor on |
| Function Set | 0x38 | 2-line mode, 5×7 font, 8-bit |
| Set DDRAM Addr | 0x80+ | Set cursor position |

#### Data Mode (RS=1)
- Write ASCII character to current cursor position

### LCD Address Map (20x4)
```
Line 1: 0x80 - 0x93  (0x80 + 0 to 19)
Line 2: 0xC0 - 0xD3  (0xC0 + 0 to 19)
Line 3: 0x94 - 0xA7  (0x94 + 0 to 19)
Line 4: 0xD4 - 0xE7  (0xD4 + 0 to 19)
```

### LCD Write Timing
```assembly
; Write instruction example
MOV DX, PORTA          ; Select data port
MOV AL, 0x38           ; Function set command
OUT DX, AL             ; Place on data bus

MOV DX, PORTB          ; Select control port
MOV AL, 00000000b      ; RS=0 (instruction), E=0
OUT DX, AL

MOV AL, 00000010b      ; RS=0, E=1 (enable high)
OUT DX, AL

CALL DELAY_LCD         ; Hold time (~1µs)

MOV AL, 00000000b      ; RS=0, E=0 (falling edge)
OUT DX, AL             ; LCD latches data

CALL DELAY_LCD         ; Execution time (~40µs-1.6ms)
```

### Display Routines
- **INIT_LCD**: Initialize LCD in 2-line, 8-bit mode
- **CLS**: Clear screen (0x01 command)
- **INST_CTRL**: Send instruction (RS=0)
- **DATA_CTRL**: Send character (RS=1)
- **PRINT_STRING**: Print null-terminated string ($-terminated)

## Timing Specifications

### LCD Timing
- **Enable Pulse Width**: ≥450ns (typically 1µs)
- **Enable Cycle**: ≥1µs
- **Setup Time**: ≥60ns (data before E high)
- **Hold Time**: ≥20ns (data after E low)
- **Instruction Execution**:  40µs-1.6ms (clear=1. 6ms)

### Keypad Timing (MM74C922)
- **Scan Rate**: ~500Hz (2ms per scan cycle)
- **Debounce Time**: 10ms typical (internal)
- **Output Valid**: Data stable 100ns after $\overline{OE}$ low
- **DA Pulse Width**:  Remains high while key held

### Software Delays
- **DEBOUNCE_DELAY**: ~20ms (200 × 1ms loops)
- **DELAY_RELAY**: Variable delay for relay switching (prevents contact bounce)
- **DELAY2**:  3-second denial message display
- **DELAY_1MS**: 1ms base delay unit

### Timer Resolution
- **Minimum**: 0 minutes (immediate action)
- **Maximum**: 9 minutes
- **Countdown Display**: Updates every minute
- **Final Countdown**: "A FEW SECONDS" for last minute

## Memory Organization

### Data Segment Variables

#### Password Storage
```assembly
NEW_PASS     DB "    ", "$"    ; 4-byte password (ASCII)
PASS_SET     DB 00h            ; Flag: 01h after setup
PASS_BUF     DB 4 DUP(?)       ; Temporary input buffer
CONFIRM_BUF  DB 4 DUP(?)       ; Confirmation buffer
```

#### Display Strings
- All strings padded to 20 characters for 20x4 LCD
- Terminated with "$" for printing routine
- Examples: 
  - `SEC_START DB "ENTER PASSWORD:     ", "$"`
  - `AC_ON DB "1. AC: ON    ", "$"`

#### Control Flags
- **TG_FLAG**: Toggle state tracking
- **MINS_FLAG**: Selected timer duration (0-9)
- **KEY_PRESSED**:  Debounce state flag

### Stack Segment
```assembly
STK SEGMENT STACK
    BOS DW 64d DUP(?)    ; Bottom of stack (64 words = 128 bytes)
    TOS LABEL WORD       ; Top of stack pointer
STK ENDS
```

## Error Handling

### Password Errors
- **Mismatch**: Return to setup screen, no lockout
- **Incorrect Entry**: Display "ACCESS DENIED", 3-second timeout, unlimited retries
- **Buffer Overflow**: Fixed 4-digit length prevents overflow

### Input Validation
- **Numeric Only**: Only 0-9 accepted for passwords/timers
- **Fixed Length**:  Exactly 4 digits required for passwords
- **Range Check**: Timer accepts 0-9 minutes only
- **Invalid Keys Ignored**: Keys A, B, C, D have no effect

### Hardware Failures
- **Relay Feedback**:  PORTB2 verification detects relay failure
- **LCD Not Ready**:  Delays ensure LCD has time to process
- **Keypad Stuck**: DA signal must transition; stuck key detected by timeout

## Safety Features

### Relay Protection
- **Startup State**: All relays OFF by default (PORTA2 = 0x00)
- **Switching Delay**:  DELAY_RELAY prevents contact arcing/bounce
- **Status Verification**: PORTB2 feedback confirms actual relay position
- **Emergency Shutdown**: Button 4 cuts all power (PORTA2 = 0x00)
- **Isolation**: Relays electrically isolate control from high-voltage devices

### Password Security
- **Masked Input**: Displays asterisks (****) instead of digits
- **ASCII Storage**: Stored as characters '0'-'9' (not plaintext vulnerable)
- **Byte-by-Byte Comparison**: No string comparison vulnerabilities
- **No Echo**: Input not visible during entry

### System Integrity
- **Register Clearing**: All registers zeroed on startup
- **Port Initialization**: Explicit mode setting for all three 8255A chips
- **Fail-Safe Default**: Power-on state is all devices OFF

## Circuit Design Considerations

### MM74C922 Interface
```
Keypad Matrix (4x4) → MM74C922
                      ↓
    ┌─────────────────┴──────────────┐
    │ Row Scan:  Y0-Y3                │
    │ Col Sense: X0-X3               │
    │ Debounce: Internal RC          │
    │ Oscillator: ~500kHz            │
    └────────────┬───────────────────┘
                 ↓
    ABCD [0-3] → 8255A #1 PORTC [0-3]
    DA [4] → 8255A #1 PORTC [4]
    DA → NOT → $\overline{OE}$ (feedback loop)
```

**Key Feature**: Self-enabling circuit
- When key pressed: DA=1 → $\overline{OE}$=0 → Outputs enabled → Data valid
- When key released: DA=0 → $\overline{OE}$=1 → Outputs high-Z → Bus idle

### LCD Interface (LM044L)
```
8255A #1 PORTA [7:0] ──→ LCD D[7:0] (8-bit parallel)
8255A #1 PORTB [0] ────→ LCD RS (Register Select)
8255A #1 PORTB [1] ────→ LCD E (Enable)
                         LCD RW ─→ GND (write-only mode)
```

**Simplification**: RW grounded = write-only
- No need to read busy flag
- Use timed delays instead
- Reduces code complexity

### Relay Driver Circuit
```
8255A #2 PORTA2 [bit] → Driver (2N2222) → Relay Coil → Device
                                         ↓
                        Feedback Sensor ← 
                                         ↓
8255A #2 PORTB2 [bit] ← Status Signal
```

**Feedback Loop**: Closed-loop control
- Ensures relay actually switched
- Detects stuck relays or driver failures
- Provides real-time status for display

## Limitations & Considerations

### Current Limitations
1. **No EEPROM**: Password lost on power cycle (resets to setup mode)
2. **No Brute-Force Protection**: Unlimited password attempts
3. **Fixed Timer Range**: Only 0-9 minutes, no seconds precision
4. **Single User**: No multi-user support
5. **No Logging**: No history of access or device state changes
6. **Write-Only LCD**: Cannot read busy flag; relies on delays
7. **No Interrupt Support**:  Polling-based keypad reading (8259 present but unused)

### Hardware Dependencies
- Requires **MM74C922** for keypad encoding (4x4 matrix specific)
- Needs **LM044L-compatible** LCD (20x4, HD44780 protocol)
- Relies on **three 8255A** chips for adequate I/O
- **Relay feedback** requires sensing circuit on each relay

### Proteus Simulation Notes
- Hardware works in **Proteus 8.x+**
- Ensure proper crystal oscillator settings for 8086 (e.g., 5MHz)
- Configure 8255A control words before any I/O operations
- Check LCD contrast settings (V0 pin) for visibility
- MM74C922 requires OSC capacitor (typically 100nF)
- Add flyback diodes across relay coils in real hardware

## Future Enhancements

### Suggested Improvements
1. **EEPROM Integration**:  Persistent password storage (e.g., 24C02)
2. **RTC Module**: Real-time clock for scheduling (e.g., DS1307)
3. **Multiple Users**: Store multiple passwords with access levels
4. **Event Logging**: Track usage patterns in EEPROM
5. **Interrupt-Driven Input**: Use 8259 for keypad interrupts
6. **Remote Control**: Add serial/wireless interface (UART)
7. **Temperature Sensing**: Auto-control AC based on sensor (LM35)
8. **Power Monitoring**: Track energy usage per device (current sensors)
9. **Voice Feedback**: Audio prompts via speaker
10. **LCD Busy Flag Reading**: Configure PORTA as input to read busy flag

### Code Optimizations
- **Macros**: Create macros for repeated LCD positioning
- **Lookup Tables**: Minute display strings in array
- **Interrupt Service Routines**: ISR for keypad and timer
- **Subroutine Libraries**: Modularize LCD, keypad, relay functions
- **Checksum**:  Add password integrity verification

## Troubleshooting

### Common Issues

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| LCD shows garbage | Incorrect initialization timing | Increase delays in INIT_LCD, verify 0x38 command |
| LCD blank | Contrast too high/low | Adjust V0 pin voltage (10kΩ pot) |
| Keys not responding | MM74C922 not enabled | Check DA → $\overline{OE}$ connection and inversion |
| Multiple key reads | Insufficient debounce | Increase DEBOUNCE_DELAY (try 50ms) |
| Keys always pressed | DA stuck high | Check MM74C922 oscillator capacitor |
| Relay not switching | Wrong port/bit | Verify PORTA2 bit assignments, check driver circuit |
| Relay switches but display wrong | PORTB2 not connected | Verify feedback sensor wiring to PORTB2 |
| Timer doesn't count | 8253A misconfigured | Check COMT initialization (0x37) |
| Password always fails | ASCII mismatch | Ensure 0-9 → '0'-'9' conversion (ADD AL, '0') |
| Cursor not visible | Display mode wrong | Use 0x0E (cursor on) instead of 0x0C |

### Debug Techniques

#### 1. Port Monitoring (Proteus)
- **Logic Analyzer**: Monitor PORTA2, PORTB2, PORTC
- **Oscilloscope**:  Check E signal timing on PORTB bit 1
- **Probe**: Verify DA signal toggles on key press

#### 2. Flag Watching
```assembly
; Insert debug displays
MOV AL, MINS_FLAG
ADD AL, '0'
CALL DATA_CTRL    ; Display flag value on LCD
```

#### 3. Relay Verification
```assembly
; After switching relay
MOV DX, PORTA2
OUT AL, 0x01      ; Command: AC on
CALL DELAY
MOV DX, PORTB2
IN AL, DX         ; Read feedback
; Compare:  should be 0x01
```

#### 4. Keypad Testing
```assembly
KEYPAD_TEST:
    MOV DX, PORTC
    IN AL, DX
    ; Display raw value on LCD to verify ABCD and DA
    JMP KEYPAD_TEST
```

#### 5. LCD Raw Test
```assembly
; Bypass routines, direct write
MOV DX, PORTA
MOV AL, 'A'
OUT DX, AL
MOV DX, PORTB
MOV AL, 0x01      ; RS=1, E=0
OUT DX, AL
MOV AL, 0x03      ; RS=1, E=1
OUT DX, AL
MOV AL, 0x01      ; RS=1, E=0 (latch)
OUT DX, AL
```

## Code Structure

### Main Sections
1. **Data Segment**: Constants, strings, buffers, flags
2. **Stack Segment**: 128-byte stack
3. **Code Segment**:
   - Initialization (INIT_DEVICES)
   - Password Setup (SET_PASSWORD_MODE)
   - Login System (SEC_SYS_START)
   - Main Menu (MENU_STARTUP)
   - Device Control (RELAY_CONTROL)
   - Timer System (TIMER)
   - LCD Routines (INIT_LCD, INST_CTRL, DATA_CTRL, etc.)
   - Keypad Routines (WAIT_FOR_KEYPRESS_FIXED, etc.)
   - Delay Routines (DELAY_1MS, DEBOUNCE_DELAY, etc.)

### Control Flow
```
START
  ↓
INIT_DEVICES
  ├─ Configure 8255A #1 (LCD + Keypad)
  ├─ Configure 8255A #2 (Relays)
  ├─ Configure 8255A #3 (Aux)
  ├─ Configure 8253A (Timer)
  ├─ Initialize LCD (INIT_LCD)
  └─ Turn off all relays (PORTA2 = 0x00)
  ↓
SET_PASSWORD_MODE (First boot)
  ├─ Prompt for new password
  ├─ Prompt for confirmation
  └─ Verify and save
  ↓
SEC_SYS_START (Login)
  ├─ Read password via keypad
  ├─ Compare with NEW_PASS
  └─ Grant/deny access
  ↓
MENU_STARTUP (Main menu)
  ├─ Read PORTB2 (relay status)
  ├─ Display device states
  └─ Wait for keypad input
  ↓
RELAY_CONTROL (Process input)
  ├─ Toggle device (write PORTA2)
  ├─ Verify via PORTB2
  ├─ Timer mode (if shutting down)
  └─ Lock system (#)
```

## Assembly Best Practices Used

### Register Management
```assembly
SUBROUTINE: 
    PUSH AX          ; Preserve registers
    PUSH BX
    ; ... work ...
    POP BX           ; Restore in reverse order
    POP AX
    RET
```

### Port I/O Pattern
```assembly
MOV DX, PORT_ADDRESS    ; Load port address
IN AL, DX               ; Read (input)
; or
OUT DX, AL              ; Write (output)
```

### Bit Manipulation
```assembly
; Set bit
OR AL, 00000100b        ; Set bit 2

; Clear bit
AND AL, 11111011b       ; Clear bit 2

; Toggle bit
XOR AL, 00000100b       ; Toggle bit 2

; Test bit
TEST AL, 00000100b      ; Test bit 2 (doesn't modify AL)
JZ BIT_WAS_ZERO
```

### Code Organization
- **Clear section comments**: Each section labeled (e.g., ;=== LCD ROUTINES ===)
- **Descriptive labels**: Names like `WAIT_FOR_KEYPRESS_FIXED` vs `FUNC1`
- **Consistent indentation**: 4 spaces for instructions, 0 for labels

## Hardware Setup Checklist

### Before Powering On
- [ ] Verify all three 8255A chips addressed correctly (0xF0, 0xE0, 0xC0 base)
- [ ] Check LCD connections: 
  - [ ] D0-D7 to PORTA (8255A #1)
  - [ ] RS to PORTB bit 0
  - [ ] E to PORTB bit 1
  - [ ] RW to GND
  - [ ] V0 (contrast) to 10kΩ pot
- [ ] Check MM74C922 connections:
  - [ ] ABCD to PORTC bits 0-3
  - [ ] DA to PORTC bit 4
  - [ ] DA to NOT gate to $\overline{OE}$
  - [ ] OSC capacitor (100nF)
- [ ] Check relay circuits:
  - [ ] Control from PORTA2 bits 0-2
  - [ ] Feedback to PORTB2 bits 0-2
  - [ ] Flyback diodes across coils
  - [ ] Proper relay driver (2N2222 + resistors)
- [ ] Check timer cancel button to PORTC2 bit 0
- [ ] Verify power supply rails (+5V, GND)

## Performance Specifications

### Response Times
- **Key Press to Display**: < 50ms (with debouncing)
- **Device Toggle**: < 100ms (relay switching time)
- **Password Check**: < 10ms (4-byte comparison)
- **LCD Update**: ~2ms per character (at 1µs per instruction)

### Resource Usage
- **RAM**: ~100 bytes (strings in code segment)
- **Stack**: 128 bytes allocated
- **I/O Ports**: 12 ports across three 8255As
- **Code Size**: ~3-4KB (depends on assembly listing)

## License & Credits

**Project**: Caesar Cipher Home Automation System  
**Architecture**: 8086 Assembly Language  
**Simulation**: Proteus Design Suite  
**Hardware**: Three 8255A PIAs, MM74C922 Keypad Encoder, LM044L LCD  
**Course**: CPE-3104 Microprocessor Systems  
**Repository**: cedvtan13/3rdYR  
**File**: CPE-3104_MicroProc/CaesarCipher/FinalProj/FinalProj. asm

---

## Quick Reference Card

### Port Quick Reference
| Port | Address | Direction | Function |
|------|---------|-----------|----------|
| PORTA | 0xF0h | OUT | LCD Data (D0-D7) |
| PORTB | 0xF2h | OUT | LCD Control (RS, E) |
| PORTC | 0xF4h | IN | Keypad (ABCD, DA) |
| PORTA2 | 0xE0h | OUT | Relay Control |
| PORTB2 | 0xE2h | IN | Relay Feedback |
| PORTC2 | 0xE4h | IN | Cancel Button |
| PORTA3 | 0xC0h | OUT | Auxiliary |

### Keypad Mapping
| Key | Code | Function | Key | Code | Function |
|-----|------|----------|-----|------|----------|
| 1 | 0x0 | AC | 2 | 0x1 | Outlet |
| 3 | 0x2 | Lights | 4 | 0x4 | Shutdown |
| 5 | 0x5 | 5 min | 6 | 0x6 | 6 min |
| 7 | 0x8 | 7 min | 8 | 0x9 | 8 min |
| 9 | 0xA | 9 min | 0 | 0xD | 0 min |
| * | 0xC | Enter | # | 0xE | Cancel/Lock |

### LCD Addresses
| Line | Start Addr | Range |
|------|------------|-------|
| 1 | 0x80 | 0x80-0x93 |
| 2 | 0xC0 | 0xC0-0xD3 |
| 3 | 0x94 | 0x94-0xA7 |
| 4 | 0xD4 | 0xD4-0xE7 |

### Control Words
| Chip | Register | Value | Meaning |
|------|----------|-------|---------|
| 8255A #1 | 0xF6h | 89h | A: OUT, B:OUT, C:IN |
| 8255A #2 | 0xE6h | 89h | A:OUT, B: OUT, C:IN |
| 8253A | 0xD6h | 37h | Square wave mode |

---

**End of Documentation**
