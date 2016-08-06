
class CardUtils():
    suit_unicodes = {'spades': '\u2660', 'diamonds': '\u2666', 
                    'clubs': '\u2663', 'hearts': '\u2665'}

    def __init(self):
       self.id = 1 
    
    @classmethod
    def as_unicode(cls, suit):
        return cls.suit_unicodes.get(suit)

