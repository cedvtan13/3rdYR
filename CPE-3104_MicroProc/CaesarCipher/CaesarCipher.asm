;  Name: Soriano, Tan
;  Description: Caesar Cipher in assembly lang

.model small
.stack 100h

.data
  prompt db 'Enter String: $'
  orig db 0dh, 0ah, 'Original: $'
  enc db 0dh, 0ah, 'Encrypted: $'
  newline db 0dh, 0ah, '$'
  input db 21, 0, 21 dup('$')
  result db 21 dup('$')

.code
  start:
    mov ax, @data
    mov ds, ax

    ;input
    mov ah, 9
    lea dx, prompt
    int 21h
    mov ah, 0ah
    lea dx, input
    int 21h

    ;shift by 3
    mov si, offset input+2
    mov di, offset result
    mov cl, [input+1]
    mov ch, 0
    mov bl, 3

  encrypt:
    jcxz show
    mov al, [si]

    cmp al, 'A'
    jb store
    cmp al, 'Z'
    jbe upper
    cmp al, 'a'
    jb store
    cmp al, 'z'
    jbe upper

  upper:
    add al, bl
    cmp al, 'z'
    jle store
    sub al, 26

  store:
    mov [di], al
    inc si
    inc di
    dec cx
    jmp encrypt

  show:
    ;had problem here for duplicating shi
    ;dupplicating encyptedd mssg
    mov si, offset input+2
    mov cl, [input+1]               ;chatgpt this part, this is for getting length
    mov ch, 0
    add si, cx
    mov byte ptr [si], '$'

    mov ah, 9
    lea dx, orig
    int 21h
    lea dx, input+2
    int 21h

    lea dx, enc
    int 21h
    lea dx, result
    int 21h

    lea dx, newline
    int 21h

    mov ah, 4ch
    int 21h
    
end start
