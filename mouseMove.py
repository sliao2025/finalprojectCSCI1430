import mouse

def mouseMove (cross, star, front, back):
    #if the back is visible
    if (cross == (-1, -1)):
        #to calculate relative position of center and finger shapes
        xdiff = abs(star[0] - back[0])
        ydiff = abs(star[1] - back[1])
        if (xdiff > ydiff):
            #moves the mouse left 100 pixels from current position in 0.2s 
            mouse.move(-100, 0, absolute=False, duration=0.2)
        else:
            #moves the mouse down 100 pixels from current position in 0.2s
            mouse.move(0, 100, absolute=False, duration=0.2)
    #if front is visible
    elif (star ==(-1, -1)):
        #makes sure back finger is not visible to ensure person is not clicking
        if (back ==(-1, -1)):
            #to calculate relative position of center and finger shapes
            xdiff = abs(cross[0] - front[0])
            ydiff = abs(cross[1] - front[1])
            if (xdiff > ydiff):
                #moves the mouse right 100 pixels from current position in 0.2s
                mouse.move(100, 0, absolute=False, duration=0.2)
            else:
                #moves the mouse up 100 pixels from current position in 0.2s
                mouse.move(0, -100, absolute=False, duration=0.2)
        else:
            mouse.click('left')



