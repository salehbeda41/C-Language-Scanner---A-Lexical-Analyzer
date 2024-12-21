import tkinter as tk  
from tkinter import scrolledtext  
import re  

class CLexicalAnalyzer:  
    def __init__(self):  
        # Keywords in C  
        self.keywords = {  
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',  
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',  
            'if', 'int', 'long', 'register', 'return', 'short', 'signed',  
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',  
            'unsigned', 'void', 'volatile', 'while'  
        }  

        # Operators in C  
        self.operators = {  
            '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',  
            '&&', '||', '!', '&', '|', '^', '~', '<<', '>>'  
        }  

        # Separators in C  
        self.separators = {  
            '(', ')', '{', '}', '[', ']', ';', ',', '.'  
        }  

        # Primitive functions in C  
        self.primitive_functions = {  
            'printf', 'scanf', 'puts', 'gets', 'fopen', 'fclose', 'fread',  
            'fwrite', 'fprintf', 'fscanf', 'fgets', 'fputs', 'malloc',  
            'calloc', 'realloc', 'free', 'exit', 'abort', 'assert'  
        }  

        self.preprocessor_directives = {'#include', '#define', '#if', '#else', '#endif', '#ifdef', '#ifndef'}

        self.special_symbols = {'#'}


    def analyze(self, code):  
        # Remove comments  
        code, comments = self.remove_comments(code)  

        tokens = []  
        current_token = ''  
        i = 0  

        while i < len(code):  
            char = code[i]  

            # Skip whitespace  
            if char.isspace():  
                if current_token:  
                    tokens.append(self.classify_token(current_token))  
                    current_token = ''  
                i += 1  
                continue  

            # Handle string literals  
            if char == '"':  
                if current_token:  
                    tokens.append(self.classify_token(current_token))  
                    current_token = ''  
                string_literal = '"'  
                i += 1  
                while i < len(code) and code[i] != '"':  
                    string_literal += code[i]  
                    i += 1  
                string_literal += '"'  
                tokens.append(('STRING_LITERAL', string_literal))  
                i += 1  
                continue  

            # Handle char literals  
            if char == "'":  
                if current_token:  
                    tokens.append(self.classify_token(current_token))  
                    current_token = ''  
                char_literal = "'"  
                i += 1  
                while i < len(code) and code[i] != "'":  
                    char_literal += code[i]  
                    i += 1  
                char_literal += "'"  
                tokens.append(('CHAR_LITERAL', char_literal))  
                i += 1  
                continue  

            # Handle operators  
            if char in '+-*/%=!<>&|^~':  
                if current_token:  
                    tokens.append(self.classify_token(current_token))  
                    current_token = ''  

                op = char  
                if i + 1 < len(code):  
                    next_char = code[i + 1]  
                    double_op = char + next_char  
                    if double_op in self.operators:  
                        op = double_op  
                        i += 1  

                tokens.append(('OPERATOR', op))  
                i += 1  
                continue  

            # Handle separators  
            if char in self.separators:  
                if current_token:  
                    tokens.append(self.classify_token(current_token))  
                    current_token = ''  
                tokens.append(('SEPARATOR', char))  
                i += 1  
                continue  

            # Handle potential identifiers and keywords  
            if char.isalpha() or char == '_':  
                word = ''  
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):  
                    word += code[i]  
                    i += 1  
                if word in self.keywords:  
                    tokens.append(('KEYWORD', word))  
                elif word in self.primitive_functions:  
                    tokens.append(('PRIMITIVE_FUNCTION', word))  
                else:  
                    tokens.append(('IDENTIFIER', word))  
                continue  
            # Handle preprocessor directives
            if char == '#':
                directive = ''
                while i < len(code) and not code[i].isspace():
                    directive += code[i]
                    i += 1
                if directive in self.preprocessor_directives:
                    tokens.append(('PREPROCESSOR_DIRECTIVE', directive))
                else:
                    tokens.append(('OTHER', directive))
                continue

            # Handle special symbols
            if char in self.special_symbols:
                if current_token:
                    tokens.append(self.classify_token(current_token))
                    current_token = ''
                tokens.append(('SPECIAL_SYMBOL', char))
                i += 1
                continue



            # If it's a digit, we classify it as a number  
            if char.isdigit():  
                number = ''  
                while i < len(code) and (code[i].isdigit() or code[i] == '.'):  
                    number += code[i]  
                    i += 1  
                if '.' in number:  
                    tokens.append(('FLOAT', number))  
                else:  
                    tokens.append(('INTEGER', number))  
                continue  

            # If it doesn't match any category, consider it an 'OTHER' token  
            current_token += char  
            i += 1  

        # Handle any remaining token  
        if current_token:  
            tokens.append(self.classify_token(current_token))  

        return tokens, comments  

    def remove_comments(self, code):  
        # Remove multi-line comments  
        multi_line_comments = re.findall(r'/\*.*?\*/', code, flags=re.DOTALL)  
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  

        # Remove single-line comments  
        single_line_comments = re.findall(r'//.*', code)  
        code = re.sub(r'//.*', '', code)  

        return code, multi_line_comments + single_line_comments  

    def classify_token(self, token):  
        # Check if token is a keyword  
        if token in self.keywords:  
            return ('KEYWORD', token)  

        # Check if token is a primitive function  
        if token in self.primitive_functions:  
            return ('PRIMITIVE_FUNCTION', token)  

        # Check if token is a number (integer or float)  
        if re.match(r'^[0-9]+(\.[0-9]+)?$', token):  
            if '.' in token:  
                return ('FLOAT', token)  
            else:  
                return ('INTEGER', token)  

        # Check if token is a valid identifier  
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):  
            return ('IDENTIFIER', token)  

        # If none of the above, return the token as is  
        return ('OTHER', token)  

class ScannerGUI:  
    def __init__(self, master):  
        self.master = master  
        master.title("C Language Scanner")  

        # Create the text area for input  
        self.input_text = scrolledtext.ScrolledText(master, width=80, height=10)  
        self.input_text.pack(padx=10, pady=10)  

        # Create the button to start scanning  
        self.scan_button = tk.Button(master, text="Scan Code", command=self.scan_code)  
        self.scan_button.pack(padx=10, pady=10)  

        # Create the text area for plain output  
        self.output_text = scrolledtext.ScrolledText(master, width=80, height=10)  
        self.output_text.pack(padx=10, pady=5)  

        # Create the text area for colored output  
        self.colored_output = scrolledtext.ScrolledText(master, width=80, height=10)  
        self.colored_output.pack(padx=10, pady=5)  

    def scan_code(self):  
        # Get the input code from the text area  
        input_code = self.input_text.get("1.0", "end-1c")  

        # Analyze the input code  
        lexical_analyzer = CLexicalAnalyzer()  
        tokens, comments = lexical_analyzer.analyze(input_code)  

        # Clear the output text areas  
        self.output_text.delete("1.0", "end")  
        self.colored_output.delete("1.0", "end")  

        # Display the tokens in plain text format  
        for token_type, value in tokens:  
            self.output_text.insert("end", f"Token Type: {token_type}, Token Value: {value}\n")  
        
        # Display the tokens in color-coded format  
        for token_type, value in tokens:  
            if token_type == 'KEYWORD':  
                self.colored_output.insert("end", f"{value} ", "keyword")  
            elif token_type == 'PRIMITIVE_FUNCTION':  
                self.colored_output.insert("end", f"{value} ", "primitive_function")  
            elif token_type == 'INTEGER':  
                self.colored_output.insert("end", f"{value} ", "integer")  
            elif token_type == 'FLOAT':  
                self.colored_output.insert("end", f"{value} ", "float")  
            elif token_type == 'IDENTIFIER':  
                self.colored_output.insert("end", f"{value} ", "identifier")  
            elif token_type == 'OPERATOR':  
                self.colored_output.insert("end", f"{value} ", "operator")  
            elif token_type == 'SEPARATOR':  
                self.colored_output.insert("end", f"{value} ", "separator")  
            elif token_type == 'STRING_LITERAL':  
                self.colored_output.insert("end", f"{value} ", "string_literal")  
            elif token_type == 'PREPROCESSOR_DIRECTIVE':
                self.colored_output.insert("end", f"{value} ", "preprocessor_directive")
            elif token_type == 'SPECIAL_SYMBOL':
                self.colored_output.insert("end", f"{value} ", "special_symbol")
            else:  
                self.colored_output.insert("end", f"{value} ", "other")  


        self.output_text.insert("end", "\nComments:\n")  
        for comment in comments:  
            self.output_text.insert("end", f"{comment}\n")  

        # Configure the tags for the colored output  
        self.colored_output.tag_config("keyword", foreground="blue")  
        self.colored_output.tag_config("primitive_function", foreground="green")  
        self.colored_output.tag_config("integer", foreground="orange")  
        self.colored_output.tag_config("float", foreground="orange")  
        self.colored_output.tag_config("identifier", foreground="black")  
        self.colored_output.tag_config("operator", foreground="red")  
        self.colored_output.tag_config("separator", foreground="purple")  
        self.colored_output.tag_config("string_literal", foreground="brown")  
        self.colored_output.tag_config("other", foreground="grey")  
        self.colored_output.tag_config("preprocessor_directive", foreground="magenta")
        self.colored_output.tag_config("special_symbol", foreground="cyan")


def main():  
    root = tk.Tk()  
    app = ScannerGUI(root)  
    root.mainloop()  

if __name__ == "__main__":  
    main()



