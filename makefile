# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -Wextra
LDFLAGS = -lasound

# Output file name
TARGET = record_alsa

# Source files
SRCS = record_mp3.c

# Regular build
all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS) $(LDFLAGS)

# Debug build
debug: $(SRCS)
	$(CC) $(CFLAGS) -g -DDEBUG -o $(TARGET)_debug $(SRCS) $(LDFLAGS)

# Clean build files
clean:
	rm -f $(TARGET) $(TARGET)_debug test.raw test.wav

# Run the normal program
run: all
	./$(TARGET)

# Run the debug version in gdb
debug-run: debug
	gdb ./$(TARGET)_debug
