class ModelTest:
    def __init__(self, base_model, raw_input, raw_output, options):
        self.base_model = base_model
        self.raw_input = raw_input
        self.raw_output = raw_output
        self.options = options.items()
        self.current_options = [None] * len(self.options)
        self.final_options = {
            'preprocess': [lambda a:a],
        }
        for i in range(len(self.base_model.layers)):
            self.final_options[f'layer{i}'] = [lambda a:a]

    def process_options(self):
        pass

    def preprocess(self, func):
        return [func(row) for row in self.raw_input]

    def test(self, option_idx=0):
        if option_idx==len(self.options):
            self.build()
            pass

        for i in self.options[option_idx]:
            self.current_options[option_idx] = i
            self.test(option_idx+1)

    def build(self):
        self.process_options()
        final_inputs = None