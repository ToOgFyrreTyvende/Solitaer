from logic import build_game, print_game


def main():
    g = build_game()
    print(g.tableaus[0])
    print_game(g)


if __name__ == "__main__":
    main()
