#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, web

log = None

def main(wf):
    # Get args from Workflow as normalized Unicode
    args = wf.args
    
    if not 'defaults' in wf.settings:
        wf.settings['defaults'] = { 'fr': 'USD', 'to': 'EUR' }
    
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
        
        if len(args) == num_args:
          fr = args[num_args - 1].upper()
        elif len(args) == num_args + 1:
          fr = args[num_args - 1].upper()
          to = args[num_args].upper()
    
        if len(fr) != 3 or len(to) != 3:
            wait()
    
    rate = get_rate(fr, to)
    
    if not rate:
        rate = get_rate_alt(fr, to)
        
    value = amount * rate

    formatted = "{:.2f}".format(value)
    
    # Add an item to Alfred feedback
    wf.add_item('%d %s = %s %s' % (amount, fr, formatted, to), valid=True, subtitle='Press enter to copy to clipboard', copytext=formatted, arg=formatted)

    # Send output to Alfred
    wf.send_feedback()
    
def set_defaults(args):
    if len(args[1]) == 3:
        cur = args[1].upper()
        
        if args[0] == 'from':
            wf.settings['defaults'] = { 'fr': cur, 'to': wf.settings['defaults']['to'] }
        if args[0] == 'to':
            wf.settings['defaults'] = { 'fr': wf.settings['defaults']['fr'], 'to': cur }

        print cur
        return
    
def wait():
    wf.add_item('Please enter a valid format', 'cur [amount] [currency code] [currency code]')
    
    wf.send_feedback()

def get_rate(fr, to):
    data = web.get('http://apilayer.net/api/live?access_key=c938bcf13e0aff152614745f41414ed4&currencies=%s,%s' % (fr, to)).json()
    
    if data['success']:
        return (1 / data['quotes']['USD%s' % fr]) * data['quotes']['USD%s' % to]
    else:
        return None

def get_rate_alt(fr, to):
    data = web.get('http://free.currencyconverterapi.com/api/v3/convert?q=%s_%s&compact=ultra' % (fr, to)).json()
    
    try:
        return data['%s_%s' % (fr, to)]
    except:
        wait()

if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))