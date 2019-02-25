
DATA SEGMENT use 16
	VB		db	111111b
	VD		dd	0d34dah		;865 498
	VW		dw	6d
	String	db	"DoroshKaruna"
	str		db 	"A"
DATA ENDS
	
CODE SEGMENT use 16
ASSUME cs:CODE, ds:DATA, es:DATA
	mov ax, DATA
	mov ds, ax
	mov es, ax
	mov bl, 11000b
	and [VB], bl		;direct adressing
	or	VB, 110			;11110b
		
	mov ax, 0d5h
	dec word ptr VD[si]			;0d34d9h basic adressing
	add word ptr VD, ax			;0eO9feh
	
	lea si, String
	lea di, str
	
	mov ax, 0
	mov cx, 8
@label2:
	inc ax
	cmp VW, ax
	movsw
	jge @label2

CODE ENDS
END