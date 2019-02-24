#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, web

log = None


def main(wf):
    # Get args from Workflow as normalized Unicode
    args = wf.args

    check_settings(wf)

    if len(args):
        if args[0] == 'from' or args[0] == 'to':
            return set_defaults(args)

    fr = wf.settings['defaults']['fr']
    to = wf.settings['defaults']['to']
    amount = 1

    if len(args):
        if args[0].replace('.', '', 1).isdigit():
            amount = float(args[0])
            num_args = 2
        else:
            num_args = 1

        if len(args) >= num_args:
            fr = validate_cur(args[num_args - 1])
        if len(args) == num_args + 1:
            to = [validate_cur(args[num_args])]

        if not fr or not to[0]:
            wait()
            return

    rates = []

    for cur in to:
        rate = get_rate(fr, cur)

        if rate:
            rates.append(rate)

            add_item(amount, fr, amount * rate, cur)
            add_item(amount, cur, amount / rate, fr)

    if len(rates) == 0:
        wait()
        return
    else:
        wf.send_feedback()


def add_item(amount, fr, value, to):
    formatted = '%g' % (value)
    wf.add_item('%g %s = %s %s' % (amount, fr, formatted, to), valid=True,
                subtitle='Press enter to copy to clipboard', copytext=formatted, arg=formatted)


def check_settings(wf):
    if not 'defaults' in wf.settings:
        wf.settings['defaults'] = {'fr': 'USD', 'to': ['EUR']}

    if isinstance(wf.settings['defaults']['to'], basestring):
        wf.settings['defaults']['to'] = [wf.settings['defaults']['to']]


def set_defaults(args):
    cur = validate_cur(args[1])

    if args[0] == 'from' and cur:
        wf.settings['defaults'] = {'fr': cur,
                                   'to': wf.settings['defaults']['to']}
    if args[0] == 'to':
        to = []

        for item in args[1:]:
            cur = validate_cur(item)
            if cur:
                to.append(cur)

        cur = (', ').join(to)

        wf.settings['defaults'] = {
            'fr': wf.settings['defaults']['fr'], 'to': to}

    print(cur)

    return


def wait():
    wf.add_item('Please enter a valid format',
                'cur [amount] [currency code] [currency code]')

    wf.send_feedback()


def get_rate(fr, to):
    data = web.get(
        'http://apilayer.net/api/live?access_key=c938bcf13e0aff152614745f41414ed4&currencies=%s,%s' % (fr, to)).json()

    if data['success']:
        return (1 / data['quotes']['USD%s' % fr]) * data['quotes']['USD%s' % to]
    else:
        return get_rate_alt(fr, to)


def get_rate_alt(fr, to):
    try:
        data = web.get(
            'http://free.currencyconverterapi.com/api/v3/convert?q=%s_%s&compact=ultra^&apiKey=5b0607fcc1fe232a0178' % (fr, to)).json()

        return data['results']['%s_%s' % (fr, to)]['val']
    except:
        return None


def validate_cur(cur):
    if len(cur) == 3:
        return cur.upper()
    else:
        return None


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
