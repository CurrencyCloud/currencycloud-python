from betamax import Betamax
import os

record_mode = 'never' if os.environ.get('TRAVIS_GH3') else 'once'

with Betamax.configure() as config:
    config.cassette_library_dir = 'test/fixtures/vcr_cassettes'
    config.default_cassette_options['record_mode'] = record_mode
    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'x' * 20)
    )
