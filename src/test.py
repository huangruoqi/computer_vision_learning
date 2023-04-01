class ModelTest:
    def __init__(self, base_model, raw_input, raw_output, options):
        self.counter = 0
        self.base_model = base_model
        self.raw_input = raw_input
        self.raw_output = raw_output
        self.defalut_options = {
            'preprocess': [],
            'batch_size': 16,
            'time_stamp': 32,
        }
        # for i in range(len(self.base_model.layers)):
        #     self.final_options[f'layer{i}']
        self.final_options = []
        self.expand_options(options.items())
        self.current_options = [None] * len(self.final_options)

    def expand_options(self, options, name=None):
        for option in options:
            if isinstance(option[1], list):
                self.extend_options(option[1], name=option[0])
            else:
                if name is None:
                    self.final_options.append(option)
                else:
                    self.final_options.append((name, option))
                
                    

    def process_options(self):
        
        
        pass

    def preprocess(self, func):
        return [func(row) for row in self.raw_input]

    def test(self, option_idx=0):
        if option_idx==len(self.final_options):
            self.build()
            pass

        if callable(self.final_options[option_idx]):
            self.current_options[option_idx] = False
            self.test(option_idx+1)
            self.current_options[option_idx] = True
            self.test(option_idx+1)
        else:
            for i in self.options[option_idx]:
                self.current_options[option_idx] = i
                self.test(option_idx+1)

    def build(self):
        self.process_options()
        final_inputs = None