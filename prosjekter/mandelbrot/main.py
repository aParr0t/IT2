import functools
import time

import numpy as np
import pygame
import pygame.locals
from pygame import mouse
from pygame.math import Vector2


def timeit(func):
    """Decorator for timing function execution time. Taken from: https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk

    Args:
        func (function): The function to time

    Returns:
        function: The function wrapped with the timer-decorator
    """
    
    @functools.wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

class Mandelbrot:
    bounding_box_ratio = 2.47 / 2.24
    start_bounding_box = [-2.00, -1.12, 0.47, 1.12]
    
    def __init__(self, *, resolution, max_iterations=100):
        self.resolution = resolution
        self.max_iterations = max_iterations
        # colors taken from: https://stackoverflow.com/a/16505538/15598055
        self.colors = np.array([
            (66, 30, 15),
            (25, 7, 26),
            (9, 1, 47),
            (4, 4, 73),
            (0, 7, 100),
            (12, 44, 138),
            (24, 82, 177),
            (57, 125, 209),
            (134, 181, 229),
            (211, 236, 248),
            (241, 233, 191),
            (248, 201, 95),
            (255, 170, 0),
            (204, 128, 0),
            (153, 87, 0),
            (106, 52, 3)
            ]
        )

    @timeit
    def render(self, region: np.ndarray):
        """Calculates the colors of the mandelbrot set in the given region of the complex plane.
        Original implementation: https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings.
        Enhanced with chatGPT: https://chat.openai.com/share/afd58fce-a285-44d1-a868-1d3ff769f62b

        Args:
            region (List | Tuple): Region of the complex plane to calculate the mandelbrot set. A region defined by top_left corner a + ib and bottom-right corner c + id, would be [a, b, c, d]

        Returns:
            numpy.Array: An array filled with the computed colors (r, g, b)
        """
        resolution_w, resolution_h = self.resolution

        colors = np.empty((resolution_w, resolution_h, 3), dtype=np.uint8)

        x, y = np.meshgrid(np.linspace(region[0], region[2], resolution_w), np.linspace(region[1], region[3], resolution_h))
        c = x + 1j * y
        c = c.transpose()  # had to fix this myself
        z = np.zeros_like(c, dtype=np.complex128)
        mask = np.ones(c.shape, dtype=bool)
        iteration = np.zeros(c.shape, dtype=np.uint16)
        
        for i in range(self.max_iterations):
            z[mask] = z[mask] * z[mask] + c[mask]
            mask = np.logical_and(mask, np.abs(z) < 4)
            iteration += mask.astype(np.uint16)
    
        colors = self._color(iteration)
        return colors

    def _color(self, iterations):
        colors = np.zeros(iterations.shape + (3,), dtype=np.uint8)
        non_escape = np.logical_and(iterations > 0, iterations < self.max_iterations)
        colors[non_escape] = np.array(self.colors)[iterations[non_escape] % 16]
        return colors


class FloatRect:
    def __init__(self, x, y, width, height):
        self._center = (x + width/2, y + height/2)
        self.x, self.y = x, y
        self.width, self.height = width, height
                
    def coords(self):
        return (self.x, self.y, self.x+self.width, self.y+self.height)

    def scale_in_place(self, scalar):
        nw, nh = self.width*scalar, self.height * scalar
        dw, dh = nw - self.width, nh - self.height
        self.x += dw/2
        self.y += dh/2
        self.width, self.height = nw, nh

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value
        self.x = self.center[0]-self.width/2
        self.y = self.center[1]-self.height/2
    
    def move_relative(self, other: tuple|list):
        self.center = (self.center[0]+other[0], self.center[1]+other[1])

class MandelbrotViewer:
    def __init__(self):
        self.mandelbrot = Mandelbrot(resolution=SCREEN_SIZE, max_iterations=100)
        b = Mandelbrot.start_bounding_box
        self.region = FloatRect(b[0], b[1], b[2]-b[0], b[3]-b[1])
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.view_offset = Vector2(0, 0)
        self.render()
    

    def render(self):
        self.frame = self.mandelbrot.render(self.region.coords())
        pygame.surfarray.blit_array(self.surface, self.frame)
        self.view_offset = (0, 0)
    
    def blit(self, target_surface: pygame.Surface):
        # print(self.view_offset)
        target_surface.blit(self.surface, self.view_offset)

    def _scale_to_region(self, vector: list | tuple):
        return ((vector[0] / SCREEN_SIZE[0]) * self.region.width, (vector[1] / SCREEN_SIZE[1]) * self.region.height)

    def _screen_pos_to_region(self, pos: tuple|list):
        scaled = self._scale_to_region(pos)
        return (self.region.x + scaled[0], self.region.y + scaled[1])

    def _zoom(self, scalar):
        new_center = self._screen_pos_to_region(mouse.get_pos())
        self.region.scale_in_place(scalar)
        self.region.center = new_center
        self.render()

    def zoom_in(self):
        self._zoom(0.5)

    def zoom_out(self):
        self._zoom(1.5)
    
    def pan(self, offset):
        self.view_offset += Vector2(offset)
        self.region.move_relative(self._scale_to_region(offset))


SCREEN_SIZE = [600, 400]

mandelbrot_viewer = MandelbrotViewer()

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.locals.DOUBLEBUF)
screen.set_alpha(None)

running = True
mouse_is_down = False
is_panning = False
pan_offset = (0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_is_down = True
            mouse.get_rel()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_is_down = False
            if not is_panning:
                if event.button == pygame.locals.BUTTON_LEFT:
                    mandelbrot_viewer.zoom_in()
                elif event.button == pygame.locals.BUTTON_RIGHT:
                    mandelbrot_viewer.zoom_out()
            is_panning = False
        if event.type == pygame.MOUSEMOTION:
            if mouse_is_down:
                is_panning = True
                pan_offset = mouse.get_rel()
                mandelbrot_viewer.pan(pan_offset)

    screen.fill((0, 0, 0))
    mandelbrot_viewer.blit(screen)

    pygame.display.flip()

pygame.quit()