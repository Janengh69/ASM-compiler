DATA SEGMENT
	VB		DB	111111b				
	VD		DB	0d5h
	VW		DB	5d
	Strin	DB	"DoroshKaruna"
	stri	DB 	"A"
DATA ENDS
CODE SEGMENT
	mov bl, 11000b  
	cmp bl, word GS:[si+1]
	jge label2
EXMPL MACRO
	cmp ax, VW
ENDM
EXMPL
	mov ax, 0d5h
	dec word ptr GS:[si+1]	 		
	add bx, ax	
EXMPL2 MACRO NUM
	inc NUM
	add bx, NUM	
ENDM
EXMPL5 MACRO NUM
	inc NUM
ENDM
EXMPL5 bx
EXMPL2 ax
	mov ax, 0
	mov cx, 0
label2:
	inc al
	cmp ax, VW
	movsw
	jge label2
CODE ENDS
END
