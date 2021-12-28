from upb.options import DurationOption, Optionable


class ScriptStage(Optionable):
    pass


class WaitStage:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_options(duration=DurationOption('Time'))
