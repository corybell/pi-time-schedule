import sys
import time
import datetime
import requests
from util import time_to_string

class Stepper():
  def __init__(self, data_host, control_host):
    self._data_host = data_host
    self._control_host = control_host
    self._step_mins = 1

  def run(self):
    self.__start_cadence()

    while True:
      now = datetime.datetime.now()
      hr = now.strftime("%H")
      min = now.strftime("%M")
      self.__log_message(f'HR: {hr} MIN: {min}')

      endpoints = self.__poll(hr, min)
      self.__call_endpoints(endpoints)

      self.__pause()
  
  def __poll(self, curr_hr, curr_min):
    endpoints = []

    relay_data = self.__http_get(f'{self._data_host}/relay')
    
    for r in relay_data:
      r_id = r['id']

      t = r['timer']
      if t is None:
        continue
      
      t_hr = t.get('hr')
      if t_hr is None:
        continue

      t_min = t.get('min')
      if t_min is None:
        continue
      
      val = self.__get_timer_val(t_hr, t_min, curr_min, curr_hr)
      endpoints.append(f'relay/{r_id}/{val}')

    return endpoints

  def __get_timer_val(self, t_hr, t_min, curr_min, curr_hr):
    if t_hr == '*':
      if t_min == '*':
        return 'on'
      else:
        min_data = self.__http_get(f'{self._data_host}/minute/{t_min}')
        return min_data[curr_min]
    else:
      hr_data = self.__http_get(f'{self._data_host}/hour/{t_hr}')
      hr_val = hr_data[curr_hr]
      if hr_val == 'on':
        if t_min == '*':
          return 'on'
        else:
          min_data = self.__http_get(f'{self._data_host}/minute/{t_min}')
          return min_data[curr_min]
    return 'off'

  def __call_endpoints(self, endpoints):
    self.__log_message('calling endpoints...')
    for endpoint in endpoints:
      url = f'{self._control_host}/{endpoint}'
      self.__http_get(url)

  def __http_get(self, url):
    try:
      self.__log_message(f'calling: {url}')
      headers = { 'Access-Control-Allow-Origin': '*' }
      r = requests.get(url = url, headers = headers)
      self.__log_message(f'response status code: {r.status_code}')
      return r.json()
    except:
      self.__log_message(f'Error calling: {url}')
      self.__log_message(f'Exception: {sys.exc_info()[0]}')

  def __pause(self):
    now = datetime.datetime.now()
    sec = int(now.strftime("%S"))
    sleep_time = (self._step_mins * 60) - sec
    
    self.__log_message(f'sleeping for {sleep_time} sec...')
    time.sleep(sleep_time)
    self.__log_message('done sleeping...')

  def __log_message(self, message):
    t = datetime.datetime.now()
    print(f'{time_to_string(t)}: {message}')

  def __start_cadence(self):
    now = datetime.datetime.now()
    sec = int(now.strftime("%S"))

    sleep_time = 60 - sec

    self.__log_message(f'sleeping for {sleep_time} sec...')
    time.sleep(sleep_time)
    self.__log_message('done sleeping...')

