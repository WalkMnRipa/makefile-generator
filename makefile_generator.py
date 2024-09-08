import os

def find_project_files(extensions):
    files = []
    for root, _, filenames in os.walk('.'):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                rel_path = os.path.relpath(os.path.join(root, filename))
                files.append(rel_path)
    return files

def get_project_info():
    name = input("Project name: ")
    use_libft = input("Use libft? (y/n): ").lower() == 'y'
    use_mlx = input("Use MLX? (y/n): ").lower() == 'y'
    return name, use_libft, use_mlx

def generate_makefile(name, src_files, header_files, use_libft, use_mlx):
    src_dirs = set(os.path.dirname(src) for src in src_files)
    include_dirs = set(os.path.dirname(header) for header in header_files)
    
    makefile = f"""# Colors
GREEN = \\033[0;32m
YELLOW = \\033[0;33m
BLUE = \\033[0;34m
RESET = \\033[0m

NAME = {name}
CC = gcc
CFLAGS = -Wall -Wextra -Werror
SRC = {' '.join(src_files)}
HEADERS = {' '.join(header_files)}
OBJ_DIR = objs
OBJ = $(SRC:%.c=$(OBJ_DIR)/%.o)

# Include all source and header directories
INCLUDES = {' '.join(f'-I{dir}' for dir in (src_dirs | include_dirs) if dir)}
"""

    if use_libft:
        makefile += "LIBFT = libft/libft.a\n"
    if use_mlx:
        makefile += "MLX = minilibx/libmlx.a\nMLX_FLAGS = -lmlx -lXext -lX11 -lm\n"

    makefile += """
all: $(NAME)

$(NAME): create_obj_dir $(OBJ)
\t@if [ ! -f $(NAME) ] || [ -n "$$(find $(OBJ_DIR) -newer $(NAME))" ]; then \\
		echo -n "$(YELLOW)Linking project... $(RESET)"; \\
"""

    if use_libft:
        makefile += "\t\t$(MAKE) -C libft > /dev/null 2>&1; \\\n"
    if use_mlx:
        makefile += "\t\t$(MAKE) -C minilibx > /dev/null 2>&1; \\\n"

    makefile += f"""\t\t$(CC) $(CFLAGS) $(INCLUDES) $(OBJ) -o $(NAME)"""
    
    if use_libft:
        makefile += " $(LIBFT)"
    if use_mlx:
        makefile += " $(MLX) $(MLX_FLAGS)"
    
    makefile += """; \\
		for i in {1..10}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.1; done; \\
		echo "$(GREEN) Done!$(RESET)"; \\
	else \\
		echo "$(GREEN)Project is already compiled and up to date.$(RESET)"; \\
	fi

create_obj_dir:
\t@mkdir -p $(OBJ_DIR) $(addprefix $(OBJ_DIR)/,$(dir $(SRC)))

$(OBJ_DIR)/%.o: %.c $(HEADERS)
\t@mkdir -p $(dir $@)
\t@echo -n "$(YELLOW)Compiling $<... $(RESET)"
\t@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
\t@echo "$(GREEN)Done!$(RESET)"

clean:
\t@echo -n "$(YELLOW)Cleaning up... $(RESET)"
"""

    if use_libft:
        makefile += "\t@$(MAKE) -C libft clean > /dev/null 2>&1\n"
    if use_mlx:
        makefile += "\t@$(MAKE) -C minilibx clean > /dev/null 2>&1\n"

    makefile += """\t@rm -rf $(OBJ_DIR)
\t@for i in {1..10}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.05; done
\t@echo "$(GREEN) Done!$(RESET)"

fclean: clean
\t@echo -n "$(YELLOW)Full cleanup... $(RESET)"
"""

    if use_libft:
        makefile += "\t@$(MAKE) -C libft fclean > /dev/null 2>&1\n"

    makefile += f"""\t@rm -f $(NAME)
\t@for i in {{1..10}}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.05; done
\t@echo "$(GREEN) Done!$(RESET)"

re: fclean all

.PHONY: all clean fclean re create_obj_dir
"""

    return makefile

def main():
    print("Welcome to the Makefile generator!")
    src_files = find_project_files(['.c'])
    header_files = find_project_files(['.h'])
    name, use_libft, use_mlx = get_project_info()
    makefile = generate_makefile(name, src_files, header_files, use_libft, use_mlx)
    
    with open('Makefile', 'w') as f:
        f.write(makefile)
    
    print("Makefile generated successfully!")

if __name__ == "__main__":
    main()