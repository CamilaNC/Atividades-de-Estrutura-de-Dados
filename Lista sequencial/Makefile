# Makefile para Lista Sequencial - Versão Final

# Variáveis
PYTHON = python
PYTHON_VERSION = $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
SOURCE_DIR = .
TEST_DIR = testes
VENV_DIR = venv

.PHONY: run test clean venv check-style install-dev help

# Comando padrão (exibe ajuda)
help:
	@echo "============================================"
	@echo "COMANDOS DISPONÍVEIS PARA LISTA SEQUENCIAL"
	@echo "============================================"
	@echo "  make run       - Executa o programa principal"
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
	@echo " Rodando testes..."
	@mkdir -p $(TEST_DIR)  # Garante que a pasta existe (funciona no Linux/Mac)
	$(PYTHON) -m unittest discover -s $(TEST_DIR) -p "test_*.py" 
	@echo " Testes finalizados. Resultado salvo em: $(TEST_DIR)/resultados_testes.txt"

# Limpeza
clean:
	@echo "Limpando arquivos temporários..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -delete
	@echo " Limpeza concluída!"

