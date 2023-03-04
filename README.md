# 4160-P1

## Game Image

![game image](https://i.imgur.com/MATf1Gk.png)

## Program Versions

- OS Versions: Windows, Linux, Mac
- Python Version: Python 3.10
- Pygame Version: 2.1.2

## Motivation

I wanted to make something visually appealing with incredibly simple game mechanics.
Google's offline dinosaur game particularly inspired me since it's such a simple game, yet you can play it for quite some time!

## Reasoning

The way I have the engine structured, it uses object-oriented programming ideologies (which happen to be my favorite).

## Image

#### Entity Package Diagram
![entity diagram](https://i.imgur.com/BhtOUHS.jpeg)

#### Events Package Diagram
![events diagram](https://i.imgur.com/gcsiNTT.png)

#### Window Package Diagram
![window diagram](https://i.imgur.com/B6kKPFL.png)

#### Game Package Diagram
![game diagram](https://i.imgur.com/0W8E6yT.png)

## Future Work

Enhancements that can be made:
- Better integrated classes. For example, the difference between `Resolutions` and `Resolution` is that `Resolutions` is just an enum of `Resolution`s, but have compatibility issues.
- Better event handling. My main game code is a tad messy.
- Pymunk is listed as a requirement, even though the dependency is not used in this game.

Generalizations:
With my engine, possible genre(s) of games that could be made include, but are not limited to:
- Run-N-Gun
- 2D Platformer
- RPG
- _...and many more!_
