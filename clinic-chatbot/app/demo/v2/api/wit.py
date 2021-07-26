from .credentials import WIT_TOKEN
import requests


def ask_wit(expression):
    result = requests.get('https://api.wit.ai/message?v=20201116&q={}'.format(expression), headers={'Authorization': WIT_TOKEN})
    jsonResult = result.json()
    try:
        if jsonResult['intents'][0]['name'] == "listDentist":
            a = requests.get('http://127.0.0.1:8080/v2/dentist')
            a = a.json()
            list_dentist = [l['name'] for l in a]

            remove_list = []
            for d in list_dentist:
                a = requests.get('http://127.0.0.1:8086/v2/timeslot?dentist={}'.format(str(d)))
                a = a.json()
                list_timeslots = [l['time'] for l in a]
                if len(list_timeslots) == 0:
                    remove_list.append(d)
            for i in remove_list:
                list_dentist.remove(i)

            dentists = ", ".join(str(x) for x in list_dentist)
            answer = 'Dentists that are available are {}.'.format(dentists)

        elif jsonResult['intents'][0]['name'] == "GetDentistInformation":
            dentist = jsonResult['entities']['wit$search_query:search_query'][0]['value']
            a = requests.get('http://127.0.0.1:8080/v2/dentist/{}'.format(dentist))
            a = a.json()
            answer = '{} is a {} works in {}.'.format(a[0]['name'], a[0]['specialization'], a[0]['location'])

        elif jsonResult['intents'][0]['name'] == "GetTimeslotsForDentist":
            dentist = jsonResult['entities']['wit$search_query:search_query'][0]['value']
            a = requests.get('http://127.0.0.1:8086/v2/timeslot?dentist={}'.format(dentist))
            a = a.json()
            list_timeslots = [(l['time']+':00'+'-'+str(int(l['time'])+1)+':00') for l in a]

            timeslots = ", ".join(x for x in list_timeslots)
            if list_timeslots:
                answer = 'Available timeslots for {} are: {}.'.format(dentist, timeslots)
            else:
                answer = '{} is not available now.'.format(dentist, timeslots)

        elif jsonResult['intents'][0]['name'] == "ReserveTimeslot":
            timeslot = jsonResult['entities']['wit$datetime:datetime'][0]['value'][11:13]
            dentist = jsonResult['entities']['wit$search_query:search_query'][0]['value']

            availablity = requests.get('http://127.0.0.1:8086/v2/timeslot?dentist={}'.format(dentist))
            availablity = availablity.json()
            list_timeslots = [l['time'] for l in availablity]
            if str(int(timeslot)) in list_timeslots:
                requests.patch('http://127.0.0.1:8086/v2/timeslot?dentist={}&time={}'.format(dentist, int(timeslot)))
                time = str(int(timeslot))+':00'+'-'+str(int(timeslot)+1)+':00'
                answer = 'You successfully book timeslot for {} at {} 11/11!'.format(dentist, time)
            else:
                if list_timeslots:
                    time = [(l+':00'+'-'+str(int(l)+1)+':00') for l in list_timeslots]
                    suggest_timeslots = ", ".join(x for x in time)
                    answer = 'Sorry! This timeslot for {} has been reserved. Other available timeslots are {}.'.format(dentist, suggest_timeslots)
                else:
                    answer = 'Sorry! This timeslot for {} has been reserved. No other timeslot available for {}.'.format(dentist, dentist)

        elif jsonResult['intents'][0]['name'] == "CancelAppointment":
            timeslot = jsonResult['entities']['wit$datetime:datetime'][0]['value'][11:13]
            dentist = jsonResult['entities']['wit$search_query:search_query'][0]['value']

            availablity = requests.get('http://127.0.0.1:8086/v2/timeslot?dentist={}'.format(dentist))
            availablity = availablity.json()
            list_timeslots = [l['time'] for l in availablity]
            if str(int(timeslot)) in list_timeslots:
                answer = 'Sorry! Not able to cancel booking since it has not been reserved.'
            else:
                requests.patch('http://127.0.0.1:8086/v2/timeslot?dentist={}&time={}'.format(dentist, int(timeslot)))
                time = str(int(timeslot)) + ':00'
                answer = 'You have successfully canceled reservation with {} at {}!'.format(dentist, time)

    except:
        answer = "I dont understand"
    return answer
