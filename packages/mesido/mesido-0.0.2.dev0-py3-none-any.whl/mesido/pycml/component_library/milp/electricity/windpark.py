from mesido.pycml import Variable

from .. import ElectricitySource


class WindPark(ElectricitySource):
    def __init__(self, name, **modifiers):
        super().__init__(name, **modifiers)

        self.component_subtype = "wind_park"

        self.add_variable(Variable, "Set_point", min=0.0, max=1.0)
