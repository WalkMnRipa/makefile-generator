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
    makefile = f"""# Colors
GREEN = \\033[0;32m
YELLOW = \\033[0;33m
BLUE = \\033[0;34m
RESET = \\033[0m

NAME = {name}
CC = cc
CFLAGS = -Wall -Wextra -Werror
"""

    if use_mlx:
        makefile += f"MLXFLAGS = -lmlx -lXext -lX11 -lm\n"

    makefile += f"""
SRC_DIR = src
CORE_DIR = $(SRC_DIR)/core
GAME_DIR = $(SRC_DIR)/game
MAP_DIR = $(SRC_DIR)/map
GRAPHICS_DIR = $(SRC_DIR)/graphics

SRCS = $(CORE_DIR)/main.c $(CORE_DIR)/init.c $(CORE_DIR)/cleanup.c \\
       $(GAME_DIR)/game_logic.c $(GAME_DIR)/player_movement.c \\
       $(MAP_DIR)/map_loader.c $(MAP_DIR)/map_validator.c $(MAP_DIR)/map_utils.c \\
       $(MAP_DIR)/map_flood_fill.c $(MAP_DIR)/map_copy.c \\
       $(GRAPHICS_DIR)/render.c $(GRAPHICS_DIR)/render_enemy.c \\
       $(GAME_DIR)/enemy_movement.c $(GAME_DIR)/enemy_init.c

OBJS_DIR = objs
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OBJS_DIR)/%.o)

"""

    if use_libft:
        makefile += f"LIBFT = {libft_dir}/libft.a\n"
    if use_mlx:
        makefile += f"MLX = {mlx_dir}/libmlx.a\n"

    makefile += """
all: $(NAME)

$(NAME): $(OBJS) """
    if use_libft:
        makefile += "$(LIBFT) "
    if use_mlx:
        makefile += "$(MLX)"
    
    makefile += f"""
\t@echo -n "$(YELLOW)Linking project... $(RESET)"
\t@$(CC) $(CFLAGS) $(OBJS) """
    
    if use_libft:
        makefile += f"-L./{libft_dir} -lft "
    if use_mlx:
        makefile += f"-L./{mlx_dir} $(MLXFLAGS) "
    
    makefile += """-o $(NAME)
\t@for i in {1..10}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.1; done
\t@echo "$(GREEN) Done!$(RESET)"

$(OBJS_DIR)/%.o: $(SRC_DIR)/%.c
\t@mkdir -p $(@D)
\t@echo -n "$(YELLOW)Compiling $<... $(RESET)"
\t@$(CC) $(CFLAGS) -I./includes"""
    
    if use_libft:
        makefile += f" -I./{libft_dir}"
    if use_mlx:
        makefile += f" -I./{mlx_dir}"
    
    makefile += """ -c $< -o $@
\t@echo "$(GREEN)Done!$(RESET)"

"""

    if use_libft:
        makefile += f"""$(LIBFT):
\t@make -C {libft_dir}

"""

    if use_mlx:
        makefile += f"""$(MLX):
\t@$(MAKE) -C {mlx_dir} > /dev/null 2>&1 || (echo "$(YELLOW)MLX compilation failed. Check {mlx_dir} for errors.$(RESET)" && exit 1)

"""

    makefile += """clean:
\t@echo -n "$(YELLOW)Cleaning up... $(RESET)"
"""
    if use_libft:
        makefile += f"\t@make -C {libft_dir} clean > /dev/null 2>&1\n"
    if use_mlx:
        makefile += f"\t@$(MAKE) -C {mlx_dir} clean > /dev/null 2>&1\n"
    makefile += """\t@rm -rf $(OBJS_DIR)
\t@for i in {1..10}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.05; done
\t@echo "$(GREEN) Done!$(RESET)"

fclean: clean
\t@echo -n "$(YELLOW)Full cleanup... $(RESET)"
"""
    if use_libft:
        makefile += f"\t@make -C {libft_dir} fclean > /dev/null 2>&1\n"
    makefile += f"""\t@rm -f $(NAME)
\t@for i in {{1..10}}; do echo -n "$(BLUE)█$(RESET)"; sleep 0.05; done
\t@echo "$(GREEN) Done!$(RESET)"

re: fclean all

.PHONY: all clean fclean re
"""

    return makefile

def main():
    print("Welcome to the Makefile generator!")
    src_files = find_project_files(['.c'])
    header_files = find_project_files(['.h'])
    name, use_libft, use_mlx, libft_dir, mlx_dir = get_project_info()
    makefile = generate_makefile(name, src_files, header_files, use_libft, use_mlx, libft_dir, mlx_dir)
    
    with open('Makefile', 'w') as f:
        f.write(makefile)
    
    print("Makefile generated successfully!")

if __name__ == "__main__":
    main()