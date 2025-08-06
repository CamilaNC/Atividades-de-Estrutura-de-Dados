PYTHON = python3
PYTHON_VERSION = $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
SOURCE_DIR = .
TEST_FILE = testes/test_fila.py
TEST_RESULTS_DIR = testes/resultados

.PHONY: run test clean venv check-style install-dev help

# Comando padrão (exibe ajuda)
help:
	@echo "============================================"
	@echo " COMANDOS DISPONÍVEIS PARA FILA CIRCULAR "
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
	@echo "Executando testes..."
	@mkdir -p $(TEST_RESULTS_DIR)
	@$(PYTHON) -m unittest $(TEST_FILE) | tee $(TEST_RESULTS_DIR)/resultados_testes.txt
	@echo "Testes concluídos! Verifique resultados em $(TEST_RESULTS_DIR)/resultados_testes.txt"

# Limpeza
clean:
	@echo "Limpando arquivos temporários..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf $(TEST_RESULTS_DIR)
	@echo "Limpeza concluída!"
