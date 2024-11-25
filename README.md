# Eritrean Rummy Web Game

An interactive web-based implementation of Eritrean Rummy (14-card variant) where you can play against a computer opponent.

## Setup

1. Install Python 3.x
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

## Game Rules

- Each player gets 14 cards
- Goal: Form valid sets and runs with all your cards
- Valid combinations:
  - Set: 3-4 cards of the same rank (e.g., three 7s)
  - Run: 3+ consecutive cards of the same suit (e.g., 4♠,5♠,6♠)
- Jokers can substitute for any card
- On your turn:
  1. Draw a card (from deck or discard pile)
  2. Discard one card
- First player to form valid combinations with all cards wins

## Features

- Interactive web interface
- Computer opponent AI
- Real-time game updates
- Visual card representation
- Automatic valid move detection
