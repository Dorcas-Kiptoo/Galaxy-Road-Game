# Galaxy Road Game

## Description
**Galaxy Road Game** is an interactive Python game built using Pygame. Navigate a sphere through a galaxy-themed road while avoiding skull obstacles. The game features a dynamic background, immersive audio effects, and a visually engaging experience with a gradual day-night cycle.

## Features
- Galaxy-themed background with star animations.
- Dynamic obstacles (skulls) that spawn in three lanes.
- Explosion effect when the player collides with an obstacle.
- Background music and sound effects for an immersive experience.
- Scoring system to track the player's progress.

## Gameplay
Use the arrow keys to control the sphere:
- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **Up Arrow**: Move up
- **Down Arrow**: Move down

**Objective**: Avoid the skull obstacles appearing in random lanes.  
The game ends when the sphere collides with an obstacle, triggering an explosion and a "Game Over" screen. The score is displayed in the top-left corner and increases with each obstacle successfully dodged.

## Installation

### Prerequisites
- Python 3.x
- Pygame library

### Steps
1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/Dorcas-Kiptoo/Galaxy-Road-Game.git
   cd galaxy-road-game
   ```
2. **Install Pygame**:
   ```bash
   pip install pygame
   ```
3. **Place Required Files**:
   - Add `skull.png` in the project directory for the obstacle image.
   - Add `music.mp3` as your background music in the project directory.
   - Add `explosion.wav` as the explosion sound effect in the project directory.
   - Add `game_over.mp3` as thw game over sound effect

## How to Run
Execute the game script using Python:
```bash
python galaxy_road_game.py
```

## File Structure
```
galaxy-road-game/
├── galaxy_road_game.py            # Main game script
├── skull.png                      # Skull image for obstacles
├── music.mp3                      # Background music file
└── Monster battle_audio_explosion.wav # Explosion sound effect
|__ game_over.mp3 #Game over sound effect
```

## Customization

### Change Obstacle Image
- Replace `skull.png` with any desired image. Ensure it's scaled properly (e.g., `60x40` pixels).
   ```python
   skull_image = pygame.image.load("your_image.png")
   ```

### Modify Background Music
- Change the `music.mp3` file to any other music of your choice:
   ```python
   background_music = "path/to/your_music.mp3"
   ```

### Adjust Difficulty
- Increase or decrease the obstacle speed for harder or easier gameplay:
   ```python
   obstacle_speed = 5  # Adjust this value
   ```

## Dependencies
- **Pygame**: The game is built using Pygame, a cross-platform library designed to create multimedia applications like games.

## Troubleshooting

### Common Issues
1. **FileNotFoundError**:
   - Ensure `skull.png`, `music.mp3`, `game_over.mp3` and `explosion.wav` are in the correct directory.

2. **No Audio Playback**:
   - Verify that the audio files are correctly referenced with their full or relative paths.
   - Initialize Pygame's mixer correctly:
     ```python
     pygame.mixer.init()
     ```

3. **Performance Issues**:
   - Close unnecessary applications to free up system resources.
   - Lower the screen resolution if needed or reduce the number of stars in `star_positions`.

## Credits
- **Pygame**: A Python library used for creating the game environment.
- **Icons8 & Flaticon**: Used for sourcing skull icons for the obstacle images.
- **Audio Resources**: Background music and sound effects obtained from free sound libraries.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


