from PIL import Image

class Tebox:
    image: Image.Image
    boxes: list

    def __init__(self, image: Image.Image) -> None:
        self.image = image

    def determine_boxes(self) -> list:
        lb = []

        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                if self.image[y, x] == 0:
                    if len(lb) > 0 and self.__pixel_are_adjacent_to_box(lb[-1], (y, x)):
                        lb[-1] = self.__merge_box_with_pixel(lb[-1], (y, x))
                    else:
                        lb.append([(y, x), (y, x)])
        
        mb = self.__merge_all_adjacent_boxes(lb)
        fb = self.__filter_included_boxes(mb)

        return self.__merge_all_adjacent_boxes(fb)

    def __pixels_are_adjacent(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

    def __pixel_are_adjacent_to_box(self, b, p):
        for z in b:
            if self.__pixels_are_adjacent(z, p):
                return True
        return False

    def __boxes_are_adjacent(self, b1, b2):
        (x1_1, y1_1), (x2_1, y2_1) = b1
        (x1_2, y1_2), (x2_2, y2_2) = b2
        return not (x2_1 < x1_2 - 1 or x2_2 < x1_1 - 1 or y2_1 < y1_2 - 1 or y2_2 < y1_1 - 1)

    def __merge_box_with_pixel(self, b, p):
        b.append(p)
        return [(min([z[0] for z in b]), min([z[1] for z in b])), (max([z[0] for z in b]), max([z[1] for z in b]))]

    def __merge_boxes(self, b1, b2):
        return [(min([z[0] for z in b1 + b2]), min([z[1] for z in b1 + b2])), (max([z[0] for z in b1 + b2]), max([z[1] for z in b1 + b2]))]

    def __merge_all_adjacent_boxes(self, boxes):
        mb = []
        while boxes:
            box = boxes.pop(0)
            merged = False
            for i in range(len(mb)):
                if self.__boxes_are_adjacent(mb[i], box):
                    mb[i] = self.__merge_boxes(mb[i], box)
                    merged = True
                    break
            if not merged:
                mb.append(box)
        return mb

    def __filter_included_boxes(self, boxes):
        fb = []
        for i in range(len(boxes)):
            included = False
            for j in range(len(boxes)):
                if i != j and boxes[i][0][0] >= boxes[j][0][0] and boxes[i][0][1] >= boxes[j][0][1] and boxes[i][1][0] <= boxes[j][1][0] and boxes[i][1][1] <= boxes[j][1][1]:
                    included = True
                    break
            if not included:
                fb.append(boxes[i])
        return fb