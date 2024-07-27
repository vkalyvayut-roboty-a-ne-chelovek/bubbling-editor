from PIL import Image, ImageDraw

from bubbling_editor.misc import AddBubblePayload


class BubblingEditorBubbleOnImage:
    def __init__(self, image_w, image_h, bubble: AddBubblePayload):
        self.image_w = image_w
        self.image_h = image_h
        self.bubble = bubble

    def make_mask(self) -> list[int]:
        result = []

        radius = self.bubble.radius
        x, y = int(self.image_w * self.bubble.pos[0]), int(self.image_h * self.bubble.pos[1])
        src_image_x1 = x - radius
        src_image_y1 = y - radius
        src_image_x2 = x + radius
        src_image_y2 = y + radius

        mask = Image.new('1', size=(radius * 2, radius * 2), color=0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=1)

        idxs = []
        for src_x in range(src_image_x1, src_image_x2):
            for src_y in range(src_image_y1, src_image_y2):
                mask_x, mask_y = src_x - src_image_x1, src_y - src_image_y1
                mask_image_pixel_idx = mask_x, mask_y
                src_image_pixel_idx = src_x, src_y
                mask_image_pixel_data = mask.getpixel(mask_image_pixel_idx)

                pixel_idx_to_set = src_image_pixel_idx if mask_image_pixel_data > 0 else None
                if 0 <= src_x < self.image_w and 0 <= src_y < self.image_h:
                    pass
                else:
                    pixel_idx_to_set = None

                if pixel_idx_to_set:
                    idxs.append(pixel_idx_to_set)
        return idxs
        # print(self.bubble)
    #     radius = self.bubble.radius
    #     src_image_x1 = self.bubble.pos[0] - radius
    #     src_image_y1 = self.bubble.pos[1] - radius
    #     src_image_x2 = self.bubble.pos[0] + radius
    #     src_image_y2 = self.bubble.pos[1] + radius
    #
    #
    #     mask = Image.new('1', size=(radius*2, radius*2), color=0)
    #     draw = ImageDraw.Draw(mask)
    #     draw.ellipse((0, 0, radius*2, radius*2), fill=1)
    #
    #     # self.image.paste(mask, (src_image_x1, src_image_y1))
    #     for mask_x in range(mask.width):
    #         for mask_y in range(mask.height):
    #             mask_pixel = mask.getpixel((mask_x, mask_y))
    #             if mask_pixel:
    #                 src_image_pixel_location = (src_image_x1 + mask_x, src_image_y1 + mask_y)
    #                 src_image_pixel_data = self.image.getpixel(src_image_pixel_location)
    #                 new_src_image_pixel_data = (src_image_pixel_data[0], src_image_pixel_data[1], src_image_pixel_data[0], 64)
    #                 if src_image_pixel_location[0] >= 0 and src_image_pixel_location[1] >= 0:
    #                     # print(src_image_pixel_data)
    #                     self.image.putpixel(src_image_pixel_location, value=new_src_image_pixel_data)
    #             # print((mask_x, mask_y), mask_pixel)
    #             # mask.putpixel()
    #
    #     # src_image_data = list(self.image.getdata())
    #     # mask_image_data = list(mask.getdata(band=0))
    #     # for mask_x, x in enumerate(range(src_image_x1, src_image_x2)):
    #     #     if 0 <= x < self.image.width:
    #     #         for mask_y, y in enumerate(range(src_image_y1, src_image_y2)):
    #     #             if 0 <= y < self.image.height:
    #     #                 src_image_pixel_idx = x + y
    #     #                 mask_image_pixel_idx = mask_x + mask_y
    #     #
    #     #                 mask_image_pixel_data = mask_image_data[mask_image_pixel_idx]
    #     #
    #     #                 if mask_image_pixel_data != 0:
    #     #                     idxs.append({'x': x, 'y': y, 'pixel': mask_image_pixel_data})
    #     #                     src_image_data[src_image_pixel_idx] = (0, 0, 0, 125)
    #
    #     # self.image.putdata(src_image_data)
    #     # print(idxs)
    #     # print('---')
    #     # print(radius)
    #     # print(src_image_x1, src_image_y1)
    #     # print(src_image_x2, src_image_y2)
    #     # print(len(idxs))
    #     # print(idxs)
    #     # print(len(mask_image_data))
    #     # print(mask_image_data)
    #
    #     # self.image.paste(mask, (src_image_x1, src_image_y1, src_image_x2, src_image_y2))
    #
    #
    #
    # def ___old(self):
    #     pass
    #     # mask = Image.new(mode='RGBA', size=(self.original_image.width, self.original_image.height), color=(0, 0, 0))
    #     # draw = ImageDraw.Draw(mask, mode='RGBA')
    #     #
    #     # c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
    #     # i_w, i_h = self.original_image.width, self.original_image.height
    #     #
    #     # for bubble in self.bubbles:
    #     #     x, y = bubble.pos[0] * i_w, bubble.pos[1] * i_h
    #     #     rel_radius = bubble.radius
    #     #     abs_radius = rel_radius
    #     #     draw.ellipse((x - abs_radius, y - abs_radius, x + abs_radius, y + abs_radius), fill=(255, 0, 0))
    #     #
    #     # # TODO костыли-костылики 🤦
    #     # # переписать, чтобы использовался расчет на основе радиуса и координат, а не обход всего массива
    #     # mask_data = mask.getdata()
    #     # resized_data = list(self.original_image.getdata())
    #     # for idx, data in enumerate(mask_data):
    #     #     if data[0] == 0:
    #     #         resized_data[idx] = (
    #     #             resized_data[idx][0],
    #     #             resized_data[idx][1],
    #     #             resized_data[idx][2],
    #     #             125)
    #     # self.original_image.putdata(resized_data)