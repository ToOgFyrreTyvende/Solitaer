from card_detector.yolodetector import extract_cards_from_image
import logic as l
import ai
import cv2

img = cv2.resize(cv2.imread("./card_detector/cards5.jpg"), (1280,720))
(pile, foundation, res_orig) = extract_cards_from_image(img)
res = res_orig[3:]
res.insert(0, res_orig[0])
print(res)


klondike = l.Klondike()
klondike.pile = [l.Card.from_str(pile)]
klondike.foundations = [[l.Card.from_str(foundation[0])], [], [], []]
klondike.tableaus = [[l.Card.from_str(card_name) for card_name in x] for x in res]
l.print_game(klondike)
print(ai.new_find_move(klondike))
cv2.imshow("Image", img)
cv2.waitKey(0)