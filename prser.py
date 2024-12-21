class Parser:
    # ANSI escape codes for colors
    COLORS = {
        'HEADER': "\033[95m",  # Magenta
        'OKBLUE': "\033[94m",  # Blue
        'OKGREEN': "\033[92m",  # Green
        'WARNING': "\033[93m",  # Yellow
        'FAIL': "\033[91m",  # Red
        'ENDC': "\033[0m",  # Reset to default
    }

    def __init__(self):
        self.grammar = {}  # Store grammar rules
        self.input_string = []  # Input string to parse
        self.current_index = 0  # Pointer for input string
        self.parse_tree = []  # To store the parse tree

    def print_colored(self, text, color):
        """Print text in the specified color."""
        print(f"{self.COLORS[color]}{text}{self.COLORS['ENDC']}")

    def input_grammar(self):
        """Dynamically input grammar from the user."""
        self.grammar.clear()
        self.print_colored("\n👎 Grammars 👎", 'HEADER')
        non_terminals = ['S', 'B']  # Fixed two non-terminals
        for nt in non_terminals:
            rules = []
            for i in range(1, 3):  # Two rules for each non-terminal
                rule = input(f"Enter rule number {i} for non-terminal '{nt}' (use capital letters for non-terminals): ").strip()
                rules.append(rule)
            self.grammar[nt] = rules

    def is_simple_grammar(self):
        """Check if the grammar is simple (no left recursion, no epsilon productions)."""
        non_terminals = ['S', 'B']
        # print("Hi from is simple")
        for nt, rules in self.grammar.items():
            # Check for left recursion
            for rule in rules:
                # print(rule)
                if rule.startswith(nt):  # Left recursion check
                    self.print_colored(f"The Grammar isn't simple: Left recursion detected in '{nt}'.", 'WARNING')
                    return False
                
            # Check for non simplicity
            for rule in rules:
                if rule.startswith(non_terminals[0]) or rule.startswith(non_terminals[1]):  # Left recursion check
                    self.print_colored(f"The Grammar isn't simple: Start with non terminal.", 'WARNING')
                    return False

            # Check for epsilon rules (empty productions)
            if any (rule == "" for rule in rules):
                self.print_colored(f"The Grammar isn't simple: Epsilon rule detected for '{nt}'.", 'WARNING')
                return False
            
            # Check if two rules for the same non-terminal start with the same symbol
            starting_symbols = [rule[0] for rule in rules if rule]  # Extract the starting symbols of the rules
            if len(starting_symbols) != len(set(starting_symbols)):
                self.print_colored(f"The Grammar isn't simple: Multiple rules for '{nt}' start with the same symbol.", 'WARNING')
                return False

            # Check for multiple rules leading to ambiguity
            if len(set(rules)) < len(rules):
                self.print_colored(f"The Grammar isn't simple: Multiple identical rules detected for '{nt}'.", 'WARNING')
                return False

        self.print_colored("The Grammar is simple.", 'OKGREEN')
        return True

    def parse_string(self, string):
        """Parse the user input string."""
        self.input_string = list(string)
        self.current_index = 0
        self.parse_tree = []
        self.print_colored(f"\nThe input String: {self.input_string}", 'OKBLUE')
        self.print_colored("The rest of unchecked string: []", 'OKBLUE')  # Placeholder for unchecked strings
        print("Parsing started...\n")
        if self.match_input('S', self.parse_tree) and self.current_index == len(self.input_string):
            self.print_colored("Your input String is Accepted.", 'OKGREEN')
            print("\nParse Tree:")
            self.display_parse_tree(self.parse_tree, "")
        else:
            self.print_colored("Your input String is Rejected.", 'FAIL')

    def match_input(self, non_terminal, tree_node):
        """Recursive descent function to parse input."""
        if non_terminal not in self.grammar:
            return False

        for rule in self.grammar[non_terminal]:
            saved_index = self.current_index
            sub_tree = []

            if self.apply_rule(rule, sub_tree):
                tree_node.append((non_terminal, rule, sub_tree))
                return True  # Rule applied successfully
            else:
                self.current_index = saved_index  # Backtrack on failure

        return False

    def apply_rule(self, rule, sub_tree):
        """Apply a single rule recursively."""
        for symbol in rule:
            if symbol.isupper():  # Non-terminal
                if not self.match_input(symbol, sub_tree):
                    return False
            else:  # Terminal
                if self.current_index < len(self.input_string) and self.input_string[self.current_index] == symbol:
                    sub_tree.append(symbol)
                    self.current_index += 1
                else:
                    return False
        return True

    def display_parse_tree(self, tree, indent):
        """Display the parse tree in a structured, GUI-like format."""
        for node in tree:
            if isinstance(node, tuple):  # Non-terminal
                print(f"{indent}{node[0]} -- {node[1]}")
                self.display_parse_tree(node[2], indent + "    |")
            else:  # Terminal
                print(f"{indent}    |-- {node}")

    def menu(self):
        """Main menu to interact with the program."""
        while True:
            self.input_grammar()
            if not self.is_simple_grammar():
                continue

            while True:
                string = input("Enter the string want to be checked: ").strip()
                self.parse_string(string)

                self.print_colored("\n========================", 'HEADER')
                print("1- Another String.")
                print("2- Enter Another Grammar.")
                print("3- Exit")
                choice = input("Enter ur choice: ").strip()

                if choice == '1':
                    continue  # Check for another string
                elif choice == '2':
                    break  # Restart grammar input
                elif choice == '3':
                    self.print_colored("Exiting...", 'OKGREEN')
                    return
                else:
                    self.print_colored("Invalid choice. Try again.", 'WARNING')

if __name__ == "__main__":
    parser = Parser()
    parser.menu()