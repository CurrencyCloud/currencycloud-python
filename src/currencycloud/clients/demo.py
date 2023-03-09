from currencycloud.http import Http
from currencycloud.resources import SimulateFunding


class Demo(Http):
    '''This class provides an interface to the Demo endpoints of the CC API'''

    def create_funding_for_demo(self, **kwargs) -> SimulateFunding:
        return SimulateFunding(self, **self.post("/v2/demo/funding/create", kwargs))