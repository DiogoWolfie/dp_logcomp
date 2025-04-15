#classe de pré-processamento - retirar comentários (// no go)
class PrePro:
    def __init__(self, source):
        self.source = source
        self.filtered_source = self.filter()

    def filter(self):
        lines = self.source.split("\n")
        clean_lines = []
        
        for line in lines:
            if "//" in line:
                line = line.split("//")[0]  # Remove comentário
            clean_lines.append(line)  # NÃO usar strip() aqui!

        return "\n".join(clean_lines) 