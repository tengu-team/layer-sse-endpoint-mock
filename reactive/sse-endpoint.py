#/usr/bin/env python3
from charms.reactive import (
    when,
    endpoint_from_flag
)
from charmhelpers.core.hookenv import (
    status_set,
    config,
    log,
)


@when('config.changed.base-url')
def consumer_active():
    cfg = config()
    base_url = cfg.get("base-url")
    if base_url:
        # Using blocked state to send messages since active states seem to be overwritten
        # by the "waiting for container" message.
        # https://discourse.jujucharms.com/t/how-to-avoid-the-waiting-for-container-message/1369
        status_set('blocked', 'active ({})'.format(base_url))
        # status_set('active', 'active ({})'.format(base_url))
        # log("set status to 'active ({})".format(base_url))
    else:
        status_set('blocked', 'Please set the "base-url" config option.')


@when('config.set.base-url')
@when('sse-endpoint.consumer.available')
def send_information():
    cfg = config()
    base_url = cfg.get("base-url")
    endpoint = endpoint_from_flag('sse-endpoint.consumer.available')
    endpoint.set_base_url(base_url)
