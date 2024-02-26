# Taboo Online Game

Welcome to the Taboo Online Game project! This project aims to recreate the classic Taboo game experience in a digital 
format using the Python programming language and the Pygame library. Now you can enjoy playing Taboo with your friends 
online, anytime and anywhere.

## Overview

The Taboo Online Game is a multiplayer adaptation of the popular Taboo board game. Players can create and join virtual 
rooms to play the game with their friends over the internet. The project consists of both server-side and client-side code. 
The server manages different rooms and facilitates communication between players, while the client provides the game 
interface for players to interact with.

## Key Features

- Multiplayer Support: Players can connect and play with their friends online in real-time.
- Room Management: The server allows players to create, join, and manage different game rooms with customizable settings.
- Socket-based Communication: All communication between the server and clients is handled using socket connections,
  ensuring efficient and reliable data exchange.
- Word Pool: The game includes a comprehensive word pool sourced from an SQL database on the server. Words are dynamically
  distributed to players during gameplay, ensuring fairness and variety.
- Privacy: Players only receive words relevant to their team, maintaining the secrecy of the game and enabling a fair
  playing field.

## How to Play

1. **Setup**: Make sure Python and Pygame are installed on your system.
2. **Server Initialization**: Start the server script to create a central hub for game rooms.
3. **Room Creation**: Players can create or join existing rooms from the client interface.
4. **Gameplay**: Once in a room, players are divided into teams and take turns guessing words while avoiding taboo terms.
5. **Scoring**: The server tracks scores and manages the game flow, ensuring a smooth and enjoyable experience.
6. **Victory**: The game ends when a team reaches the designated score limit, and the winning team is declared.

## Requirements

- Python 3.x
- Pygame library
- SQL database for word storage

## Contributions

Contributions to this project are welcome! Whether you want to add new features, fix bugs, or improve documentation, feel free to fork this repository and submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE), allowing for modification and distribution under certain conditions. See the LICENSE file for more details.
