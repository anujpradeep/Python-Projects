import pygame

WIDTH = 640
HEIGHT = 480
MAX_FRAMES = 25

def find_centers(location, textRect,width,height):
    if location == "top_right":
        center_x = width - textRect.width/2
        center_y = textRect.height/2
    elif location == "top_left":
        center_x = textRect.width/2
        center_y = textRect.height/2
    elif location == "top_middle":
        center_x = width/2
        center_y = textRect.height/2
    elif location == "bottom_right":
        center_x = width - textRect.width/2
        center_y = height - textRect.height/2
    elif location == "bottom_left":
        center_x = textRect.width/2
        center_y = height - textRect.height - 15
    elif location == "bottom_middle":
        center_x = width/2
        center_y = height - textRect.height/2
    elif location == "center":
        center_x = width / 2
        center_y = height / 2
    elif location == "center_left":
        center_x = textRect.width/2
        center_y = height / 2
    elif location == "center_right":
        center_x = width - textRect.width/2
        center_y = height / 2
    else:
        print("Location given was not in the right format")
        return 0, 0

    return center_x, center_y


def render_texts(screen, text_string, font_string, size, fg, bg, location, texts_count=1):
    font = pygame.font.SysFont(font_string, size)
    width = screen.get_width()
    height = screen.get_height()
    if texts_count > 1:
        texts = []
        texts_Rect = []

        texts.append(font.render(text_string[0], True, fg, bg))
        texts_Rect.append(texts[0].get_rect())

        (center_x, center_y) = find_centers(location, texts_Rect[0],width,height)

        texts_Rect[0].center = (center_x, center_y)
        screen.blit(texts[0], texts_Rect[0])

        center_y += texts_Rect[0].height / 2
        for i, my_text in enumerate(text_string):
            if i != 0:
                texts.append(font.render(my_text, True, fg, bg))
                texts_Rect.append(texts[i].get_rect())

                center_y += texts_Rect[i].height / 2

                texts_Rect[i].center = (center_x, center_y)
                screen.blit(texts[i], texts_Rect[i])

    else:
        text = font.render(text_string[0], True, fg, bg)
        textRect = text.get_rect()

        (center_x, center_y) = find_centers(location, textRect,width,height)

        textRect.center = (center_x, center_y)
        screen.blit(text, textRect)
