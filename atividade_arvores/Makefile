
CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra
BIN = exercicios
SRC = main.c
OUT = resultado.txt

all: $(BIN)

$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC)

run: $(BIN)
	./$(BIN) | tee $(OUT)
	@echo "▶ Saída completa também salva em $(OUT)"

clean:
	rm -f $(BIN) $(OUT)
