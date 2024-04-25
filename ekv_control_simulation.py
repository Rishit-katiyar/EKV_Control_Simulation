import pygame
import sys
import math

# Define constants
THRUSTER_POWER = 2  # Thruster power in m/s
MAX_SPEED = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ACCELERATION_FACTOR = 0.1
ROTATION_FACTOR = 0.05
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
FONT_SIZE = 20

class EKV:
    def __init__(self):
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.velocity = 0
        self.orientation = 0  # Angle in radians
        self.angular_velocity = 0
        self.thrusters = {'forward': False, 'backward': False}
        self.radius = 20
        self.height = 40
        self.rect = pygame.Rect(self.position[0] - self.radius, self.position[1] - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        # Update velocity based on thrusters
        if self.thrusters['forward']:
            self.velocity = min(self.velocity + ACCELERATION_FACTOR, MAX_SPEED)
        elif self.thrusters['backward']:
            self.velocity = max(self.velocity - ACCELERATION_FACTOR, -MAX_SPEED)
        else:
            self.velocity *= 0.99  # Apply slight friction to slow down when no thrusters are activated

        # Update position based on velocity
        self.position[0] += self.velocity * math.cos(self.orientation)
        self.position[1] -= self.velocity * math.sin(self.orientation)

        # Update orientation based on angular velocity
        self.orientation += self.angular_velocity

        # Update rectangle position
        self.rect.center = (self.position[0], self.position[1])

    def rotate(self, angle):
        self.angular_velocity = angle * ROTATION_FACTOR

    def draw(self, screen):
        # Draw EKV as a cylinder with forward edge in red
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.circle(screen, WHITE, self.position, self.radius)
        forward_edge_end = (self.position[0] + self.radius * math.cos(self.orientation), self.position[1] - self.radius * math.sin(self.orientation))
        pygame.draw.line(screen, RED, self.position, forward_edge_end, 3)  # Draw the forward edge

    def draw_controls(self, screen):
        # Display control instructions on the screen
        font = pygame.font.Font(None, FONT_SIZE)
        controls_text = [
            "Controls:",
            "W/S: Increase/Decrease Speed",
            "A/D: Rotate Left/Right",
        ]
        y_offset = 10
        for text in controls_text:
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, y_offset))
            y_offset += FONT_SIZE + 5

    def handle_boundary_constraints(self):
        # Handle boundary constraints
        if self.position[0] < 0:
            self.position[0] = SCREEN_WIDTH
        elif self.position[0] > SCREEN_WIDTH:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = SCREEN_HEIGHT
        elif self.position[1] > SCREEN_HEIGHT:
            self.position[1] = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    ekv = EKV()

    # Dictionary to map keyboard keys to thruster commands
    key_bindings = {
        pygame.K_w: 'forward',
        pygame.K_s: 'backward',
        pygame.K_a: 'rotate_left',
        pygame.K_d: 'rotate_right',
    }

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Check if the pressed key corresponds to a thruster command
                if event.key in key_bindings:
                    thruster_command = key_bindings[event.key]
                    if thruster_command.startswith('rotate'):
                        # If it's a rotation command, call rotate method with appropriate angle
                        rotation_direction = 1 if thruster_command == 'rotate_right' else -1
                        ekv.rotate(rotation_direction)
                    elif thruster_command == 'forward':
                        ekv.thrusters['forward'] = True
                    elif thruster_command == 'backward':
                        ekv.thrusters['backward'] = True
            elif event.type == pygame.KEYUP:
                if event.key in key_bindings:
                    thruster_command = key_bindings[event.key]
                    if thruster_command.startswith('rotate'):
                        # Stop rotation when key is released
                        ekv.angular_velocity = 0
                    elif thruster_command == 'forward':
                        ekv.thrusters['forward'] = False
                    elif thruster_command == 'backward':
                        ekv.thrusters['backward'] = False

        # Update EKV position and handle constraints
        ekv.update()
        ekv.handle_boundary_constraints()

        # Draw EKV and controls
        ekv.draw(screen)
        ekv.draw_controls(screen)

        # Update display and control frame rate
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

