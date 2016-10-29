import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(levelname)-5s - %(name)s:%(funcName)s -- %(message)s',
        }
    },
    'handlers': {
        'standard': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['standard'],
            'level': 'INFO',
        },
    },
    'disable_existing_loggers': False,
})
