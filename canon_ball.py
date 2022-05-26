import time

import pygame

from dataclasses import dataclass

"""
    Canon-ball simulation code by dp4tea,2022
    Inspired by Matthias Müller - Ten Minute Physics
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    

"""


@dataclass
class Velocity:
    x: float
    y: float

    def invert_x(self):
        self.x *= -1

    def invert_y(self):
        self.y *= -1


class Ball:
    def __init__(self, x: int, y: int, radius:int, velocity: Velocity):
        self.x = x
        self.y = y

        self.radius = radius
        self.velocity = velocity

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)


class MainSimulation:
    def __init__(self, resolution, target_tps):
        self.running = False
        self.ball = Ball(0, 600, 10, Velocity(10, -20))
        self.resolution = resolution
        self.target_tps = target_tps

    def start_simulation(self):
        pygame.init()
        delta_t = 1 / self.target_tps

        screen = pygame.display.set_mode(self.resolution)
        screen.fill((255, 255, 255))
        self.running = True
        while self.running:
            self.simulate(delta_t)
            self.draw(screen)
            self.check_events()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

    def draw(self, screen) -> None:
        screen.fill((255, 255, 255))
        self.ball.draw(screen)
        pygame.display.update()

    def simulate(self, delta_t) -> None:
        n = 20  # sub-steps
        for i in range(n):
            self.ball.x += self.ball.velocity.x * delta_t / n

            self.ball.velocity.y += 9.8 * delta_t / n  #
            self.ball.y = self.ball.y + self.ball.velocity.y * delta_t / n
        # print(self.ball.y)
        if self.ball.x <= 0 or self.ball.x >= self.resolution[0]:
            self.ball.velocity.invert_x()
        if self.ball.y <= 0 or self.ball.y >= self.resolution[1]:
            self.ball.velocity.invert_y()


a = MainSimulation((800, 800), 60)
a.start_simulation()
