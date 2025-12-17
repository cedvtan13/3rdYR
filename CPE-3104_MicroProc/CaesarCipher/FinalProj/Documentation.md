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
- **8255A** - Programmable Peripheral Interface (Multiple instances)
- **8259** - Programmable Interrupt Controller

### Input/Output Devices
- **BUTTON** - Physical push buttons
- **KEYPAD-PHONE** - 4x4 Matrix Keypad (0-9, *, #)
- **LCD (20x4)** - 20 characters × 4 lines display

### Power & Control Components
- **CAPACITOR** - Filtering/decoupling capacitors
- **DIODE** - Protection diodes
- **FUSE** - Circuit protection
- **LAMP** - Visual indicators/controlled devices
- **LED** - Status indicators
- **LM044L** - LCD Controller (20x4)
- **LOGICSTATE** - Logic level indicators
- **MM74C922** - 16-Key Encoder IC
- **RELAY** - Electromagnetic switches for device control
- **RES (Resistor)** - Pull-up/pull-down resistors
- **VSINE** - AC power source simulation

## System Architecture

### Port Configuration

#### 8255A #1 (Main I/O)
- **PORTA (0xF0h)** - Not used in current code
- **PORTB (0xF2h)** - Not used in current code
- **PORTC (0xF4h)** - Keypad input (4-bit key value + status bit)
- **COM_REG (0xF6h)** - Control register (Mode:  89h - OUT/OUT/IN)

#### 8255A #2 (Device Control)
- **PORTA2 (0xE0h)** - Relay control output (3 bits:  AC, Power Outlet, Lights)
- **PORTB2 (0xE2h)** - Device status input (reads relay feedback)
- **PORTC2 (0xE4h)** - Not actively used
- **COM_REG2 (0xE6h)** - Control register (Mode: 89h - OUT/OUT/IN)

#### 8255A #3
- **PORTA3 (0xC0h)** - Reserved
- **PORTB3 (0xC2h)** - Reserved
- **PORTC3 (0xC4h)** - Reserved
- **COM_REG3 (0xC6h)** - Control register

#### 8253A Timer
- **COMT (0xD6h)** - Timer control register (Mode: 37h - Square wave generator)

### Relay Control Bit Mapping
- **Bit 0** - Air Conditioner (AC)
- **Bit 1** - Power Outlet (PO)
- **Bit 2** - Lights (LI)

## Features

### 1. Security System
- **Password Protection**:  4-digit password required for access
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
- **Visual Feedback**:  Countdown display on LCD

### 4. User Interface (20x4 LCD)

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

## Keypad Layout

```
[1] [2] [3] [A]
[4] [5] [6] [B]
[7] [8] [9] [C]
[*] [0] [#] [D]
```

### Key Functions
- **0-9**: Numeric input for passwords and timers
- **\***: Enter/Confirm action
- **#**: Back/Cancel or Lock system
- **A-D**: Not used in current implementation

### Key Value Mapping (Port C Lower Nibble)
- `0x00` = 1
- `0x01` = 2
- `0x02` = 3
- `0x04` = 4
- `0x05` = 5
- `0x06` = 6
- `0x08` = 7
- `0x09` = 8
- `0x0A` = 9
- `0x0C` = * (Enter)
- `0x0D` = 0
- `0x0E` = # (Back/Lock)

## Operation Flow

### Startup Sequence
1. **Initialize Devices**
   - Configure 8255A ports (I/O direction)
   - Set 8253A timer mode
   - Turn off all relays
   - Initialize LCD display

2. **Password Setup** (First Boot)
   - Display "SET NEW PASSWORD:"
   - User enters 4-digit password (displays as ****)
   - Display "CONFIRM PASSWORD:"
   - User re-enters password
   - If match:  "PASSWORD SET!" → Continue to main menu
   - If mismatch: "NOT MATCHED!" → Restart setup

### Normal Operation

1. **Login Screen**
   - Display "ENTER PASSWORD:"
   - User enters 4-digit password
   - If correct: Access granted → Main menu
   - If incorrect: "ACCESS DENIED" → Retry after 3-second delay

2. **Main Menu**
   - Display "PRESS # TO LOCK" (Line 1)
   - Show device status (Lines 2-4):
     ```
     1. AC:  ON/OFF    2.PWR: ON/OFF
     3.LIGHTS: ON/OFF
     4.SHUTDOWN ALL
     ```

3. **Device Control**
   - Press 1-3 to toggle individual devices
   - Press 4 for shutdown all
   - Press # to lock system (return to login)

4. **Timer Mode** (when turning off device)
   - Display "SET TIMER:"
   - Display "SELECT 0-9 MIN"
   - Show current selection (updates as user presses keys)
   - Press * to start countdown
   - Press # to cancel and return to main menu
   - Timer counts down and executes shutdown

## Debouncing Implementation

The system uses **hardware-assisted debouncing** with the MM74C922 encoder IC, complemented by software debouncing: 

### Software Debouncing Strategy
```assembly
WAIT_FOR_KEYPRESS_FIXED:
1. Wait for NO key pressed
2. Debounce delay (~20ms)
3. Wait for key press
4. Debounce delay (~20ms)
5. Verify key still pressed (reject noise)
6. Read key value
7. Wait for key release
8. Debounce delay (~20ms)
9. Verify key still released
10. Return key value
```

This prevents: 
- **Bounce errors**:  Multiple reads from single press
- **Ghost presses**: Electrical noise interpreted as input
- **Stuck keys**: System waiting indefinitely

## Timing Specifications

### Delays
- **DEBOUNCE_DELAY**: ~20ms (200 × 1ms loops)
- **DELAY_RELAY**: Variable delay for relay switching safety
- **DELAY2**:  3-second denial message display
- **Timer countdown**: 1-minute intervals with visual updates

### Timer Resolution
- **Minimum**: 0 minutes (immediate)
- **Maximum**: 9 minutes
- **Countdown display**: Updates every minute
- **Final countdown**: "A FEW SECONDS" for last minute

## Memory Organization

### Data Segment Variables

#### Password Storage
```assembly
NEW_PASS     DB "    ", "$"    ; 4-byte password (ASCII)
PASS_SET     DB 00h            ; Flag:  01h after setup
PASS_BUF     DB 4 DUP(?)       ; Temporary input buffer
CONFIRM_BUF  DB 4 DUP(?)       ; Confirmation buffer
```

#### Display Strings
- All strings padded to 20 characters for 20x4 LCD
- Terminated with "$" for printing routine

#### Control Flags
- **TG_FLAG**: Toggle state tracking
- **MINS_FLAG**: Selected timer duration (0-9)
- **KEY_PRESSED**: Debounce state flag

### Stack Segment
```assembly
BOS DW 64d DUP(?)    ; Bottom of stack (64 words)
TOS LABEL WORD       ; Top of stack pointer
```

## LCD Control

### Instruction Commands
- **0x01**: Clear display
- **0x38**: 2-line mode, 5×7 font
- **0x0E**: Display ON, cursor ON
- **0x06**: Entry mode, increment cursor
- **0x80**: Set cursor to Line 1, column 0
- **0xC0**: Set cursor to Line 2, column 0
- **0x94**: Set cursor to Line 3, column 0
- **0xD4**: Set cursor to Line 4, column 0

### Display Routines
- **INIT_LCD**: Initialize LCD in 2-line mode
- **CLS**: Clear screen
- **INST_CTRL**: Send instruction to LCD
- **DATA_CTRL**: Send character data to LCD
- **PRINT_STRING**: Print null-terminated string

## Error Handling

### Password Errors
- **Mismatch**: Return to setup screen, no lockout
- **Incorrect entry**: Display "ACCESS DENIED", 3-second timeout, retry allowed
- **No penalties**: Unlimited retry attempts (consider adding lockout in production)

### Input Validation
- **Numeric only**: Only 0-9 accepted for passwords/timers
- **Fixed length**:  Exactly 4 digits required for passwords
- **Range check**: Timer accepts 0-9 minutes only
- **Invalid keys ignored**: Non-assigned keys have no effect

## Safety Features

### Relay Protection
- **Startup state**: All relays OFF by default
- **Switching delay**:  DELAY_RELAY prevents contact bounce
- **Status verification**: Reads back relay state from PORTB2
- **Emergency shutdown**: Button 4 cuts all power

### Password Security
- **Masked input**: Displays asterisks (****) instead of digits
- **ASCII storage**: Stored as ASCII characters ('0'-'9')
- **Comparison**: Byte-by-byte verification
- **No echo**: Input not visible in memory dumps

### System Integrity
- **Register clearing**: All registers zeroed on startup
- **Port initialization**: Explicit mode setting for all 8255A chips
- **Watchdog concept**: Could add timer-based auto-lock (not implemented)

## Limitations & Considerations

### Current Limitations
1. **No EEPROM**: Password lost on power cycle (resets to setup mode)
2. **No brute-force protection**:  Unlimited password attempts
3. **Fixed timer range**: Only 0-9 minutes, no seconds precision
4. **Single user**: No multi-user support
5. **No logging**: No history of access or device state changes

### Hardware Dependencies
- Requires **MM74C922** for keypad encoding
- Needs **8253A** for timer functionality (though minimally used)
- Relies on **8255A** for all I/O operations
- LCD must be **LM044L-compatible** (20x4)

### Proteus Simulation Notes
- Hardware works in **Proteus 8.x+**
- Ensure proper crystal oscillator settings for 8086
- Configure 8255A ports before use
- Check LCD contrast settings in simulation

## Future Enhancements

### Suggested Improvements
1. **EEPROM Integration**:  Persistent password storage
2. **RTC Module**: Real-time clock for scheduling
3. **Multiple Users**: User profiles with different access levels
4. **Event Logging**: Track usage patterns
5. **Remote Control**: Serial/wireless interface
6. **Temperature Sensing**: Auto-control AC based on temperature
7. **Power Monitoring**: Track energy usage per device
8. **Voice Feedback**: Audio prompts via speaker

### Code Optimizations
- Consolidate repeated LCD position calls
- Create macro for device status display
- Implement interrupt-driven keypad reading
- Use lookup tables for minute display strings
- Add checksum for password integrity

## Troubleshooting

### Common Issues

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| LCD shows garbage | Incorrect initialization | Check INIT_LCD timing, verify 8255A mode |
| Keys not responding | Debounce too short | Increase DEBOUNCE_DELAY value |
| Multiple key reads | Insufficient release wait | Ensure WAIT_FOR_RELEASE called |
| Relay not switching | Wrong port/bit | Verify PORTA2 connections, check relay driver |
| Timer doesn't count | 8253A misconfigured | Check COMT initialization (37h) |
| Password always fails | ASCII mismatch | Ensure digits converted to ASCII ('0'-'9') |

### Debug Tips
1. **Monitor ports**: Use Proteus logic analyzer on PORTA2, PORTC
2. **Check flags**: Watch PASS_SET, MINS_FLAG, KEY_PRESSED
3. **LCD debugging**: Display debug values using DATA_CTRL
4. **Relay feedback**: Read PORTB2 to confirm relay state
5. **Timing issues**: Adjust delay loops if simulation speed varies

## Code Structure

### Main Sections
1. **Initialization** (INIT_DEVICES)
2. **Password Setup** (SET_PASSWORD_MODE)
3. **Login System** (SEC_SYS_START)
4. **Main Menu** (MENU_STARTUP)
5. **Device Control** (RELAY_CONTROL)
6. **Timer System** (TIMER)
7. **Utility Routines** (LCD, Delays, Debouncing)

### Control Flow
```
START
  ↓
INIT_DEVICES → Initialize hardware
  ↓
SET_PASSWORD_MODE → First-time setup
  ↓
SEC_SYS_START → Login screen
  ↓
MENU_STARTUP → Main menu (device status)
  ↓
RELAY_CONTROL → Handle button presses
  ↓
├─ Device Toggle (AC/PO/LI)
├─ TIMER → Delayed shutdown
└─ LOCK_SYSTEM → Return to login
```

## Assembly Best Practices Used

### Register Management
- Push/pop registers in subroutines
- Clear registers before use
- Preserve critical values in memory

### Code Organization
- Clear section comments
- Descriptive labels
- Consistent indentation

### Hardware Interaction
- Explicit port definitions
- Read-modify-write for bit operations
- Status verification after writes

## License & Credits

**Project**: Caesar Cipher Home Automation System  
**Architecture**: 8086 Assembly Language  
**Simulation**: Proteus Design Suite  
**Author**: [Your Name/Team]  
**Course**: CPE-3104 Microprocessor Systems  

---

## Quick Reference Card

### Keypad Quick Guide
| Key | Function |
|-----|----------|
| 0-9 | Enter digit |
| * | Confirm/Enter |
| # | Back/Lock |

### Device Buttons
| Button | Device |
|--------|--------|
| 1 | Air Conditioner |
| 2 | Power Outlet |
| 3 | Lights |
| 4 | Shutdown All |

### LCD Addresses
| Line | Address | Usage |
|------|---------|-------|
| 1 | 0x80 | Title/Prompt |
| 2 | 0xC0 | Input/Status 1 |
| 3 | 0x94 | Status 2 |
| 4 | 0xD4 | Options |

### Port Map
| Port | Address | Function |
|------|---------|----------|
| PORTC | 0xF4h | Keypad input |
| PORTA2 | 0xE0h | Relay control |
| PORTB2 | 0xE2h | Relay status |

---

**End of Documentation**
