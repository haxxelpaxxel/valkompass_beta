from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequestKeyError
import sys

app = Flask(__name__)

# Dictionary för att lagra partiernas positioner på varje fråga
party_positions = {
    'Socialdemokraterna': [2, 2, 2, 1, 2, 2, 2, 1, 1, 2],
    'Moderaterna': [3, 1, 1, 3, 1, 2, 3, 2, 2, 2],
    'Sverigedemokraterna': [3, 2, 3, 2, 3, 3, 2, 3, 2, 1],
    'Centerpartiet': [1, 1, 1, 2, 1, 1, 2, 2, 2, 2],
    'Vänsterpartiet': [2, 3, 2, 1, 3, 3, 1, 3, 3, 3],
    'Kristdemokraterna': [2, 2, 2, 2, 1, 1, 2, 1, 1, 1],
    'Liberalerna': [2, 1, 2, 2, 1, 1, 2, 1, 1, 2],
    'Miljöpartiet': [1, 3, 3, 1, 2, 3, 1, 3, 3, 3],
    # Lägg till andra partier och deras positioner här
}

# Funktion för att beräkna totalpoäng och avgöra vilket parti som är närmast
def calculate_closest_party(answers):
    closest_party = None
    min_distance = float('inf')

    for party, positions in party_positions.items():
        # Undvik None-värden och konvertera till strängar
        party_answers = [str(answer) for answer in answers]
        distance = sum(abs(int(answer) - position) for answer, position in zip(party_answers, positions))
        if distance < min_distance:
            min_distance = distance
            closest_party = party

    return closest_party

@app.route('/')
def index():
    # Frågor och svarsalternativ
    questions = {
        'question1': {
            'text': 'Bör Sverige öka eller minska subventionerna till jordbruket?',
            'options': {
                'Öka subventionerna': 1,
                'Behålla på nuvarande nivå': 2,
                'Minska subventionerna': 3,
            }
        },
        'question2': {
            'text': 'Hur ser du på användningen av genmodifierade organismer (GMO) inom svensk lantbruk?',
            'options': {
                'Positivt, bör främjas': 1,
                'Neutral, behöver mer information': 2,
                'Negativt, bör begränsas': 3,
            }
        },
        'question3': {
            'text': 'Vad anser du om skogsbrukets påverkan på biologisk mångfald?',
            'options': {
                'Positivt, det gynnar biologisk mångfald': 1,
                'Neutral, behöver mer information': 2,
                'Negativt, det skadar biologisk mångfald': 3,
            }
        },
        'question4': {
            'text': 'Hur viktigt anser du det är att främja ekologiskt jordbruk för att minska användningen av bekämpningsmedel och konstgödsel?',
            'options': {
                'Mycket viktigt': 1,
                'Ganska viktigt': 2,
                'Inte viktigt alls': 3,
            }
        },
        'question5': {
            'text': 'Bör Sverige öka användningen av förnybar energi inom lantbruket?',
            'options': {
                'Ja, kraftigt öka användningen': 1,
                'Ja, öka användningen': 2,
                'Nej, behålla nuvarande nivå': 3,
            }
        },
        'question6': {
            'text': 'Vad anser du om importen av livsmedel och dess påverkan på svensk livsmedelsproduktion?',
            'options': {
                'Positivt, det berikar utbudet': 1,
                'Neutral, behöver mer information': 2,
                'Negativt, det hotar svensk livsmedelsproduktion': 3,
            }
        },
        'question7': {
            'text': 'Hur ser du på användningen av antibiotika inom animalieproduktionen?',
            'options': {
                'Positivt, det är nödvändigt för att säkra djurhälsan': 1,
                'Neutral, behöver mer information': 2,
                'Negativt, det ökar risken för resistens': 3,
            }
        },
        'question8': {
            'text': 'Bör Sverige tillåta odling av genmodifierade grödor?',
            'options': {
                'Ja, utan restriktioner': 1,
                'Ja, med vissa restriktioner': 2,
                'Nej, det bör förbjudas': 3,
            }
        },
        'question9': {
            'text': 'Hur viktigt anser du att främja lokalproducerade livsmedel för att minska klimatpåverkan?',
            'options': {
                'Mycket viktigt': 1,
                'Ganska viktigt': 2,
                'Inte viktigt alls': 3,
            }
        },
        'question10': {
            'text': 'Vad anser du om användningen av konstgödsel inom jordbruket?',
            'options': {
                'Positivt, det ökar avkastningen': 1,
                'Neutral, behöver mer information': 2,
                'Negativt, det leder till övergödning': 3,
            }
        },
    }

    return render_template('index.html', questions=questions)

@app.route('/calculate_results', methods=['POST'])
def calculate_results():
    try:
        # Hämta svarsalternativen från dolda fält i POST-förfrågan
        answers = [request.form.get(f'question{i}','No answer') for i in range(1, 11)]

	# Skriv ut svaren för att felsöka
        print("Received answers:", answers)

        # Om svaret är 'No answer', använd ett defaultvärde, t.ex. 0
        party_answers = [0 if answer == 'No answer' else int(answer) for answer in answers]

        # Beräkna vilket parti som är närmast användarens åsikter
        closest_party = calculate_closest_party(party_answers)

        return render_template('results.html', closest_party=closest_party)

    except BadRequestKeyError as e:
        # Hantera felet när nyckeln inte finns i POST-förfrågan
        error_message = f"BadRequestKeyError: {str(e)}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
