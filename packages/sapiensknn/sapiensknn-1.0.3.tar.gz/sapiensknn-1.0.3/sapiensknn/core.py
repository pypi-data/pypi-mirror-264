class SapiensKNN:
    def __init__(self, k=1, normalization=False, regression=False):
        self.__k = max((1, int(k))) if type(k) in (int, float) else 1
        self.__normalization = bool(normalization) if type(normalization) in (bool, int, float) else False
        self.__regression = bool(regression) if type(regression) in (bool, int, float) else False
        self.__one_dimensional = False
        self.__inputs, self.__outputs = [], []
        self.__maximums = []
    def __embedding(self, x=[]):
        if self.__one_dimensional: result_x = [[ord(z) for z in str(y)] if type(y) not in (int, float, bool) else [float(y)] for y in x] if len(x) > 0 else [[0]]
        else:
            result_x = [[int(''.join([str(ord(i)) for i in str(z)])) if type(z) not in (int, float, bool) else float(z) for z in y] for y in x] if len(x) > 0 else [[0]]
            if len(self.__maximums) <= 0: self.__maximums = [max(y) for y in list(map(list, zip(*result_x)))]
            if self.__normalization: result_x = [[z/self.__maximums[i] for i, z in enumerate(y)] for y in result_x]
        return result_x
    def fit(self, inputs=[], outputs=[]):
        try:
            inputs, outputs = list(inputs) if type(inputs) in (tuple, list) else [[0]], list(outputs) if type(outputs) in (tuple, list) else [[0]]
            if type(inputs[0]) not in (tuple, list): self.__one_dimensional = True
            self.__inputs, self.__outputs = self.__embedding(x=inputs), outputs
        except Exception as error: print('ERROR during training: '+str(error))
    def saveModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 4: path = 'SapiensKNN-Model.knn'
            if path[-4:].lower() != '.knn': path += '.knn'
            dataset = {"one_dimensional": int(self.__one_dimensional), "inputs": self.__inputs, "outputs": self.__outputs, "maximums": self.__maximums}
            from json import dumps
            model = dumps(dataset)
            from re import sub
            parameters = sub(r'[^0-9\s]', '', str(model).strip())
            parameters_count = len(parameters.split(chr(32)))
            if parameters_count < 1000: model_size = f'{parameters_count}P'
            elif parameters_count < 1_000_000: model_size = f'{parameters_count // 1000}K'
            elif parameters_count < 1_000_000_000: model_size = f'{parameters_count // 1_000_000}M'
            elif parameters_count < 1_000_000_000_000: model_size = f'{parameters_count // 1_000_000_000}B'
            else: model_size = f'{parameters_count // 1_000_000_000_000}T'
            binary_data = ''.join(format(ord(char), '08b') for char in model)
            binary_data = binary_data.replace('000', '2').replace('001', '3').replace('010', '4').replace('011', '5')
            binary_data = binary_data.replace('100', '6').replace('101', '7').replace('110', '8').replace('111', '9')
            if path[-4:].lower() == '.knn': path = path[:-4]+f'-{model_size}.knn'
            with open(path, 'w', encoding='utf-8') as file: file.write(binary_data)
        except Exception as error: print('ERROR during saving model: '+str(error))
    def loadModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 4: path = 'SapiensKNN-Model.knn'
            if path[-4:].lower() != '.knn': path += '.knn'
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
            self.__one_dimensional, self.__inputs, self.__outputs, self.__maximums = dataset['one_dimensional'], dataset['inputs'], dataset['outputs'], dataset['maximums']
        except Exception as error: print('ERROR during loading model: '+str(error))
    def transferLearning(self, transmitter_path='', receiver_path='', rescue_path=''):
        try:
            transmitter_path, receiver_path, rescue_path = str(transmitter_path).strip(), str(receiver_path).strip(), str(rescue_path).strip()
            from os import path
            if len(transmitter_path) <= 0 or len(receiver_path) <= 0 or not path.exists(transmitter_path) or not path.exists(receiver_path): return
            self.loadModel(path=transmitter_path)
            from copy import deepcopy
            inputs, outputs, maximums = deepcopy(self.__inputs), deepcopy(self.__outputs), deepcopy(self.__maximums)
            self.loadModel(path=receiver_path)
            self.__inputs, self.__outputs, self.__maximums = self.__inputs+inputs, self.__outputs+outputs, [max((x, y)) for x, y in zip(self.__maximums, maximums)]
            self.saveModel(path=rescue_path)
        except Exception as error: print('ERROR during transferring learning: '+str(error))
    def predict(self, inputs=[]):
        try:
            outputs = []
            inputs = list(inputs) if type(inputs) in (tuple, list) else [[0]]
            if len(inputs) <= 0: inputs = [[0]]
            inputs = self.__embedding(x=inputs)
            from math import sqrt
            from collections import Counter
            for input in inputs:
                differences, nearest_neighbors = [], []
                for self_input in self.__inputs:
                    difference = sum([sqrt((a-b)**2) for a, b in zip(input, self_input)])
                    differences.append(difference)
                if self.__k <= 1: nearest_neighbors = [differences.index(min(differences))]
                else: nearest_neighbors = sorted(range(len(differences)), key=lambda i: differences[i])[:self.__k]
                labels = [self.__outputs[int(k)] for k in nearest_neighbors]
                if self.__regression:
                    try: calculation_result = sum(labels)/len(labels)
                    except:
                        try:
                            transposed_matrix = list(map(list, zip(*labels)))
                            calculation_result = [sum(x)/len(x) for x in transposed_matrix]
                        except: calculation_result = self.__outputs[differences.index(min(differences))]
                else: calculation_result = most_common_element = max(labels, key=lambda x: labels.count(x) if isinstance(x, (tuple, list)) else Counter(labels)[x])
                outputs.append(calculation_result)
            return outputs
        except Exception as error:
            print('ERROR during prediction: '+str(error))
            return []
    def test(self, inputs=[], outputs=[]):
        try:
            results = self.predict(inputs=inputs)
            total = min((len(outputs), len(results))) if len(outputs) != len(results) else len(outputs)
            hits = sum(x == y for x, y in zip(results, outputs))/total
            misses = 1-hits
            return {"hits": hits, "errors": misses}
        except Exception as error:
            print('ERROR during testing: '+str(error))
            return {"hits": 0, "errors": 1}
