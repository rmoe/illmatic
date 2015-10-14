# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'illmatic.controllers.root.RootController',
    'modules': ['illmatic'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/illmatic/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

sqlalchemy = {
    'url'           : 'postgresql://illmatic:zaq123@localhost/illmatic',
    'echo'          : False,
    'echo_pool'     : False,
    'pool_recycle'  : 3600,
    'encoding'      : 'utf-8'
}


logging = {
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'illmatic': {'level': 'DEBUG', 'handlers': ['console']},
        'pecan': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                       '[%(threadName)s] %(message)s'),
        '__force_dict__': True
        }
    }
}
