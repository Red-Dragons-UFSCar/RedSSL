import numpy as np
import codecs, json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

file_path = './constants/filter_parameters.json'

logger = True

dt = 1/60

parameters = dict()

# Matriz da covariancia do ruido do processo
# -> indica a confiança no processo do filtro que, neste caso, assume velocidade como constante,
#    aumentar os valores do filtro reduz a confiança no processo e vice versa
parameters['Q'] = np.array([[(1.0 / 2) * (np.power(dt, 3)), 0                            , (1.0 / 1) * (np.power(dt, 2)), 0                            ],
                            [0                            , (1.0 / 2) * (np.power(dt, 3)), 0                            , (1.0 / 1) * (np.power(dt, 2))],
                            [(1.0 / 1) * (np.power(dt, 2)), 0                            , np.power(dt, 1)              , 0                            ],
                            [0                            , (1.0 / 1) * (np.power(dt, 2)), 0                            , np.power(dt, 1)              ]])

# Matriz da covariancia do ruida da medicao
# -> indica a confiança nas medidas que o filtro recebe como entrada, neste caso, as posições dos robôs,
#    aumentar os valores do filtro reduz a confiança nas medições e vice versa
parameters['R'] = np.array([[0.01, 0   ],
                            [0   , 0.01]])

# Matriz da covariancia do estado do filtro
# -> indica a confiança no estado atual do filtro e é atualizado com as iterações sobre o filtro,
#    seu primeiro valor indica a confiança no estado inicial do filtro
parameters['P'] = np.array([[10, 0 , 0  , 0  ],
                            [0 , 10, 0  , 0  ],
                            [0 , 0 , 100, 0  ],
                            [0 , 0 , 0  , 100]])

# parameters['Q'] = np.ones([4, 4])
# parameters['R'] = np.ones([2, 2])
# parameters['P'] = np.ones([4, 4])

with open(file_path, "w") as write_file:
    json.dump(parameters, write_file, cls=NumpyEncoder)

with open(file_path, "r") as read_file:
    json_load = json.load(read_file)

if logger:
    for param in json_load:
        if (parameters[param] == np.asarray(json_load[param])).all():
            print(f'Parâmetro {param} salvo e recuperado com sucesso')
        else:
            print(f'Falha ao salvo e/ou recuperado o parâmetro {param}')