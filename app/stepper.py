import time
import datetime
# import requests
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

      # endpoints = self.__poll(hr, min)
      # self.__call_endpoints(endpoints)

      self.__pause()

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

