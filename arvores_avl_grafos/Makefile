


CC       ?= gcc
CFLAGS   ?= -std=c11 -Wall -Wextra -Wpedantic -O2
LDFLAGS  ?=
TARGET   ?= main
SRC      ?= main.c
OBJ      := $(SRC:.c=.o)
RESULTS_DIR ?= resultados


LAST_LOG := $(shell ls -t $(RESULTS_DIR)/exec_*.txt 2>/dev/null | head -n1)

.PHONY: help all build run debug asan release show-log clean clean-logs clean-all


help:
	@echo "======================"
	@echo " Comandos disponíveis "
	@echo "======================"
	@echo " make            - Compila (equivale a 'make all')"
	@echo " make run        - Roda ./$(TARGET)"
	@echo " make debug      - Compila com símbolos (-g) e sem otimização"
	@echo " make asan       - Compila com Address/UB Sanitizer"
	@echo " make release    - Compila otimizado (-O3)"
	@echo " make show-log   - Mostra o último log em $(RESULTS_DIR)/"
	@echo " make clean      - Remove .o/.exe e esvazia $(RESULTS_DIR)/ (mantém a pasta)"
	@echo " make clean-logs - Remove a pasta $(RESULTS_DIR)/ inteira"
	@echo " make clean-all  - Limpa tudo (binários e logs)"


all: $(TARGET)
build: all

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

debug: CFLAGS += -O0 -g
debug: clean $(TARGET)
	@echo "[OK] Build de debug pronto: $(TARGET)"

asan: CFLAGS += -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer
asan: LDFLAGS += -fsanitize=address,undefined
asan: clean $(TARGET)
	@echo "[OK] Build com ASan/UBSan pronto: $(TARGET)"

release: CFLAGS += -O3
release: clean $(TARGET)
	@echo "[OK] Build de release pronto: $(TARGET)"

show-log:
	@if [ -z "$(LAST_LOG)" ]; then \
		echo "Nenhum log encontrado em $(RESULTS_DIR)/. Rode 'make run' primeiro."; \
	else \
		echo "Mostrando: $(LAST_LOG)"; \
		echo "---------------------------------------"; \
		cat "$(LAST_LOG)"; \
		echo "---------------------------------------"; \
	fi

clean:
	@rm -f $(OBJ) $(TARGET) 2>/dev/null || true
	@# esvazia resultados/ mas mantém a pasta
	@if [ -d "$(RESULTS_DIR)" ]; then \
		find "$(RESULTS_DIR)" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true; \
	fi
	@# (opcional) suporte a PowerShell no Windows puro
	@command -v powershell >/dev/null 2>&1 && powershell -NoProfile -Command "if (Test-Path '$(RESULTS_DIR)') { Remove-Item '$(RESULTS_DIR)\\*' -Recurse -Force -ErrorAction SilentlyContinue }" || true
	@echo "[OK] Limpeza simples concluída."

clean-logs:
	@rm -rf "$(RESULTS_DIR)"
	@echo "[OK] Logs removidos (pasta $(RESULTS_DIR)/)."

clean-all: clean clean-logs
	@rm -f $(TARGET)
	@echo "[OK] Limpeza total concluída."
