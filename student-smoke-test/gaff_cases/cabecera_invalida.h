// Cabecera sin guardas de inclusión (0x5003h)

struct nodo_interno // 0x301Dh: Definición de estructura expuesta en .h
{
    int dato;
    struct nodo_interno *sig;
};

void procesar_nodo(struct nodo_interno *n);
