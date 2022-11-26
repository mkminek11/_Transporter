from random import choice
import pyglet

class Tile:
    def __init__(self, texture, pattern:str="GGGG"):
        self.pattern = pattern
        self.bg = pyglet.sprite.Sprite(texture, batch=Grid.batch, group=Grid.bg)
        self.fg = pyglet.sprite.Sprite(Grid.buildings[2], batch=Grid.batch, group=Grid.fg)
        self.have_fg = False

    def move(self, x:int=0, y:int=0, scale:float=1.0):
        self.bg.x = x
        self.bg.y = y
        self.bg.scale = scale
        self.bg.visible = True
        self.fg.x = x
        self.fg.y = y
        self.fg.scale = scale
    
    def hide(self):
        self.bg.visible = False
        self.fg.visible = False

    def set_fg(self, tex):
        self.fg.image = tex
        self.fg.visible = True
        self.have_fg = True

    def show_fg(self):
        if self.have_fg:
            self.fg.visible = True

class Grid:
    g = []
    batch = pyglet.graphics.Batch()
    bg = pyglet.graphics.OrderedGroup(0)
    fg = pyglet.graphics.OrderedGroup(1)
    tex = pyglet.image.ImageGrid(pyglet.image.load("ground.png"), 5, 5)
    buildings = pyglet.image.ImageGrid(pyglet.image.load("buildings.png"), 1, 3)
    tiles = ["WWWW", "WGWW", "WGGW", "GGGW", "GGGG", "WWWW", "GWWW", "GGWW", "GGWG", "GGGG", "WWWW", "WWWG", "GWWG", "GWGG", "GGGG", "WWWW", "WWGW", "WWGG", "WGGG", "GGGG", "GGGG", "GGGG", "GGGG", "GGGG", "GGGG"]

    def __init__(self, width:int=3, height:int=4):
        Grid.g = [[Tile(Grid.tex[4]) for _ in range(width)] for _ in range(height)]
        self._generate()
        self._place_base()
        self.scale = 1
        self.x = 0
        self.y = 0
    
    def _generate(self):
        for rn, row in enumerate(Grid.g):
            for cn, cell in enumerate(row):
                self.random(cn, rn)

    def _place_base(self):
        gggg = []
        for rn, row in enumerate(Grid.g):
            for cn, cell in enumerate(row):
                if cell.pattern == "GGGG":
                    gggg.append([Grid.g[rn][cn], rn, cn])
        c:list[Tile, int, int] = choice(gggg)
        c[0].set_fg(Grid.buildings[0])
        print(c[1], c[2])
        # c[0].bg.image = Grid.buildings[0]

    def draw(self, width, height):
        sc = 64*self.scale
        for rn, row in enumerate(Grid.g):
            for cn, cell in enumerate(row):
                x = self.x+cn*sc
                y = self.y+rn*sc
                if not x > width and not y > height and not x+sc < 0 and not y+sc < 0:
                    cell.hide()
                    cell.move(x, y, self.scale)
                    cell.show_fg()
                else:
                    cell.hide()
        Grid.batch.draw()

    def _place(self, texture, pattern:str="GGGG", x:int=0, y:int=0):
        g = Grid.g[y][x]
        g.pattern = pattern
        g.bg.image = texture

    def random(self, x:int=0, y:int=0):
        available = Grid.tiles[:]
        tiles = Grid.tiles[:]
        if x > 0:
            sx = Grid.g[y][x-1].pattern
            for a in tiles:
                if a[0] == sx[1] and a[3] == sx[2]:
                    pass
                else:
                    available.remove(a)
        tiles = available[:]
        if y > 0:
            sy = Grid.g[y-1][x].pattern
            for a in tiles:
                if a[2] == sy[1] and a[3] == sy[0]:
                    pass
                else:
                    available.remove(a)
        r = choice(available)
        self._place(Grid.tex[Grid.tiles.index(r)], r, x, y)

    def set_scale(self, scale:float=1.0, mouse_x:int=0, mouse_y:int=0):
        if scale <= 0.1 or scale >= 3:
            return
        gw = len(Grid.g[0])
        gh = len(Grid.g)

        w1 = mouse_x-self.x
        w = 64*self.scale*gw
        wn = 64*scale*gw

        h1 = mouse_y-self.y
        h = 64*self.scale*gh
        hn = 64*scale*gh

        self.x = mouse_x - (w1/w * wn)
        self.y = mouse_y - (h1/h * hn)
        self.scale = scale
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy