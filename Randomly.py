import sys
import pygame
import random


class RandomPixels:  # RandomPixels class: Initialise pygame and display, colours, background, pixel, speed, text, cursor, input variables, etc.
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.HALF_SCREEN_HEIGHT = self.screen_height // 2  # Vertical position for user input field
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

        self.GREY = (100, 114, 129)  # Initial/starting colour
        self.WHITE = (255, 255, 255)  # Moving pixel colour
        self.BLACK = (0, 0, 0)  # Background colour
        self.RED = (255, 0, 0)  # Warning colour
        self.current_colour = self.GREY

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BLACK)

        self.pixels = []
        self.speed = 0.4
        self.SPEED_MINIMUM = 0.1
        self.SPEED_MAXIMUM = 100.0
        self.SPEED_MULTIPLIER_DIVISOR = 1.1
        self.SPACING_FACTOR = 3  # Pixel overcrowding prevention at start area
        self.move_accumulator = 0.0  # Track partial movement
        self.key_repeat_delay = 0  # Control held keys repeat (lower = faster repeats)

        self.TITLE ="RANDOMLY"
        self.font = pygame.font.Font(None, 36)
        self.TITLE_CENTRE = (self.screen_width - self.font.size(self.TITLE)[0]) // 2  # True centre for title
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        self.cursor_timer = 0
        self.cursor_visible = True
        self.CURSOR_BLINK = 500  # Milliseconds

        self.active_input = True
        self.awaiting_input = False
        self.first_input_number = ''
        self.second_input_size = ''
        self.current_input = ''
        self.pixel_warning_number = ""
        self.pixel_warning_size = ""

    
    def run(self):  # Main loop which handles user inputs, instructions, pixel and display updates
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.active_input:
                        self.handle_input(event)
                    else:
                        self.handle_controls(event)

            if self.active_input:
                self.update_cursor_blink()
                self.display_instructions_and_input()
            elif not self.paused:
                self.update_and_draw_pixels()
                if self.background_filled():
                    self.running = False

            pygame.display.flip()
            self.clock.tick(40)  # 40 FPS limit

        pygame.quit()


    def render_text(self, text, x, y, color=None):  # Render and draw text
        text_surface = self.font.render(text, True, color or self.WHITE)
        self.screen.blit(text_surface, (x, y))


    def update_cursor_blink(self):  # Cursor blinking
        self.cursor_timer += self.clock.get_time()
        if self.cursor_timer >= self.CURSOR_BLINK:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0


    def display_instructions_and_input(self):  # Display instructions, inputs, warnings
        self.screen.fill(self.BLACK)
        self.render_text(self.TITLE, self.TITLE_CENTRE, 1, self.GREY)  # Display name of program

        instructions = [
            "ESC: Exit from program",
            "UP/DOWN: Change speed of moving pixels",
            "LEFT/RIGHT: Change colour of moving pixels",
            "SPACE: Pause/Resume"
        ]
        for i in range(len(instructions)):
            self.render_text(instructions[i], 50, 100 + i * 30)

        first_display_value = self.first_input_number if self.awaiting_input else self.current_input
        first_cursor = "_" if self.cursor_visible and not self.awaiting_input else ""
        self.render_text(f"Enter the number of pixels: {first_display_value}{first_cursor}", 50, self.HALF_SCREEN_HEIGHT)

        next_prompt_height = self.HALF_SCREEN_HEIGHT + (80 if self.pixel_warning_number else 40)
        if self.pixel_warning_number:
                self.render_text(self.pixel_warning_number, 50, self.HALF_SCREEN_HEIGHT + 40, self.RED)
            
        if self.awaiting_input:
            second_cursor = "_" if self.cursor_visible else ""
            self.render_text(f"Enter the pixel size: {self.current_input}{second_cursor}", 50, next_prompt_height)
            if self.pixel_warning_size:
                self.render_text(self.pixel_warning_size, 50, next_prompt_height + 40, self.RED)


    def handle_input(self, event):  # User input handling
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            if not self.awaiting_input:
                try:
                    self.pixel_number = abs(int(self.current_input))
                    self.first_input_number = self.current_input
                    self.current_input = ''
                    self.awaiting_input = True
                except ValueError:
                    self.current_input = ''
            else:
                try:
                    self.pixel_size = abs(int(self.current_input))
                    self.second_input_size = self.current_input
                    self.current_input = ''
                    self.active_input = False
                    self.start_area()
                except ValueError:
                    self.current_input = ''

        elif event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input += event.unicode
        self.update_input_warnings()


    def update_input_warnings(self):  # Real-time threshold checks during input, and warning display
        try:
            value = int(self.current_input) if self.current_input else 0
            if not self.awaiting_input:
                self.pixel_warning_number = "Warning: Above 1000 pixels expect performance degradation!" if value > 1000 else ""
            else:
                self.pixel_warning_size = "Warning: Above 50 pixel size the program might end suddenly!" if value > 50 else ""
        except ValueError:
            if not self.awaiting_input:
                self.pixel_warning_number = ""
            else:
                self.pixel_warning_size = ""


    def start_area(self):  # Calculate start area and positions for pixels
        grid_size = int(self.pixel_number ** 0.5)
        spacing = self.pixel_size * self.SPACING_FACTOR
        start_x = (self.screen_width - (grid_size * spacing)) // 2
        start_y = (self.screen_height - (grid_size * spacing)) // 2

        if (start_x < 0 or start_y < 0 or
            (start_x + grid_size * spacing) > self.screen_width or
            (start_y + grid_size * spacing) > self.screen_height):  # Check and exit if start area exceeds the screen size
            print(f"Fatal error: {self.pixel_number} pixels of size {self.pixel_size} do not fit on the screen!")
            sys.exit(1)

        for i in range(self.pixel_number):
            x = start_x + (i % grid_size) * spacing
            y = start_y + (i // grid_size) * spacing
            self.pixels.append((x, y))


    def move_pixel(self, current_x, current_y, pixel_size):  # Move pixel randomly based on size within fullscreen
        move_x, move_y = random.choice([(-pixel_size, 0), (pixel_size, 0), (0, -pixel_size), (0, pixel_size)])
        new_x = max(0, min(self.screen_width - pixel_size, current_x + move_x))
        new_y = max(0, min(self.screen_height - pixel_size, current_y + move_y))
        return new_x, new_y


    def move_all_pixels(self, moves):  # Move pixels, draw trails and bounce
        for _ in range(moves):
            for i in range(len(self.pixels)):
                x, y = self.pixels[i]
                new_x, new_y = self.move_pixel(x, y, self.pixel_size)
                self.draw_trail(x, y, new_x, new_y, self.pixel_size, self.current_colour)
                self.pixels[i] = (new_x, new_y)
            self.collision_and_bounce()


    def draw_trail(self, start_x, start_y, end_x, end_y, pixel_size, colour):  # Draw continuous trail between start and end positions
        trail_x = end_x - start_x
        trail_y = end_y - start_y
        steps = max(abs(trail_x // pixel_size), abs(trail_y // pixel_size))
        if steps == 0:
            return
        
        for step in range(steps + 1):
            x = start_x + (trail_x * step) // steps
            y = start_y + (trail_y * step) // steps
            self.background.fill(colour, (x, y, pixel_size, pixel_size))

    
    def update_and_draw_pixels(self):  # Update moving pixels and draw their trails (multiple moves allowed per frame at higher speeds)
        self.move_accumulator += self.speed
        moves = int(self.move_accumulator)
        
        if moves > 0:
            self.move_accumulator -= moves
            self.move_all_pixels(moves)
        self.handle_speed_keys()
        self.screen.blit(self.background, (0, 0))

        for x, y in self.pixels:
            self.screen.fill(self.WHITE, (x, y, self.pixel_size, self.pixel_size))
        self.render_text(self.TITLE, self.TITLE_CENTRE, 1, self.current_colour)  # Keep name of program during runnning


    def collision_and_bounce(self):  # Check pixel collisions and change direction randomly
        pixel_rectangles = [pygame.Rect(x, y, self.pixel_size, self.pixel_size) for x, y in self.pixels]
        for i in range(len(self.pixels)):
            for j in range(i + 1, len(self.pixels)):
                if pixel_rectangles[i].colliderect(pixel_rectangles[j]):
                    self.pixels[i] = self.move_pixel(*self.pixels[i], self.pixel_size)
                    self.pixels[j] = self.move_pixel(*self.pixels[j], self.pixel_size)


    def background_filled(self):  # Check for remaining black background pixels
        pixel_array = pygame.surfarray.array3d(self.screen)  # Get direct pixel data as a NumPy array (much faster than screen.get_at)
        black_color = (self.BLACK[0], self.BLACK[1], self.BLACK[2])    # Ensure black is a tuple like (0, 0, 0), so it matches the 3D NumPy array
        return not (pixel_array == black_color).all(axis=-1).any()  # Check for any black pixels


    def handle_speed_keys(self):  # Handle key delay, press and hold for speed
        if self.key_repeat_delay > 0:
            self.key_repeat_delay -= 1
        elif pygame.key.get_pressed()[pygame.K_UP]:
                self.adjust_speed(increase=True)
                self.key_repeat_delay = 4  # 4 is just a bit longer (in ms) than the average key press duration at 40 FPS
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.adjust_speed(increase=False)
                self.key_repeat_delay = 4  # Lower values = faster repeats


    def handle_controls(self, event):  # Control key actions during running (speed, colour changes and pause)
        if event.key == pygame.K_UP:
            self.adjust_speed(increase=True)
        elif event.key == pygame.K_DOWN:
            self.adjust_speed(increase=False)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            self.current_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused


    def adjust_speed(self, increase=True):  # Increase and decrease pixel speed
        if increase:
            self.speed = min(self.SPEED_MAXIMUM, self.speed * self.SPEED_MULTIPLIER_DIVISOR)  # Multiplicative increase
        else:
            self.speed = max(self.SPEED_MINIMUM, self.speed / self.SPEED_MULTIPLIER_DIVISOR)   # Multiplicative decrease
    

def main():  # Create instance of RandomPixels class and runs the app
    try:
        randomly = RandomPixels()
        randomly.run()
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        pygame.quit()


if __name__ == "__main__":
    main()
