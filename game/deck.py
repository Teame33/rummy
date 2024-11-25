import random
from .card import Card

class Deck:
    """A deck of playing cards"""
    
    def __init__(self):
        self.cards = []
        self._create_deck()
        self.shuffle()
    
    def _create_deck(self):
        """Create a standard deck with two jokers"""
        # Standard cards
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(rank, suit))
        
        # Add two jokers
        self.cards.append(Card('Joker', '★', True))
        self.cards.append(Card('Joker', '★', True))
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def draw(self):
        """Draw a card from the deck"""
        if not self.cards:
            return None
        return self.cards.pop()
    
    def add_card(self, card):
        """Add a card to the deck"""
        self.cards.append(card)
    
    def is_empty(self):
        """Check if deck is empty"""
        return len(self.cards) == 0
    
    def remaining(self):
        """Get number of remaining cards"""
        return len(self.cards)
