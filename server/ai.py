import logic as l


def main():
    g = l.build_game()
    print(g.tableaus[0])
    l.print_game(g)


if __name__ == "__main__":
    main()
