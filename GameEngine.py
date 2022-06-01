#########################################################################################
# print("This Game devloped by Yahia Droubi - 2016 - , NO Engines , NO Pre-implementations Funcs")
################################################


class staticsVars():
    player_name = ""
    coins_get = 0
    bonus_Pts = 0
    enemies_killed = 0
    dying_times = 0
    level_reached = 1
    score = 0

    setSounds = True
    setJumpingLev = 10
    SetBulletsSameTime = 8
    BossBullets = 5
    EasyToKill=True
    ActivateShield = False

    # BGMusicOn = False
    standingnow = False
    endthis = None
    IwasHere = None
    GateOpened = False
    Finished = False

    # first time for [boss random movement]
    x_boss = 800
    y_boss = 350

    FinalBossisDead = False
    greetsDone = False


    # Rendered Text Statics for [headshot and INFO] label
    win = None
    RenderdText = None
    text_x = None
    text_y = None

class staticLevel :
    level_was = 1
    moved_to_side = False

def myGameFun():
    import pygame as py
    import pymysql
    import datetime
    from random import randint
    # from time import sleep, time
    from network import Network

    py.init() #turn all of py on.

    # if ur getting here from Pause Menu , not first time
    # didn't have time to fix glitches now , will do later so
    if(staticsVars.level_reached==1):
        staticsVars.coins_get = 0
    if(staticsVars.level_reached==2):
        staticsVars.coins_get = 5
        staticLevel.moved_to_side = True

    if(staticsVars.level_reached==3):
        staticsVars.coins_get = 0
        staticsVars.bonus_Pts = 0
        staticsVars.enemies_killed = 0
        staticsVars.dying_times = 0
        staticsVars.level_reached = 1
        staticsVars.score = 0
        if(staticsVars.GateOpened):
            staticsVars.GateOpened = False


    move_event = py.USEREVENT + 2
    hide_HS_event = py.USEREVENT + 3

    py.time.set_timer(move_event, 800)

    font = py.font.SysFont('Bauhaus 93', 38, False)
    font_small = py.font.SysFont('Arial', 23, True)


    screen_width = 1280
    screen_height = 650
    level_window = py.display.set_mode((screen_width, screen_height))

    py.display.set_caption("Yahia's simple Game")



    # list of pics
    walkRight = [py.image.load('img/PlayerR1.png'), py.image.load('img/PlayerR2.png'), py.image.load('img/PlayerR3.png'),
                 py.image.load('img/PlayerR4.png'), py.image.load('img/PlayerR5.png'), py.image.load('img/PlayerR6.png'),
                 py.image.load('img/PlayerR7.png'), py.image.load('img/PlayerR8.png'), py.image.load('img/PlayerR9.png'), py.image.load('img/PlayerShootingR.png')]

    # list emsheee ysar
    walkLeft = [py.image.load('img/PlayerL1.png'), py.image.load('img/PlayerL2.png'), py.image.load('img/PlayerL3.png'),
                py.image.load('img/PlayerL4.png'), py.image.load('img/PlayerL5.png'), py.image.load('img/PlayerL6.png'),
                py.image.load('img/PlayerL7.png'), py.image.load('img/PlayerL8.png'), py.image.load('img/PlayerL9.png'), py.image.load('img/PlayerShootingL.png')]

    bg = py.image.load('img/bg.jpg')
    bg2 = py.image.load('img/bg2.jpg')
    bg3 = py.image.load('img/bg3.jpg')
    city = py.image.load('img/city_background.jpg')

    intro = py.mixer.Sound('sounds/intro.wav')
    coinSound = py.mixer.Sound('sounds/coin.wav')
    treasureSound = py.mixer.Sound('sounds/hidden.wav')
    WinningSound = py.mixer.Sound('sounds/winSound.wav')
    hitSound = py.mixer.Sound('sounds/hit.wav')
    hitSound2 = py.mixer.Sound('sounds/hit2.ogg')
    laserSound = py.mixer.Sound('sounds/LaserBullet.ogg')
    bulletSound2 = py.mixer.Sound('sounds/single_shot_sound.wav')
    bulletSound = py.mixer.Sound('sounds/shotsound.wav')
    EnemyKilledSound = py.mixer.Sound('sounds/EnemyKilled.ogg')
    Stage3 = py.mixer.Sound('sounds/Stage3.wav')
    Stage2 = py.mixer.Sound('sounds/Secret.wav')
    bossMove = py.mixer.Sound('sounds/trans.wav')
    plDead = py.mixer.Sound('sounds/dead.wav')
    bossDead = py.mixer.Sound('sounds/BossDead.wav')
    GameOver = py.mixer.Sound('sounds/game_over.wav')
    jumpSound = py.mixer.Sound('sounds/jump.wav')
    enemyShout = py.mixer.Sound('sounds/enemyShout.wav')
    reservedItem = py.mixer.Sound('sounds/reserved_item.wav')


    if (staticsVars.setSounds):
        intro.play()

    class icons():
        keyIconVisible=False
        ShieldIconVisible = True
        x = 200
        y = 5
        keyIcon = py.image.load('img/keyIcon.jpg')
        shieldIcon = py.image.load('img/shieldIcon.jpg')

        def drawIcon(self):
             if icons.keyIconVisible:
                  level_window.blit(icons.keyIcon, (icons.x, icons.y))
                  icons.hitbox = (icons.x , icons.y  , 51, 51)
                  py.draw.rect(level_window, (0, 0, 250), icons.hitbox, 2)
             if icons.ShieldIconVisible and (staticsVars.ActivateShield):
                  level_window.blit(icons.shieldIcon, (icons.x+56, icons.y))
                  icons.hitbox = (icons.x+56, icons.y, 51, 51)
                  py.draw.rect(level_window, (0, 0, 250), icons.hitbox, 2)

    clock = py.time.Clock()

    # SAVE TO DATABASE :
    def savingStatistics():
        conn3 = pymysql.connect(host='localhost', port=3306, user='root', password='0599', db='Statistics_gameDB',
                                cursorclass=pymysql.cursors.DictCursor)
        gaming_date = datetime.datetime.now()

        try:
            with conn3.cursor() as curser:
                sqlquery = "INSERT INTO high_scores(Date,player_name,coins_get,enemies_killed,dying_times,level_reached,last_score) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                curser.execute(sqlquery, (
                    gaming_date, staticsVars.player_name, int(staticsVars.coins_get), int(staticsVars.enemies_killed), int(staticsVars.dying_times), int(staticsVars.level_reached), int(staticsVars.score)))
                conn3.commit()

        finally:
            conn3.close()

        # END SAVING

    # button to go anywhere
    class button():
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, win, outline=None):
            # Call this method to draw the button on the screen
            if outline:
                py.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

            py.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font = py.font.SysFont('comicsans', 30)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        def isOver(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True;

            return False;


    btn = button((100,100,0),screen_width-150,60,150,40,"Disable Sounds")

    # -------------------------------------------------
    # Main Object is here
    # --------------------------------------------------
    class player(object):
        def __init__(self, x, y, width, height,name="Player"):
            self.name = name
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            if(staticsVars.EasyToKill==True):
                self.vel = 6
            else :
                self.vel = 4
            self.isJump = False
            self.isShooting = False
            self.left = False
            self.right = False
            self.walkCount = 0
            self.jumpCount = staticsVars.setJumpingLev
            self.standing = True
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            self.alive = "Yes"
            self.ScoreMulti = 0
            self.coinsMulti = 0
            self.YouKilledMulti =0

        # walkCounter to help locating the right pic from the list WalkRight or Left
        def drawtheHero(self, level_window):
            if self.walkCount + 1 >= 26:
                self.walkCount = 0

            # pics of walking , I put in a list , so using index would get me the right pic
            if not (self.standing):
                if self.left:
                    level_window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    level_window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            elif (self.isShooting):
                if self.right:
                    level_window.blit(walkRight[9], (self.x, self.y))
                else:
                    level_window.blit(walkLeft[9], (self.x, self.y))

            else:
                if self.right:
                    level_window.blit(walkRight[0], (self.x, self.y))
                else:
                    level_window.blit(walkLeft[0], (self.x, self.y))
            # x and y is changing so we need to re implement the hitbox every move so we use x of player and y
            # and ( up there ) initial data is called just when creating the obj , so we write it here again
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            # py.draw.rect(level_window, (255,0,0), self.hitbox,2)

        def hitPl(self,bywhom=""):
            if(staticsVars.ActivateShield==False):
                self.isJump = False
                self.jumpCount = staticsVars.setJumpingLev
            # yes its happened , python is way deffirent than OTHER OPP
            # u could use the obj of another class in this class , "how beautiful' :

            #    if I use enemy (name of the class) , it will check all enemies location , so a confliction will e5rb betha
                if(enemyWhoHitP.x >= 0 and enemyWhoHitP.x <= 100):
                    self.x = enemyWhoHitP.x + 100
                else :
                    self.x = 30
                self.y = screen_height - 100
                self.walkCount = 0
                if(staticsVars.setSounds):
                    plDead.play()

                if(bywhom=="By Yourself"):
                    font1 = py.font.SysFont('comicsans', 60)
                    text = font1.render('-2 [Ops , You Shot yourself]', 1, (255, 0, 0))
                elif((bywhom=="By Boss")):
                    font1 = py.font.SysFont('comicsans', 60)
                    if(staticsVars.EasyToKill==True):
                        text = font1.render('-15 [Boss Got You , Try Again]', 1, (255, 0, 0))
                    else :
                        text = font1.render('-25 [Boss Got You , Try Again]', 1, (255, 0, 0))
                else:
                    font1 = py.font.SysFont('comicsans', 60)
                    if(staticsVars.EasyToKill==True):
                        text = font1.render('-5', 1, (255, 0, 0))
                    else :
                        text = font1.render('-10', 1, (255, 0, 0))

                level_window.blit(text, (600 - (text.get_width() / 2), 150))
                py.display.update()
                # when the Hero take a hit
                # delay means to not respond to anything until the time ends , so We must make an exception if user clicked on quit
                # so I made the   i < 200
                i = 0
                while i < 200:
                    py.time.delay(4)
                    i += 1
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            i = 201
                            savingStatistics()
                            py.quit()

    # --------------------------------
    # non-main objects like bullets
    # --------------------------------
    class ShootsClass(object):
        # another obj like bullet ..
        def __init__(self, x, y, radius, color, facing,type=""):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            # جهة توجه الطلقة
            # what side to shoot
            self.facing = facing
            if(staticsVars.EasyToKill==True):
                self.vel = 13 * facing
            else :
                self.vel = 7 * facing
            self.type = type

        def drawObject(self, level_window):
            # didn't use a pic for bullets to improve performance , u know generating too much "loading pic" will y5rb betna
            if(self.type=="BossShot"):
                py.draw.circle(level_window, self.color, (self.x, self.y), self.radius)
            else :
                if(staticsVars.EasyToKill==True):
                    py.draw.circle(level_window, self.color, (self.x, self.y), self.radius)
                elif(staticsVars.EasyToKill==False):
                    py.draw.aaline(level_window,self.color,[self.x,self.y],[self.x+10,self.y],5)
    # ------------
    # objects can be stand on
    # ------------
    class Block(object):
        blockIMG = py.image.load('img/block.jpg')


        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.standingNow = False
            self.wasHere = False
             # tuple
            self.hitbox = (self.x , self.y , 124, 124)
            self.visible = True

        def drawBlock(self, level_window):
             if self.visible:
                  level_window.blit(self.blockIMG, (self.x, self.y))
                  self.hitbox = (self.x , self.y  , 124, 124)
                  # py.draw.rect(level_window, (255,0,0), self.hitbox,2)


    class MovingObject(object):
        movingGround = py.image.load('img/movingBox.png')
        movingCarp = py.image.load('img/moving_cp.png')
        slider = py.image.load('img/slider.png')
        catcher = py.image.load('img/catcher.png')


        def __init__(self,x, y, width=0, height=0, end=0):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.x, self.end]
            self.pathUP = [self.y,self.end]
            self.vel = 4
            self.hitbox = (self.x+4, self.y , 80, 35)
            self.visible = False
            self.standingNow = False
            self.wasHere = False
            self.style="normal"

        def drawMovingObj(self, level_window,pic=1,style="normal"):
                self.visible = True
                self.style = style
                if self.visible:
                    if(self.style!="slider" and self.style !="catcher"):
                        self.move()
                        if(pic == 1):
                            level_window.blit(self.movingGround, (self.x, self.y))
                            self.hitbox = (self.x+4, self.y, 80, 35)
                        elif(pic==2):
                            level_window.blit(self.movingCarp, (self.x,self.y))
                            self.hitbox = (self.x+4, self.y, 70, 50)
                    elif(self.style=="slider"):
                        level_window.blit(self.slider, (self.x, self.y))
                        self.hitbox = (self.x + 4, self.y+15, 200, 40)
                    elif(self.style=="catcher"):
                        level_window.blit(self.catcher, (self.x, self.y))
                        self.hitbox = (self.x + 10, self.y + 10, 75, 50)

                    # frame of box :
                    # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)


        def move(self):
            if(self.style=="normal"):
                if self.vel > 0:
                    if self.x + self.vel < self.path[1]:
                        self.x += self.vel
                    else:
                        self.vel = self.vel * -1
                else:
                    if self.x - self.vel > self.path[0]:
                        self.x += self.vel
                    else:
                        self.vel = self.vel * -1
            if(self.style=="up-down"):
                if self.vel > 0:
                    if self.y + self.vel < self.pathUP[1]:
                        self.y += self.vel
                    else:
                        self.vel = self.vel * -1
                else:
                    if self.y - self.vel > self.pathUP[0]:
                        self.y += self.vel
                    else:
                        self.vel = self.vel * -1



    class GroundsToStand(object):
        groundPNG = py.image.load('img/flyingGround.png')



        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
            self.standingNow = False
            self.wasHere = False
             # tuple
            self.hitbox = (self.x + 10, self.y + 4, 80, 70)
            self.visible = True

        def drawGround(self, level_window,new_x,new_y):
             self.x,self.y=new_x,new_y

             if self.visible:
                  level_window.blit(self.groundPNG, (self.x, self.y))
                  self.hitbox = (self.x + 10, self.y + 4 , 80, 70)
                  # py.draw.rect(level_window, (255,0,0), self.hitbox,2)

        def stand_on(self):
            print('ur standing on here ')


    # -------------------
    # 2nd Main objects class here
    # -------------------
    class FinalBoss(object):
        MoveRight = py.image.load('img/FinalBossRight.png')
        MoveLeft = py.image.load('img/FinalBossLeft.png')
        DeadBoss = py.image.load('img/bossDead.png')

        def __init__(self, name="Final Boss", width=0, height=0):
            self.name = name
            self.x =0
            self.y=0
            self.width = width
            self.height = height
            self.hitbox = [0,0,0,0]
            self.health = 100
            self.visible = True
            self.left = False
            self.right = False
            self.dead = False
            self.alive = "Yes , Boss is fighting u"
            self.type="no type for final boss"
            # would help only when push theHero if he touch boss
            self.facing=-1


        def DrawBoss(self,lvl_window,new_x=100,new_y=300):
            if (self.dead == True):
                self.alive = "NO , You did a good work "
            else :
                self.alive = "Yes! He is"

            if(self.visible==True) and not(self.dead):
                self.x= new_x
                self.y = new_y

                if ( theHero.x > self.x):
                    lvl_window.blit(self.MoveRight, (self.x, self.y))
                    self.right = True
                    self.left = False
                    self.facing = 1

                else :
                    lvl_window.blit(self.MoveLeft, (self.x, self.y))
                    self.right = False
                    self.left = True
                    self.facing = -1

                self.hitbox = (self.x , self.y  , 187, 284)

                py.draw.rect(lvl_window, (255, 0, 0), (self.hitbox[0] + 35, self.hitbox[1] - 30, 100, 20))
                py.draw.rect(lvl_window, (0, 180, 0), (self.hitbox[0] + 35, self.hitbox[1] - 30, (0 - (-self.health)), 20))
                # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)

            if (self.dead):
                lvl_window.blit(self.DeadBoss, (self.x,self.y+100))



        def Enemy_hit(self):
            if self.health > 0:
                if (staticsVars.EasyToKill == True):
                    self.health -= 1
                else:
                    self.health -= .5
                if (staticsVars.setSounds == True):
                    hitSound2.play()
            else:
                # kill enemy ,
                if (staticsVars.setSounds == True):
                    bossDead.play()

                self.visible = False
                self.dead = True
                staticsVars.enemies_killed += 1
                staticsVars.FinalBossisDead = True


            print('Final Boss hitted by 1')

    class enemy(object):
        # enemy walking imgs list
        walkRight = [py.image.load('img/enemy/Right1E.png'), py.image.load('img/enemy/Right2E.png'), py.image.load('img/enemy/Right3E.png'),
                     py.image.load('img/enemy/Right4E.png'), py.image.load('img/enemy/Right5E.png'), py.image.load('img/enemy/Right6E.png'),
                     py.image.load('img/enemy/Right7E.png'), py.image.load('img/enemy/Right8E.png'), py.image.load('img/enemy/Right9E.png')]

        walkLeft = [py.image.load('img/enemy/Left1E.png'), py.image.load('img/enemy/Left2E.png'), py.image.load('img/enemy/Left3E.png'),
                    py.image.load('img/enemy/Left4E.png'), py.image.load('img/enemy/Left5E.png'), py.image.load('img/enemy/Left6E.png'),
                    py.image.load('img/enemy/Left7E.png'), py.image.load('img/enemy/Left8E.png'), py.image.load('img/enemy/Left9E.png')]

        DeadEnemy = py.image.load('img/enemy/DeadEnemy.png')



        flying_to_right = py.image.load('img/rocket/flying_enemy_to_right.png')
        flying_to_right = py.transform.scale(flying_to_right,(100,100))

        flying_to_left = py.image.load('img/rocket/flying_enemy_to_left.png')
        flying_to_left = py.transform.scale(flying_to_left,(100,100))

        def __init__(self, name="noName Enemy",x=0, y=0, width=0, height=0, end=0):
            self.name = name
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
          # start point for enemy and path's end :D
            self.path = [self.x, self.end]
            self.walkCount = 0
            self.fly_vel = 15
            self.dead = False
            self.alive = "YES ! "
            if (staticsVars.EasyToKill == False):
                self.vel = 6
            else:
                self.vel = 3
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            self.health = 10
            self.visible = True
            self.type=""



        def drawEnemy(self, level_window,type="e"):
            if (self.dead):
                self.alive = "NO , Killed by You"
            else :
                self.alive = "Yes! he's walking"

            if(type=="fly"):
                self.type = type
                self.AI_move(type)
                if self.visible:
                    if self.fly_vel > 0:
                        level_window.blit(self.flying_to_right, (self.x, self.y))
                    else :
                        level_window.blit(self.flying_to_left, (self.x, self.y))

                    py.draw.rect(level_window, (255, 0, 0), (self.hitbox[0]+10, self.hitbox[1] - 20, 80, 10))
                    py.draw.rect(level_window, (0, 128, 0),(self.hitbox[0]+10, self.hitbox[1] - 20, 80 - (5 * (10 - self.health)), 10))
                    self.hitbox = (self.x , self.y + 20, 100, 60)

                    # frame of enemy :
                    # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)
            else :

                if self.visible and not(self.dead):
                    self.AI_move()
                    if self.walkCount + 1 >= 27:
                        self.walkCount = 0

                    if self.vel > 0:
                        level_window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                    else:
                        level_window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1

                    # enemy health bar
                    py.draw.rect(level_window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                    py.draw.rect(level_window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
                    self.hitbox = (self.x + 17, self.y + 10, 31, 55)
                if (self.dead):
                    level_window.blit(self.DeadEnemy, (self.x, self.y+20))


            # frame of enemy :
            #     py.draw.rect(level_window, (255,0,0), self.hitbox,2)

        def AI_move(self,type="e"):
            if(type=="fly"):

                if self.fly_vel > 0:
                    if self.x + self.fly_vel < self.path[1]:
                        self.x += self.fly_vel
                    else:
                        self.fly_vel = self.fly_vel * -1

                else:
                    if self.x - self.fly_vel > self.path[0]:
                        self.x += self.fly_vel
                    else:
                        self.fly_vel = self.fly_vel * -1



            else:
                if self.vel > 0:
                    if self.x + self.vel < self.path[1]:
                        self.x += self.vel
                    else:
                        self.vel = self.vel * -1
                        self.walkCount = 0
                else:
                    if self.x - self.vel > self.path[0]:
                        self.x += self.vel
                    else:
                        self.vel = self.vel * -1
                        self.walkCount = 0

        def Enemy_hit(self):
            if self.health > 0:
                if(staticsVars.EasyToKill==True):
                    self.health -= 1
                else :
                    self.health -= .2
                if (staticsVars.setSounds == True):
                    hitSound.play()
            else:
                # kill enemy ,
                if(staticsVars.setSounds==True):
                    EnemyKilledSound.play()

                fontx = py.font.SysFont('comicsans', 20)
                Bonus = fontx.render('- 2 [health] ', 1, (250, 0, 0), (0, 0, 0))
                level_window.blit(Bonus, (500, 500))
                self.visible = False
                self.dead = True
                staticsVars.enemies_killed += 1
                print("lol yahia , you just killed the enemy you programmed")



            print('Enemy hitted by 1')


    # ---------------------------------------
    # functions Objects
    # ---------------------------------------
    class hide_treasure(object):
        treasurePNG = py.image.load('img/treasure_small.png')



        def __init__(self, x, y):
            self.x = x
            self.y = y
             # tuple
            self.hitbox = (self.x+5 , self.y+5 , 120,100 )
            self.visible = False

        def drawTreasure(self, level_window):
             if (self.visible):
                  level_window.blit(self.treasurePNG, (self.x, self.y))
             else:
                  if(staticsVars.level_reached==2):
                      self.hitbox = (self.x+5 , self.y+5 , 120, 100)
                      # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)



        def pickedUP(self):
            self.visible = True
            if(staticsVars.setSounds == True):
                treasureSound.play()

            print('Wow , 100 coin , what a treasuer')
            staticsVars.bonus_Pts += 10


    # --------------------------------------------------
    class coin(object):
        # coinGIF = py.image.load('img/coin.gif')
        coinPNG = py.image.load('img/coin.png')



        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
             # tuple
            self.hitbox = (self.x+30 , self.y+25 , 40,50 )
            self.visible = True

        def drawCoin(self, level_window,new_x,new_y):
             self.x,self.y = new_x,new_y
             if self.visible:
                  level_window.blit(self.coinPNG, (self.x, self.y))
                  self.hitbox = (self.x , self.y  , 35, 60)
                  # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)


        def pickedUP(self):
            self.visible = False
            if(staticsVars.setSounds == True):
                coinSound.play()

            print('u deserved that coin')
            staticsVars.coins_get += 1

    class Addon(object):
        shieldPNG = py.image.load('img/shield.png')


        def __init__(self, x=0, y=0,type=""):
            self.x = x
            self.y = y
            self.hitbox = (self.x+10 , self.y+5 , 35,30 )
            self.visible = True
            self.type = type

        def drawAddon(self, level_window,new_x=0,new_y=0):
             if(new_x!=0):
                 self.x,self.y = new_x,new_y
             if self.visible:
                 if(self.type=="shield"):
                      level_window.blit(self.shieldPNG, (self.x, self.y))
                      self.hitbox = (self.x+10 , self.y+5  , 35, 30)
                      # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)


        def pickedUP(self):
            self.visible = False
            staticsVars.bonus_Pts +=5
            if(staticsVars.setSounds == True):
                reservedItem.play()
            print('u deserved that Addon')
            if (self.type == "shield"):
                staticsVars.ActivateShield=True
                font2 = py.font.SysFont('Freestyle Script', 80)
                fontArial = py.font.SysFont('AR DELANEY',50)
                text = font2.render('Wow , [SHIELD] , NO DIYING FOR NOW ', 1, (0, 0, 0))
                text2 = fontArial.render('Cheat Code for De/Activate this any time : ZXC (same time)', 1, (255, 0, 0))
                level_window.blit(text, (600 - (text.get_width() / 2), 150))
                level_window.blit(text2, (600 - (text2.get_width() / 2), 250))
                py.display.update()
                i = 0
                while i < 150:
                    py.time.delay(15)
                    i += 1
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            i = 151
                            savingStatistics()
                            py.quit()

    class Gate(object):
            GateJPG = py.image.load('img/gate.jpg')
            keyPNG = py.image.load('img/key.png')
            keyPNG = py.transform.scale(keyPNG, (100, 100))



            def __init__(self, x, y,keyx,keyy):
                self.x = x
                self.y = y
                self.keyx = keyx
                self.keyy = keyy
                self.hitbox = (self.x,self.y,118,180)
                 # tuple
                self.Keyhitbox = (self.keyx+20 , self.keyy+30 , 100,80 )
                self.visible = False
                self.keyVisible = False

            def drawGate(self, level_window):
                 if self.visible:
                      level_window.blit(self.GateJPG, (self.x, self.y))
                      self.hitbox = (self.x , self.y  , 118, 180)
                      # py.draw.rect(level_window, (255, 0, 0), self.hitbox, 2)
            def drawKey(self, level_window):
                 if self.keyVisible:
                      level_window.blit(self.keyPNG, (self.keyx, self.keyy))
                      self.Keyhitbox = (self.keyx+40 , self.keyy+20  , 50, 60)
                      # py.draw.rect(level_window, (255, 0, 0), self.Keyhitbox, 2)


            def FoundIT(self):
                # self.visible = False
                if(staticsVars.setSounds == True):
                    WinningSound.play()
                print('Gate or its key ')
                staticsVars.bonus_Pts += 10



    # -----------------------------------------------------
    # Defenitions of Functions
    # -----------------------------------------------------
    def HelloMousePointer(mouse_pos,list_of_Peds=[]):
        for ped in list_of_Peds:
            if mouse_pos[0]> ped.hitbox[0] and mouse_pos[0]< ped.hitbox[0] + ped.hitbox[2] and mouse_pos[1] > ped.hitbox[1] and mouse_pos[1]<ped.hitbox[1]+ped.hitbox[3]:
                    print("مرحبا",ped.name)
                    fontx = py.font.SysFont('comicsans', 20)
                    details = fontx.render(str('Name : '+ped.name+"  Alive ? "+ped.alive), 1, (0, 0, 0), (255, 255, 255))

                    staticsVars.win = level_window
                    staticsVars.RenderdText = details
                    staticsVars.text_x = ped.x
                    staticsVars.text_y = ped.y - 50
                    py.time.set_timer(hide_HS_event, 200)

                    if event.type == py.MOUSEBUTTONDOWN:
                        if (staticsVars.setSounds):
                            enemyShout.play()

    # theHero.hitbox[1] = player head
    # ground.hitbox[1] = object head
    # ground.hitbox[1] + ground.hitbox[3] = object bottom (y end)
    # theHero.hitbox[1] + theHero.hitbox[3] = player feets
    # ground.hitbox[0] = object left
    # ground.hitbox[0]+ground.hitbox[2] = object right
    # theHero.hitbox[0] = player left
    # theHero.hitbox[0] + theHero.hitbox[2] = player right


    def PlatformBounds(AllPlatforms = []):

        # ----------------------------------
        # a beautiful reminder  , just don't use a external variable ,, use an object self one , so everyone has its on time
        for groundx in AllPlatforms :
                if theHero.hitbox[1] + theHero.hitbox[3] >= groundx.hitbox[1] and theHero.hitbox[1] + theHero.hitbox[3] <= groundx.hitbox[1]+25:
                    if theHero.hitbox[0] + theHero.hitbox[2] > groundx.hitbox[0] and theHero.hitbox[0] < groundx.hitbox[0] + groundx.hitbox[2]:
                        if ( groundx.standingNow == False ):
                            theHero.isJump = False
                        if ( groundx.standingNow == False ):
                            theHero.isJump = False
                        if ((not keys[py.K_UP]) and (not keys[py.K_w])):
                          theHero.jumpCount = 0
                        else :
                            theHero.jumpCount = staticsVars.setJumpingLev




                        groundx.standingNow = True
                        staticsVars.endthis = True

                elif not ((theHero.hitbox[1] + theHero.hitbox[3] >= groundx.hitbox[1] and theHero.hitbox[1] + theHero.hitbox[3] <= groundx.hitbox[1]+25) and (theHero.hitbox[0] + theHero.hitbox[2] > groundx.hitbox[0] and theHero.hitbox[0] < groundx.hitbox[0] + groundx.hitbox[2])):
                    groundx.standingNow = False
                    staticsVars.endthis = False
                    if (theHero.y < (screen_height) and not ((theHero.hitbox[1] + theHero.hitbox[3] >= groundx.hitbox[1] and theHero.hitbox[1] + theHero.hitbox[3] <= groundx.hitbox[1]+25) and (theHero.hitbox[0] + theHero.hitbox[2] > groundx.hitbox[0] and theHero.hitbox[0] < groundx.hitbox[0] + groundx.hitbox[2]))):
                        staticsVars.endthis = True

                    if (theHero.y < (screen_height - theHero.height-60) and not(neg ==1)):
                        theHero.y +=2
                        theHero.isJump = True

    #----------------------------------------------------------------------------------------------------------


    def HitByEnemy(enemies = []):
        for enemyxy in enemies :
            if enemyxy.visible == True:
                if theHero.hitbox[1] < enemyxy.hitbox[1] + enemyxy.hitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > enemyxy.hitbox[1]:
                    if theHero.hitbox[0] + theHero.hitbox[2] > enemyxy.hitbox[0] and theHero.hitbox[0] < enemyxy.hitbox[0] + enemyxy.hitbox[2]:
                        if(staticsVars.ActivateShield==False):
                            theHero.hitPl()
                            staticsVars.score -= 5
                            if(staticsVars.EasyToKill==False):
                                staticsVars.score -=15
                            enemyWhoHitP.x = enemyxy.x
                            staticsVars.dying_times +=1
                        # this to make some enemies push u when collis..
                        if(enemyxy.type=="fly"):
                            theHero.x+=enemyxy.fly_vel
                        elif(enemyxy.name=="The Boss") :
                            theHero.x += ((enemyxy.width/3)*enemyxy.facing)
                        elif(enemyxy.name=="Shreder" and (theHero.y>=enemyxy.y-10 and theHero.y<=enemyxy.y+10 )):
                            theHero.x += enemyxy.vel




    def HitByShots(Shoots = []):
        for shotx in Shoots :
            if shotx.y - shotx.radius < theHero.hitbox[1] + theHero.hitbox[3] and shotx.y + shotx.radius > \
                    theHero.hitbox[1]:
                if shotx.x + shotx.radius > theHero.hitbox[0] and shotx.x - shotx.radius < theHero.hitbox[0] + \
                        theHero.hitbox[2]:
                    if (staticsVars.ActivateShield == False):
                        theHero.hitPl("By Boss")
                        staticsVars.score -= 25
                        print("Boss got you ")
                        Shoots.pop(Shoots.index(shotx))
                        staticsVars.dying_times += 1



    def MovewithObject(movObjs = [],EnemywhoStandsOnIt=[]):
        for objX in movObjs :
            if objX.visible == True:
                if theHero.hitbox[1] < objX.hitbox[1] + objX.hitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > objX.hitbox[1]:
                    if theHero.hitbox[0] + theHero.hitbox[2] > objX.hitbox[0] and theHero.hitbox[0] < objX.hitbox[0] + objX.hitbox[2]:
                        if(objX.style=="catcher"):
                            theHero.x=objX.x
                        if(objX.style=="normal"):
                            theHero.x+=objX.vel
                        elif(objX.style=="slider"):
                            # same here as normal yes, but diff in moving itself there
                            theHero.x += objX.vel
                        elif(objX.style=="up-down"):
                            theHero.y+=objX.vel
                for enyx in EnemywhoStandsOnIt :
                    if enyx.hitbox[1] < objX.hitbox[1] + objX.hitbox[3] and enyx.hitbox[1] + enyx.hitbox[3] > \
                            objX.hitbox[1]:
                        if enyx.hitbox[0] + enyx.hitbox[2] > objX.hitbox[0] and enyx.hitbox[0] < objX.hitbox[
                            0] + objX.hitbox[2]:
                            if (objX.style == "normal" or objX.style == "slider"):
                                # to fix glitch when final boss dies , maybe this will move him so
                                if (objX.style == "normal" and enyx.name == "The Boss" and enyx.dead):
                                    print("Boss I'm the Carpet And I don't want to move u cuz ur dead")
                                else :
                                    enyx.x += (objX.vel-2)
                            elif (objX.style == "up-down"):
                                # to fix glitch when final boss dies , maybe this will rise him so
                                if(enyx.name=="The Boss" and enyx.dead):
                                    print("dude , Boss I'm the Moving Box And I don't want to rise u up cuz ur dead")
                                else :
                                    enyx.y += (objX.vel-2)
                            # to fix a glitch when kill enemy on slider , he will just move to infinite so this :
                            if(enyx.dead) :
                                if(enyx.x>objX.hitbox[0] + objX.hitbox[2]):
                                   enyx.x=objX.hitbox[0] + objX.hitbox[2]

    def CollisionWithObjects(Walls=[]):
        for wallx in Walls:
            # #من يسار الحيط
            if theHero.hitbox[0]+theHero.hitbox[2]>=wallx.hitbox[0]:
                 if theHero.hitbox[1]+theHero.hitbox[3]>wallx.hitbox[1]+30:
                     if theHero.hitbox[1]< wallx.hitbox[1]+wallx.hitbox[3]-50 :
                         if theHero.hitbox[0]<wallx.hitbox[0]+(wallx.hitbox[2]/2):
                             theHero.x -= ((theHero.hitbox[0] + theHero.hitbox[2]) - wallx.hitbox[0] )
            #
            # # # ن يمين الحيط
            if theHero.hitbox[0]<=wallx.hitbox[0]+wallx.hitbox[2]:
                if(theHero.hitbox[0]>wallx.hitbox[0]+(wallx.hitbox[2]/2)):
                     if theHero.hitbox[1]+theHero.hitbox[3]>wallx.hitbox[1]+30:
                         if theHero.hitbox[1]< wallx.hitbox[1]+wallx.hitbox[3]-50 :
                             if theHero.hitbox[0]+theHero.hitbox[2]>wallx.hitbox[0]:
                                 theHero.x += ((wallx.hitbox[0] + wallx.hitbox[2]) - theHero.hitbox[0])
            #     # bottom collision
            if (theHero.hitbox[1]<=wallx.hitbox[1]+wallx.hitbox[3]):
                if (theHero.hitbox[1]>wallx.hitbox[1]):
                    if(theHero.hitbox[0]>wallx.hitbox[0]):
                        if(theHero.hitbox[0]+theHero.hitbox[2]<wallx.hitbox[0]+wallx.hitbox[2]):
                             theHero.y+=((wallx.hitbox[1]+wallx.hitbox[3])-theHero.hitbox[1])
            # Roof Collision
            if (theHero.hitbox[1]+theHero.hitbox[3]>=wallx.hitbox[1]):
                if(theHero.hitbox[1]+theHero.hitbox[3]<wallx.hitbox[1]+(wallx.hitbox[3]/2)):
                    if(theHero.hitbox[0]+theHero.hitbox[3]>wallx.hitbox[0]):
                        if(theHero.hitbox[0]<wallx.hitbox[0]+wallx.hitbox[3]):

                            theHero.y-=((theHero.hitbox[1]+theHero.hitbox[3])-wallx.hitbox[1])

                            if (wallx.standingNow == False):
                                theHero.isJump = False
                            if ((not keys[py.K_UP]) and (not keys[py.K_w])):
                                theHero.jumpCount = 0
                            else:
                                theHero.jumpCount = staticsVars.setJumpingLev

                            wallx.standingNow = True
                            staticsVars.endthis = True
            else :
                wallx.standingNow = False
                staticsVars.endthis = False
                if (theHero.y < (screen_height) and not ((theHero.hitbox[1] + theHero.hitbox[3] >= wallx.hitbox[1] and theHero.hitbox[1] + theHero.hitbox[3] <= wallx.hitbox[1] + 25) and (theHero.hitbox[0] + theHero.hitbox[2] > wallx.hitbox[0] and theHero.hitbox[0] < wallx.hitbox[0] + wallx.hitbox[2]))):
                    staticsVars.endthis = True

                if (theHero.y < (screen_height - theHero.height - 60) and not (neg == 1)):
                    theHero.y += 1
                    theHero.isJump = True

    def TouchCoinAndPickitUP(coins = []):
    # collison between coin and the Player
        for coinx in coins :
            if coinx.visible == True:
                if theHero.hitbox[1] < coinx.hitbox[1] + coinx.hitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > \
                        coinx.hitbox[1]:
                    if theHero.hitbox[0] + theHero.hitbox[2] > coinx.hitbox[0] and theHero.hitbox[0] < coinx.hitbox[0] + \
                            coinx.hitbox[2]:
                        coinx.pickedUP()
                        staticsVars.score += 5


    def FindTreasure(treasures = []):
    # collison between treasure and the Player
        for treasurex in treasures :
            if treasurex.visible == False and staticsVars.level_reached==2:
                if theHero.hitbox[1] < treasurex.hitbox[1] + treasurex.hitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > \
                        treasurex.hitbox[1]:
                    if theHero.hitbox[0] + theHero.hitbox[2] > treasurex.hitbox[0] and theHero.hitbox[0] < treasurex.hitbox[0] + \
                            treasurex.hitbox[2]:
                        treasurex.pickedUP()
                        temp_score=staticsVars.score

                        staticsVars.score += 100

                        font2 = py.font.SysFont('comicsans', 100)
                        text = font2.render('+ 100 Score , A treasure found <3 ', 1, (255, 230, 0))
                        level_window.blit(text, (600 - (text.get_width() / 2), 200))
                        py.display.update()
                        i = 0
                        while i < 150:
                            py.time.delay(10)
                            i += 1
                            for event in py.event.get():
                                if event.type == py.QUIT:
                                    i = 151
                                    savingStatistics()
                                    py.quit()
    def FindGate(Gates = []):
        # collison between gate and the Player
        if(staticsVars.level_reached==3):
            for gatex in Gates :
                gatex.visible = True
                if icons().keyIconVisible==True:
                    if theHero.hitbox[1] < gatex.hitbox[1] + gatex.hitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > \
                            gatex.hitbox[1]:
                        if theHero.hitbox[0] + theHero.hitbox[2] > gatex.hitbox[0] and theHero.hitbox[0] < gatex.hitbox[0] + \
                                gatex.hitbox[2] and staticsVars.coins_get>=5 and staticsVars.enemies_killed>4 and staticsVars.FinalBossisDead:
                                    gatex.FoundIT()
                                    staticsVars.score += 100
                                    font2 = py.font.SysFont('Bauhaus 93',50,False)
                                    text = font2.render('Congratulations , The Gate is Opened now', 1, (255, 250, 150))
                                    level_window.blit(text, (600 - (text.get_width() / 2), 200))
                                    staticsVars.GateOpened = True
                                    gatex.visible = False
                                    py.display.update()
                                    i = 0
                                    while i < 150:
                                        py.time.delay(10)
                                        i += 1
                                        for event in py.event.get():
                                            if event.type == py.QUIT:
                                                i = 151
                                                savingStatistics()
                                                py.quit()


                if gatex.keyVisible == False and icons.keyIconVisible==False :
                    if theHero.hitbox[1] < gatex.Keyhitbox[1] + gatex.Keyhitbox[3] and theHero.hitbox[1] + theHero.hitbox[3] > \
                            gatex.Keyhitbox[1]:
                        if theHero.hitbox[0] + theHero.hitbox[2] > gatex.Keyhitbox[0] and theHero.hitbox[0] < gatex.Keyhitbox[0] + \
                                gatex.Keyhitbox[2]:
                            gatex.visible=True
                            icons.keyIconVisible = True
                            gatex.keyVisible = True
                            gatex.FoundIT()
                            staticsVars.score += 100
                            font2 = py.font.SysFont('Bauhaus 93', 50)
                            text = font2.render('Hidden key for the Final Gate [Found]  ', 1, (92, 131, 189))
                            level_window.blit(text, (600 - (text.get_width() / 2), 200))
                            py.display.update()
                            i = 0
                            while i < 150:
                                py.time.delay(10)
                                i += 1
                                for event in py.event.get():
                                    if event.type == py.QUIT:
                                        i = 151
                                        savingStatistics()
                                        py.quit()
                            gatex.keyVisible = False





    def checkLevelandSetThings(all_en):
        if (staticsVars.score < -150 and staticsVars.EasyToKill == True):
            print("Game Over")
            font2 = py.font.SysFont('Chiller', 100)
            if(staticsVars.setSounds):
                GameOver.play()
            text = font2.render(':( :( Game Over :( :(  ', 1, (255, 250, 150))
            level_window.blit(text, (600 - (text.get_width() / 2), 250))
            staticsVars.Finished = True


        elif(staticsVars.EasyToKill==False and staticsVars.score<-400):
                print("Game Over")
                font2 = py.font.SysFont('Chiller', 100)
                if (staticsVars.setSounds):
                    GameOver.play()
                text = font2.render(':( Game Over :( ', 1, (255, 250, 150))
                level_window.blit(text, (600 - (text.get_width() / 2), 250))
                staticsVars.Finished = True


        else :
            if (staticsVars.GateOpened ):
                level_window.blit(city, (0, 0))
                font2 = py.font.SysFont('Courier', 50)
                font2x = py.font.SysFont('Bauhaus 93', 60)
                text = font2.render('Congratulations : YOUR SAFE NOW ', 1, (255, 0, 0),(0,0,0))
                text2 = font2x.render('Your City is a head  , click on X to close', 1, (255, 0, 0))
                level_window.blit(text, (600 - (text.get_width() / 2), 200))
                level_window.blit(text2, (600 - (text2.get_width() / 2), 300))
                py.display.update()
                i = 0
                while i < 150:
                    py.time.delay(5000)
                    i += 1
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            i = 151
                            savingStatistics()
                            py.quit()

            else :
                if(staticsVars.coins_get>=12):
                    level_window.blit(bg3, (0, 0))
                    Final_Level()

                    if (staticLevel.level_was == 2):
                        staticsVars.level_reached += 1
                        for enemyd in all_en:
                            enemyd.health = 10
                            enemyd.visible = True
                            enemyd.dead = False

                        staticLevel.level_was = 3


                elif (staticsVars.coins_get>=5 and staticsVars.enemies_killed>=1 and staticsVars.coins_get<12):
                    if(theHero.x>screen_width-100):
                        staticLevel.moved_to_side = True
                    else :
                        level_window.blit(bg, (0, 0))
                    # you must move to the left side of the screen to enter level 2
                        GoToOtherLevel = font.render('You must go from here ---> ', 1, (250, 0, 0))
                        level_window.blit(GoToOtherLevel, (850, screen_height-100))

                    if(staticLevel.moved_to_side):
                        level_window.blit(bg2, (0, 0))
                        Level_TwoItems()
                        if (staticLevel.level_was == 1 )    :
                             staticsVars.level_reached += 1
                             for enemyd in all_en:
                                    enemyd.health = 10
                                    enemyd.visible = True
                                    enemyd.dead = False

                             staticLevel.level_was = 2


                elif (staticsVars.coins_get<=5 ):
                    # background first to not hide the objects
                    level_window.blit(bg, (0, 0))
                    # second
                    Level_OneItems()

                    staticLevel.level_was = 1


    def Level_OneItems():
        flyinGround.drawGround(level_window,100,480)
        sando.drawGround(level_window,200,390)
        cause4.drawGround(level_window,400,300)
        cause5.drawGround(level_window,810,330)
        cause6.drawGround(level_window,1000,430)
        cause7.drawGround(level_window,690,450)
        Slider.drawMovingObj(level_window,3,"slider")





        # this is here because of a Weird-Rare Glicth happened when jumping from TopRight side of screen
        coin6.drawCoin(level_window,-700, -100)
        coin7.drawCoin(level_window,-600, screen_height-100)
        coin8.drawCoin(level_window,-100, screen_height-200)
        coin9.drawCoin(level_window,-400, 160)
        coin10.drawCoin(level_window,-900, 200)
        coin11.drawCoin(level_window,-1000, 50)
        coin12.drawCoin(level_window,-1100, 300)
              ########################################

        coin1.drawCoin(level_window,700, screen_height-300)
        coin2.drawCoin(level_window,600, screen_height-125)
        coin3.drawCoin(level_window,100, 150)
        coin4.drawCoin(level_window,300, 300)
        coin5.drawCoin(level_window,1050, 120)



        FinalBossX.DrawBoss(level_window,-500, -500)

    def Level_TwoItems():
        flyinGround.drawGround(level_window,100,380)
        sando.drawGround(level_window,200,290)
        cause4.drawGround(level_window,350,210)
        cause5.drawGround(level_window,810,230)
        cause6.drawGround(level_window,1000,330)
        cause7.drawGround(level_window,690,350)
        cause8.drawGround(level_window,40,450)
        cause9.drawGround(level_window,730,490)
        cause10.drawGround(level_window,850,530)
        MovingCP.drawMovingObj(level_window,2)
        Slider.drawMovingObj(level_window,3,"slider")





        #will help if coming from pause menu not a new game
        coin1.visible,coin2.visible,coin3.visible,coin4.visible,coin5.visible = False,False,False,False,False

        shield.drawAddon(level_window)
        coin6.drawCoin(level_window,700, 100)
        coin7.drawCoin(level_window,600, screen_height-100)
        coin8.drawCoin(level_window,100, screen_height-200)
        coin9.drawCoin(level_window,400, 160)
        coin10.drawCoin(level_window,900, 200)
        coin11.drawCoin(level_window,1000, 50)
        coin12.drawCoin(level_window,1100, 300)

    class HiFinal():
        final_mission_music = True
        notChange = False

    def Final_Level():
        if(Titles_Static.FinalStage=="We are in"):
            if HiFinal.final_mission_music:
                if (staticsVars.setSounds == True):
                    music = py.mixer.music.load('sounds/FinalTheme.mp3')
                    py.mixer.music.play(-1)
                    HiFinal.final_mission_music = False

            flyinGround.drawGround(level_window,1100,200)
            sando.drawGround(level_window,250,300)
            cause4.drawGround(level_window,700,150)
            cause5.drawGround(level_window,160,200)

            if(HiFinal.notChange == False):
                cause6.drawGround(level_window,-100,-100)
                cause7.drawGround(level_window,-100,-100)
                cause8.drawGround(level_window,-100,-100)
                cause9.drawGround(level_window,-100,-100)
                cause10.drawGround(level_window,-100,-100)
                HiFinal.notChange = True



            if (FinalBossX.visible) and not (FinalBossX.dead):
                for e in py.event.get():
                    if e.type == move_event:  # is called every '800' milliseconds
                        if(staticsVars.setSounds):
                            bossMove.play()
                        staticsVars.x_boss = randint(int(screen_width/3), screen_width - 100)
                        staticsVars.y_boss = randint((screen_height / 2), (screen_height / 2) + 100)
                        print("Final Boss is moving ")

            FinalBossX.DrawBoss(level_window, staticsVars.x_boss, staticsVars.y_boss)
                # Final Boss Shots
            if (FinalBossX.visible ):
                if FinalBossX.left:
                    facing = -1
                else:
                    facing = 1
                    # this bullet is going out from the right side
                b1x = ShootsClass(round(FinalBossX.x + FinalBossX.width), round((FinalBossX.y + FinalBossX.height // 2)+15), 9,
                                (255, 255, 153),
                                facing,"BossShot")
                # from the left side
                b2x = ShootsClass(round(FinalBossX.x), round((FinalBossX.y + FinalBossX.height // 2)+15), 9, (255, 255, 153), facing,"BossShot")
                # how many bullets can be at the same time
                if len(LaserShoots) < staticsVars.BossBullets:
                    if (staticsVars.setSounds == True):
                        laserSound.play()

                    if (FinalBossX.right == True):
                        LaserShoots.append(b1x)

                    else:
                        LaserShoots.append(b2x)
                # to take affects from boss shots
                HitByShots(LaserShoots)

    def printHeadShotOnScreen():
        # print first
        staticsVars.win.blit(staticsVars.RenderdText,(staticsVars.text_x,staticsVars.text_y))
        # then to hide it # (make it none again)
        for e in py.event.get():
            if e.type == hide_HS_event:  # is called after a head shot : '200' milliseconds
                staticsVars.win = None

    # framesRefreshing
    def redrawGameFrames():
        # InEvery frame background will fill again to avoid tkrar el sour ell btthrk

        list_of_enemies =[Aku_aku,Shreder,bada,xFighter]
        checkLevelandSetThings(list_of_enemies)
              # making a surface from the str by using render ,
        scoreText = font.render('Score: ' + str(staticsVars.score), 1, (250, 0, 0))
        HighLights = font_small.render('Coins : ' + str(staticsVars.coins_get)+' | Killed: ' + str(staticsVars.enemies_killed), 1, (203, 180, 10))
        level_window.blit(scoreText, (10, 10))
        level_window.blit(HighLights, (10, 55))

        Shreder.drawEnemy(level_window)
        xFighter.drawEnemy(level_window)
        Catcher.drawMovingObj(level_window, 4, "catcher")
        Aku_aku.drawEnemy(level_window)
        bada.drawEnemy(level_window)
        FlyBomb.drawEnemy(level_window,"fly")
        Carpet2.drawMovingObj(level_window, 2)

        theHero.drawtheHero(level_window)
        Player2.drawtheHero(level_window)
        MovingBox.drawMovingObj(level_window,1,"up-down")







        treasure.drawTreasure(level_window)
        Gate1.drawGate(level_window)
        Gate1.drawKey(level_window)
        icons().drawIcon()


        block1.drawBlock(level_window)
        btn.draw(level_window)



        # drawing the bullet u shoot , in framesP.S
        for bullet in bullets:
            {bullet.drawObject(level_window)}

        # drawing the bullet u shoot , in framesP.S
        for laserShot in LaserShoots:
            {laserShot.drawObject(level_window)}

        #(10) I made this with this way  : cuz 1st : Enemy_hit is not a drawable fun in my case , second if I put the blit in (bullet collison area)
        # the Background of level would be drawn after the collison so textRendered would be hidden . but here its drawn before this ->
        if(staticsVars.win != None):
            # the if statement cuz before shooting the head , the win static variable by default is a type of non .(not a window var)
            printHeadShotOnScreen()

        Player2.x, Player2.y,Player2.walkCount,Player2.standing, Player2.left,Player2.right,Player2.isShooting = parse_data(send_data())


        py.display.update()


    # ---------------------------------------------------
    # Main Loop " Here is calling functions and whatever "
    # ---------------------------------------------------
    net = Network()
    def send_data():
        """
        Send position to server
        :return: None
        """
        # why int(theHero.y) ? cuz jumping will format it to float ,
        # and here in Parse_data where splitting the text so if its not as usual (int) it will make exception

        # changes the bools to int , cuz when its a string bool() will think "False" or any text ".." = True but only "" (empty) is False
        # but when change 0 and 1 to bool() , everything is correct
        data = str(net.id) + ":" + str(theHero.x) + "," + str(int(theHero.y)) + "," + str(theHero.walkCount) + "," + str(int(theHero.standing)) + "," + str(int(theHero.left)) + "," + str(int(theHero.right)) + "," + str(int(theHero.isShooting))
        reply = net.send(data)
        # print(reply)
        return reply

    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            # x , y , walkcount,isStanding,Left,Right,isShooting
            print(d)

            return int(d[0]), int(d[1]), int(d[2]), bool(int(d[3])), bool(int(d[4])), bool(int(d[5])), bool(int(d[6]))
        except:
            return 1200,0,0,False,False,False,False


    theHero = player(80, screen_height-100 , 64, 64,staticsVars.player_name)
    Player2 = player(200, screen_height-100 , 64, 64,"Local Multiplayer Friend")



    class Titles_Static():
        FinalStage = ""
        SecondStage = ""

    FinalBossX = FinalBoss("The Boss",187,284)
    Aku_aku = enemy("Aku aku",300, screen_height-85 , 64, 64, 600)
    Shreder = enemy("Shreder",0, screen_height-120 , 64, 64, 520)
    bada = enemy("Bx Anymo",520, screen_height-80 , 64, 64, 800)
    xFighter = enemy("x Fighter",700, screen_height-110 , 64, 64, 1100)
    FlyBomb = enemy("Fly Bomb",0,100,64,64,1000)
    enemyWhoHitP = enemy()


    coin1 = coin(700, screen_height-250 )
    coin2 = coin(600, screen_height-125 )
    coin3 = coin(100, screen_height-400 )
    coin4 = coin(400, screen_height-300 )
    coin5 = coin(900, screen_height-270 )
    coin6 = coin()
    coin7 = coin()
    coin8 = coin()
    coin9 = coin()
    coin10 = coin()
    coin11 = coin()
    coin12 = coin()

    shield = Addon(1240,50,"shield")

    x_key = randint(50, int(screen_width/3))
    y_key = randint(int(screen_height/2), int(screen_height-60))
    Gate1 = Gate(1120,screen_height-200,x_key,y_key)

    xtrea = randint(0, screen_width-50)
    ytrea = randint((screen_height/2), screen_height-50)

    treasure = hide_treasure(xtrea,ytrea)

    flyinGround = GroundsToStand()
    sando = GroundsToStand()
    cause4 = GroundsToStand()
    cause5 = GroundsToStand()
    cause6 = GroundsToStand()
    cause7 = GroundsToStand()
    cause8 = GroundsToStand()
    cause9 = GroundsToStand()
    cause10 = GroundsToStand()

    MovingBox = MovingObject(1170,100,85,36,550)
    MovingCP = MovingObject(900,160,85,36,1200)
    Carpet2 = MovingObject(450,300,85,36,1200)
    Slider = MovingObject(840,screen_height-70,200,50)
    Catcher = MovingObject(600,screen_height-100,50,50)

    block1 = Block(350,screen_height-140)

    toSeparateBetweenShots = 0
    bullets = []
    LaserShoots = []
    run = True
    while run:

        # events from mouse , like pressing on sth , so on
        for event in py.event.get():
            # press on X to close
            if event.type == py.QUIT:
                savingStatistics()
                run = False



            pos = py.mouse.get_pos();

            # its for soundsSet btn now
            if (btn.isOver(pos)):
                btn.color = (250,250,153)
                if event.type == py.MOUSEBUTTONDOWN:
                        btn.color = (2,55,250)
                        print("u just clicked the button")
                        if(staticsVars.setSounds == False):
                            btn.text = "Disable Sounds"
                            staticsVars.setSounds = True
                        elif(staticsVars.setSounds == True) :
                            staticsVars.setSounds = False
                            btn.text = "Enable Sounds"
            else :
                btn.color = (0,255,0)
                # print(pos)



        if not (staticsVars.Finished):
        # speed of the game
            clock.tick(27)
            if (staticsVars.level_reached == 2 and Titles_Static.SecondStage == ""):
                Titles_Static.SecondStage = "We are in"
                if(staticsVars.setSounds):
                    Stage2.play()

            if(staticsVars.level_reached==3 and Titles_Static.FinalStage == ""):
                Titles_Static.FinalStage="We are in"
                if(staticsVars.setSounds):
                    Stage3.play()
                level_window.fill((0,0,0))
                font2x = py.font.SysFont('comicsans', 100)
                font1x = py.font.SysFont('comicsans', 50)

                text = font2x.render('Welcome to the Final Stage', 1,
                                    (255, 0, 0), (0, 0, 0))
                text2 = font1x.render('Your almost to the End, U just need to pass throug the gate, Easy huh ??',1,(255,255,255))
                text3 = font1x.render('be patient, 1st You need to find a [Hidden KEY] ,',1,(255,255,255))
                text4 = font1x.render(' but watch ur steps THE FINAL BOSS is waiting for you ',1,(255,255,255))
                text5 = font2x.render('Are You Ready? , Good luck ',1,(255,255,0))


                level_window.blit(text, (600 - (text.get_width() / 2), 60))
                level_window.blit(text2, (30, 180))
                level_window.blit(text3, (200, 240))
                level_window.blit(text4, (160, 300))
                level_window.blit(text5, (600 - (text.get_width() / 2), 400))

                py.display.update()

                i = 0
                while i < 200:
                    py.time.delay(50)
                    i += 1
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            i = 201
                            savingStatistics()
                            py.quit()

            if(staticsVars.FinalBossisDead and not(staticsVars.greetsDone) ):
                staticsVars.greetsDone = True
                if(staticsVars.setSounds):
                    # BackGround Music stop
                    py.mixer.music.stop()

                font1 = py.font.SysFont('comicsans', 60)
                text = font1.render('♥ Cheers , Final Boss has been defeated , Great Work ♥', 1, (255, 0, 0),(0,0,0))
                text2 = font1.render('Have You Found The Hidden Key yet ?! ', 1, (0, 0, 0),(255,255,255))

                level_window.blit(text, (600 - (text.get_width() / 2), 150))
                level_window.blit(text2, (600 - (text2.get_width() / 2), 250))
                py.display.update()
                i = 0
                while i < 200:
                    py.time.delay(20)
                    i += 1
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            i = 201
                            savingStatistics()
                            py.quit()


            list_of_all_peds = [theHero,Aku_aku, Shreder, bada, xFighter, FlyBomb, FinalBossX]
            HelloMousePointer(pos, list_of_all_peds)

            list_of_Grounds = [cause7,flyinGround,sando,cause4,cause5,cause6,block1,cause8,cause9,cause10,MovingCP,Slider]
            CollisionWithObjects(list_of_Grounds)

            PlatformBounds([MovingBox,Carpet2])

            list_of_enemies =[Aku_aku,Shreder,bada,xFighter,FlyBomb,FinalBossX]
            HitByEnemy(list_of_enemies)

            list_of_coins = [coin1,coin2,coin3,coin4,coin5,coin6,coin7,coin8,coin9,coin10,coin11,coin12,shield]
            TouchCoinAndPickitUP(list_of_coins)

            MovewithObject([MovingBox, MovingCP, Slider , Catcher,Carpet2], list_of_enemies)



            FindTreasure([treasure])
            FindGate([Gate1])

            if toSeparateBetweenShots > 0:
                toSeparateBetweenShots += 1
            if toSeparateBetweenShots > 2:
                toSeparateBetweenShots = 0

            # Kill ememies with your bullets :D , yeah kill them
            for enemyx in list_of_enemies :
                for bullet in bullets:
                    # collison between bullet and enemy
                    if bullet.y - bullet.radius < enemyx.hitbox[1] + enemyx.hitbox[3] and bullet.y + bullet.radius > enemyx.hitbox[
                        1]:
                        if bullet.x + bullet.radius > enemyx.hitbox[0] and bullet.x - bullet.radius < enemyx.hitbox[0] + \
                                enemyx.hitbox[2]:

                            if enemyx.dead == False :
                                enemyx.Enemy_hit()
                                staticsVars.score += 1
                                # HeadShots :D
                                if(bullet.y<(enemyx.hitbox[1]+enemyx.hitbox[3]/2)):
                                    enemyx.health -=1
                                    print("You just shot his Head")
                                    fontx = py.font.SysFont('comicsans', 20)
                                    Bonus = fontx.render('- 2 [HeadShot] ', 1, (250, 0, 0), (0, 0, 0))
                                           # (10) why this ?
                                    # level_window.blit(Bonus, (enemyx.x, enemyx.y - 50))
                                    staticsVars.win = level_window
                                    staticsVars.RenderdText = Bonus
                                    staticsVars.text_x = enemyx.x
                                    staticsVars.text_y = enemyx.y-50
                                    # to hide the [headshot label] after a 200 ms
                                    py.time.set_timer(hide_HS_event, 200)

                                    # to make al rasasa disapeear when hit him
                                bullets.pop(bullets.index(bullet))
                    # Shoot ur self haha
                    if bullet.y - bullet.radius < theHero.hitbox[1] + theHero.hitbox[3] and bullet.y + bullet.radius > \
                            theHero.hitbox[1]:
                        if bullet.x + bullet.radius > theHero.hitbox[0] and bullet.x - bullet.radius < theHero.hitbox[0] + \
                                theHero.hitbox[2]:
                            if (staticsVars.ActivateShield == False):
                                theHero.hitPl("By Yourself")
                                staticsVars.score -= 2
                                print("You just shot ur self")
                                bullets.pop(bullets.index(bullet))

            for bullet in bullets:
                # how to move al- rasasa and finsih its path
                    if bullet.x < screen_width and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))


            for laser_shot in LaserShoots:
                    if laser_shot.x < screen_width and laser_shot.x > 0:
                        laser_shot.x += laser_shot.vel
                    else:
                        LaserShoots.pop(LaserShoots.index(laser_shot))

            keys = py.key.get_pressed()
            if keys[py.K_z]:
                if keys[py.K_x]:
                    if keys[py.K_c]:
                        if(staticsVars.ActivateShield==False):
                            print("Cheat Activated , You Won't Die now ")
                            staticsVars.ActivateShield = True
                        else :
                            print("Cheat Deactivated, you are not invincible anymore ")
                            staticsVars.ActivateShield = False

            if keys[py.K_x] and staticsVars.GateOpened :
                savingStatistics()
                py.quit()
            if keys[py.K_ESCAPE] :
                savingStatistics()
                py.quit()
            # give our event a name
            RESET_EVENT = py.USEREVENT + 1
            # space button to shoot the Rasasaaat
            if (keys[py.K_SPACE] or keys[py.K_RCTRL]) and toSeparateBetweenShots == 0:

                theHero.isShooting = True
                py.time.set_timer(RESET_EVENT, 100)


                if theHero.left:
                    facing = -1
                else:
                    facing = 1
                # this bullet is going out from the right side
                b1 = ShootsClass(round(theHero.x + theHero.width), round(theHero.y + theHero.height // 2), 6, (250, 0, 0),
                                facing)
                # from the left side
                b2 = ShootsClass(round(theHero.x), round(theHero.y + theHero.height // 2), 6,(250, 0, 0), facing)
                # how many bullets can be at the same time
                if len(bullets) < staticsVars.SetBulletsSameTime:
                    if (staticsVars.setSounds == True):
                        if(staticsVars.EasyToKill==False):
                            bulletSound.play()
                        else :
                            bulletSound2.play()


                    if (theHero.right == True):
                        bullets.append(b1)

                    else :
                        bullets.append(b2)


                toSeparateBetweenShots = 1
            else :
                for e in py.event.get():
                    if e.type == RESET_EVENT:
                        theHero.isShooting = False


            if keys[py.K_LEFT] or keys[py.K_a]:
                theHero.x -= theHero.vel
                theHero.left = True
                theHero.right = False
                theHero.standing = False
                if theHero.x < theHero.vel:
                    theHero.x = screen_width
            elif keys[py.K_RIGHT] or keys[py.K_d]:
                theHero.x += theHero.vel
                theHero.right = True
                theHero.left = False
                theHero.standing = False
                if theHero.x > screen_width - theHero.width - theHero.vel:
                    theHero.x = theHero.vel
            else:
                theHero.standing = True
                theHero.walkCount = 0
            # jumping
            if (theHero.isJump == False) :
                if (keys[py.K_UP] or keys[py.K_w]):
                    if(staticsVars.setSounds):
                        jumpSound.play()
                    theHero.isJump = True
                    theHero.right = False
                    theHero.left = False
                    theHero.walkCount = 0
            else:

                if theHero.jumpCount >= -staticsVars.setJumpingLev:

                    neg = 1
                    if theHero.jumpCount < 0 :
                        neg = -1
                    # print((theHero.jumpCount ** 2) * 0.5 * neg ) //sth here look carefully
                    theHero.y -= (theHero.jumpCount ** 2) * 0.5 * neg
                    if(theHero.y < (screen_height - theHero.height-40) and (staticsVars.IwasHere==False)):
                        theHero.y += 3
                    theHero.jumpCount -= 1
                    if (neg == -1 and theHero.y > (screen_height - theHero.height-40) ):
                        theHero.y -=8
                        theHero.isJump = False
                        theHero.jumpCount = staticsVars.setJumpingLev
                        print("Reached The Ground ")
                        if(staticsVars.endthis == True):
                            neg = 1
                            theHero.jumpCount = staticsVars.setJumpingLev
                            staticsVars.IwasHere = None
                            # theHero.isJump = False




                else:
                    theHero.isJump = False
                    theHero.jumpCount = staticsVars.setJumpingLev
                #     fix jumping send data




            redrawGameFrames()


    py.quit()
#########################################################################################
# print("This Game devloped by Yahia Droubi - 2016 - , NO Engines , NO Pre-implementations Funcs")
################################################
####         ##          ##    ######
####          ##        ##    ##     #
####           ##     ##     ##      ##
####            ##  ##      ##      ##
####             ####      ##      ##
####             ###      ##    ##
####             ###     #######
####             ###
####             ###
#################################################
