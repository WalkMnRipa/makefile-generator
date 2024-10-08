import os

def find_project_files(extensions, exclude_dirs=None):
    files = []
    for root, dirs, filenames in os.walk('.'):
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                rel_path = os.path.relpath(os.path.join(root, filename))
                files.append(rel_path)
    return files

def get_project_info():
    name = input("Project name: ")
    use_libft = input("Use libft? (y/n): ").lower() == 'y'
    use_mlx = input("Use MLX? (y/n): ").lower() == 'y'
    if use_libft:
        libft_dir = input("Libft directory (default: libft): ") or "libft"
    else:
        libft_dir = None
    if use_mlx:
        mlx_dir = input("MLX directory (default: minilibx-linux): ") or "minilibx-linux"
    else:
        mlx_dir = None
    return name, use_libft, use_mlx, libft_dir, mlx_dir

def generate_makefile(name, src_files, header_files, use_libft, use_mlx, libft_dir, mlx_dir):
    makefile = """# Colors
GREEN = \\033[0;32m
YELLOW = \\033[0;33m
RED = \\033[0;31m
BLUE = \\033[0;34m
RESET = \\033[0m

"""
    makefile += f"""NAME = {name}
CC = cc
CFLAGS = -Wall -Wextra -Werror
"""

    if use_mlx:
        makefile += f"MLXFLAGS = -lmlx -lXext -lX11 -lm\n"

    makefile += f"""
SRCS = {' '.join(src_files)}

OBJS_DIR = objs
OBJS = $(SRCS:%.c=$(OBJS_DIR)/%.o)

DEPS = $(OBJS:.o=.d)

"""

    if use_libft:
        makefile += f"LIBFT = {libft_dir}/libft.a\n"
    if use_mlx:
        makefile += f"MLX = {mlx_dir}/libmlx.a\n"

    makefile += "\nall: $(NAME)\n\n"

    makefile += "$(NAME): $(OBJS)"
    if use_libft:
        makefile += " $(LIBFT)"
    if use_mlx:
        makefile += " $(MLX)"
    makefile += "\n"
    makefile += f"\t@$(CC) $(CFLAGS) $(OBJS) "
    
    if use_libft:
        makefile += f"-L{libft_dir} -lft "
    if use_mlx:
        makefile += f"-L{mlx_dir} $(MLXFLAGS) "
    
    makefile += "-o $(NAME)\n"
    makefile += '\t@echo "$(BLUE)$(NAME) created!$(RESET)"\n\n'

    makefile += """$(OBJS_DIR)/%.o: %.c
\t@mkdir -p $(@D)
\t@printf "$(YELLOW)Compiling $<... $(RESET)"
\t@if $(CC) $(CFLAGS) -MMD -MP -I./includes"""
    
    if use_libft:
        makefile += f" -I{libft_dir}"
    if use_mlx:
        makefile += f" -I{mlx_dir}"
    
    makefile += """ -c $< -o $@ 2>/dev/null; then \
		printf "$(GREEN)Done!$(RESET)\\n"; \
	else \
		printf "$(RED)Failed!$(RESET)\\n"; \
		exit 1; \
	fi

"""

    if use_mlx:
        makefile += f"""$(MLX):
\t@echo "$(YELLOW)Compiling MLX...$(RESET)"
\t@$(MAKE) -C {mlx_dir} > /dev/null 2>&1
\t@echo "$(GREEN)MLX compilation done!$(RESET)"

"""

    if use_libft:
        makefile += f"""$(LIBFT):
\t@echo "$(YELLOW)Compiling libft...$(RESET)"
\t@$(MAKE) -C {libft_dir} > /dev/null 2>&1
\t@echo "$(GREEN)libft compilation done!$(RESET)"

"""

    makefile += """clean:
\t@echo "$(YELLOW)Cleaning up...$(RESET)"
"""
    if use_libft:
        makefile += f"\t@$(MAKE) -C {libft_dir} clean > /dev/null\n"
    if use_mlx:
        makefile += f"\t@$(MAKE) -C {mlx_dir} clean > /dev/null\n"
    makefile += """\t@rm -rf $(OBJS_DIR)
\t@echo "$(GREEN)Clean done!$(RESET)"

fclean: clean
\t@echo "$(YELLOW)Full cleanup...$(RESET)"
"""
    if use_libft:
        makefile += f"\t@$(MAKE) -C {libft_dir} fclean > /dev/null\n"
    if use_mlx:
        makefile += f"\t@$(MAKE) -C {mlx_dir} clean > /dev/null\n"
    makefile += f"""\t@rm -f $(NAME)
\t@echo "$(GREEN)Full cleanup done!$(RESET)"

re: fclean all

.PHONY: all clean fclean re"""

    makefile += "\n\n-include $(DEPS)\n"

    return makefile

def main():
    print("Welcome to the Makefile generator!")
    name, use_libft, use_mlx, libft_dir, mlx_dir = get_project_info()
    
    exclude_dirs = []
    if use_libft:
        exclude_dirs.append(libft_dir)
    if use_mlx:
        exclude_dirs.append(mlx_dir)
    
    src_files = find_project_files(['.c'], exclude_dirs)
    header_files = find_project_files(['.h'], exclude_dirs)
    
    makefile = generate_makefile(name, src_files, header_files, use_libft, use_mlx, libft_dir, mlx_dir)
    
    with open('Makefile', 'w') as f:
        f.write(makefile)
    
    print("Makefile generated successfully!")

if __name__ == "__main__":
    main()