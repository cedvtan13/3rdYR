;====================================================================
; Main.asm with FIXED debouncing and 20x4 LCD support
;====================================================================

DATA SEGMENT
    PORTA       EQU 0F0h
    PORTB       EQU 0F2h
    PORTC       EQU 0F4h
    COM_REG     EQU 0F6h
    
    PORTA2      EQU 0E0h
    PORTB2      EQU 0E2h
    PORTC2      EQU 0E4h
    COM_REG2    EQU 0E6h
    
    PORTA3      EQU 0C0h
    PORTB3      EQU 0C2h
    PORTC3      EQU 0C4h
    COM_REG3    EQU 0C6h
   
    COMT        EQU 0D6h
    
    ; 20-character strings for 20x4 LCD
    CLEAR       DB  "                    ", "$"
    SEC_START   DB  "ENTER PASSWORD:    ", "$"
    
    DENIED      DB  "ACCESS DENIED      ", "$"
    ; REMOVED DEFAULT PASSWORD - ALWAYS SET NEW ONE
    
    ; New password variables
    NEW_PASS    DB  "    ", "$"                     ; 4 spaces for new password
    PASS_SET    DB  00h                             ; Flag: always 1 after setup
    SET_MODE    DB  "SET NEW PASSWORD:  ", "$"
    CONFIRM     DB  "CONFIRM PASSWORD:  ", "$"
    MATCH       DB  "PASSWORD SET!      ", "$"
    NO_MATCH    DB  "NOT MATCHED!       ", "$"
    ; REMOVED SET_PROMPT - GO DIRECTLY TO PASSWORD SETUP
    LOCK_PROMPT DB  "PRESS # TO LOCK    ", "$"
    
    ; Shortened device status strings for 20-char display
    AC_ON       DB  "1.AC: ON    ", "$"
    AC_OFF      DB  "1.AC: OFF   ", "$"
    
    PO_ON       DB  "2.PWR: ON   ", "$"
    PO_OFF      DB  "2.PWR: OFF  ", "$"
    
    LI_ON       DB  "3.LIGHTS: ON ", "$"
    LI_OFF      DB  "3.LIGHTS:OFF ", "$"
    
    SD_ALL      DB  "4.SHUTDOWN ALL ", "$"
    
    TMR         DB  "SET TIMER:       ", "$"
    CANCELLED   DB  "ACTION STOPPED   ", "$"
    
    OFF_PMT     DB  "SHUTTING DOWN... ", "$"
    ON_PMT      DB  "TURNING ON...    ", "$"
    ALL_PMT     DB  "ALL SHUTTING DOWN", "$"
    
    BACK        DB  "#:BACK *:ENTER   ", "$"
    PRESS       DB  "SELECT 0-9 MIN   ", "$"
    
    MIN0        DB  "00 MINUTES       ", "$"
    MIN1        DB  "01 MINUTE        ", "$"
    MIN2        DB  "02 MINUTES       ", "$"
    MIN3        DB  "03 MINUTES       ", "$"
    MIN4        DB  "04 MINUTES       ", "$"
    MIN5        DB  "05 MINUTES       ", "$"
    MIN6        DB  "06 MINUTES       ", "$"
    MIN7        DB  "07 MINUTES       ", "$"
    MIN8        DB  "08 MINUTES       ", "$"
    MIN9        DB  "09 MINUTES       ", "$"
    
    SEC_MSG     DB  "A FEW SECONDS    ", "$"

    TG_FLAG     DB  00h
    MINS_FLAG   DB  00h
    
    ; Temporary buffers
    PASS_BUF    DB  4 DUP(?)
    CONFIRM_BUF DB  4 DUP(?)
    
    ; Keypad debounce flag
    KEY_PRESSED DB  00h
    
DATA ENDS

STK SEGMENT STACK
     BOS DW 64d DUP(?)
     TOS LABEL WORD
STK ENDS

CODE    SEGMENT PUBLIC "CODE"
    ASSUME CS:CODE, DS:DATA

START:
    ; Set up data segment
    MOV AX, DATA
    MOV DS, AX
    
    ; Clear all registers
    XOR AX, AX
    XOR BX, BX
    XOR CX, CX
    XOR DX, DX
    XOR SI, SI
    XOR DI, DI
    
;===========================Initialize device and LCD display=================================
INIT_DEVICES:
    MOV DX, COM_REG
    MOV AL, 89h             ;CONTROL WORD FOR OUTPUT OUTPUT INPUT 8255
    OUT DX, AL
    
    MOV DX, COM_REG2
    MOV AL, 8Bh             ;CONTROL WORD FOR OUTPUT INPUT INPUT 8255
    OUT DX, AL
    
    MOV DX, COM_REG2
    MOV AL, 89h             ;CONTROL WORD FOR OUTPUT OUTPUT INPUT 8255
    OUT DX, AL
    
    MOV DX, COMT
    MOV AL, 37h             ;CONTROL WORD FOR SQUARE WAVE GENERATOR 8253
    OUT DX, AL
    
    ;TURN OFF ALL RELAYS
    MOV DX, PORTA2
    MOV AL, 00h
    OUT DX, AL
    
    CALL INIT_LCD
    
;==========================START WITH PASSWORD SETUP==========================================
; REMOVED CHOOSE MODE - ALWAYS START WITH PASSWORD SETUP
JMP SET_PASSWORD_MODE

;==========================PASSWORD SETTING MODE================================
SET_PASSWORD_MODE:
    CALL CLS
    
    ; Step 1: Enter new password
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, SET_MODE        ; "SET NEW PASSWORD:"
    CALL PRINT_STRING
    
    XOR CX, CX
    MOV SI, OFFSET PASS_BUF ; Point to password buffer
    
ENTER_NEW_PASS:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    ; Check for special keys
    CMP AL, 0Ch              ; '*' to confirm
    JE CONFIRM_NEW_PASSWORD
    CMP AL, 0Eh              ; '#' to cancel/restart
    JE SET_PASSWORD_MODE
    
    ; Store digit with ASCII conversion
    CMP AL, 0Dh              ; Check if 0
    JNE NOT_ZERO1
    MOV AL, '0'              ; Convert to ASCII '0'
    JMP STORE_DIGIT1
    
NOT_ZERO1:
    CMP AL, 09h              ; Check if > 9
    JG ENTER_NEW_PASS        ; Invalid, ignore
    ADD AL, '0'              ; Convert 1-9 to ASCII '1'-'9'
    
STORE_DIGIT1:
    MOV [SI], AL             ; Store ASCII character
    INC SI
    INC CX
    
    ; Display asterisk at correct position
    MOV AL, 0C0h            ; Line 2
    ADD AL, CL              ; Move to position (1-based)
    DEC AL                  ; Adjust to 0-based
    CALL INST_CTRL
    MOV AL, '*'
    CALL DATA_CTRL
    
    CMP CX, 04h
    JL ENTER_NEW_PASS        ; Continue until 4 digits
    
    ; Auto-proceed to confirmation after 4 digits
    JMP CONFIRM_NEW_PASSWORD

CONFIRM_NEW_PASSWORD:
    CALL CLS
    
    ; Step 2: Confirm password
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, CONFIRM         ; "CONFIRM PASSWORD:"
    CALL PRINT_STRING
    
    XOR CX, CX
    MOV SI, OFFSET CONFIRM_BUF ; Point to confirm buffer
    
ENTER_CONFIRM_PASS:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    ; Check for special keys
    CMP AL, 0Ch              ; '*' to confirm
    JE VERIFY_PASSWORDS
    CMP AL, 0Eh              ; '#' to cancel/restart
    JE SET_PASSWORD_MODE
    
    ; Store digit with ASCII conversion
    CMP AL, 0Dh              ; Check if 0
    JNE NOT_ZERO2
    MOV AL, '0'              ; Convert to ASCII '0'
    JMP STORE_DIGIT2
    
NOT_ZERO2:
    CMP AL, 09h              ; Check if > 9
    JG ENTER_CONFIRM_PASS    ; Invalid, ignore
    ADD AL, '0'              ; Convert 1-9 to ASCII '1'-'9'
    
STORE_DIGIT2:
    MOV [SI], AL             ; Store ASCII character
    INC SI
    INC CX
    
    ; Display asterisk at correct position
    MOV AL, 0C0h            ; Line 2
    ADD AL, CL              ; Move to position (1-based)
    DEC AL                  ; Adjust to 0-based
    CALL INST_CTRL
    MOV AL, '*'
    CALL DATA_CTRL
    
    CMP CX, 04h
    JL ENTER_CONFIRM_PASS    ; Continue until 4 digits
    
    ; Auto-verify after 4 digits
    JMP VERIFY_PASSWORDS

VERIFY_PASSWORDS:
    ; Compare PASS_BUF and CONFIRM_BUF (both in ASCII)
    MOV CX, 04h
    MOV SI, OFFSET PASS_BUF
    MOV DI, OFFSET CONFIRM_BUF
    
COMPARE_LOOP:
    MOV AL, [SI]
    MOV BL, [DI]
    CMP AL, BL
    JNE PASSWORDS_DIFFERENT
    INC SI
    INC DI
    LOOP COMPARE_LOOP
    
    ; Passwords match - save to NEW_PASS
    MOV CX, 04h
    MOV SI, OFFSET PASS_BUF
    MOV DI, OFFSET NEW_PASS
    
SAVE_PASSWORD:
    MOV AL, [SI]
    MOV [DI], AL             ; Copy ASCII character
    INC SI
    INC DI
    LOOP SAVE_PASSWORD
    
    ; Set flag to use new password
    MOV PASS_SET, 01h
    
    ; Display success message - FIXED DISPLAY ISSUE
    CALL CLS                 ; Clear screen first
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, CLEAR           ; Clear line 1
    CALL PRINT_STRING
    
    MOV AL, 0C0h            ; Line 2 - CENTER THE MESSAGE
    CALL INST_CTRL
    LEA SI, MATCH           ; "PASSWORD SET!"
    CALL PRINT_STRING
    
    MOV BX, 0FFFh
    CALL DELAY_1MS
    
    JMP SEC_SYS_START

PASSWORDS_DIFFERENT:
    ; Display mismatch message - FIXED DISPLAY ISSUE
    CALL CLS                 ; Clear screen first
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, CLEAR           ; Clear line 1
    CALL PRINT_STRING
    
    MOV AL, 0C0h            ; Line 2 - CENTER THE MESSAGE
    CALL INST_CTRL
    LEA SI, NO_MATCH        ; "NOT MATCHED!"
    CALL PRINT_STRING
    
    MOV BX, 0FFFh
    CALL DELAY_1MS
    
    JMP SET_PASSWORD_MODE

;==========================Security System Start========================================== 
SEC_SYS_START:
    CALL CLS
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, SEC_START       ; "ENTER PASSWORD:"
    CALL PRINT_STRING
    
    ; Clear password buffer
    MOV DI, OFFSET CONFIRM_BUF
    MOV CX, 04h
    MOV AL, 0
CLEAR_PASS_BUF:
    MOV [DI], AL
    INC DI
    LOOP CLEAR_PASS_BUF
    
    XOR CX, CX
    MOV DI, OFFSET CONFIRM_BUF ; Use buffer for entered password
    
GET_PASSWORD_DIGITS:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    ; Store digit with ASCII conversion
    CMP AL, 0Dh              ; Check if 0
    JNE NOT_ZERO_ENTRY
    MOV AL, '0'              ; Convert to ASCII '0'
    JMP STORE_ENTRY
    
NOT_ZERO_ENTRY:
    CMP AL, 09h              ; Check if > 9
    JG GET_PASSWORD_DIGITS   ; Invalid, ignore
    ADD AL, '0'              ; Convert 1-9 to ASCII '1'-'9'
    
STORE_ENTRY:
    MOV [DI], AL             ; Store in buffer
    INC DI
    INC CX
    
    ; Display asterisk at correct position
    MOV AL, 0C0h            ; Line 2
    ADD AL, CL              ; Move to position
    DEC AL                  ; Adjust
    CALL INST_CTRL
    MOV AL, '*'
    CALL DATA_CTRL
    
    CMP CX, 04h
    JL GET_PASSWORD_DIGITS   ; Continue until 4 digits
    
    ; Now verify the password - ALWAYS CHECK AGAINST NEW_PASS
    ; REMOVED DEFAULT PASSWORD CHECK
    MOV CX, 04h
    MOV SI, OFFSET NEW_PASS
    MOV DI, OFFSET CONFIRM_BUF
    
CHECK_PASSWORD:
    MOV AL, [SI]
    MOV BL, [DI]
    CMP AL, BL
    JNE ACCESS_DENIED
    INC SI
    INC DI
    LOOP CHECK_PASSWORD
    
    JMP MENU_STARTUP         ; Password correct

ACCESS_DENIED:
    ; FIXED DISPLAY ISSUE - Clear screen and properly display message
    CALL CLS                 ; Clear entire screen first
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, DENIED          ; "ACCESS DENIED"
    CALL PRINT_STRING
    
    ; No stack to clear here since we're using buffer
    MOV CX, 03h
DENIED_DELAY:
    CALL DELAY2
    LOOP DENIED_DELAY
    
    JMP SEC_SYS_START

;===========================POWER CONTROL SYSTEM================================================= 
MENU_STARTUP:
    CALL CLS
    
    ; Display lock prompt at top (Line 1)
    MOV AL, 080h            ; Line 1, column 0
    CALL INST_CTRL
    LEA SI, LOCK_PROMPT     ; "PRESS # TO LOCK"
    CALL PRINT_STRING
    
CHECK_STATUS_AC:
    MOV AL, 0C0h            ; Line 2, column 0
    CALL INST_CTRL
    
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 001b
    JNZ CHECK_AC_ON
    CALL AC_L
    JMP CHECK_STATUS_PO
    
CHECK_STATUS_PO:
    MOV AL, 0C0h            ; Line 2, continue
    CALL INST_CTRL
    
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 010b
    JNZ CHECK_PO_ON
    CALL PO_L
    JMP CHECK_STATUS_LI
    
CHECK_STATUS_LI:
    MOV AL, 094h            ; Line 3, column 0
    CALL INST_CTRL
    
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 100b
    JNZ CHECK_LI_ON
    CALL LI_L
    CALL SD
    JMP RELAY_CONTROL
       
CHECK_AC_ON:
    CALL AC_H
    JMP CHECK_STATUS_PO
    
CHECK_PO_ON:
    CALL PO_H
    JMP CHECK_STATUS_LI
    
CHECK_LI_ON:
    CALL LI_H
    CALL SD
    JMP RELAY_CONTROL

;===========================Relay Control System=========================================
RELAY_CONTROL:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    ; Process the key
    CMP AL, 00h              ; Button 1 - AC Toggle
    JE CHECK_AC_STATUS
    
    CMP AL, 01h              ; Button 2 - PO Toggle
    JE CHECK_PO_STATUS
    
    CMP AL, 02h              ; Button 3 - LI Toggle
    JE CHECK_LI_STATUS
    
    CMP AL, 04h              ; Button 4 - Shutdown Toggle
    JE SHUTDOWN_ALL
    
    CMP AL, 0Eh              ; Button # - Lock system
    JE LOCK_SYSTEM
    
    ; Invalid key
    JMP RELAY_CONTROL

LOCK_SYSTEM:
    CALL WAIT_FOR_RELEASE_FIXED
    JMP SEC_SYS_START
    
;============================AC==================================
CHECK_AC_STATUS:
    CALL WAIT_FOR_RELEASE_FIXED
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 01h
    JZ TURN_AC_ON
    JMP TURN_AC_OFF
    
TURN_AC_ON:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, ON_PMT          ; "TURNING ON..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    OR AL, 001b
    OUT DX, AL
    JMP MENU_STARTUP
    
TURN_AC_OFF:
    MOV SI, 0Fh
    MOV AL, 001b
    MOV [SI], AL
    JMP TIMER
    
AC_OFF_NEXT:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, OFF_PMT         ; "SHUTTING DOWN..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    AND AL, 11111110b
    OUT DX, AL
    JMP MENU_STARTUP

;============================POWER OUTLET==================================
CHECK_PO_STATUS:
    CALL WAIT_FOR_RELEASE_FIXED
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 02h
    JZ TURN_PO_ON
    JMP TURN_PO_OFF
    
TURN_PO_ON:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, ON_PMT          ; "TURNING ON..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    OR AL, 010b
    OUT DX, AL
    JMP MENU_STARTUP
    
TURN_PO_OFF:
    MOV SI, 0Fh
    MOV AL, 010b
    MOV [SI], AL
    JMP TIMER
    
PO_OFF_NEXT:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, OFF_PMT         ; "SHUTTING DOWN..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    AND AL, 11111101b
    OUT DX, AL
    JMP MENU_STARTUP

;==============================LIGHTS==================================
CHECK_LI_STATUS:
    CALL WAIT_FOR_RELEASE_FIXED
    MOV DX, PORTB2
    IN AL, DX
    AND AL, 04h
    JZ TURN_LI_ON
    JMP TURN_LI_OFF
    
TURN_LI_ON:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, ON_PMT          ; "TURNING ON..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    OR AL, 100b
    OUT DX, AL
    JMP MENU_STARTUP
    
TURN_LI_OFF:
    MOV SI, 0Fh
    MOV AL, 100b
    MOV [SI], AL
    JMP TIMER
    
LI_OFF_NEXT:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, OFF_PMT         ; "SHUTTING DOWN..."
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    IN AL, DX
    AND AL, 11111011b
    OUT DX, AL
    JMP MENU_STARTUP

;==============================SHUTDOWN ALL==================================
SHUTDOWN_ALL:
    CALL WAIT_FOR_RELEASE_FIXED
    MOV SI, 0Fh
    MOV AL, 000b
    MOV [SI], AL
    JMP TIMER

SD_OFF_NEXT:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, ALL_PMT         ; "ALL SHUTTING DOWN"
    CALL PRINT_STRING
    CALL DELAY_RELAY
    MOV DX, PORTA2
    MOV AL, 000b
    OUT DX, AL
    JMP MENU_STARTUP

;========================================================================
ALL_OFF:
    CALL AC_L
    CALL PO_L
    CALL LI_L
    CALL SD
RET
    
AC_L:
    MOV AL, 0C0h            ; Line 2, column 0
    CALL INST_CTRL
    LEA SI, AC_OFF          ; "1.AC: OFF"
    CALL PRINT_STRING
RET
    
AC_H:
    MOV AL, 0C0h            ; Line 2, column 0
    CALL INST_CTRL
    LEA SI, AC_ON           ; "1.AC: ON"
    CALL PRINT_STRING
RET
    
PO_L:
    MOV AL, 0C0h            ; Line 2
    MOV AL, 0CAh            ; Line 2, column 10
    CALL INST_CTRL
    LEA SI, PO_OFF          ; "2.PWR: OFF"
    CALL PRINT_STRING
RET
    
PO_H:
    MOV AL, 0C0h
    MOV AL, 0CAh            ; Line 2, column 10
    CALL INST_CTRL
    LEA SI, PO_ON           ; "2.PWR: ON"
    CALL PRINT_STRING
RET
    
LI_L:
    MOV AL, 094h            ; Line 3, column 0
    CALL INST_CTRL
    LEA SI, LI_OFF          ; "3.LIGHTS:OFF"
    CALL PRINT_STRING
RET
    
LI_H:
    MOV AL, 094h            ; Line 3, column 0
    CALL INST_CTRL
    LEA SI, LI_ON           ; "3.LIGHTS: ON"
    CALL PRINT_STRING
RET

SD:
    MOV AL, 0D4h            ; Line 4, column 0
    CALL INST_CTRL
    LEA SI, SD_ALL          ; "4.SHUTDOWN ALL"
    CALL PRINT_STRING
RET

;========================================================================
; FIXED DEBOUNCING ROUTINES
;========================================================================

; Wait for a key press with PROPER debouncing (waits for press AND release)
WAIT_FOR_KEYPRESS_FIXED:
    PUSH DX
    PUSH BX
    
    ; First wait for NO key pressed
WAIT_NO_KEY:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Check if key is available
    JNZ WAIT_NO_KEY         ; Wait until no key
    
    CALL DEBOUNCE_DELAY     ; Debounce no-key
    
    ; Now wait for key press
WAIT_KEY_PRESS:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Check if key is available
    JZ WAIT_KEY_PRESS       ; Wait for key press
    
    CALL DEBOUNCE_DELAY     ; Debounce press
    
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Verify key is still pressed
    JZ WAIT_KEY_PRESS       ; If not, it was noise
    
    ; Key is pressed - get value
    AND AL, 0Fh             ; Get key value
    MOV BL, AL              ; Save it
    
    ; Now wait for key release
WAIT_KEY_RELEASE:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Check if key is still pressed
    JNZ WAIT_KEY_RELEASE    ; Wait for release
    
    CALL DEBOUNCE_DELAY     ; Debounce release
    
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Verify key is still released
    JNZ WAIT_KEY_RELEASE    ; If not, continue waiting
    
    MOV AL, BL              ; Restore key value
    POP BX
    POP DX
RET

; Wait for key release (standalone)
WAIT_FOR_RELEASE_FIXED:
    PUSH AX
    PUSH DX
    CALL DEBOUNCE_DELAY     ; Initial debounce
    
WAIT_FOR_REL_FIXED:
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Check if key is still pressed
    JNZ WAIT_FOR_REL_FIXED  ; Keep waiting if still pressed
    
    CALL DEBOUNCE_DELAY     ; Debounce release
    
    MOV DX, PORTC
    IN AL, DX
    TEST AL, 10h            ; Check again
    JNZ WAIT_FOR_REL_FIXED  ; If still pressed, continue waiting
    
    POP DX
    POP AX
RET

; Standard debounce delay (~20ms)
DEBOUNCE_DELAY:
    PUSH BX
    MOV BX, 00C8h           ; 200 decimal = ~20ms
    CALL DELAY_1MS
    POP BX
RET

;========================================================================
; TIMER (Updated for 20x4 display)
;========================================================================
TIMER:
    CALL CLS
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, TMR             ; "SET TIMER:"
    CALL PRINT_STRING
    
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, PRESS           ; "SELECT 0-9 MIN"
    CALL PRINT_STRING
    
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN0            ; "00 MINUTES"
    CALL PRINT_STRING
    
    LEA SI, BACK
    MOV AL, 0D4h            ; Line 4
    CALL INST_CTRL
    CALL PRINT_STRING
   
TIMER_INPUT_LOOP:
    CALL WAIT_FOR_KEYPRESS_FIXED
    
    ; Process timer input
    CMP AL, 00H
    JE M1
    CMP AL, 01H
    JE M2
    CMP AL, 02H
    JE M3
    CMP AL, 04H
    JE M4
    CMP AL, 05H
    JE M5
    CMP AL, 06H
    JE M6
    CMP AL, 08H
    JE M7
    CMP AL, 09H
    JE M8
    CMP AL, 0AH
    JE M9
    CMP AL, 0DH             ; 0
    JE M0
    CMP AL, 0CH             ; * to start
    JE TIMER_START
    CMP AL, 0Eh             ; # to go back
    JE MENU_STARTUP
    
    ; Invalid key
    JMP TIMER_INPUT_LOOP

M0:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN0
    CALL PRINT_STRING
    MOV MINS_FLAG, 0
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M1:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN1
    CALL PRINT_STRING
    MOV MINS_FLAG, 1
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M2:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN2
    CALL PRINT_STRING
    MOV MINS_FLAG, 2
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M3:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN3
    CALL PRINT_STRING
    MOV MINS_FLAG, 3
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M4:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN4
    CALL PRINT_STRING
    MOV MINS_FLAG, 4
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M5:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN5
    CALL PRINT_STRING
    MOV MINS_FLAG, 5
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M6:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN6
    CALL PRINT_STRING
    MOV MINS_FLAG, 6
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M7:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN7
    CALL PRINT_STRING
    MOV MINS_FLAG, 7
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M8:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN8
    CALL PRINT_STRING
    MOV MINS_FLAG, 8
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
M9:
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, MIN9
    CALL PRINT_STRING
    MOV MINS_FLAG, 9
    CALL WAIT_FOR_RELEASE_FIXED
    JMP TIMER_INPUT_LOOP
    
TIMER_START:
    CALL WAIT_FOR_RELEASE_FIXED
    CALL CLS
    
    ; Check which minute was selected
    CMP MINS_FLAG, 00h
    JE SET_MIN0
    CMP MINS_FLAG, 01h
    JE SET_MIN1
    CMP MINS_FLAG, 02h
    JE SET_MIN2
    CMP MINS_FLAG, 03h
    JE SET_MIN3
    CMP MINS_FLAG, 04h
    JE SET_MIN4
    CMP MINS_FLAG, 05h
    JE SET_MIN5
    CMP MINS_FLAG, 06h
    JE SET_MIN6
    CMP MINS_FLAG, 07h
    JE SET_MIN7
    CMP MINS_FLAG, 08h
    JE SET_MIN8
    CMP MINS_FLAG, 09h
    JE SET_MIN9
    
SET_MIN0:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    MOV SI, 0Fh
    MOV AL, [SI]
    CMP AL, 000b
    JE SD_OFF_NEXT
    CMP AL, 001b
    JE AC_OFF_NEXT
    CMP AL, 010b
    JE PO_OFF_NEXT
    CMP AL, 100b
    JE LI_OFF_NEXT
    
SET_MIN1:
    DEC MINS_FLAG
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, SEC_MSG
    CALL PRINT_STRING
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN2:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN1
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN3:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN2
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN4:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN3
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN5:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN4
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN6:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN5
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN7:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN6
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN8:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN7
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START
    
SET_MIN9:
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, MIN8
    CALL PRINT_STRING
    DEC MINS_FLAG
    CALL TIMER_SECONDS
    JMP TIMER_START

TIMER_SECONDS:
    MOV DX, 05h
    
SEC_DELAY:
    XOR AX, AX
    PUSH DX
    MOV DX, PORTC2
    IN AL, DX
    CMP AL, 00h
    JE CANCEL
    POP DX
    CALL DELAY
    DEC DX
    CMP DX, 00h
    JE DONE
    JMP SEC_DELAY
    
DONE:
RET

CANCEL:
    CALL CLS
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, CANCELLED
    CALL PRINT_STRING
    CALL DELAY_RELAY
    CALL CLS
    JMP MENU_STARTUP

;========================================================================
; UTILITY ROUTINES
;========================================================================

CLS:
    MOV AL, 080h            ; Line 1
    CALL INST_CTRL
    LEA SI, CLEAR
    CALL PRINT_STRING
    
    MOV AL, 0C0h            ; Line 2
    CALL INST_CTRL
    LEA SI, CLEAR
    CALL PRINT_STRING
    
    MOV AL, 094h            ; Line 3
    CALL INST_CTRL
    LEA SI, CLEAR
    CALL PRINT_STRING
    
    MOV AL, 0D4h            ; Line 4
    CALL INST_CTRL
    LEA SI, CLEAR
    CALL PRINT_STRING
RET
    
PRINT_STRING:
    MOV AL, [SI]
    CMP AL, "$"
    JE PS_DONE
    CALL DATA_CTRL
    INC SI
    JMP PRINT_STRING
PS_DONE:
RET
 
DELAY:
    MOV CX, 0FFCh
L3:
    PUSH CX
    MOV CX, 10
L2:
    NOP
    LOOP L2
    POP CX
    LOOP L3
RET
 
DELAY1:
    MOV BX, 0FFh
    CALL DELAY_1MS
RET
  
DELAY2:
    MOV BX, 0FFF5h
    CALL DELAY_1MS
RET
 
DELAY_RELAY:
    MOV BX, 0FFF1h
    CALL DELAY_1MS
RET
 
DELAY_KEYPAD:
    MOV BX, 0032h
    CALL DELAY_1MS
RET
 
DELAY_1MS:
    MOV DX, PORTA3
    MOV AL, 0CFH
    OUT DX, AL
    MOV AL, 07H
    OUT DX, AL
    DEC BX
    JNZ DELAY_1MS
RET

INIT_LCD:
    MOV AL, 38h             ; 8-bit, 2-line, 5x7 font
    CALL INST_CTRL
    MOV AL, 08h             ; Display off
    CALL INST_CTRL
    MOV AL, 01h             ; Clear display
    CALL INST_CTRL
    MOV AL, 06h             ; Entry mode: increment, no shift
    CALL INST_CTRL
    MOV AL, 0Ch             ; Display on, cursor off
    CALL INST_CTRL
RET

INST_CTRL:
    PUSH AX
    MOV DX, PORTA
    OUT DX, AL
    MOV DX, PORTB
    MOV AL, 02h             ; RS=0, RW=0, E=1 (pulse)
    OUT DX, AL
    CALL DELAY1
    MOV DX, PORTB
    MOV AL, 00h             ; RS=0, RW=0, E=0
    OUT DX, AL
    POP AX
RET

DATA_CTRL:
    PUSH AX
    MOV DX, PORTA
    OUT DX, AL
    MOV DX, PORTB
    MOV AL, 03h             ; RS=1, RW=0, E=1 (pulse)
    OUT DX, AL
    CALL DELAY1
    MOV DX, PORTB
    MOV AL, 01h             ; RS=1, RW=0, E=0
    OUT DX, AL
    POP AX
RET
 
ENDLESS:
    JMP ENDLESS
    
CODE    ENDS
    END START
