from os.path import expanduser, exists, abspath


def update_env_file(env_path = '.env'):

    home_dir = expanduser('~')
    proj_dir = abspath('.')
    new_lines = []
    found_home_dir = False
    found_proj_dir = False

    # Read existing lines from .env file, or create a new list if file doesn't exist
    if exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Iterate over each line to find HOME_DIR and update it
    for line in lines:

        if line.strip().startswith('HOST_HOME_DIR='):
            new_lines.append(f'HOST_HOME_DIR={home_dir}\n')
            new_lines[-1] = str(new_lines[-1]).replace('\\', '/')
            found_home_dir = True
        elif line.strip().startswith('HOST_PROJ_DIR='):
            new_lines.append(f'HOST_PROJ_DIR={proj_dir}\n')
            new_lines[-1] = str(new_lines[-1]).replace('\\', '/')
            found_proj_dir = True
        else:
            new_lines.append(f'{line}')
    
    # If HOST_HOME_DIR wasn't found, append it to the file
    if not found_home_dir:
        new_lines.append(f'HOST_HOME_DIR={home_dir}\n')
    
    # If HOST_PROJ_DIR wasn't found, append it to the file
    if not found_proj_dir:
        new_lines.append(f'HOST_PROJ_DIR={proj_dir}\n')
    
    # Write updated content back to .env file
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    

if __name__ == '__main__':
    update_env_file()