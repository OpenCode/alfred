# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from random import choice


MORNING_QUOTES = [
    'Spero che questa sia una buona giornata!',
    'Perché cadiamo, signore? Per imparare a rimetterci in piedi',
    'Le posso consigliare di portare con sé un sandwich, signore?',
    'I pipistelli saranno notturni ma anche per i miliardari playboy '
    'è tardi alzarsi alle {hour}... '
    'Condurre una doppia vita ha il suo prezzo, temo...'
]

AFTERNOON_QUOTES = [
    'Spero che abbia trascorso una buona mattinata!',
    'Mio caro ragazzo, talvolta è una mera distrazione '
    'leggere tali corbellerie, il più delle volte è una perdita di tempo.',
    'Temo che la dottoressa Meridian sia stata rapita. '
    'Il signorino Dick è scappato. '
    'La caverna è andata distrutta. E... c\'è un altro bug da fixare!'
]

EVENING_QUOTES = [
    'Spero che questa possa ancora essere una buona giornata!',
    'Suo padre aveva ragione; lei è un eroe, io me ne intendo. '
]

NIGHT_QUOTES = [
    'Spero sia stata una buona giornata!',
    'Non dovrebbe essere a letto? Ah, già. Parliamo di lei!',
    'Vada a riposare. Riconosca i suoi limiti!',
]


def say(hour=None):
    if not hour:
        hour = datetime.now().hour
    if 6 <= hour <= 12:
        moment_of_the_day = 'Buongiorno Signorino!'
        quotes = MORNING_QUOTES
    elif 13 <= hour <= 17:
        moment_of_the_day = 'Buon Pomeriggio Signorino!'
        quotes = AFTERNOON_QUOTES
    elif 18 <= hour <= 23:
        moment_of_the_day = 'Buonasera Signorino!'
        quotes = EVENING_QUOTES
    else:
        moment_of_the_day = 'Buonanotte Signorino!'
        quotes = NIGHT_QUOTES
    random_quote = choice(quotes)
    if '{hour}' in random_quote:
        random_quote = random_quote.format(hour=hour)
    return moment_of_the_day, random_quote
