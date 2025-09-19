#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <time.h>
#include <errno.h>

#ifdef _WIN32
  #include <direct.h>  // _mkdir
  #define MKDIR(p) _mkdir(p)
#else
  #include <sys/stat.h>
  #include <sys/types.h>
  #define MKDIR(p) mkdir(p, 0777)
#endif

// ============================
// Logger (espelho: terminal + arquivo)
// ============================
static FILE *LOGF = NULL;
static char LOG_PATH[512] = {0};

static void tee_vprintf(const char *fmt, va_list ap) {
    va_list aq;
    va_copy(aq, ap);
    vprintf(fmt, ap);
    if (LOGF) vfprintf(LOGF, fmt, aq);
    va_end(aq);
}

static int tee_printf(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    tee_vprintf(fmt, ap);
    va_end(ap);
    if (LOGF) fflush(LOGF);
    fflush(stdout);
    return 0;
}

static int tee_puts(const char *s) {
    int r1 = puts(s);
    if (LOGF) { fputs(s, LOGF); fputc('\n', LOGF); fflush(LOGF); }
    fflush(stdout);
    return r1;
}

// cria pasta resultados/ e abre arquivo com timestamp
static void init_logger(void) {
    const char *dir = "resultados";
    if (MKDIR(dir) == -1 && errno != EEXIST) {
        fprintf(stderr, "Aviso: não foi possível criar pasta '%s' (%s)\n", dir, strerror(errno));
    }
    time_t t = time(NULL);
    struct tm *lt = localtime(&t);
    char ts[64];
    strftime(ts, sizeof(ts), "exec_%Y-%m-%d_%H-%M-%S.txt", lt);
    snprintf(LOG_PATH, sizeof(LOG_PATH), "%s/%s", dir, ts);
    LOGF = fopen(LOG_PATH, "w");
    if (!LOGF) {
        fprintf(stderr, "Aviso: não foi possível abrir log '%s' (%s)\n", LOG_PATH, strerror(errno));
    }
}

static void close_logger(void) {
    if (LOGF) {
        fclose(LOGF);
        LOGF = NULL;
    }
}

// ============================
// Util: vetor dinâmico de int
// ============================
typedef struct {
    int *data;
    size_t size, cap;
} IntVec;

static void vec_init(IntVec *v) { v->data=NULL; v->size=0; v->cap=0; }
static void vec_push(IntVec *v, int x) {
    if (v->size == v->cap) {
        size_t nc = v->cap ? v->cap*2 : 8;
        int *p = (int*)realloc(v->data, nc*sizeof(int));
        if (!p) { perror("realloc"); exit(1); }
        v->data = p; v->cap = nc;
    }
    v->data[v->size++] = x;
}
static void vec_free(IntVec *v) { free(v->data); v->data=NULL; v->size=v->cap=0; }
static void vec_print(const IntVec *v) {
    tee_printf("[");
    for (size_t i=0; i<v->size; ++i) {
        tee_printf("%d%s", v->data[i], (i+1<v->size?", ":""));
    }
    tee_printf("]\n");
}

// ============================
// BST
// ============================
typedef struct BSTNode {
    int valor;
    struct BSTNode *esq, *dir;
} BSTNode;

static BSTNode* bst_new(int v) {
    BSTNode *n = (BSTNode*)calloc(1, sizeof(BSTNode));
    if (!n) { perror("calloc"); exit(1); }
    n->valor = v;
    return n;
}

static BSTNode* bst_inserir_rec(BSTNode *no, int v) {
    if (!no) return bst_new(v);
    if (v < no->valor) no->esq = bst_inserir_rec(no->esq, v);
    else if (v > no->valor) no->dir = bst_inserir_rec(no->dir, v);
    return no;
}

static bool bst_buscar_rec(BSTNode *no, int v) {
    if (!no) return false;
    if (v == no->valor) return true;
    if (v < no->valor) return bst_buscar_rec(no->esq, v);
    return bst_buscar_rec(no->dir, v);
}

static BSTNode* bst_minimo(BSTNode *no) {
    while (no && no->esq) no = no->esq;
    return no;
}

static BSTNode* bst_remover_rec(BSTNode *no, int v) {
    if (!no) return NULL;
    if (v < no->valor) no->esq = bst_remover_rec(no->esq, v);
    else if (v > no->valor) no->dir = bst_remover_rec(no->dir, v);
    else {
        if (!no->esq) { BSTNode *d=no->dir; free(no); return d; }
        if (!no->dir) { BSTNode *e=no->esq; free(no); return e; }
        BSTNode *s = bst_minimo(no->dir);
        no->valor = s->valor;
        no->dir = bst_remover_rec(no->dir, s->valor);
    }
    return no;
}

static void bst_pre(BSTNode *no, IntVec *out) {
    if (!no) return; vec_push(out, no->valor); bst_pre(no->esq,out); bst_pre(no->dir,out);
}
static void bst_em(BSTNode *no, IntVec *out) {
    if (!no) return; bst_em(no->esq,out); vec_push(out, no->valor); bst_em(no->dir,out);
}
static void bst_pos(BSTNode *no, IntVec *out) {
    if (!no) return; bst_pos(no->esq,out); bst_pos(no->dir,out); vec_push(out, no->valor);
}

static void bst_print_sideways(BSTNode *no, int nivel) {
    if (!no) return;
    bst_print_sideways(no->dir, nivel+1);
    for (int i=0;i<nivel;i++) tee_printf("    ");
    tee_printf("%d\n", no->valor);
    bst_print_sideways(no->esq, nivel+1);
}

static void bst_free(BSTNode *no) {
    if (!no) return;
    bst_free(no->esq);
    bst_free(no->dir);
    free(no);
}

// ============================
// AVL
// ============================
typedef struct AVLNode {
    int chave;
    int altura;
    struct AVLNode *esq, *dir;
} AVLNode;

static int avl_alt(AVLNode *n) { return n ? n->altura : 0; }
static int avl_max(int a, int b) { return a>b?a:b; }

static AVLNode* avl_new(int k) {
    AVLNode *n = (AVLNode*)calloc(1,sizeof(AVLNode));
    if (!n) { perror("calloc"); exit(1); }
    n->chave = k; n->altura = 1;
    return n;
}

static int avl_fb(AVLNode *n) { return n ? avl_alt(n->esq) - avl_alt(n->dir) : 0; }

static AVLNode* avl_rot_dir(AVLNode *y) {
    AVLNode *x = y->esq;
    AVLNode *T2 = x ? x->dir : NULL;
    if (x) x->dir = y;
    y->esq = T2;
    y->altura = 1 + avl_max(avl_alt(y->esq), avl_alt(y->dir));
    if (x) x->altura = 1 + avl_max(avl_alt(x->esq), avl_alt(x->dir));
    return x ? x : y;
}

static AVLNode* avl_rot_esq(AVLNode *x) {
    AVLNode *y = x->dir;
    AVLNode *T2 = y ? y->esq : NULL;
    if (y) y->esq = x;
    x->dir = T2;
    x->altura = 1 + avl_max(avl_alt(x->esq), avl_alt(x->dir));
    if (y) y->altura = 1 + avl_max(avl_alt(y->esq), avl_alt(y->dir));
    return y ? y : x;
}

static AVLNode* avl_inserir_rec(AVLNode *no, int k) {
    if (!no) return avl_new(k);
    if (k < no->chave) no->esq = avl_inserir_rec(no->esq, k);
    else if (k > no->chave) no->dir = avl_inserir_rec(no->dir, k);
    else return no;

    no->altura = 1 + avl_max(avl_alt(no->esq), avl_alt(no->dir));
    int fb = avl_fb(no);

    // LL
    if (fb > 1 && k < (no->esq ? no->esq->chave : k)) {
        tee_printf("  \xE2\x86\x92 Rotação à DIREITA (LL) no nó %d\n", no->chave);
        return avl_rot_dir(no);
    }
    // RR
    if (fb < -1 && k > (no->dir ? no->dir->chave : k)) {
        tee_printf("  \xE2\x86\x92 Rotação à ESQUERDA (RR) no nó %d\n", no->chave);
        return avl_rot_esq(no);
    }
    // LR
    if (fb > 1 && k > (no->esq ? no->esq->chave : k)) {
        tee_printf("  \xE2\x86\x92 Rotação à ESQUERDA (LR - passo 1) no nó %d\n", no->esq ? no->esq->chave : -1);
        no->esq = avl_rot_esq(no->esq);
        tee_printf("  \xE2\x86\x92 Rotação à DIREITA (LR - passo 2) no nó %d\n", no->chave);
        return avl_rot_dir(no);
    }
    // RL
    if (fb < -1 && k < (no->dir ? no->dir->chave : k)) {
        tee_printf("  \xE2\x86\x92 Rotação à DIREITA (RL - passo 1) no nó %d\n", no->dir ? no->dir->chave : -1);
        no->dir = avl_rot_dir(no->dir);
        tee_printf("  \xE2\x86\x92 Rotação à ESQUERDA (RL - passo 2) no nó %d\n", no->chave);
        return avl_rot_esq(no);
    }
    return no;
}

static void avl_pre(AVLNode *no, IntVec *out) {
    if (!no) return; vec_push(out, no->chave); avl_pre(no->esq,out); avl_pre(no->dir,out);
}

static void avl_print_sideways(AVLNode *no, int nivel) {
    if (!no) return;
    avl_print_sideways(no->dir, nivel+1);
    for (int i=0;i<nivel;i++) tee_printf("    ");
    tee_printf("%d\n", no->chave);
    avl_print_sideways(no->esq, nivel+1);
}

static bool avl_check_balance_rec(AVLNode *no, int *altura_out) {
    if (!no) { *altura_out = 0; return true; }
    int he=0, hd=0;
    bool okE = avl_check_balance_rec(no->esq, &he);
    bool okD = avl_check_balance_rec(no->dir, &hd);
    int fb = he - hd;
    *altura_out = 1 + avl_max(he, hd);
    return okE && okD && (fb >= -1 && fb <= 1);
}

static int avl_factor(AVLNode *no) { return avl_fb(no); }

static void avl_list_factors(AVLNode *no) {
    if (!no) return;
    tee_printf("  Nó %d: FB=%d, altura=%d\n", no->chave, avl_factor(no), no->altura);
    avl_list_factors(no->esq);
    avl_list_factors(no->dir);
}

static void avl_free(AVLNode *no) {
    if (!no) return;
    avl_free(no->esq); avl_free(no->dir); free(no);
}

// ============================
// Grafos (A..F)
// ============================
#define GN 6
static const char *VN[GN] = {"A","B","C","D","E","F"};
static int idx_of(char c) { return (int)(c - 'A'); }

static void grafo_build_matrix(int M[GN][GN]) {
    memset(M, 0, sizeof(int)*GN*GN);
    // A-B, A-C
    M[idx_of('A')][idx_of('B')] = M[idx_of('B')][idx_of('A')] = 1;
    M[idx_of('A')][idx_of('C')] = M[idx_of('C')][idx_of('A')] = 1;
    // B-D, B-E
    M[idx_of('B')][idx_of('D')] = M[idx_of('D')][idx_of('B')] = 1;
    M[idx_of('B')][idx_of('E')] = M[idx_of('E')][idx_of('B')] = 1;
    // C-F
    M[idx_of('C')][idx_of('F')] = M[idx_of('F')][idx_of('C')] = 1;
    // E-F
    M[idx_of('E')][idx_of('F')] = M[idx_of('F')][idx_of('E')] = 1;
}

static void grafo_print_matrix(int M[GN][GN]) {
    tee_printf("Ordem (alfabética) dos vértices: [");
    for (int i=0;i<GN;i++) tee_printf("%s%s", VN[i], (i+1<GN?", ":""));
    tee_printf("]\nMatriz de adjacência:\n");
    tee_printf("     ");
    for (int j=0;j<GN;j++) tee_printf(" %2s", VN[j]);
    tee_printf("\n");
    for (int i=0;i<GN;i++) {
        tee_printf(" %2s ", VN[i]);
        for (int j=0;j<GN;j++) tee_printf(" %2d", M[i][j]);
        tee_printf("\n");
    }
}

typedef struct { int q[128]; int h, t; } Queue;
static void q_init(Queue *q){ q->h=q->t=0; }
static bool q_empty(Queue *q){ return q->h==q->t; }
static void q_push(Queue *q, int x){ q->q[q->t++]=x; }
static int  q_pop(Queue *q){ return q->q[q->h++]; }

static void bfs(int M[GN][GN], int s) {
    bool vis[GN]={0};
    Queue q; q_init(&q);
    vis[s]=true; q_push(&q, s);
    IntVec ordem; vec_init(&ordem);
    while (!q_empty(&q)) {
        int u=q_pop(&q); vec_push(&ordem, u);
        for (int v=0; v<GN; v++) if (M[u][v] && !vis[v]) { vis[v]=true; q_push(&q, v); }
    }
    tee_printf("BFS a partir de %s: [", VN[s]);
    for (size_t i=0;i<ordem.size;i++) tee_printf("%s%s", VN[ordem.data[i]], (i+1<ordem.size?", ":""));
    tee_printf("]\n");
    vec_free(&ordem);
}

static void dfs_rec(int M[GN][GN], int u, bool *vis, IntVec *ordem) {
    vis[u]=true; vec_push(ordem, u);
    for (int v=0; v<GN; v++) if (M[u][v] && !vis[v]) dfs_rec(M, v, vis, ordem);
}
static void dfs(int M[GN][GN], int s) {
    bool vis[GN]={0};
    IntVec ordem; vec_init(&ordem);
    dfs_rec(M, s, vis, &ordem);
    tee_printf("DFS a partir de %s: [", VN[s]);
    for (size_t i=0;i<ordem.size;i++) tee_printf("%s%s", VN[ordem.data[i]], (i+1<ordem.size?", ":""));
    tee_printf("]\n");
    vec_free(&ordem);
}

// ============================
// Exercícios
// ============================
static void exercicio_1(void) {
    tee_puts("\n=== Exercício 1: BST inserir e remover nó 60 ===");
    int valores[] = {45,20,60,15,25,50,70,65,80};
    size_t n = sizeof(valores)/sizeof(valores[0]);
    BSTNode *raiz = NULL;
    for (size_t i=0;i<n;i++) raiz = bst_inserir_rec(raiz, valores[i]);

    tee_puts("BST após inserções (visão deitada):");
    bst_print_sideways(raiz, 0);

    tee_puts("Removendo o nó 60...");
    raiz = bst_remover_rec(raiz, 60);

    tee_puts("BST após remover 60 (visão deitada):");
    bst_print_sideways(raiz, 0);
    bst_free(raiz);
}

static void exercicio_2(void) {
    tee_puts("\n=== Exercício 2: Percursos em BST ===");
    int seq[] = {10,4,15,2,6,12,18};
    size_t n = sizeof(seq)/sizeof(seq[0]);
    BSTNode *r=NULL;
    for (size_t i=0;i<n;i++) r = bst_inserir_rec(r, seq[i]);

    IntVec pre, in, pos;
    vec_init(&pre); vec_init(&in); vec_init(&pos);
    bst_pre(r, &pre); bst_em(r, &in); bst_pos(r, &pos);

    tee_printf("Pré-ordem : "); vec_print(&pre);
    tee_printf("Em-ordem  : "); vec_print(&in);
    tee_printf("Pós-ordem : "); vec_print(&pos);

    vec_free(&pre); vec_free(&in); vec_free(&pos);
    bst_free(r);
}

static void exercicio_3(void) {
    tee_puts("\n=== Exercício 3: AVL com rotações passo a passo ===");
    int seq[] = {10,20,30,40,50,25};
    size_t n = sizeof(seq)/sizeof(seq[0]);
    AVLNode *r = NULL;
    for (size_t i=0;i<n;i++) {
        int x = seq[i];
        tee_printf("Inseriu %d.\n", x);
        r = avl_inserir_rec(r, x);
        tee_puts("Estado atual (visão deitada):");
        avl_print_sideways(r, 0);
    }
    IntVec pre; vec_init(&pre); avl_pre(r, &pre);
    tee_printf("Percurso em pré-ordem da AVL final: "); vec_print(&pre);
    int h=0; bool ok = avl_check_balance_rec(r, &h);
    tee_printf("Árvore está balanceada? %s\n", ok?"true":"false");
    vec_free(&pre); avl_free(r);
}

static void exercicio_4(void) {
    tee_puts("\n=== Exercício 4: Grafo (matriz de adjacência, BFS, DFS) ===");
    int M[GN][GN];
    grafo_build_matrix(M);
    grafo_print_matrix(M);
    bfs(M, idx_of('A'));
    dfs(M, idx_of('A'));
}

static void exercicio_5_6_7_demo(void) {
    tee_puts("\n=== Exercícios 5, 6 e 7: Node, inserir, buscar e percursos (BST) ===");
    int seq[] = {8,3,10,1,6,14,4,7,13};
    size_t n = sizeof(seq)/sizeof(seq[0]);
    BSTNode *r=NULL;
    for (size_t i=0;i<n;i++) r = bst_inserir_rec(r, seq[i]);

    tee_puts("BST (visão deitada):");
    bst_print_sideways(r, 0);

    tee_printf("Buscar 7  \xE2\x86\x92 %s\n", bst_buscar_rec(r,7) ? "true":"false");
    tee_printf("Buscar 11 \xE2\x86\x92 %s\n", bst_buscar_rec(r,11)? "true":"false");

    IntVec pre,in,pos; vec_init(&pre); vec_init(&in); vec_init(&pos);
    bst_pre(r,&pre); bst_em(r,&in); bst_pos(r,&pos);
    tee_printf("Pré-ordem : "); vec_print(&pre);
    tee_printf("Em-ordem  : "); vec_print(&in);
    tee_printf("Pós-ordem : "); vec_print(&pos);

    vec_free(&pre); vec_free(&in); vec_free(&pos);
    bst_free(r);
}

static void exercicio_8_demo(void) {
    tee_puts("\n=== Exercício 8: AVL - inserir, alturas, fatores, rotações e verificação ===");
    int seq[] = {30,20,40,10,25,35,50,5};
    size_t n = sizeof(seq)/sizeof(seq[0]);
    AVLNode *r=NULL;
    for (size_t i=0;i<n;i++) r = avl_inserir_rec(r, seq[i]);

    tee_puts("AVL (visão deitada):");
    avl_print_sideways(r, 0);

    int h=0; bool ok = avl_check_balance_rec(r, &h);
    tee_printf("Árvore está balanceada? %s\n", ok?"true":"false");
    tee_puts("Fator de balanceamento por nó (pré-ordem):");
    avl_list_factors(r);

    avl_free(r);
}

// ============================
// Main
// ============================
int main(void) {
    init_logger();
    tee_puts("=== Execução iniciada ===");
    if (LOG_PATH[0]) tee_printf("Arquivo de log: %s\n\n", LOG_PATH);

    exercicio_1();
    exercicio_2();
    exercicio_3();
    exercicio_4();
    exercicio_5_6_7_demo();
    exercicio_8_demo();

    tee_puts("\n=== Execução finalizada ===");
    if (LOG_PATH[0]) tee_printf("Saída completa salva em: %s\n", LOG_PATH);
    close_logger();

    // mensagem final apenas no stdout (fora do tee)
    if (LOG_PATH[0]) printf("\n[OK] Saída também foi salva em: %s\n", LOG_PATH);
    return 0;
}
