from typing import List

from logic import build_game, print_game, move, draw, Klondike, check_move, Card


def get_nr_of_flipped(tableau: List[Card]) -> int:
    result = 0
    for card in tableau:
        if card.flipped:
            result += 1
    return result


def find_move(g: Klondike):
    moves = 0
    # pile
    if len(g.pile) == 0:
        print("Draw")
        g.stock, g.pile = draw(g.stock, g.pile)
        print_game(g)
    for j in range(len(g.tableaus)):  # looks through different tableaus
        # if len(g.tableaus[j]) == 0:
        #       print("Skip " + str(j+1))
        #        continue 
        if check_move(g.pile[-1], g.tableaus[j]):
            g.pile, g.tableaus[j] = move(1, g.pile, g.tableaus[j])
            print("Match in tableau " + str(j+1) + " Move " + str(1) + " 0 " + str(j+1))
            print_game(g)
            moves += 1
            break

    # tableaus
    for i in range(7):
        if len(g.tableaus[i]) == 0:
            print("Skip " + str(i+1))
            continue
        for j in range(len(g.tableaus)):  # looks through different tableaus
            # if len(g.tableaus[j]) == 0:
            #    print("Skip " + str(j+1))
            #    continue 
            if check_move(g.tableaus[i][-get_nr_of_flipped(g.tableaus[i])], g.tableaus[j]):
                g.tableaus[i], g.tableaus[j] = move(get_nr_of_flipped(g.tableaus[i]), g.tableaus[i], g.tableaus[j])
                print("Match in tableau " + str(j+1) + " Move " + str(1) + " " + str(i+1) + " " + str(j+1))
                print_game(g)
                moves += 1
                break
    if moves == 0:
        print("Draw")
        g.stock, g.pile = draw(g.stock, g.pile)
        print_game(g)


def main():
    g = build_game(False)
    print_game(g); print()
    g.stock, g.pile = draw(g.stock, g.pile)
    print_game(g); print()

    for i in range(100):
        find_move(g)


if __name__ == "__main__":
    main()
