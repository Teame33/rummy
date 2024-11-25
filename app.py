from flask import Flask, jsonify, request, session
from game.rummy_game import RummyGame
from dotenv import load_dotenv
import os
import random
import string
import time
import threading

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Store active games with their codes
games = {}
game_codes = {}

def generate_game_code():
    """Generate a unique 4-letter game code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=4))
        if code not in game_codes:
            return code

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/create-game', methods=['POST'])
def create_game():
    """Create a new game and return its code"""
    game = RummyGame()
    game_id = id(game)
    code = generate_game_code()
    
    games[game_id] = game
    game_codes[code] = game_id
    session['game_id'] = game_id
    
    return jsonify({
        'status': 'success',
        'code': code,
        'state': game.get_state()
    })

@app.route('/join-game', methods=['POST'])
def join_game():
    """Join an existing game using a code"""
    code = request.json.get('code', '').upper()
    print(f"Trying to join game with code: {code}")  # Debug log
    print(f"Available codes: {list(game_codes.keys())}")  # Debug log
    
    if code not in game_codes:
        return jsonify({
            'status': 'error',
            'message': 'Invalid game code'
        }), 404
    
    game_id = game_codes[code]
    session['game_id'] = game_id
    return jsonify({
        'status': 'success',
        'state': games[game_id].get_state()
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/game-state')
def game_state():
    """Get current game state"""
    try:
        game_id = session.get('game_id')
        if not game_id:
            return jsonify({'error': 'No active game session'}), 404
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        return jsonify(games[game_id].get_state())
    except Exception as e:
        print(f"Error in game_state: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/draw-card', methods=['POST'])
def draw_card():
    """Draw a card from deck or discard pile"""
    try:
        game_id = session.get('game_id')
        if not game_id:
            return jsonify({'error': 'No active game session'}), 404
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        source = request.json.get('source', 'deck')
        player = request.json.get('player', 'player1')
        
        if source not in ['deck', 'discard']:
            return jsonify({'error': 'Invalid source'}), 400
        
        game = games[game_id]
        success = game.player_draw(source, player)
        
        if success:
            return jsonify({'status': 'success', 'state': game.get_state()})
        return jsonify({'error': 'Invalid move'}), 400
    except Exception as e:
        print(f"Error in draw_card: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/discard-card', methods=['POST'])
def discard_card():
    """Discard a card"""
    try:
        game_id = session.get('game_id')
        if not game_id:
            return jsonify({'error': 'No active game session'}), 404
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        card_index = request.json.get('card_index')
        player = request.json.get('player', 'player1')
        
        if card_index is None:
            return jsonify({'error': 'No card index provided'}), 400
            
        game = games[game_id]
        success = game.player_discard(card_index, player)
        
        if success:
            return jsonify({'status': 'success', 'state': game.get_state()})
        return jsonify({'error': 'Invalid move'}), 400
    except Exception as e:
        print(f"Error in discard_card: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def cleanup_old_games():
    """Clean up inactive games older than 30 minutes"""
    current_time = time.time()
    inactive_threshold = 30 * 60  # 30 minutes
    
    to_remove = []
    for game_id, game in games.items():
        if not hasattr(game, 'last_activity'):
            game.last_activity = current_time
        elif current_time - game.last_activity > inactive_threshold:
            to_remove.append(game_id)
    
    for game_id in to_remove:
        # Remove from both dictionaries
        code = next((code for code, gid in game_codes.items() if gid == game_id), None)
        if code:
            del game_codes[code]
        del games[game_id]

@app.before_request
def update_game_activity():
    """Update last activity time for the current game"""
    game_id = session.get('game_id')
    if game_id in games:
        games[game_id].last_activity = time.time()

def start_cleanup_scheduler():
    while True:
        time.sleep(300)  # 5 minutes
        cleanup_old_games()

cleanup_thread = threading.Thread(target=start_cleanup_scheduler, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Rummy server on port {port}...")
    app.run(host='0.0.0.0', port=port)
