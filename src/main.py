import os
import os.path
import shutil

from functions import markdown_to_html_node, extract_title

def main():
    copy_tree('./public', './static')
    # generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_pages_recursive('content', 'template.html', 'public')

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

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):

    listing = os.listdir(dir_path_content)
    # print(listing)
    for item in listing:
        path = os.path.join(dir_path_content, item)

        if os.path.isfile(path) and path.endswith('.md'):
            new_name = item.removesuffix('.md') + '.html'
            dst = os.path.join(dest_dir_path, new_name)
            generate_page(path, template_path, dst)
            print(f'{path} should be processed -> {dst}')
        elif os.path.isdir(path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(path, template_path, new_dest_dir_path)

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