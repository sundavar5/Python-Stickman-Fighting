
import math

class AnimationState:
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    ATTACK = "attack"

class AnimationController:
    def __init__(self):
        self.state = AnimationState.IDLE
        self.timer = 0

    def update(self, dt):
        self.timer += dt

    def get_offsets(self, state, timer):
        # Return offsets for limbs relative to body
        # Format: (left_arm_angle, right_arm_angle, left_leg_angle, right_leg_angle)
        # Angles in degrees? Or just arbitrary offsets? Let's do limb end offsets for now or angles.
        # Let's do simple procedural angles.

        if state == AnimationState.IDLE:
            # Breathing effect
            breath = math.sin(timer * 0.005) * 2
            return (0, 0, 0, 0, breath) # Extra val for body bounce

        elif state == AnimationState.RUN:
            speed = 0.02
            arm_swing = math.sin(timer * speed) * 30
            leg_swing = math.cos(timer * speed) * 30
            return (arm_swing, -arm_swing, -leg_swing, leg_swing, 0)

        elif state == AnimationState.JUMP:
            return (-45, -45, 20, 10, 0)

        elif state == AnimationState.ATTACK:
            # Punch animation
            # Right arm punches out
            punch_extend = math.sin(timer * 0.02) * 45 if timer < 150 else 0
            return (-30, 45 + punch_extend, -10, 10, 0)

        return (0, 0, 0, 0, 0)
