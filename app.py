from flask import Flask, jsonify, request, session
from game.rummy_game import RummyGame
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Store active games
games = {}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/new-game', methods=['POST'])
def new_game():
    """Start a new game"""
    game = RummyGame()
    game_id = id(game)
    games[game_id] = game
    session['game_id'] = game_id
    return jsonify({'status': 'success', 'state': game.get_state()})

@app.route('/game-state')
def game_state():
    """Get current game state"""
    game_id = session.get('game_id')
    if game_id not in games:
        return jsonify({'error': 'No active game'}), 404
    return jsonify(games[game_id].get_state())

@app.route('/draw-card', methods=['POST'])
def draw_card():
    """Draw a card from deck or discard pile"""
    game_id = session.get('game_id')
    if game_id not in games:
        return jsonify({'error': 'No active game'}), 404
    
    source = request.json.get('source', 'deck')
    player = request.json.get('player', 'player1')
    
    game = games[game_id]
    success = game.player_draw(source, player)
    
    if success:
        return jsonify({'status': 'success', 'state': game.get_state()})
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/discard-card', methods=['POST'])
def discard_card():
    """Discard a card"""
    game_id = session.get('game_id')
    if game_id not in games:
        return jsonify({'error': 'No active game'}), 404
    
    card_index = request.json.get('card_index')
    player = request.json.get('player', 'player1')
    
    if card_index is None:
        return jsonify({'error': 'No card index provided'}), 400
        
    game = games[game_id]
    success = game.player_discard(card_index, player)
    
    if success:
        return jsonify({'status': 'success', 'state': game.get_state()})
    return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Rummy server on port {port}...")
    app.run(host='0.0.0.0', port=port)
