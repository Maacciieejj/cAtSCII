import sys  # by zapisywaz zawartosc konsoli  TeeOutput:



# ponizej funkcja przekazuje  zawartość konsoli na ekran i do pliku zawartosc
class TeeOutput:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()