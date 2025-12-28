
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman
from stickfight.src.constants import GRAVITY, GROUND_Y

def test_physics():
    stickman = Stickman(100, 100)

    # Simulate a few frames
    print(f"Initial Y: {stickman.position.y}")

    # Frame 1
    stickman.update()
    print(f"Frame 1 Y: {stickman.position.y}")
    if stickman.velocity.y != GRAVITY:
        print("FAIL: Gravity not applied")
        sys.exit(1)

    # Simulate falling to ground
    for _ in range(100):
        stickman.update()

    print(f"Final Y: {stickman.position.y}")
    if stickman.position.y != GROUND_Y:
        print(f"FAIL: Stickman did not stop at ground {GROUND_Y}, stopped at {stickman.position.y}")
        sys.exit(1)

    print("Physics test passed")

if __name__ == "__main__":
    test_physics()
