class Card:
    """A playing card"""
    SUITS = ['♥', '♦', '♣', '♠']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, rank, suit, is_joker=False):
        self.rank = rank
        self.suit = suit
        self.is_joker = is_joker
    
    def __str__(self):
        if self.is_joker:
            return '🃏'
        return f'{self.rank}{self.suit}'
    
    def to_dict(self):
        """Convert card to dictionary for JSON serialization"""
        return {
            'rank': self.rank,
            'suit': self.suit,
            'is_joker': self.is_joker,
            'display': str(self),
            'color': 'red' if self.suit in ['♥', '♦'] else 'black'
        }
    
    @staticmethod
    def from_dict(data):
        """Create a card from dictionary data"""
        return Card(data['rank'], data['suit'], data['is_joker'])
