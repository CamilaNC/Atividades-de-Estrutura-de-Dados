
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>
#include <time.h>
#include <stdarg.h>


static FILE *LOGF = NULL;


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
    puts(s);
    if (LOGF) { fputs(s, LOGF); fputc('\n', LOGF); fflush(LOGF); }
    fflush(stdout);
    return 0;
}

static int tee_putchar(int c) {
    putchar(c);
    if (LOGF) { fputc(c, LOGF); fflush(LOGF); }
    fflush(stdout);
    return c;
}

#define printf(...)   tee_printf(__VA_ARGS__)
#define puts(s)       tee_puts(s)
#define putchar(c)    tee_putchar(c)


static void ler_linha(char *buf, size_t tam) {
    if (fgets(buf, (int)tam, stdin)) {
        size_t n = strlen(buf);
        if (n && buf[n-1] == '\n') buf[n-1] = '\0';
    } else {
        buf[0] = '\0';
    }
}

static void ler_string(const char *prompt, char *buf, size_t tam) {
    printf("%s", prompt);
    ler_linha(buf, tam);
    if (LOGF) { fprintf(LOGF, "%s%s\n", prompt, buf); fflush(LOGF); }
}

static int ler_int(const char *prompt) {
    char linha[256];
    int x;
    while (1) {
        printf("%s", prompt);
        ler_linha(linha, sizeof(linha));
        // grava também o que foi digitado
        if (LOGF) { fprintf(LOGF, "%s%s\n", prompt, linha); fflush(LOGF); }
        if (sscanf(linha, "%d", &x) == 1) return x;
        puts("Entrada inválida. Tente novamente.");
    }
}

static int* ler_vetor_int(int *n_out) {
    int n = ler_int("Tamanho da lista (n >= 0): ");
    if (n < 0) n = 0;
    int *v = (int*)malloc(sizeof(int) * (size_t)n);
    if (!v && n > 0) {
        puts("Falha ao alocar memória.");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < n; i++) {
        char prompt[64];
        sprintf(prompt, "v[%d] = ", i);
        v[i] = ler_int(prompt);
    }
    *n_out = n;
    return v;
}

// ============================
// Parte 1 — Recursão
// ============================
static void inverter_str_rec(char *s, int i, int j) {
    if (i >= j) return;
    char tmp = s[i]; s[i] = s[j]; s[j] = tmp;
    inverter_str_rec(s, i+1, j-1);
}
static void inverter_str(char *s) {
    if (!s) return;
    int n = (int)strlen(s);
    inverter_str_rec(s, 0, n > 0 ? n-1 : 0);
}

static int maximo_rec(const int *v, int n) {
    if (n == 1) return v[0];
    int m = maximo_rec(v + 1, n - 1);
    return v[0] > m ? v[0] : m;
}

static long long soma_rec(const int *v, int n) {
    if (n == 0) return 0;
    return v[0] + soma_rec(v + 1, n - 1);
}

// ============================
// Parte 2 — Árvores Binárias (BST)
// ============================
typedef struct No {
    int valor;
    struct No *esq, *dir;
} No;

static No* novo_no(int valor) {
    No *n = (No*)malloc(sizeof(No));
    if (!n) { puts("Sem memória."); exit(EXIT_FAILURE); }
    n->valor = valor; n->esq = n->dir = NULL;
    return n;
}

// 1) Inserção em BST
static No* inserir_bst(No *raiz, int valor) {
    if (!raiz) return novo_no(valor);
    if (valor < raiz->valor) raiz->esq = inserir_bst(raiz->esq, valor);
    else                     raiz->dir = inserir_bst(raiz->dir, valor);
    return raiz;
}

// 2) Percursos
static void pre_ordem(No *r) { if (r){ printf("%d ", r->valor); pre_ordem(r->esq); pre_ordem(r->dir);} }
static void in_ordem(No *r)  { if (r){ in_ordem(r->esq); printf("%d ", r->valor); in_ordem(r->dir);} }
static void pos_ordem(No *r) { if (r){ pos_ordem(r->esq); pos_ordem(r->dir); printf("%d ", r->valor);} }

// 3) Altura
static int altura(No *r) {
    if (!r) return 0;
    int he = altura(r->esq), hd = altura(r->dir);
    return 1 + (he > hd ? he : hd);
}

// 4) Contagens
static int contar_nos(No *r) {
    if (!r) return 0;
    return 1 + contar_nos(r->esq) + contar_nos(r->dir);
}
static int contar_folhas(No *r) {
    if (!r) return 0;
    if (!r->esq && !r->dir) return 1;
    return contar_folhas(r->esq) + contar_folhas(r->dir);
}

// 5) Busca
static int buscar_bst(No *r, int x) {
    if (!r) return 0;
    if (r->valor == x) return 1;
    if (x < r->valor) return buscar_bst(r->esq, x);
    return buscar_bst(r->dir, x);
}

// 6) Mín/Máx
static int minimo_bst(No *r, int *ok) {
    if (!r) { *ok = 0; return 0; }
    while (r->esq) r = r->esq;
    *ok = 1; return r->valor;
}
static int maximo_bst_val(No *r, int *ok) {
    if (!r) { *ok = 0; return 0; }
    while (r->dir) r = r->dir;
    *ok = 1; return r->valor;
}

// 7) Verificar se é BST (qualquer árvore)
static int eh_bst_limites(No *r, long long minv, long long maxv) {
    if (!r) return 1;
    if (r->valor < minv || r->valor > maxv) return 0;
    return eh_bst_limites(r->esq, minv, (long long)r->valor - 1) &&
           eh_bst_limites(r->dir, (long long)r->valor + 1, maxv);
}
static int eh_bst(No *r) { return eh_bst_limites(r, LLONG_MIN, LLONG_MAX); }

static void liberar(No *r) {
    if (!r) return;
    liberar(r->esq); liberar(r->dir); free(r);
}

static void imprimir_percursos(No *raiz) {
    puts("Pré-ordem:");  pre_ordem(raiz);  puts("");
    puts("In-ordem:");   in_ordem(raiz);   puts("");
    puts("Pós-ordem:");  pos_ordem(raiz);  puts("");
}

static void menu_arvores(void) {
    No *raiz = NULL;
    while (1) {
        puts("\n=== ÁRVORES BINÁRIAS (BST) ===");
        puts("1) Inserir valor na BST");
        puts("2) Percursos (pré / in / pós)");
        puts("3) Altura");
        puts("4) Contagem de nós e folhas");
        puts("5) Buscar valor na BST");
        puts("6) Menor e maior valor da BST");
        puts("7) Verificar se é BST");
        puts("8) Limpar árvore");
        puts("9) Inserção rápida (lote) — n valores");
        puts("0) Voltar");
        int op = ler_int("Escolha: ");

        if (op == 0) {
            liberar(raiz);
            return;
        } else if (op == 1) {
            int x = ler_int("Valor a inserir: ");
            raiz = inserir_bst(raiz, x);
            puts("Inserido.");
        } else if (op == 2) {
            if (!raiz) puts("Árvore vazia.");
            else imprimir_percursos(raiz);
        } else if (op == 3) {
            printf("Altura = %d\n", altura(raiz));
        } else if (op == 4) {
            printf("Nós = %d, Folhas = %d\n", contar_nos(raiz), contar_folhas(raiz));
        } else if (op == 5) {
            int x = ler_int("Valor a buscar: ");
            printf("%d %s na BST.\n", x, buscar_bst(raiz, x) ? "está" : "não está");
        } else if (op == 6) {
            int ok1, ok2;
            int mn = minimo_bst(raiz, &ok1);
            int mx = maximo_bst_val(raiz, &ok2);
            if (!ok1 || !ok2) puts("Árvore vazia.");
            else printf("Menor = %d, Maior = %d\n", mn, mx);
        } else if (op == 7) {
            printf("A árvore %s uma BST.\n", eh_bst(raiz) ? "É" : "NÃO é");
        } else if (op == 8) {
            liberar(raiz); raiz = NULL;
            puts("Árvore limpa.");
        } else if (op == 9) {
            int n = ler_int("Quantos valores? ");
            for (int i = 0; i < n; i++) {
                char p[64]; sprintf(p, "valor[%d] = ", i);
                int x = ler_int(p);
                raiz = inserir_bst(raiz, x);
            }
            puts("Lote inserido.");
        } else {
            puts("Opção inválida.");
        }
    }
}

static void print_menu_principal(void) {
    puts("\n=========== MENU PRINCIPAL ===========");
    puts(" 01) Inverter string");
    puts(" 02) Máximo em lista");
    puts(" 03) Soma recursiva da lista");
    puts(" 04) Árvores binárias (submenu)");
    puts(" 05) Sair");
    puts("======================================");
}

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);

    LOGF = fopen("resultado.txt", "w");
    if (!LOGF) {
        perror("resultado.txt");
    }

    while (1) {
        print_menu_principal();
        int op = ler_int("Escolha: ");

        if (op == 5) {
            puts("Até mais!");
            break;
        } else if (op == 1) {
            char buf[1024];
            ler_string("Digite a string: ", buf, sizeof(buf));
            inverter_str(buf);
            printf("Invertida: \"%s\"\n", buf);
        } else if (op == 2) {
            int n; int *v = ler_vetor_int(&n);
            if (n == 0) {
                puts("Lista vazia não possui máximo.");
            } else {
                int m = maximo_rec(v, n);
                printf("Máximo = %d\n", m);
            }
            free(v);
        } else if (op == 3) {
            int n; int *v = ler_vetor_int(&n);
            long long s = soma_rec(v, n);
            printf("Soma = %lld\n", s);
            free(v);
        } else if (op == 4) {
            menu_arvores();
        } else {
            puts("Opção inválida.");
        }
    }

    if (LOGF) { fflush(LOGF); fclose(LOGF); LOGF = NULL; }
    return 0;
}
