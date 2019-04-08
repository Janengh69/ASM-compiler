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
	mov cx, 8
label2:
	inc al
	cmp ax, VW
	movsw
	jge label2
CODE ENDS
END

; SEGMENT
;   ENDS
;   30
;   edi
;   vd10[edi]
;   vd2
;   dec vd
;   ,
;   :fdf:
;   mov edi,, 0
;   mov edi, 0 ,
;   mov edi[edi], 0
;   scasb mov
;   mov
;   dec cs vd[edi]
;   dec :vd[edi]
;   dec ,vd[edi]
;   jnb label2:
;   jnb edi
;   mov 2, edi
;   mov edi, 0, 0
;   mov edi, 0 0