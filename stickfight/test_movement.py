
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman

def test_movement():
    player = Stickman(100, 600)

    # Test Move Right
    player.move(1)
    player.update()
    if player.velocity.x <= 0:
        print("FAIL: Player not moving right")
        sys.exit(1)

    print("Player moving right OK")

    # Test Move Left
    player.velocity.x = 0
    player.move(-1)
    player.update()
    if player.velocity.x >= 0:
        print("FAIL: Player not moving left")
        sys.exit(1)

    print("Player moving left OK")

    # Test Jump
    player.on_ground = True
    player.jump()
    if player.velocity.y >= 0:
        print("FAIL: Player did not jump")
        sys.exit(1)

    print("Player jump OK")
    print("Input/Movement tests passed")

if __name__ == "__main__":
    test_movement()
