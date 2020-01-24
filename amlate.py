#!/usr/bin/env python3
# cuz sometimes ppl are late
# proudly written in vim

import json
import pendulum
import configparser
import dateutil.parser as date_parser
from etnawrapper import EtnaWrapper


def handle_date():
    """Deal with date."""
    today = pendulum.now()
    start_day = today.start_of('day')
    end_day = today.end_of('day')

    start = str(start_day).split('T')[0]
    end = str(end_day).split('T')[0]

    real_start = date_parser.parse(start)
    real_end = date_parser.parse(end)

    return real_start, real_end


def setup_api():
    ini = configparser.ConfigParser()
    ini.read('config.ini')

    etna_id = ini['ETNA']['etna_id']
    etna_passwd = ini['ETNA']['etna_password']
    creds = EtnaWrapper(login=etna_id, password=etna_passwd)

    return creds


def main():
    w = setup_api()
    start, end = handle_date()
    js_data = json.loads(json.dumps(w.get_events(start_date=start, end_date=end)))
    content = {
           "tags":[
               "pedago",
               "suivi",
               "retard"
           ],
           "users": [],
           "title": "Retard",
           "message": "Bonjour,\nJe vais etre en retard\n Cordialement."
    }

    for i in range(0, len(js_data)):
        # if there is an activity named seminaire
        # then create ticket
        if js_data[i]['activity_name'] != "Séminaire":
            w.open_ticket(content)
            print("ticket created")
            break


if __name__ == '__main__':
    main()
