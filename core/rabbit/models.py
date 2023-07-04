# import settings
# from nameko.constants import NON_PERSISTENT, PERSISTENT
# from nameko.standalone.events import event_dispatcher

# config = {
#     'AMQP_URI': f'amqp://{settings.RABBITMQ_CONFIG.username}:'
#                 f'{settings.RABBITMQ_CONFIG.password}@{settings.RABBITMQ_CONFIG.host}:'
#                 f'{settings.RABBITMQ_CONFIG.port}/{settings.RABBITMQ_CONFIG.vhost}'
# }

# dispatch_event = event_dispatcher(
#     config, use_confirms=False
# )
