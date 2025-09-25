from betamax import Betamax
from betamax_serializers import pretty_json

import os

record_mode = 'never'

Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/vcr_cassettes'
    config.default_cassette_options['record_mode'] = record_mode
    config.default_cassette_options['serialize_with'] = 'prettyjson'
    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'x' * 20)
    )
