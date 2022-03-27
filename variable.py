import re

provinces = ['Agrigento', 'Alessandria', 'Ancona', 'Aosta', 'Aquila ', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino',
             'Bari', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano', 'Brescia', 'Brindisi',
             'Cagliari', 'Caltanissetta', 'Campobasso', 'Caserta', 'Catania', 'Catanzaro', 'Chieti', 'Como', 'Cosenza',
             'Cremona', 'Crotone', 'Cuneo', 'Enna', 'Ferrara', 'Firenze', 'Foggia', 'Forli e Cesena', 'Frosinone',
             'Genoa', 'Gorizia', 'Grosseto',
             'Imperia', 'Isernia',
             'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca',
             'Macerata', 'Mantova', 'Massa-Carrara', 'Matera', 'Messina', 'Milan', 'Modena',
             'Naples', 'Novara', 'Nuoro',
             'Oristano',
             'Padua', 'Palermo', 'Parma', 'Pavia', 'Perugia', 'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa',
             'Pistoia', 'Pordenone', 'Potenza', 'Prato',
             'Ragusa', 'Ravenna', 'Reggio Calabria', 'Reggio Emilia', 'Rieti', 'Rimini', 'Rome', 'Rovigo',
             'Salerno', 'Sassari', 'Savona', 'Siena', 'Syracuse', 'Sondrio',
             'Taranto', 'Teramo', 'Terni', 'Turin', 'Trapani', 'Trento', 'Treviso', 'Trieste',
             'Udine',
             'Varese', 'Venice', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo']

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }


msg_suggestion = "Hey, a friend of you thinks you would be amazing in guiding new exciting experencies. " \
               "Check our website www.fantasthike.com and sign up to our service for starting your new adventure!"

msg_signup = " Hey, thanks for signin up to our website. Start hiking now! What do you wait?"