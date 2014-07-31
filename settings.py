# General configurations for wordpress-workflow
SITE_CONFIG = {
    'version': '3.9.1',
    'locale': 'es_ES',
    'theme': 'yourtheme',

    'dev': {
        'url': 'wordpress-workflow.local',
        'title': 'New Project',
        #Admin config
        'admin_user': 'admin',
        'admin_password': 'password',
        'admin_email': 'admin@email.com',
        #database config 
        'dbname': 'wordpress_workflow',
        'dbuser': 'root',
        'dbpassword': 'password',
        'dbhost': 'localhost'
    }
}
# 3rd party plugins

PLUGINS_CONFIG = {
    'wordpress-seo': {
        'active': True,
        'version': 'stable'
    },
    'contact-form-7': {
        'active': True,
        'version': 'stable'
    },
    'wp-super-cache': {
        'active': True,
        'version': 'stable'
    },
}

# Own plugins
CUSTOM_PLUGINS_CONFIG = {
    'jetpack': {
        'active': True
    }
}
