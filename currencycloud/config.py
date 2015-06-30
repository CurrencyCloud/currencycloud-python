DEBUG = False

ENV_PRODUCTION = 'production'
ENV_DEMOSTRATION = 'demonstration'
ENV_UAT = 'uat'

CONFIG = {
    'retry_count': 3,
    'environments': {
        ENV_PRODUCTION: 'https://api.thecurrencycloud.com',
        ENV_DEMOSTRATION: 'https://devapi.thecurrencycloud.com',
        ENV_UAT: 'https://api-uat1.ccycloud.com',
    }
}
