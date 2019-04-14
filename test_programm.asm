DATA SEGMENT
	VB		DB	111111b				
	VD		DD	0d34dah
	VW		DW	5d
	Strin	DB	"DoroshKaruna"
	stri	DB 	"A"
DATA ENDS
CODE SEGMENT
	mov bl, 11000b
	cmp bl, VB
	jge label2
EXMPL MACRO 	
	and VB, bl		
	or	VB, 110	
ENDM  
EXMPL
	mov ax, 0d5h
	dec word ptr GS:[si+1]			
	add word ptr VD, ax			
EXMPL2 MACRO NUM
	inc NUM
ENDM	
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
