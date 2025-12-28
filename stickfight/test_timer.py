
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman

def test_animation_timer():
    stickman = Stickman(100, 100)

    # Simulate 5 frames of 16ms
    for _ in range(5):
        stickman.update(dt=16)

    print(f"Timer: {stickman.animator.timer}")

    # Expected: 5 * 16 = 80
    if stickman.animator.timer != 80:
        print(f"FAIL: Timer should be 80, got {stickman.animator.timer}")
        sys.exit(1)

    print("Animation timer test passed")

if __name__ == "__main__":
    test_animation_timer()
