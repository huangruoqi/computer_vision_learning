import numpy as np

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

        self.final_inputs = None
        self.final_outputs = None
        self.final_params = None


    def expand_options(self, options, name=None):
        for option in options:
            if isinstance(option[1], list) and callable(option[1][0]):
                self.expand_options(option[1], name=option[0])
            else:
                if name is None:
                    self.final_options.append(option)
                else:
                    self.final_options.append((name, option))
                
                    

    def process_options(self):
        self.final_inputs = self.raw_inputs
        self.final_outputs = self.raw_outputs
        self.final_params = {}
        for i, (name, options) in enumerate(self.final_options):
            option_idx = self.current_options[i]
            if option_idx is None:
                continue
            option = options[option_idx]
            if name == 'preprocess':
                self.process(option, self.final_inputs)
            elif name in ['batch_size', 'time_stamp']:
                self.final_params[name] = option
            else:
                raise Exception(f"option <{name}> not found")

    def process(self, func, data):
        return [func(row) for row in data]

    def test(self, option_idx=0):
        if option_idx==len(self.final_options):
            self.build()
            pass

        if callable(self.final_options[option_idx][0]):
            self.current_options[option_idx] = None
            self.test(option_idx+1)
            for i in self.final_options[option_idx]:
                self.current_options[option_idx] = i
                self.test(option_idx+1)
        else:
            for i in self.final_options[option_idx]:
                self.current_options[option_idx] = i
                self.test(option_idx+1)

    def build(self):
        self.process_options()
        self.final_inputs = np.array(self.final_inputs)
        input_shape = self.final_inputs.shape
        
        
        
        