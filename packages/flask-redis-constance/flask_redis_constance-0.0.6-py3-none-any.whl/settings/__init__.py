import os
import importlib
import subprocess

# from redis import Redis
# from celery.schedules import crontab

try:
    user_settings = importlib.import_module('settings')
except Exception as err:
    print(f"{type(err).__name__}: {err}")
    user_settings = None


SOFTWARE = getattr(user_settings, 'SOFTWARE', 'Raspack')

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(32)])
SECRET_KEY = getattr(user_settings, 'SECRET_KEY', 'e|r!qqw0wo!Jf-:phn#JQ\x0c(Q9xJI&ZW_')

BASE_DIR = getattr(user_settings, 'BASE_DIR', os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
SQLALCHEMY_DATABASE_URI = getattr(user_settings, 'SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(BASE_DIR, 'canpi.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = getattr(user_settings, 'SQLALCHEMY_TRACK_MODIFICATIONS', False)
JSON_FILE = getattr(user_settings, 'JSON_FILE', os.path.join(BASE_DIR, 'raspack/', 'default_settings.json'))

# CANBUS HAT configuration
CAN_TIMEOUT = getattr(user_settings, 'CAN_TIMEOUT', 500)

# Constance module configuration
CONSTANCE_CONFIG = getattr(user_settings, 'CONSTANCE_CONFIG', {
    # Config CAN bus HAT
    "CAN_NAME": ("can0", "Nom CAN bus par defaut"),
    "CAN_BITRATE": (125000, "Bitrate CAN"),
    "CAN_PROG_NAME": ("can0", "Nom CAN bus pour le script"),
    "CAN_PROG_BITRATE": (125000, "Bitrate CAN"),

    # Config global
    "JIG_NAME": (f"{SOFTWARE}0", "Nom du JIG"),
    "CLOCK_DOWN": (1445, "Heure d'extinction"),
    "TIMER": (15, "Delais avant extinction"),
    "SHUTDOWN": (1, "Status extinction"),
    "MODE": ("DIAG", "Select mode: DIAG, CAL, SEM"),
    "KEYMAP": ("FR", "Mappage clavier USB Scanner (FR ou UK)"),

    # Config Network
    "ADDR_SERVER": ("//10.115.141.229/CSDAtelier", "Lecteur réseau"),
    "USERNAME": ("", "Username montage lecteur réseau"),
    "PASSWORD": ("", "Password montage lecteur réseau"),
    "DOMAIN": ("", "Domain montage lecteur réseau"),
    "PATH_SERVER": ('/mnt/CSD', 'Path lecteur Réseau'),
    "PATH_LOG": ('LOGS/LOG_DL_CAL', 'Path log lecteur Réseau'),
    "API_URL": ("", "Url API CSD Dashboard"),
    "API_TOKEN": ("", "Token for CSD Dashboard"),
    "NTP_SERVER": ("fr.pool.ntp.org", "Serveur NTP"),
})

CONSTANCE_CONFIG_FIELDSETS = getattr(user_settings, 'CONSTANCE_CONFIG_FIELDSETS', {
    'CAN_BUS': (
        'CAN_NAME', 'CAN_BITRATE', 'CAN_PROG_NAME', 'CAN_PROG_BITRATE'
    ),
    'GLOBAL': (
        'JIG_NAME', 'CLOCK_DOWN', 'TIMER', 'SHUTDOWN', 'MODE', 'KEYMAP'
    ),
    'NETWORK': (
        'ADDR_SERVER', 'USERNAME', 'PASSWORD', 'DOMAIN', 'PATH_SERVER', "PATH_LOG",
        'API_URL', 'API_TOKEN', 'NTP_SERVER'
    )
})


# Logger Configuration
EMAIL_HOST = getattr(user_settings, 'EMAIL_HOST', '')
SERVER_EMAIL = getattr(user_settings, 'SERVER_EMAIL', '')
ADMIN_EMAIL = getattr(user_settings, 'ADMIN_EMAIL', [])


LOGGING_CONFIG = getattr(user_settings, 'LOGGING_CONFIG', {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'level': 'WARNING',
        },
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        },
        'mail_admin': {
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'default',
            'level': 'ERROR',
            'mailhost': EMAIL_HOST,
            'fromaddr': SERVER_EMAIL,
            'toaddrs': ADMIN_EMAIL,
            'subject': f'{subprocess.check_output(["hostname"]).decode("utf-8").strip().capitalize()} Error System',
        }
    },
    'loggers': {
        'interface': {
            'handlers': ['default', 'mail_admin'],
            'level': 'WARNING',
            'propagate': False,
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'mail_admin'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'mail_admin'],
    }
})
