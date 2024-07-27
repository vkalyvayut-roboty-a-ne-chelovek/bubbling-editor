from PIL import Image, ImageDraw

from bubbling_editor.misc import AddBubblePayload


class BubblingEditorBubbleOnImage:
    def __init__(self, image: Image, bubble: AddBubblePayload):
        self.image = image
        self.bubble = bubble

    def apply_bubble(self):
        pass

    def ___old(self):
        mask = Image.new(mode='RGBA', size=(self.original_image.width, self.original_image.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(mask, mode='RGBA')

        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.original_image.width, self.original_image.height

        for bubble in self.bubbles:
            x, y = bubble.pos[0] * i_w, bubble.pos[1] * i_h
            rel_radius = bubble.radius
            abs_radius = rel_radius
            draw.ellipse((x - abs_radius, y - abs_radius, x + abs_radius, y + abs_radius), fill=(255, 0, 0))

        # TODO костыли-костылики 🤦
        # переписать, чтобы использовался расчет на основе радиуса и координат, а не обход всего массива
        mask_data = mask.getdata()
        resized_data = list(self.original_image.getdata())
        for idx, data in enumerate(mask_data):
            if data[0] == 0:
                resized_data[idx] = (
                    resized_data[idx][0],
                    resized_data[idx][1],
                    resized_data[idx][2],
                    125)
        self.original_image.putdata(resized_data)