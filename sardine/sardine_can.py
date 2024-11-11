from PIL import Image
import numpy as np

class SardineCans:

    image: Image.Image
    cans: list

    def __init__(self, image: Image.Image) -> None:
        self.image = image
        self.cans = self.__determine_cans()

    def get_cans(self) -> list:
        return self.cans

    def __determine_cans(self) -> list:
        lb = []
        li = np.array(self.image)

        for y in range(li.shape[0]):
            for x in range(li.shape[1]):
                if li[y, x] == 0:
                    if len(lb) > 0 and self.__pixel_are_adjacent_to_can(lb[-1], (y, x)):
                        lb[-1] = self.__merge_can_with_pixel(lb[-1], (y, x))
                    else:
                        lb.append([(y, x), (y, x)])
        
        mb = self.__merge_all_adjacent_cans(lb)
        fb = self.__filter_included_cans(mb)

        return self.__merge_all_adjacent_cans(fb)
    
    def __pixels_are_adjacent(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

    def __pixel_are_adjacent_to_can(self, b, p):
        for z in b:
            if self.__pixels_are_adjacent(z, p):
                return True
        return False

    def __cans_are_adjacent(self, b1, b2):
        (x1_1, y1_1), (x2_1, y2_1) = b1
        (x1_2, y1_2), (x2_2, y2_2) = b2
        return not (x2_1 < x1_2 - 1 or x2_2 < x1_1 - 1 or y2_1 < y1_2 - 1 or y2_2 < y1_1 - 1)

    def __merge_can_with_pixel(self, b, p):
        b.append(p)
        return [(min([z[0] for z in b]), min([z[1] for z in b])), (max([z[0] for z in b]), max([z[1] for z in b]))]

    def __merge_cans(self, b1, b2):
        return [(min([z[0] for z in b1 + b2]), min([z[1] for z in b1 + b2])), (max([z[0] for z in b1 + b2]), max([z[1] for z in b1 + b2]))]

    def __merge_all_adjacent_cans(self, cans):
        mb = []
        while cans:
            can = cans.pop(0)
            merged = False
            for i in range(len(mb)):
                if self.__cans_are_adjacent(mb[i], can):
                    mb[i] = self.__merge_cans(mb[i], can)
                    merged = True
                    break
            if not merged:
                mb.append(can)
        return mb

    def __filter_included_cans(self, cans):
        fb = []
        for i in range(len(cans)):
            included = False
            for j in range(len(cans)):
                if i != j and cans[i][0][0] >= cans[j][0][0] and cans[i][0][1] >= cans[j][0][1] and cans[i][1][0] <= cans[j][1][0] and cans[i][1][1] <= cans[j][1][1]:
                    included = True
                    break
            if not included:
                fb.append(cans[i])
        return fb

    staticmethod
    def get_coordinates(can: tuple, rate: int = 1) -> tuple:
        (y1, x1), (y2, x2) = can

        x1 = x1 * rate - (rate - 1) // 2
        y1 = y1 * rate - (rate - 1) // 2
        x2 = (x2 + 1) * rate + (rate - 1) // 3
        y2 = (y2 + 1) * rate + (rate - 1) // 3

        return (x1, y1), (x2, y2)