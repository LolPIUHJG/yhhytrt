key_switch_camera = 'c'
key_switch_mode = 'z'

key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'
key_up = 'e'
key_down = 'g'

key_tyrn_left = 'n'
key_tyrn_right = 'm'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.hero = loader.loadMode('simley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTO(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)    
        base.camera.reparentTO(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.camera = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseIntrefaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTO(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def tyrn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def tyrn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):

        x_from = round(self.hero.detx())
        y_from = round(self.hero.dety())
        z_from = round(self.hero.detz())
         
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)

    def check_dir(self, angle):
        if angle >=0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle =(self.hero.getH()+180) % 360
        self.move_to(angle)
   
    def left(self):
        angle =(self.hero.getH()  + 90) % 360
        self.move_to(angle)

    def right(self):
        angle =(self.hero.getH()+ 270) % 360
        self.move_to(angle)

 
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] +1 
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
    
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.genZ() + 1)

    def down(self):
        if self.mode and self.hero.detZ() > 1:
            self.hero.setZ(self.hero.detZ() - 1)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.detH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.block.land.delBlockFrom(pos)


    def accept_events(self):
        base.accept(key_tyrn_left, self.tyrn_left)
        base.accept(key_tyrn_left + '-repeat', self.tyrn_left)
        base.accept(key_tyrn_right, self.tyrn_right)
        base.accept(key_tyrn_right + '-repeat', self.tyrn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_tyrn_left, self.up)
        base.accept(key_tyrn_left + '-repeat', self.up)
        base.accept(key_tyrn_right, self.down)
        base.accept(key_tyrn_right + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

