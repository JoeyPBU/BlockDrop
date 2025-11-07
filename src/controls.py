import pygame

class Controls:
    """
    Handles input for Drop Block. Only detects player intent and returns actions.
    """

    def __init__(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.axis_x = 0
        self.hat_x = 0
        self.hat_y = 0

        # Continuous move tracking
        self.MOVE_DELAY = 120
        self.last_move_time = {"left": 0, "right": 0, "down": 0}

    def get_actions(self, events):
        """
        Process all events and returns a dict of actions for this frame.

        Returns:
            dict: action booleans, e.g., {"move_left": True, "rotate": False, ...}
        """
        current_time = pygame.time.get_ticks()
        actions = {
            "move_left": False,
            "move_right": False,
            "move_down": False,
            "rotate": False,
            "pause_toggle": False,
            "reset": False,
            "quit": False,
        }

        # --- Process events ---
        for event in events:
            if event.type == pygame.QUIT:
                actions["quit"] = True

            # --- Keyboard ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    actions["pause_toggle"] = True
                elif event.key == pygame.K_r:
                    actions["reset"] = True
                elif event.key == pygame.K_UP:
                    actions["rotate"] = True

            # --- Joystick buttons ---
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in [0, 1, 3]:  # A/B/X = rotate
                    actions["rotate"] = True
                elif event.button == 7:  # + = pause
                    actions["pause_toggle"] = True
                elif event.button == 6:  # - = reset
                    actions["reset"] = True

            # --- Hat (D-pad) ---
            if event.type == pygame.JOYHATMOTION:
                self.hat_x, self.hat_y = event.value

            # --- Joystick axis ---
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.axis_x = event.value if abs(event.value) > 0.5 else 0

        # --- Continuous input handling ---
        keys = pygame.key.get_pressed()

        def can_move(direction):
            return current_time - self.last_move_time[direction] > self.MOVE_DELAY

        # Keyboard
        if keys[pygame.K_LEFT] and can_move("left"):
            actions["move_left"] = True
            self.last_move_time["left"] = current_time
        if keys[pygame.K_RIGHT] and can_move("right"):
            actions["move_right"] = True
            self.last_move_time["right"] = current_time
        if keys[pygame.K_DOWN] and can_move("down"):
            actions["move_down"] = True
            self.last_move_time["down"] = current_time

        # Hat
        if self.hat_x == -1 and can_move("left"):
            actions["move_left"] = True
            self.last_move_time["left"] = current_time
        elif self.hat_x == 1 and can_move("right"):
            actions["move_right"] = True
            self.last_move_time["right"] = current_time
        if self.hat_y == -1 and can_move("down"):
            actions["move_down"] = True
            self.last_move_time["down"] = current_time

        # Joystick
        if self.axis_x < -0.5 and can_move("left"):
            actions["move_left"] = True
            self.last_move_time["left"] = current_time
        elif self.axis_x > 0.5 and can_move("right"):
            actions["move_right"] = True
            self.last_move_time["right"] = current_time

        return actions
