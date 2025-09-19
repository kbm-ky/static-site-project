import os
import os.path
import shutil

def main():
    copy_tree('./public', './static')

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