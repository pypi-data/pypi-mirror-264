class SapiensNB:
    def __init__(self):
        self.__inputs, self.__outputs = [], []
        self.__type_outputs = []
        self.__absolute_class = 1
    def fit(self, inputs=[], outputs=[]):
        try:
            inputs, outputs = list(inputs) if type(inputs) in (tuple, list) else [[0]], list(outputs) if type(outputs) in (tuple, list) else [[0]]
            if type(inputs[0]) not in (tuple, list): inputs = [[x] for x in inputs]
            self.__inputs, self.__outputs = inputs, outputs
            for output in self.__outputs:
                if output not in self.__type_outputs: self.__type_outputs.append(output)
            self.__absolute_class = self.__getAbsoluteClass()
        except Exception as error: print('ERROR during training: '+str(error))
    def saveModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 3: path = 'SapiensNB-Model.nb'
            if path[-3:].lower() != '.nb': path += '.nb'
            dataset = {"inputs": self.__inputs, "outputs": self.__outputs, "type_outputs": self.__type_outputs, "absolute_class": self.__absolute_class}
            from json import dumps
            model = dumps(dataset)
            from re import sub
            parameters = sub(r'[{}\[\]:,\s]|"inputs"|"outputs"', '', str(model).strip())
            parameters_count = len(parameters)
            if parameters_count < 1000: model_size = f'{parameters_count}P'
            elif parameters_count < 1_000_000: model_size = f'{parameters_count // 1000}K'
            elif parameters_count < 1_000_000_000: model_size = f'{parameters_count // 1_000_000}M'
            elif parameters_count < 1_000_000_000_000: model_size = f'{parameters_count // 1_000_000_000}B'
            else: model_size = f'{parameters_count // 1_000_000_000_000}T'
            binary_data = ''.join(format(ord(char), '08b') for char in model)
            binary_data = binary_data.replace('000', '2').replace('001', '3').replace('010', '4').replace('011', '5')
            binary_data = binary_data.replace('100', '6').replace('101', '7').replace('110', '8').replace('111', '9')
            if path[-3:].lower() == '.nb': path = path[:-3]+f'-{model_size}.nb'
            with open(path, 'w', encoding='utf-8') as file: file.write(binary_data)
        except Exception as error: print('ERROR during saving model: '+str(error))
    def loadModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 3: path = 'SapiensNB-Model.nb'
            if path[-3:].lower() != '.nb': path += '.nb'
            from os import path as _path
            if not _path.exists(path): return
            with open(path, 'r', encoding='utf-8') as file: binary_data = str(file.read()).strip()
            binary_data = binary_data.replace('2', '000').replace('3', '001').replace('4', '010').replace('5', '011')
            binary_data = binary_data.replace('6', '100').replace('7', '101').replace('8', '110').replace('9', '111')
            original_string = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
            from json import loads
            try: dataset = loads(original_string)
            except:
                from ast import literal_eval
                dataset = literal_eval(original_string)
            self.__inputs, self.__outputs, self.__type_outputs, self.__absolute_class = dataset['inputs'], dataset['outputs'], dataset['type_outputs'], dataset['absolute_class']
        except Exception as error: print('ERROR during loading model: '+str(error))
    def transferLearning(self, transmitter_path='', receiver_path='', rescue_path=''):
        try:
            transmitter_path, receiver_path, rescue_path = str(transmitter_path).strip(), str(receiver_path).strip(), str(rescue_path).strip()
            from os import path
            if len(transmitter_path) <= 0 or len(receiver_path) <= 0 or not path.exists(transmitter_path) or not path.exists(receiver_path): return
            self.loadModel(path=transmitter_path)
            from copy import deepcopy
            inputs, outputs, type_outputs = deepcopy(self.__inputs), deepcopy(self.__outputs), deepcopy(self.__type_outputs)
            self.loadModel(path=receiver_path)
            self.__inputs, self.__outputs, self.__type_outputs = self.__inputs+inputs, self.__outputs+outputs, self.__type_outputs+type_outputs
            self.saveModel(path=rescue_path)
        except Exception as error: print('ERROR during transferring learning: '+str(error))
    def __differenceText(self, value1='', value2=''):
        try:
            value1, value2 = str(value1), str(value2)
            if len(value1) < len(value2):
                nequal, lvalue = len(value2), [char for char in word]
                if len(value1.strip()) <= 0: value1 = ' '
                for x in lvalue:
                    if x in value2: nequal -= 1
                difference = nequal
            else:
                nequal, lvalue = len(value1), [char for char in word]
                if len(value2.strip()) <= 0: value2 = ' '
                for x in lvalue:
                    if x in value1: nequal -= 1
                difference = nequal
            return difference
        except: return 0
    def __numberClass(self, _entry=[], _class=[]):
        try:
            result = 0
            try: partnumber = 1/len(_entry)
            except: partnumber = 0
            for inputs, outputs in zip(self.__inputs, self.__outputs):
                if outputs == _class:
                    total = 0
                    for entry in _entry:
                        if entry in inputs: total += partnumber
                    result += total
            return result
        except: return 0
    def __totalClass(self, _entry=[]):
        try:
            result = 0
            try: partnumber = 1/len(_entry)
            except: partnumber = 0
            for inputs in self.__inputs:
                total = 0
                for entry in _entry:
                    if entry in inputs: total += partnumber
                result += total
            if result <= 0: result = 1
            return result
        except: return 1
    def __getAbsoluteClass(self):
        try: return max([1, len(self.__outputs)])
        except: return 1
    def __bayesTheorem(self, inputs=[]):
        try:
            outputs, inlist = [], False
            for entry in inputs:
                classes, percentages = {}, []
                for output in self.__type_outputs:
                    try:
                        countclass = self.__outputs.count(output)
                        if countclass <= 0: countclass = 1
                        percentage = (self.__numberClass(entry, output)/countclass)*(countclass/self.__absolute_class)/(self.__totalClass(entry)/self.__absolute_class)
                        if type(output) in (tuple, list): outclass, inlist = output, True
                        else: outclass = output
                        try: classes[outclass] = percentage
                        except: classes[str(outclass)] = percentage
                        percentages.append(percentage)
                    except:
                        percentages = []
                        break
                if sum(percentages) <= 0:
                    try:
                        sumdiffs = []
                        for train in self.__inputs:
                            diffs = []
                            for i, _ in enumerate(entry):
                                try: cell1 = entry[i]
                                except: cell1 = 0
                                try: cell2 = train[i]
                                except: cell2 = 0
                                try:
                                    if type(cell1) in (bool, int, float) and type(cell2) in (bool, int, float): diff = abs(float(cell1)-float(cell2))
                                    else: diff = self.__differenceText(cell1, cell2)
                                except: diff = 0
                                diffs.append(diff)
                            sumdiffs.append(sum(diffs))
                        index, percent, percents = sumdiffs.index(min(sumdiffs)), 1, []
                        for i, _ in enumerate(entry):
                            try: cell1 = entry[i]
                            except: cell1 = 0
                            try: cell2 = self.__inputs[index][i]
                            except: cell2 = 0
                            try:
                                if type(cell1) in (bool, int, float) and type(cell2) in (bool, int, float): percent = min([cell1, cell2])/max([cell1, cell2])
                                else: percent = 1
                            except: percent = 1
                            percents.append(percent)
                        total = sum(percents)/len(percents)
                        if total <= 0: total = .5
                        elif total < .5: total = abs(1 - total)
                        elif total > 1: total = 1
                        rest = (1-total)/len(self.__type_outputs)
                        for output in self.__type_outputs:
                            if output == self.__outputs[index]:
                                if type(output) in (tuple, list): outclass, inlist = output, True
                                else: outclass = output
                                try: classes[outclass] = total
                                except: classes[str(outclass)] = total
                            else:
                                if type(output) in (tuple, list): outclass, inlist = output, True
                                else: outclass = output
                                try: classes[outclass] = rest
                                except: classes[str(outclass)] = rest
                    except:
                        try: classes[self.__type_outputs[-1][0]] = 1
                        except: classes[str(self.__type_outputs[-1][0])] = 1
                classify = list(classes.keys())[list(classes.values()).index(max(list(classes.values())))]
                try: classes['classify'] = eval(classify) if '{' in classify or '[' in classify else classify
                except: classes['classify'] = classify
                outputs.append(classes)
            return outputs
        except: return []
    def predict(self, inputs=[]):
        try:
            outputs = []
            inputs = list(inputs) if type(inputs) in (tuple, list) else [[0]]
            if len(inputs) <= 0: inputs = [[0]]
            if type(inputs[0]) not in (tuple, list): inputs = [[x] for x in inputs]
            outputs = self.__bayesTheorem(inputs)
            return outputs
        except Exception as error:
            print('ERROR during prediction: '+str(error))
            return []
    def test(self, inputs=[], outputs=[]):
        try:
            results = self.predict(inputs=inputs)
            total = min((len(outputs), len(results))) if len(outputs) != len(results) else len(outputs)
            hits = sum(x['classify'] == y for x, y in zip(results, outputs))/total
            misses = 1-hits
            return {"hits": hits, "errors": misses}
        except Exception as error:
            print('ERROR during testing: '+str(error))
            return {"hits": 0, "errors": 1}
