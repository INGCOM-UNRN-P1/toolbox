// Cabecera sin guardas de inclusión (0x5003h)

struct nodo_interno // 0x0035h: Definición de estructura expuesta en .h
{
    int dato;
    struct nodo_interno *sig;
};

void procesar_nodo(struct nodo_interno *n);
