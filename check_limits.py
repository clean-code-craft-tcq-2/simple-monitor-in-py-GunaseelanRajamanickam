
battery_parameter_range = {
  'temperature': {'min': 0, 'max': 45},
  'soc': {'min': 20, 'max': 80},
  'charge_rate': {'min': 0, 'max': 0.8}
}

def check_battery_parameter(battery_parameter, battery_parameter_value):
  if battery_parameter_value < battery_parameter_range[battery_parameter]['min'] or battery_parameter_value > battery_parameter_range[battery_parameter]['max']:
    print(battery_parameter + ' is out of range!')
    return False
  return True

def battery_is_ok(battery_parameter):
  parameter_verdict = {}
  for attribute in battery_parameter:
    parameter_verdict[attribute] = check_battery_parameter(attribute, battery_parameter[attribute])
  if False in [parameter_verdict['temperature'], parameter_verdict['soc'], parameter_verdict['charge_rate']]:
    return False
  return True


if __name__ == '__main__':
  assert(battery_is_ok({'temperature': 25, 'soc': 70, 'charge_rate': 0.7}) is True)
  assert(battery_is_ok({'temperature': 50, 'soc': 85, 'charge_rate': 0}) is False)
