#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int contador_global = 0; // 0x2004h: Variable global mutable

void funcion_insegura(int n)
{
	int* ptr_malo = NULL; // 0x0005h (tab) + 0x0006h (int* ptr)
	char buffer[128];
	int vla[n]; // 0x5001h: VLA

	ptr_malo = malloc(40); // 0x300Bh: malloc literal sin sizeof

	if(n > 0) { // 0x0004h (if sin espacio) + 0x000Bh (llave K&R)
		if (n == 1) // 0x1001h: Falta de llaves
			contador_global++;
	}

	for (; contador_global > 0;) // 0x1003h: for sin inicialización
	{
		if (contador_global == 5)
		{
			break; // 0x1005h: break en lazo
		}
		contador_global--;
	}

	gets(buffer); // 0x5006h: gets inseguro
	strcpy(buffer, "test"); // 0x5004h: strcpy sin validación

	if (ptr_malo == NULL)
	{
		goto salir; // 0x1006h: uso de goto
	}

salir:
	if (ptr_malo != NULL)
	{
		free(ptr_malo);
	}
}
