# PI-TIME-SCHEDULE
python3 | pip3 | pipenv | pytest

## INSTALL
`pipenv install`

## START APP
`pipenv run ./scripts/start.sh`

## TESTS
`pipenv run ./scripts/test.sh`

## SUPERVISOR
- move config file to: `/etc/supervisor/conf.d/pi-time-schedule.conf`
- restart: `sudo systemctl restart supervisor.service`
- open client: `sudo supervisorctl`
- get logs: `tail pi-time-schedule stderr`