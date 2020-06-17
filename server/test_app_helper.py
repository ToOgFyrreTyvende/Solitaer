img1 = img2 = img3 = img4 = 'data:image/jpeg;base64,'


with open('./test/images/img1.txt') as file:
    img1 = img1 + file.readline()
#
# with open('./test/images/img2.txt') as file:
#     img2 = img2 + file.readline()
#
# with open('./test/images/img3.txt') as file:
#     img3 = img3 + file.readline()
#
# with open('./test/images/img4.txt') as file:
#     img4 = img4 + file.readline()


def json_img_one() -> dict:
    return {"data": img1}

#
# def json_img_two() -> dict:
#     return {"data": img2}
#
#
# def json_img_three() -> dict:
#     return {"data": img3}
#
#
# def json_img_four() -> dict:
#     return {"data": img4}
