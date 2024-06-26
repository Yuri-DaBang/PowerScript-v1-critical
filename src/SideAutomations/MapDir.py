import os
import json

def map_directory(base_dir):
    mapped_files = {}
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            #if file.endswith('.py'):
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                key = relative_path.replace("//", "/").replace("//", "/")#.replace(".py","").replace(".infy","").replace(".infy2","").replace(".skiy","").replace(".pack","")#.replace(".py","")
                absolute_path = os.path.abspath(os.path.join(root, file))
                mapped_files[key] = absolute_path
            #elif file.endswith('.infy'):
            #    relative_path = os.path.relpath(os.path.join(root, file), base_dir)
            #    key = relative_path.replace("//", "/").replace(".infy", "")
            #    absolute_path = os.path.abspath(os.path.join(root, file))
            #    mapped_files[key] = absolute_path
            #else:
            #    relative_path = os.path.relpath(os.path.join(root, file), base_dir)
            #    key = relative_path.replace("//", "/")
            #    absolute_path = os.path.abspath(os.path.join(root, file))
            #    mapped_files[key] = absolute_path
    
    return mapped_files

def main():
    base_dir = r"E:/enchant/sbin/Infiniti-Lang/all/mip/infiniti3"
    mapped_files = map_directory(base_dir)
    
    for key, value in mapped_files.items():
        print(f'"{key}": "{value}",')

if __name__ == '__main__':
    main()
