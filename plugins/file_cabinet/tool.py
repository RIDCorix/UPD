from upd.extension import Tool

class FileCabinet(Tool):

    def get_id(self):
        return 'file_cabinet'

    def get_name(self):
        return 'File Cabinet'

tool = FileCabinet()
