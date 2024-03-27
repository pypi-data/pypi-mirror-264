from typing import Optional

from .alert.alertwrapper import AlertWrapper
from .config.slackwebhookfactory import SlackWebhookFactory

alert_wrapper: Optional[AlertWrapper] = None


def setup_alert(alias, channel):
    global alert_wrapper
    slack_factory = SlackWebhookFactory()
    slack_bot = slack_factory.create_webhook(channel=channel)

    if not slack_bot:
        raise Exception('Could not create slack webhook')
    alert_wrapper = AlertWrapper(alias, slack_bot)
    alert_wrapper.send_alert(f'{alias} started.', type_='INFO')


def create_sub_alert(alias: str):
    global alert_wrapper
    if alert_wrapper:
        return AlertWrapper(alias, alert_wrapper.slack_bot)
    else:
        raise Exception('AlertWrapper not initialized')


def send_alert(message, error=None, type_='ERROR', alias=None):
    global alert_wrapper
    if alert_wrapper:
        alert_wrapper.send_alert(message, error, type_, alias)
    else:
        AlertWrapper.log_msg_error(alias, message, error, type_)
