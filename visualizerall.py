import pygame
from colornumbers import *
import random
from time import sleep

pygame.init()
myfont = pygame.font.SysFont('timesnewroman', 20)


# window class with all the required specifications for drawing the window
class Window:

    hozPadding = 100
    verPadding = 150


    def __init__(self, width, height, myList):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption("Sorting Visualizer")
        self.area(myList)


    def area(self, myList):
        self.myList = myList
        self.minValue = min(myList)
        self.maxValue = max(myList)

        self.widthElement = (self.width - self.hozPadding) // len(myList)
        self.heightElement = (self.height - self.verPadding) // (self.maxValue - self.minValue)


# generating the list that needs to be sorted
def generateList(elements, minValue, maxValue):
    myList = []

    for _ in range(elements):
        element = random.randint(minValue, maxValue)
        myList.append(element)

    return myList


# drawing the text on the window
def drawScreen(window):

    window.screen.fill((250, 214, 165))

    # draw starting text
    startText = myfont.render("S to Start", True, BLACK)
    window.screen.blit(startText, (window.hozPadding//2 + startText.get_width(), window.verPadding//2))

    # draw quicksort text
    quickText = myfont.render("Q for quicksort", True, BLACK)
    window.screen.blit(quickText, (window.hozPadding//2 + 200, window.verPadding//2))

    # draw bubble sort text
    bubbleText = myfont.render("B for bubblesort", True, BLACK)
    window.screen.blit(bubbleText, (window.hozPadding//2 + 350, window.verPadding//2))
    
    # draw quit text
    resetText = myfont.render("R to Reset", True, BLACK)
    window.screen.blit(resetText, (window.width - window.hozPadding//2 - resetText.get_width()*2, window.verPadding//2))

    slowText = myfont.render("H for Slow", True, BLACK)
    window.screen.blit(slowText, (window.hozPadding//2 + slowText.get_width() * 1.5, window.verPadding//4))

    mediumText = myfont.render("J for Medium", True, BLACK)
    window.screen.blit(mediumText, (window.hozPadding//2 + mediumText.get_width() * 2.5, window.verPadding//4))

    fastText = myfont.render("K for Fast", True, BLACK)
    window.screen.blit(fastText, (window.hozPadding//2 + fastText.get_width() * 5.5, window.verPadding//4))

    # quitText = myfont.render("Q to quit", True, BLACK)
    # window.screen.blit(quitText, (window.width - window.hozPadding//2 - quitText.get_width()*2, window.verPadding//2))

    # call function that draws the list as rectangles
    drawRects(window, {}, False)

    pygame.display.update()


def drawRects(window, swapColors, clear):

    myList = window.myList

    if clear == True:
        whiteRect = (window.hozPadding//2, window.verPadding, window.width - window.hozPadding, window.height - window.verPadding)
        pygame.draw.rect(window.screen, (250, 214, 165), whiteRect)

    for index, value in enumerate(myList):

        color = COLORS[index%4]

        if index in swapColors:
            color = swapColors[index]

        # draw each rectangle according to the index
        pygame.draw.rect(window.screen, color, pygame.Rect(window.hozPadding//2 + window.widthElement*index , window.height - (window.heightElement * value), window.widthElement, window.heightElement*value))

    if clear:
        pygame.display.update()

# partition for quick sort 
def partition(window, left, right, speed):

    middle = (left + right) // 2

    window.myList[left], window.myList[middle] = window.myList[middle], window.myList[left]

    pivotIndex = left
    pivotValue = window.myList[left]

    for scan in range(left+1, right+1):
        if scan < len(window.myList):
            if window.myList[scan] < pivotValue:
                pivotIndex += 1
                window.myList[scan], window.myList[pivotIndex] = window.myList[pivotIndex], window.myList[scan]
                drawRects(window, {scan:RED, pivotIndex:GREEN}, True)
                sleep(speed)

    window.myList[left], window.myList[pivotIndex] = window.myList[pivotIndex], window.myList[left]

    return pivotIndex

# quick sort divide and conquer
def quickSort(window, left, right, speed):
    if left < right:
        pivotPoint = partition(window, left, right, speed)
        quickSort(window, left, pivotPoint-1, speed)
        quickSort(window, pivotPoint+1, right, speed)


def bubbleSort(window, speed):

    length = len(window.myList)

    for i in range(length):
        for j in range(length - i - 1):
            if window.myList[j] > window.myList[j+1]:
                window.myList[j], window.myList[j+1] = window.myList[j+1], window.myList[j]
                drawRects(window, {j:RED, j+1:GREEN}, True)
                sleep(speed)



def mainLoop():
    running = True

    nrElements = 50
    minValue = 0
    maxValue = 100

    width = 800
    height = 600

    

    clock = pygame.time.Clock()


    myList = generateList(nrElements, minValue, maxValue)

    window = Window(width, height, myList)

    start = False
    # created has started variable so i cannot start sorting when the list is sorted
    hasStarted = False
    # check if user has chosen the sort
    algo = ""
    speed = 0.015

    while running:
        clock.tick(60)
        # print(pygame.mouse.get_pos())
        drawScreen(window)
        
        if start == True:
            
            hasStarted = True
            start = False

            if algo == "quicksort":
                quickSort(window, 0, nrElements, speed)
                algo = ""
            elif algo == "bubblesort":
                bubbleSort(window, speed/2)
                algo = ""

        for event in pygame.event.get():
            # x button
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                
                # check if the list is not already sorted
                if not hasStarted:
                    if algo:
                        # start sorting the list
                        if event.key == pygame.K_s:
                            start = True

                if event.key == pygame.K_q:
                    algo = "quicksort"

                if event.key == pygame.K_b:
                    algo = "bubblesort"

                if event.key == pygame.K_h:
                    speed = 0.03

                if event.key == pygame.K_j:
                    speed = 0.015

                if event.key == pygame.K_k:
                    speed = 0.008

                # reset if r is pressed
                if event.key == pygame.K_r:
                    mainLoop()
                    running = False



mainLoop()