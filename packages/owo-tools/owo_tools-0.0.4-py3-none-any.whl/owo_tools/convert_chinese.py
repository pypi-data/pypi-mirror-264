"""
This script provides a function to convert Chinese text between Simplified and Traditional Chinese characters.
It uses the OpenCC library for the conversion.

Usage:
    python convert_chinese.py -i <input_file> -o <output_file> --conversion <conversion_direction> [--verbose]

Arguments:
    -i, --input: Input file path.
    -o, --output: Output file path.
    --conversion: Conversion direction. Choose 's2t' for Simplified to Traditional or 't2s' for Traditional to Simplified.
    --verbose: Display all replaced text. (Optional)

Example:
    python convert_chinese.py -i input.txt -o output.txt --conversion s2twp --verbose
"""
#%%
import re
import argparse
from opencc import OpenCC
import argparse

def print_colored(text, color):
    """Prints the text in the specified color."""
    colors = {
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "reset": "\033[0m"
    }
    print(f"{colors[color]}{text}{colors['reset']}")

def convert_chinese(input_path, output_path, conversion, verbose=False, error_handling='warn-skip'):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError as e:
        if error_handling == 'error':
            print_colored(f"Error reading file {input_path} with UTF-8 encoding: {e}. Aborting.", "red")
            raise e
        elif error_handling == 'warn':
            print_colored(f"Warning: Could not read file {input_path} with UTF-8 encoding: {e}. Skipping.", "yellow")
            return
        elif error_handling == 'skip':
            return

    
    def replace_text(match):
        cc = OpenCC(conversion)  # 根據用戶選擇設定繁簡轉換
        original = match.group()
        converted = cc.convert(original)
        if verbose:
            print(f"\t{original} -> {converted}")
        return converted
    
    converted_content = re.sub(r'[\u4e00-\u9fa5]+', replace_text, content)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(converted_content)
        
    if verbose:
        print_colored(f"Conversion completed. Output written to {output_path}.", "green")

#%%
def main():
    parser = argparse.ArgumentParser(description="Convert between Simplified and Traditional Chinese.")
    parser.add_argument("-i", "--input", required=True, help="Input file path.")
    parser.add_argument("-o", "--output", required=True, help="Output file path.")
    parser.add_argument("--conversion", choices=['s2t', 't2s', 's2twp'], default="s2twp", help="Conversion direction: 's2t' for Simplified to Traditional, 't2s' for Traditional to Simplified, 's2twp` for Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases).")
    parser.add_argument("--verbose", action="store_true", help="Display all replaced text.")
    parser.add_argument("--error-handling", choices=['error', 'warn', 'skip'], default='warn', help="Error handling method when encountering non UTF-8 encoded files. 'error' to abort, 'warn' to display a warning and skip the file, 'skip' to skip the file without warning. Default is 'warn'.")


    args = parser.parse_args()

    convert_chinese(args.input, args.output, args.conversion, args.verbose)


if __name__ == "__main__":
    main()
