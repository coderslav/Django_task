"""
TODO custom logging system. Include requests messages in console!
Logging settings module for whole Django project "News_Paper"

Classes
----------
LevelFilter:
    Logging level filter


Variables
----------
log_set:
    Dict logging settings for settings.py
"""


class LevelFilter(object):
    """
     Logging level filter

        Attributes
        ----------
        level_name : str
            required parameter ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' etc)

        Methods
        -------
        filter(self, record: LogRecord object)
            compares level from LogRecord object with level_name attribute and return True or False
    """
    def __init__(self, level):
        self.level_name = level

    def filter(self, record) -> bool:

        return record.levelname == self.level_name


log_set = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'style': '{',
            'format': '{asctime} {levelname} {message}',
        },
        'advanced': {
            'style': '{',
            'format': '{asctime} {levelname} {message} {pathname}'
        },
        'super_advanced': {
            'style': '{',
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}'
        },
        'info_for_file': {
            'style': '{',
            'format': '{asctime} {levelname} {module} {message}'
        },
        'info_for_file_advanced': {
            'style': '{',
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'debug_level_filter': {
            '()': 'News_Paper.logging_settings.LevelFilter',
            'level': 'DEBUG',
        },
        'info_level_filter': {
            '()': 'News_Paper.logging_settings.LevelFilter',
            'level': 'INFO',
        },
        'warning_level_filter': {
            '()': 'News_Paper.logging_settings.LevelFilter',
            'level': 'WARNING',
        },
        'error_level_filter': {
            '()': 'News_Paper.logging_settings.LevelFilter',
            'level': 'ERROR',
        },
        'critical_level_filter': {
            '()': 'News_Paper.logging_settings.LevelFilter',
            'level': 'CRITICAL',
        },

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'debug_level_filter'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_advanced': {
            'level': 'WARNING',
            'filters': ['require_debug_true', 'warning_level_filter'],
            'class': 'logging.StreamHandler',
            'formatter': 'advanced'
        },
        'console_super_advanced': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'super_advanced'
        },
        'file': {
            'level': 'INFO',
            'filters': ['info_level_filter'],
            'class': 'logging.FileHandler',
            'formatter': 'info_for_file',
            'filename': 'general.log',
        },
        'file_advanced': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'info_for_file_advanced',
            'filename': 'errors.log',
        },
        'security_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'info_for_file',
            'filename': 'security.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'advanced',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_advanced', 'console_super_advanced', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_advanced', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_advanced', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_advanced'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['file_advanced'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'propagate': False,
        },
    }
}
