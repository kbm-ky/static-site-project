import os
import os.path
import shutil

from functions import markdown_to_html_node, extract_title

def main():
    copy_tree('./public', './static')
    generate_page('content/index.md', 'template.html', 'public/index.html')

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'rt') as f:
        markdown = f.read()

    with open(template_path, 'rt') as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    new_content = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    dir_part = os.path.split(dest_path)[0]
    if not os.path.exists(dir_part):
        os.makedirs(dir_part)

    with open(dest_path, 'wt') as f:
        f.write(new_content)


# Copies src to dst, deleting dst if it exists
def copy_tree(dst: str, src: str):
    # See if dst exists and is directory
    if os.path.exists(dst):
        if not os.path.isdir(dst):
            print(f'LOG: dst is not a directory!')
            raise Exception('dst is not a directory!')

        print(f'LOG: dst exists: {dst}')
        #Delete it
        shutil.rmtree(dst)
        print(f'LOG: dst deleted.')

    # See if src exists 
    if not os.path.exists(src):
        print(f'LOG: src does not exist!: {src}')
        raise Exception(f'src does not exist!: {src}')
    # and is a directory 
    if not os.path.isdir(src):
        print(f'LOG: src is not a directory!')
        raise Exception(f'src is not a directory!')
    
    # Copy tree, no thanks recursion
    print(f'LOG: copying src -> dst: {src} -> {dst}')
    shutil.copytree(src, dst)

    pass

if __name__ == '__main__':
    main()