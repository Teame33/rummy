from .deck import Deck
from .card import Card

class RummyGame:
    """Eritrean Rummy game logic"""
    
    def __init__(self):
        self.deck = Deck()
        self.discard_pile = []
        self.player1_hand = []
        self.player2_hand = []
        self.current_turn = 'player1'
        self.game_over = False
        self.winner = None
        self._deal_initial_cards()
    
    def _deal_initial_cards(self):
        """Deal 14 cards to each player"""
        for _ in range(14):
            self.player1_hand.append(self.deck.draw())
            self.player2_hand.append(self.deck.draw())
        # Start discard pile
        self.discard_pile.append(self.deck.draw())
    
    def player_draw(self, source='deck', player='player1'):
        """Player draws a card from deck or discard pile"""
        if self.current_turn != player or self.game_over:
            return False
            
        if source == 'deck' and not self.deck.is_empty():
            if player == 'player1':
                self.player1_hand.append(self.deck.draw())
            else:
                self.player2_hand.append(self.deck.draw())
            return True
        elif source == 'discard' and self.discard_pile:
            if player == 'player1':
                self.player1_hand.append(self.discard_pile.pop())
            else:
                self.player2_hand.append(self.discard_pile.pop())
            return True
        return False
    
    def player_discard(self, card_index, player='player1'):
        """Player discards a card"""
        if self.current_turn != player or self.game_over:
            return False
            
        hand = self.player1_hand if player == 'player1' else self.player2_hand
        if 0 <= card_index < len(hand):
            card = hand.pop(card_index)
            self.discard_pile.append(card)
            # Switch turns
            self.current_turn = 'player2' if player == 'player1' else 'player1'
            self._check_winner()
            return True
        return False
    
    def _check_winner(self):
        """Check if there's a winner"""
        if not self.player1_hand:
            self.game_over = True
            self.winner = 'player1'
        elif not self.player2_hand:
            self.game_over = True
            self.winner = 'player2'
    
    def get_state(self):
        """Get current game state"""
        return {
            'player1_hand': [card.to_dict() for card in self.player1_hand],
            'player2_hand': [card.to_dict() for card in self.player2_hand],
            'discard_pile_top': self.discard_pile[-1].to_dict() if self.discard_pile else None,
            'deck_remaining': self.deck.remaining(),
            'current_turn': self.current_turn,
            'game_over': self.game_over,
            'winner': self.winner
        }
