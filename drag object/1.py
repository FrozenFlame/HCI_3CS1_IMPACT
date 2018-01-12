import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Vroom vroom')
clock = pygame.time.Clock()

carImg= pygame.image.load('racecar.png')
carImgReso = (68,52)    # 68x52 ung dimensions ng racecar.png

x = (display_width * 0.45)
y = (display_height * 0.8)

x_key = ""
y_key = ""


def car(draw_x,draw_y):
    gameDisplay.blit(carImg,(draw_x,draw_y))

held = False

x_change = 0
y_change = 0

crashed = False

while not crashed:

    carMaxPos_x = x + carImgReso[0]                      # ung area na kinalalagyan nung image is supposedly [(x to carMaxPos_x), (y to car MaxPos_y)]
    carMaxPos_y = y + carImgReso[1]
    mouse_x, mouse_y = pygame.mouse.get_pos()

    adjusted_mx = mouse_x - (carImgReso[0]/2)            # adjusted mouse position pra pag-click, nasa gitna nung img ung mouse
    adjusted_my = mouse_y - (carImgReso[1]/2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
                x_key = "left"
            elif event.key == pygame.K_RIGHT:
                x_change = 5
                x_key = "right"
            elif event.key == pygame.K_UP:
                y_change = -5
                y_key = "up"
            elif event.key == pygame.K_DOWN:
                y_change = 5
                y_key = "down"

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and x_key == "left") or (event.key == pygame.K_RIGHT and x_key == "right"):
                x_change = 0
            elif (event.key == pygame.K_UP and y_key == "up") or (event.key == pygame.K_DOWN and y_key == "down"):
                y_change = 0


        if event.type == pygame.MOUSEBUTTONDOWN and x <= mouse_x <= carMaxPos_x and y <= mouse_y <= carMaxPos_y:            # checking na ung position ng mouse is within the area of the image
            held = True
        if event.type == pygame.MOUSEBUTTONUP:
            held = False

    x += x_change
    y += y_change

    if held:
        x = adjusted_mx
        y = adjusted_my

    gameDisplay.fill(white)
    car(x,y)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()
