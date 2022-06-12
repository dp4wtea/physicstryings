
from vector import Vector2d
import pygame

from dataclasses import dataclass
from random import randint

""" Billiard simulation code by dp4tea,2022 
    Inspired by Matthias Müller - Ten Minute Physics 
The above copyright 
notice and this permission notice shall be included in all copies or substantial portions of the Software. THE 
SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE. 
    
"""


class Ball:
    def __init__(self, x: int, y: int, radius, velocity: Vector2d, mass: float):
        self.pos = Vector2d(x, y)
        self.mass = mass
        self.radius = radius
        self.velocity = velocity.clone()  # velocity now just vector2d :)
        self.color = (randint(50, 255), randint(1, 255), randint(1, 255))

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)

    def simulate(self, delta_t, gravity):
        n = 20
        sdt = delta_t / n
        for i in range(n):
            self.velocity += gravity.scale_to_new_vector(sdt)
            self.pos += self.velocity.scale_to_new_vector(sdt)


@dataclass
class PhysicScene:
    gravity: Vector2d
    worldSize: Vector2d
    balls: list[Ball]
    dt: float = 0.016666666666666666  # 1/60 seconds
    restitution: float = 1

    def add_ball(self, ball: Ball):
        self.balls.append(ball)


class MainSimulation:
    def __init__(self, resolution):

        self.running = False
        self.resolution = resolution
        self.physics_scene = PhysicScene(Vector2d(0, 0), Vector2d(0, 0), self.generate_starting_balls(10))

    def generate_starting_balls(self, number_of_balls: int) -> list[Ball]:
        result = []
        for i in range(number_of_balls):
            radius = randint(29, 40)
            x = randint(radius, self.resolution[0] - radius)
            y = randint(radius, self.resolution[0] - radius)

            result.append(Ball(x, y, radius, Vector2d(randint(1, 10), randint(1, 10)), radius**2 * 3))
        return result

    def start_simulation(self):
        pygame.init()
        # delta_t = 1 / self.target_tps

        screen = pygame.display.set_mode(self.resolution)
        screen.fill((255, 255, 255))
        self.running = True
        while self.running:
            self.simulate()
            self.draw(screen)
            self.check_events()
            # print(self.calculate_sum_energy())

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

    def draw(self, screen) -> None:
        screen.fill((255, 255, 255))  # clear screen
        for obj in self.physics_scene.balls:
            obj.draw(screen)
        pygame.display.update()
        screen.fill((255, 255, 255))

    def handle_balls_collision(self, ball1: Ball, ball2: Ball):
        vect_btw_balls = ball1.pos - ball2.pos  # vector from one ball pos to other

        distance_between_balls = abs(vect_btw_balls)
        if distance_between_balls == 0 or distance_between_balls > ball1.radius + ball2.radius:  # check collision

            return
        vect_btw_balls.normalize()

        corr = vect_btw_balls.scale_to_new_vector((ball1.radius + ball2.radius - distance_between_balls) / 2)

        ball1.pos += corr
        ball2.pos -= corr

        v1 = ball1.velocity * vect_btw_balls  # v1 projection on vect_btw_balls(float)
        v2 = ball2.velocity * vect_btw_balls  # v2 projection on vect_btw_balls(float)
        m1 = ball1.mass
        m2 = ball2.mass
        new_v1 = (m1 * v1 + m2 * v2 - m2 * (v1 - v2) * self.physics_scene.restitution) / (m1 + m2)
        new_v2 = (m1 * v1 + m2 * v2 - m1 * (v2 - v1) * self.physics_scene.restitution) / (m1 + m2)
        ball1.velocity += vect_btw_balls.scale_to_new_vector(new_v1 - v1)
        ball2.velocity += vect_btw_balls.scale_to_new_vector(new_v2 - v2)

    def handle_wall_collision(self, ball: Ball):

        if ball.pos.x < ball.radius:
            ball.pos.x = ball.radius
            ball.velocity.x *= -1
        elif ball.pos.x > (self.resolution[0] - ball.radius):
            ball.pos.x = self.resolution[0] - ball.radius
            ball.velocity.x *= -1
        if ball.pos.y < ball.radius:
            ball.pos.y = ball.radius
            ball.velocity.y *= -1
        elif ball.pos.y > (self.resolution[1] - ball.radius):
            ball.pos.y = self.resolution[1] - ball.radius
            ball.velocity.y *= -1

    def simulate(self) -> None:

        # we just iterate through all balls and check for collisions
        num_of_balls = len(self.physics_scene.balls)
        for j in range(0, num_of_balls):

            for i in range(j + 1, num_of_balls):
                self.handle_balls_collision(self.physics_scene.balls[i], self.physics_scene.balls[j])
            self.handle_wall_collision(self.physics_scene.balls[j])
            self.physics_scene.balls[j].simulate(self.physics_scene.dt, self.physics_scene.gravity)


a = MainSimulation((800, 800))
a.start_simulation()
