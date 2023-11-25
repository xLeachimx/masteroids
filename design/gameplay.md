# Gameplay Design

## Primary Mechanics:

---

### Pending:
- The Player will be able to fire a pellet which will travel from the front of their ship
- The Player will complete a level when no asteroids are left
- The Player will continue to be presented levels until the Player loses
- The Player will have 3 lives
- The Player will have their lives replenished each level
- The Player will lose a life and be reset to the start position if an asteroid collides with them
- The Player will lose the game when they have no lives remaining
- Player pellets will despawn when they hit the edge of the screen
- Player pellets will despawn when they hit an asteroid
- When a pellet collides with an asteroid that asteroid will split such that:
  - A large asteroid becomes 4 medium asteroids
  - A medium asteroid becomes 2 small asteroids
  - A small asteroid becomes nothing
- When a pellet collides with an asteroid the Player's score will be updated by:
  - 1,000 points if it was large asteroid
  - 100 points if it was a medium asteroid
  - 10 points if it was a small asteroid
- A leaderboard of the top 10 player runs will be kept
- The player may add their name to the leaderboard if they would rank in the top 10

### Completed:
- The Player will start with a total of 0 points
- The Player will be represented by an isosceles triangle
- The Player will be able to rotate their craft clockwise or counterclockwise
- The Player will be able to move their ship forward
- The Player will be able to stop their ship
- Changes in player velocity will align to a linear acceleration curve
- The Player will be halted when they hit the edge of the screen
- Asteroids will exist in 3 possible size: large, medium, small
- Asteroids will have a constant velocity, randomly determined at spawn
- Asteroids will bounce off of the edges of the screen
- Asteroids shape will be procedurally designed based on a number of sectors
  - Large asteroids have 12 sections 
  - Medium asteroids have 8 sections
  - Small asteroids have 6 sections
- The Player will initially spawn in the center of the screen with the point of the ship facing at 0 degrees on the unit circle.

## Secondary Mechanics

Note: All secondary mechanics replace the primary mechanics they improve, when completed.

---

### Pending:

- The Player will experience screen wrap when hitting the edge of the screen, both vertical and horizontal
- Asteroids will experience screen wrap when hitting the edge of the screen
- Asteroids will bounce off one another if they collide
- Asteroids slowly rotate as they move through space
- The Player and Asteroids are sized relative to the smallest screen dimension

### Completed: