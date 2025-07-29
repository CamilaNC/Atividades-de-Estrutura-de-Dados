PYTHON = python3
PYTHON_VERSION = $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
TEST_DIR = ./testes
SOURCE_DIR = .
TEST_FILE = test_lista.py
TEST_RESULTS_DIR = testes

.PHONY: run test clean help

# Comando padrão (exibe ajuda)
help:
	@echo "============================================"
	@echo "COMANDOS DISPONÍVEIS PARA LISTA ENCADEADA"
	@echo "============================================"
	@echo "  make run       - Executa o programa principal interativo"
	@echo "  make test      - Executa todos os testes unitários"
	@echo "  make clean     - Remove arquivos temporários e caches"
	@echo "  make help      - Mostra esta mensagem de ajuda"
	@echo "============================================"

# Execução principal
run:
	@echo "Iniciando execução do programa principal..."
	@$(PYTHON) $(SOURCE_DIR)/main.py
	@echo "Execução concluída com sucesso!"

# Testes unitários
test:
	@echo "Executando testes com saída detalhada..."
	@mkdir -p "$(TEST_DIR)"
	@PYTHONPATH=$(SOURCE_DIR) $(PYTHON) -m unittest discover -s "$(TEST_DIR)" -v 2>&1 | tee "$(TEST_DIR)/resultados_testes.txt"
	@echo "Testes concluídos! Verifique resultados em $(TEST_DIR)/resultados_testes.txt"
# Limpeza
clean:
	@echo "Limpando arquivos temporários..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find $(TEST_DIR) -type f -name "resultados_testes.txt" -delete
	@echo "Limpeza concluída"