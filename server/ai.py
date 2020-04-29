from typing import List

from logic import build_game, print_game, move, draw, Klondike, check_move, Card


def get_nr_of_flipped(tableau: List[Card]) -> int:
    result = 0
    for card in tableau:
        if card.flipped:
            result += 1
    return result

def game_won(g: Klondike):
    if len(g.foundations[0]) == 13 and len(g.foundations[1]) == 13 and len(g.foundations[2]) == 13 and len(g.foundations[3]) == 13:
        return True
    return False    

def find_move(g: Klondike):
    moves = 0
    # pile
    if len(g.pile) == 0 and len(g.stock) != 0:
        print("Draw")
        g.stock, g.pile = draw(g.stock, g.pile)
        # print_game(g)
    if len(g.pile) != 0:
        for f in range(4): # looks through different foundations 
            if check_move(g.pile[-1], g.foundations[f], to_foundation = True):
                g.pile, g.foundations[f] = move(1, g.pile, g.foundations[f])
                return
        for j in range(len(g.tableaus)):  # looks through different tableaus
            # if len(g.tableaus[j]) == 0:
            #       print("Skip " + str(j+1))
            #        continue 
            if check_move(g.pile[-1], g.tableaus[j]):
                g.pile, g.tableaus[j] = move(1, g.pile, g.tableaus[j])
                print("Match in tableau " + str(j+1) + " Move " + str(1) + " 0 " + str(j+1))
                # print_game(g)
                moves += 1
                return

    # tableaus
    for i in range(7):
        if len(g.tableaus[i]) == 0:
            #print(" Skip" + str(i+1))
            continue
        for f in range(4): # looks through different foundations 
            if check_move(g.tableaus[i][-1], g.foundations[f], to_foundation = True):
                g.tableaus[i], g.foundations[f] = move(1, g.tableaus[i], g.foundations[f])
                return
        for j in range(len(g.tableaus)):  # looks through different tableaus
            # if len(g.tableaus[j]) == 0:
            #    print("Skip " + str(j+1))
            #    continue 
            if g.tableaus[i][-get_nr_of_flipped(g.tableaus[i])] == g.tableaus[i][0] and g.tableaus[i][0].value == 13: continue
            if check_move(g.tableaus[i][-get_nr_of_flipped(g.tableaus[i])], g.tableaus[j]):
                g.tableaus[i], g.tableaus[j] = move(get_nr_of_flipped(g.tableaus[i]), g.tableaus[i], g.tableaus[j])
                print("Match in tableau " + str(j+1) + " Move " + str(1) + " " + str(i+1) + " " + str(j+1))
                # print_game(g)
                moves += 1
                return
    if moves == 0:
        print("Draw")
        g.stock, g.pile = draw(g.stock, g.pile)
        # print_game(g)


def main():
    g = build_game(False)
    print_game(g); print()
    g.stock, g.pile = draw(g.stock, g.pile)
    print_game(g); print()

    while not game_won(g):
        find_move(g)
        print_game(g)
    print("Game Won !!!")


if __name__ == "__main__":
    main()
