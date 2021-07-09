from stepper import Stepper
# import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATA_HOST = getenv('DATA_HOST')
CONTROL_HOST = getenv('CONTROL_HOST')

# wait for API to boot
# time.sleep(60)

Stepper(DATA_HOST, CONTROL_HOST).run()
