
limit = {
  'temperature': {'min': 0, 'max': 45},
  'soc': {'min': 20, 'max': 80},
  'charge_rate': {'min': 0, 'max': 0.8}
}

threshold = {
  'temperature': 4,
  'soc': 4,
  'charge_rate': 0.04
}

warning_message = {
  'EN':{
    'temperature': {'min': 'Warning: Approaching less temperature', 'max': 'Warning: Approaching high temperature', 'out_of_range': 'Temperature is out of range!'},
    'soc': {'min': 'Warning: Approaching discharge', 'max': 'Warning: Approaching charge-peak', 'out_of_range': 'State of Charge is out of range!'},
    'charge_rate': {'min': 'Warning: Approaching less charge-rate', 'max': 'Warning: Approaching high charge-rate', 'out_of_range': 'Charge rate is out of range!'}
  },
  'DE':{
    'temperature': {'min': 'Warnung: Annäherung an weniger Temperatur', 'max': 'Warnung: Annähernd hohe Temperatur', 'out_of_range': 'Die Temperatur liegt außerhalb des Bereichs!'},
    'soc': {'min': 'Warnung: Nahende Entladung', 'max': 'Warnung: Annäherung an den Ladespitzenwert', 'out_of_range': 'Der Ladezustand ist außer Reichweite!'},
    'charge_rate': {'min': 'Warnung: Annäherung an weniger Ladungsrate', 'max': 'Warnung: Annäherung an hohe Ladegeschwindigkeit', 'out_of_range': 'Die Laderate liegt außerhalb des Bereichs!'}
  }
}

scaling_factor = {
  'temperature': {'celsius': 1, 'fahrenheit': 5/9, 'kelvin': 1},
  'soc': {'percent': 1, 'one': 100},
  'charge_rate': {'percent': 1/100, 'one': 1}
}

offset = {
  'temperature': {'celsius': 0, 'fahrenheit': -32, 'kelvin': -273.15},
  'soc': {'percent': 0, 'one': 0},
  'charge_rate': {'percent': 0, 'one': 0}
}

def print_warning(warning_text):
  if warning_text == 'No Warning':
    return None 
  print(warning_text)

def is_lower_state_of_parameter_tolerant(parameter, value, language):
  if value >= limit[parameter]['min'] and value <= (limit[parameter]['min'] + threshold[parameter]):
    warning_text = warning_message[language][parameter]['min']
    return warning_text
  return 'No Warning'

def is_higher_state_of_parameter_tolerant(parameter, value, language):
  if value <= limit[parameter]['max'] and value >= (limit[parameter]['max'] - threshold[parameter]):
    warning_text = warning_message[language][parameter]['max']
    return warning_text
  return 'No Warning'

def convert_to_calculation_value(parameter, value, unit):
  value = value + offset[parameter][unit] * scaling_factor[parameter][unit]
  return value


def is_battery_paremeter_ok(parameter, value, unit, language):
  value = convert_to_calculation_value(parameter, value, unit)
  warning_text = is_lower_state_of_parameter_tolerant(parameter, value, language)
  print_warning(warning_text)
  warning_text = is_higher_state_of_parameter_tolerant(parameter, value, language)
  print_warning(warning_text)
  if value < limit[parameter]['min'] or value > limit[parameter]['max']:
    warning_text = warning_message[language][parameter]['out_of_range']
    print_warning(warning_text)
    return False
  return True

def battery_is_ok(parameter, language):
  parameter_verdict = {}
  for attribute in parameter:
    parameter_verdict[attribute] = is_battery_paremeter_ok(attribute, parameter[attribute]['value'], parameter[attribute]['unit'], language)
  if False in [parameter_verdict['temperature'], parameter_verdict['soc'], parameter_verdict['charge_rate']]:
    return False
  return True


if __name__ == '__main__':
  assert(battery_is_ok({'temperature': {'value': 25, 'unit': 'celsius'}, 'soc': {'value': 70, 'unit': 'percent'}, 'charge_rate': {'value': 0.7, 'unit': 'one'}}, 'EN') is True)
  assert(battery_is_ok({'temperature': {'value': 50, 'unit': 'celsius'}, 'soc': {'value':85, 'unit': 'percent'}, 'charge_rate': {'value':0, 'unit': 'one'}}, 'DE') is False)
