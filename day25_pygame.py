from __future__ import annotations
from pathlib import Path
from typing import NamedTuple, Tuple
import pygame 
import os 
import argparse 
import time


class Point(NamedTuple):
    x: int
    y: int 

class CucumberMap:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.map_item : dict[Point, str] = {}
        self.num_steps = 0
        self.movement = False
        self.tiles = { '.': Tile(0, (160,160,220)), 
                       'v': Tile(8, (220,160,160), 'v'),
                       '>': Tile(8, (160,220,160), '>') }
    
    def get_neighbors(self, p : Point) -> Tuple[Point, Point]:
        p_h = Point(p.x, (p.y + 1) % self.cols)
        p_v = Point((p.x + 1) % self.rows, p.y)
        return p_h, p_v 

    def is_free(self, p : Point) -> bool:
        return self.map_item[p] == "."

    def move(self, p1 : Point, p2 : Point) -> None:
        """move from p1 to p2; p1 gets free"""
        self.map_item[p2] = self.map_item[p1]
        self.map_item[p1] = "."

    def step(self, view) -> None:
        # first reset
        view.win.fill((0, 0, 0))
        move_store : list[tuple[Point, Point]]= []
        self.movement = False 
        for p in self.map_item.keys():
            p_h, _ = self.get_neighbors(p)
            if self.map_item[p] == ">" and self.is_free(p_h):
                # print(p, p_h)
                move_store.append((p, p_h))
        
        if len(move_store): self.movement = True 
        while move_store: 
            self.move(*move_store.pop())
        
        if self.movement: self.print_map(view)

        for p in self.map_item.keys():
            _, p_v = self.get_neighbors(p)
            if self.map_item[p] == "v" and self.is_free(p_v):
                move_store.append((p, p_v))

        if len(move_store): self.movement = True 
        while move_store: self.move(*move_store.pop())

        if self.movement:
            self.print_map(view)

        self.num_steps += 1
        
    @classmethod
    def parse(cls, inp : str) -> CucumberMap:
        cmap = cls()
        cmap.rows = len(inp.split("\n"))
        cmap.cols = len(inp.split("\n")[0])
        
        for ridx, line in enumerate(inp.split("\n")):
            for cidx, s in enumerate(line):
                    cmap.map_item[Point(ridx, cidx)] = s 

        return cmap 

    def print_map(self, view):
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                p = Point(ridx, cidx)
                # print(self.map_item[p].rjust(2), end = "")
                pos = (10 + p.x * 7 + p.y * 7, 540 - p.x * 4 + p.y * 4)
                self.tiles[self.map_item[p]].blit(view.win, pos)
            # print("")

class View:
    def __init__(self, W : int = 1920, H : int = 1080, FPS : int = 60) -> None:
        self.width = W
        self.height = H 
        self.fps = FPS
        self.save = False 
        self.frame_cnt = 0
        self.tmp_path = ""

    def setup(self, title = "advent"):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.font = pygame.freetype.SysFont("Courier", 14) # font and fontsize
        self.font.origin = True 
        self.clock = pygame.time.Clock()
        self.win.fill((0, 0, 0)) # when you win -- fill the screen with black

    def record(self, output_path): # whats the point of this function - to start off the directory
        self.save = True 
        self.output_path = output_path
        self.tmp_path = Path(output_path).parent
        for f in self.tmp_path.glob("frame_*.jpg"):
            os.remove(f)
        print("recording video to: ", self.output_path)
    
    def render(self, controller):
        for object in controller.objects:
            object.step(self)
            if not object.movement: self.finish()
        
        pygame.display.update()
        self.clock.tick(self.fps) # tick by 30fps

        if controller.animate:
            self.frame_cnt += 1
            if self.save:
                pygame.image.save(self.win, self.tmp_path / f"frame_{self.frame_cnt}.jpg")

    def finish(self):
        if not self.save:
            return 
        print("saving video now...")
        import ffmpeg
        snaps = "{}/frame_*.jpg".format(str(self.tmp_path.name))
        print(snaps)
        ffmpeg.input(snaps, pattern_type = "glob", framerate = self.fps).output(self.output_path).run()
        print("clean up snaps")
        for f in self.tmp_path.glob("frame_*.jpg"):
            os.remove(f)

class Controller:
    def __init__(self, start_anim = True) -> None:
        self.animate = start_anim
        self.quit = False 
        self.objects = []
        self.clickables = []
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--rec", help = "record movie", action = "store_true")
        parser.add_argument("-f", "--fps", help = "fix fps", type = int)
        self.args = parser.parse_args()

    def add(self, object, clickable = False):
        self.objects.append(object)
        if clickable:
            self.clickables.append(object)

    def run(self, view):
        if self.args.rec:
            view.record(Path.cwd() / "videosaoc/aocvideo.mp4")
        if self.args.fps:
            view.fps= self.args.fps
        pygame.event.clear()
        start = time.time()
        fcnt = 0
        while not self.quit:
            view.render(self)
            fcnt += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True 
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_SPACE:
                        self.animate = not self.animate # what
                    if event.key == pygame.K_ESCAPE:
                        self.quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for obj in self.clickables:
                        obj.click(pos, True) # click an object by intersecting mouse location and obj locaiton
                if event.type == pygame.MOUSEBUTTONUP:
                    pos= pygame.mouse.get_pos()
                    for obj in self.clickables:
                        obj.click(pos, False)
            delta = time.time() - start 
            if delta >= 3:
                print(f"FPS: {fcnt / delta}") # WHY THO
                fcnt = 0
                start = time.time()

        pygame.quit()
        view.finish()


class Tile:
    def __init__(self, height, color, chr = None):
        self.height = height
        self.color = color
        self.chr = chr
        self.size = 3
        self.tmp = pygame.Surface((16, self.height + 8), pygame.SRCALPHA)
        self.tmp.fill((0, 0, 0, 0))
        self.render(self.tmp, (0, 4))

    def render(self, surface, pos):
        (x, y0) = pos
        y1 = y0 + self.height
        B = self.size

        col2 = (255, 255, 255)
        pygame.draw.polygon(surface, self.color, [(x, y0), (x + B*2, y0 - B), (x + B*4, y0),
                                                  (x + B*2, y0 + B)])
        pygame.draw.polygon(surface, col2, [(x, y0), (x + B*2, y0 - B), (x + B*4, y0),
                                            (x + B*2, y0 + B)], 1)
        col3 = (80, 80, 80)
        col4 = (40, 40, 40)
        #if self.chr == '>':
        #    pygame.draw.line(surface,col3,(x+6,y0+2),(x+10,y0-2))
        #elif self.chr == 'v':
        #    pygame.draw.line(surface,col3,(x+8,y0-2),(x+8,y0+2))
        pygame.draw.polygon(surface, col4, [(x, y0), (x + B*2, y0 + B), (x + B*4, y0), (x + B*4, y1),
                                            (x + B*2, y1 + B), (x, y1)])
        pygame.draw.line(surface, col3, (x, y0), (x, y1))
        pygame.draw.line(surface, col3, (x + B*2, y0 + B), (x + B*2, y1 + B))
        pygame.draw.line(surface, col3, (x + B*4, y0), (x + B*4, y1))

    def blit(self, surface, pos):
        (x, y) = pos
        surface.blit(self.tmp, (x, y - self.height))

def read_inp(inp : str, controller, view) -> int:
    cm = CucumberMap.parse(inp)
    controller.add(cm)
    controller.run(view)

    return cm.num_steps

if __name__ == "__main__":
    # pass
    datfile = Path("day25.txt").read_text()

    view= View()
    view.setup("Day 25")
    controller = Controller()
    read_inp(datfile, controller, view)