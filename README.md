# C Language Scanner - A Lexical Analyzer

This project provides a basic lexical analyzer for the C programming language. It can be used to identify and classify tokens (keywords, identifiers, operators, etc.) within C code.

### Features

  * Identifies keywords, primitive functions, identifiers, operators, separators, string literals, and floating-point numbers.
  * Handles preprocessor directives like `#include` and `#define`.
  * Recognizes special symbols like `#`.
  * Removes comments (both single-line and multi-line) before scanning.
  * Offers two output formats:
      * Plain text: lists token type and value for each token.
      * Colored text: highlights different token types with distinct colors for better readability.

### Usage

1.  **Clone the repository or download the code.**
2.  **Install required libraries:**
      - tkinter
      - re (regular expressions)
3.  **Run the program:**
    ```bash
    python main.py
    ```

This will launch a graphical user interface (GUI) with two text areas for input and output.

### User Interface (GUI)

  * **Input Text Area:** Write your C code here.
  * **Scan Code Button:** Click this button to analyze the code.
  * **Output Text Area:** Displays the token type and value of each token in plain text format.
  * **Colored Output Text Area:** Displays the tokens with color-coding based on their type.

### Color Coding (Colored Output)

  * Keyword: Blue
  * Primitive Function: Green
  * Integer/Float: Orange
  * Identifier: Black
  * Operator: Red
  * Separator: Purple
  * String Literal: Brown
  * Other: Grey
  * Preprocessor Directive: Magenta
  * Special Symbol: Cyan



