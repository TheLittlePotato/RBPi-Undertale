import pygame, random, math, time
import RPi.GPIO as GPIO

def text(text,size,color,font='font.ttf'):
    font = pygame.font.Font(font,size)
    txt = font.render(text,1,color)
    return txt

def blitcenter(surf,pos): # Blit pygame.Surface with center anchor
    screen.blit(surf,[pos[0]-surf.get_size()[0]/2,pos[1]-surf.get_size()[1]/2])

mixer = pygame.mixer
pygame.init()
mixer.init()

window = pygame.display.set_mode([600,500])
pygame.display.set_caption('UNDERTALE')

#mettre un * au début et à la fin des dialogues
texte = "..."
font = pygame.font.Font('font.ttf', 15)

heart = pygame.image.load("heart0.png")
heart1 = pygame.image.load("heart1.png")
legs = pygame.image.load("sans/sans_legs.png")

talk = mixer.Sound('sfx/talk1.ogg')
talkSmall = mixer.Sound('sfx/talkSmall.ogg')
talkSmall1 = mixer.Sound('sfx/talkSmall.ogg')

px = 250
py = 300

pygame.key.set_repeat(1,1)

face = 'norm'
torso = 'norm'

char = 0
tempsSpeech = 200
enMarche = False
compteur = 0

qdat = []

qfl = open('quotes.txt')
qraw = qfl.read().split('\n')
qfl.close()

for i in qraw:
    i = i.split('/')
    qdat.append(i)

tick = 0

#Musique
mixer.music.load('bg.ogg')
mixer.music.play(-1)

screen = pygame.Surface([600,500])
screen.fill([0,0,0])

blitcenter(pygame.image.load('sans/sans_torso_'+torso+'.png'),[300,90])
blitcenter(pygame.image.load('sans/sans_face_'+face+'.png'),[300,50])
blitcenter(legs,[300,137])

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

while 1:
    if enMarche:
        label = font.render(texte[:char],15,(255,255,255))
        screen.blit(label, (150,300))
        char = char + 1
        if char == 0 or char %4 == 1:
            talk.play()
            
        time.sleep(0.06)
        
        if texte[char - 2] == ' ' and char -1 <= len(texte):
            time.sleep(0.2)
        
    if char == len(texte):
        enMarche = False

    if GPIO.input(18) == False and enMarche == False:            
        compteur = random.choice([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35])
        texteRaw = qdat[compteur]
        texte = "{}%".format(texteRaw)
        texte = texte.replace("[","").replace("'","").replace("\"","").replace("]","")
        enMarche = True
        char = 0
        screen.fill([0,0,0])

        blitcenter(pygame.image.load('sans/sans_torso_'+torso+'.png'),[300,90])
        blitcenter(pygame.image.load('sans/sans_face_'+face+'.png'),[300,50])
        blitcenter(legs,[300,137])
            
            
    window.blit(screen,[0,0])
    pygame.display.flip()
    tick+=1
