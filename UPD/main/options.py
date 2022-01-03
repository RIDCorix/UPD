from upd.options import ChoiceOption

class RendererOption(ChoiceOption):

    @property
    def value(self):
        from upd.renderers import renderers
        return renderers[self._value]

    def real_time_init(self):
        from upd.renderers import renderers

        self.choice([
                {
                    'id': id,
                    'name': renderer.name
                } for id, renderer in renderers.items()
            ]
        )
