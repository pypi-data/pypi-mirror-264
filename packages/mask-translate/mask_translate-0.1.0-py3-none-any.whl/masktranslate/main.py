from argparse import ArgumentParser, Namespace
import os
import json
import sys
from xml.etree import ElementTree as et


def mobile_translate(directory, file):
    for dirpath, dirnames, filenames in os.walk(directory):
        if file in filenames:
            return os.path.join(directory, file)
    return None


def recursive_translate(data):
    for key, value in data.items():
        if isinstance(value, dict):
            recursive_translate(value)
        else:
            data[key] = ''.join(['█' if char != ' ' and char != '\n' else char for char in value])


def default_op(directory, filename):
    source_file = os.path.join(directory, "src", "assets", "i18n", "en.json")
    destination_file = os.path.join(directory, "src", "assets", "i18n", f"{filename}.json")
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            recursive_translate(data)
        with open(destination_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Translation file masked successfully and saved as '{filename}.json'")
    except FileNotFoundError:
        print('The source file was not found. \nIf the angular project is not in the directory that the script is currently running from, \nSpecify it after typing mask-translate, \nfor example mask-translate "path/to/project" ')


def main():
    if sys.stdin.isatty():
        parser = ArgumentParser(description='CLI app that masks the characters of a website')
        parser.add_argument('--name', type=str, default='glyph', help='Specify the name of the copied translation file, the default name is glyph', required=False)
        parser.add_argument('directory', type=str, nargs='?', default=os.getcwd(), help='Specify the directory of the Angular project, the default is the current working directory')
        args: Namespace = parser.parse_args()
        angular_json_path = os.path.join(args.directory, 'angular.json')
        file_path = mobile_translate(args.directory, 'strings.xml')
        if os.path.exists(angular_json_path):
            default_op(args.directory, args.name)
        elif os.path.exists(file_path):
            tree = et.parse('strings.xml')
            root = tree.getroot()
            for string in root.findall('string'):
                string.text = ''.join('█' if char != ' ' and char != '\n' else char for char in string.text)
            tree.write(f'{args.name}.xml')
            print('File masked successfully')
    else:
        if sys.stdout.isatty():
            input_text = sys.stdin.read().strip()
            if input_text.strip().startswith('{') or input_text.strip().startswith('['):
                data = json.loads(input_text)
                recursive_translate(data)
                print(data)
            else:
                tree = et.ElementTree(et.fromstring(input_text))
                root = tree.getroot()
                for element in root.iter():
                    if element.text is not None:
                        element.text = ''.join('█' if char != ' ' and char != '\n' else char for char in element.text)
                tree.write(sys.stdout, encoding='unicode')
        else:
            try:
                input_text = sys.stdin.read().strip()
                if input_text.strip().startswith('{') or input_text.strip().startswith('['):
                    data = json.loads(input_text)
                    recursive_translate(data)
                    print(json.dumps(data, indent=2))
                    print("Translation file using stdin masked successfully", file=sys.stderr)
                else:
                    tree = et.ElementTree(et.fromstring(input_text))
                    root = tree.getroot()
                    for element in root.iter():
                        if element.text is not None:
                            element.text = ''.join('█' if char != ' ' and char != '\n' else char for char in element.text)
                    xml_text = et.tostring(root, encoding='utf-16')
                    sys.stdout.buffer.write(xml_text)
                    print(f"File masked successfully and saved", file=sys.stderr)
            except (json.JSONDecodeError, et.ParseError):
                print("Error: Invalid JSON or XML input.")


if __name__ == '__main__':
    main()