from upd.options import ChoiceOption

class RendererOption(ChoiceOption):

    def real_time_init(self):
        from upd.renderers import renderers

        self.choice([
                {
                    'id': renderer.__name__,
                    'name': renderer().name
                } for renderer in renderers
            ]
        )