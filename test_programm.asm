DATA SEGMENT
	VB		DB	111111b
	VD		DD	0d34dah
	VW		DW	5d
	Stringd	DB	"DoroshKaruna"
	stri	DB 	"A"
DATA ENDS
	
CODE SEGMENT
	mov bl, 11000b
EXMPL MACRO 	
	and VB, bl		;direct adressing
	or	VB, 110	
ENDM  
EXMPL
	mov ax, 0d5h
	dec word ptr GS:[si+1]			;basic adressing
	add word ptr VD, ax			
EXMPL2 MACRO NUM
	inc NUM
ENDM	
EXMPL2 6
	mov si, offset String
	mov di, offset stri
	
	mov ax, 0
	mov cx, 8
@label2:
	inc ax
	cmp VW, ax
	movsw
	jge @label2

CODE ENDS
END