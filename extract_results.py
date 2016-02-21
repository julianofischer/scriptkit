#TODO: Ler os arquivos de cada diretório e criar um json baseado no formato a seguir:


''' IndividualNodeBufferOccupancyReport
 { id : { time: buffer occupancy } }

 obter: 1. Evolução da ocupação média (excluindo nós maliciosos) [hardcoded]
        2. Evolução para cada nó (mais fácil)

        OBS.: Fazer em outro arquivo para compartilhar este com a comunidade

'''


'''
formato total

{ label : {
           x1: { label: [values] }
           x2:   ...
           x3:   ...
           x4:   ...
           ...   ...
           xx:   ...
          }

}

'''

'''
formato do arquivo:

ylabel: sabe-se antecipadamente
xlabel: obtém-se via argumento

{ xlabel:xlabel,
  ylabel:ylabel,
  linhas: [label : 'label',
           xs : [], ys: [],
           confidences: []
          ]
}
'''

__author__ = 'juliano'

import matplotlib
matplotlib.use('Qt4Agg')
import constants
import argparse, os, sys, json
import pprint
import statistics
from math import sqrt
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
help_msg = '''The dirs to extract results from and the label assigned to it. E.g. --dir /home/var1 MyVar1
              --dir /home/var2/ MyVar2'''
parser.add_argument('-d','--dir', nargs=2, help=help_msg, action='append', required=True, metavar= ("DIR","LABEL"))

#If omitted, it uses the name of the folder structure
#parser.add_argument('--x-tics', nargs='+', help="Labels for X tics.", required=False)
parser.add_argument('-x','--x-label', type=str, help="Label for X axis.", required=False, default='not set')
parser.add_argument('--grayscale', dest='grayscale', action='store_true', required=False, help="Pass this argument if "
                                                                                               "grayscale images are "
                                                                                               "needed. This argument "
                                                                                               "overlaps any value passe "
                                                                                               "to --style")

parser.add_argument('--file-extension', dest='file_extension', default='png', type=str, choices=['jpg','png','ps','eps',
                                                                                            'tif','tiff','svg','jpeg',
                                                                                                 'pdf'])

parser.add_argument('--style', default='classic', type=str, choices = ['seaborn-darkgrid', 'seaborn-notebook', 'classic',
                                                                       'seaborn-ticks', 'dark_background', 'bmh',
                                                                       'seaborn-talk', 'grayscale','ggplot',
                                                                       'fivethirtyeight', 'seaborn-colorblind',
                                                                       'seaborn-deep', 'seaborn-whitegrid',
                                                                       'seaborn-bright','seaborn-poster','seaborn-muted',
                                                                       'seaborn-paper', 'seaborn-white',
                                                                       'seaborn-pastel','seaborn-dark',
                                                                       'seaborn-dark-palette'])

args = parser.parse_args()

dirs = args.dir
xlabel = args.x_label

def check_args():
    if args.grayscale:
        print ('[style] grayscale')
    else:
        print('[style] %s' % args.style)

    print ('[xlabel] %s' % args.x_label)
    print ('[file extension] %s' % args.file_extension)
    #print ('[x tics] %s' % args.x_tics)
    print ('[dirs] %s' % str(args.dir))



#le os valores de um arquivo único
def read_values(file):
    d = {}

    lines = [l.strip() for l in open(file, 'r')]
    lines = lines[1:-2] #ignore the first and last two lines

    for line in lines:
        line = line.split()
        label = line[0][:-1]
        value = line[1]
        d[label] = value

    return d

#faz a junção dos valores obtidos pelo método anterior
#visto que é necessário todos os valores para uma mesma variável

#extract information from one dir
def read_dir(directory):
    files = [f for f in os.listdir(directory) if "MessageStatsReport" in f]

    values = {}
    for file in files:
        v = read_values(directory+"/"+file)

        for k, value in v.items():
            if k not in values:
                values[k] = {"values" : []}

            values[k]["values"].append(value)

    return values

def read_dirs (directory):
    '''
    :param directory:
    :return:
    '''
    dirs = [file for file in os.listdir(directory) if os.path.isdir(directory+"/"+file)]

    d = {}

    for thedir in dirs:
        values = read_dir(directory+"/"+thedir)
        d[float(thedir)] = values

    return d

def assertions(values):
    sim_time_list = values['sim_time']["values"]
    created = values['created']["values"]

    #check if all the values are equal
    assert  sim_time_list.count(sim_time_list[0]) == len(sim_time_list), "distinct sim_time for simulations"

    #since the number of runs is the same, are metric must have the same number of values
    sizes = [len(v) for v["values"] in values.values()]
    assert sizes.count(sizes[0]) == len(sizes), "Distinct number of simulation metrics"

    #check if the number of messages created is equal for every simulation run
    assert created.count(created[0]) == len(created), "Distinct number of messages created"

def calc_statistics(dictionary):
    for v in dictionary.values():
        for n in v.values():
            for k, m in n.items():
                converted = list(map(float, m["values"]))
                n[k]["mean"] = statistics.mean(converted)
                n[k]["variance"] = statistics.variance(converted)
                n[k]["std"] = statistics.stdev(converted)
                n[k]["confidence"] = calc_confidence(converted, n[k]["variance"])

def test_statistics():
    x = [0.9500, 0.9410, 0.9470, 0.9350, 0.9450, 0.9450, 0.9450, 0.9510, 0.9480, 0.9490]
    print (statistics.mean(x))
    print (statistics.stdev(x))
    print (statistics.variance(x))
    print (calc_confidence(x, statistics.stdev(x)))

#computes confidence interval using t-Student distribution
def calc_confidence(lista, stdev):
    degrees_of_freedom = len(lista) - 1
    try:
        value = constants.ic_95[degrees_of_freedom]
        confidence_value = value * (stdev/sqrt(len(lista)))
        return confidence_value
    except:
        print("Unable to compute for %d samples [1,35]" % len(lista))

def extract_from_dict(dictionary, var):
    result = {}

    for k,v  in dictionary.items():
        if k not in result:
            result[k] = {'xs':[], 'ys':[], 'confidences': []}

        for x in v:
            if x not in result[k]['xs']:
                result[k]['xs'].append(x)

            for y in v[x]:
                if y == var:
                    result[k]['ys'].append(v[x][y]['mean'])
                    result[k]['confidences'].append(v[x][y]['confidence'])
                    break

    return result


def test_styles(dictionary):
    styles = ['seaborn-darkgrid',
              'seaborn-notebook',
              'classic',
              'seaborn-ticks',
              'dark_background',
              'bmh',
              'seaborn-talk',
              'grayscale',
              'ggplot',
              'fivethirtyeight',
              'seaborn-colorblind',
              'seaborn-deep',
              'seaborn-whitegrid',
              'seaborn-bright',
              'seaborn-poster',
              'seaborn-muted',
              'seaborn-paper',
              'seaborn-white',
              'seaborn-pastel',
              'seaborn-dark',
              'seaborn-dark-palette']

    for s in styles:
        print_graph(dictionary, s)

def print_graph(dictionary, style=args.style, xlabel=xlabel, ylabel='ylabel', filename='name'):

    filename = filename + "." + args.file_extension

    #grayscale override previous style
    if args.grayscale:
        style = 'grayscale'

    plt.style.use(style)

    for i, k in enumerate(dictionary.items()):
        label = k[0]
        d = k[1]
        first_x = int(d['xs'][0])
        last_x = int(d['xs'][-1])

        plt.xticks(range(first_x, last_x + 1))

        plt.errorbar(d['xs'], d['ys'], yerr=d['confidences'],
                     fmt=constants.MARKERS[i], ms=constants.MARKER_SIZE, label=label)


    xticks, xtickslabels = plt.xticks()
    # shift 5/4 a step to the left
    xmin = (5*xticks[0] - xticks[1])/4.
    # shaft 5/4 a step to the right
    xmax = (5*xticks[-1] - xticks[-2])/4
    plt.xlim(xmin, xmax)
    plt.xticks(xticks)

    yticks, ytickslabels = plt.yticks()
    ymin = (5*yticks[0] - yticks[1])/4.
    # shaft 5/4 a step to the right
    ymax = (5*yticks[-1] - yticks[-2])/4
    plt.ylim(ymin, ymax)
    plt.yticks(yticks)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend (loc='best') #same as loc=0
    plt.grid('on')
    plt.tight_layout()

    if args.file_extension == 'eps' or args.file_extension == 'ps' or 'pdf':
        plt.savefig(filename,dpi=400)
    else:
        plt.savefig(filename)


    plt.show()
    plt.close()

def save_json(json_v, directory, filename):
    filename = directory+"/"+filename

    with open(filename,'w') as f:
        j = json.dump(json_v,f)

#extract and save all vars
def extract_and_save(d):

    if not os.path.exists(constants.RESULT_DIR):
        os.makedirs(constants.RESULT_DIR)

    for k,v in constants.constants_readable.items():
        r = extract_from_dict(d, k)
        save_json(r, constants.RESULT_DIR, k)
        filename = k
        filename="/".join([constants.RESULT_DIR, filename])
        print_graph(r,ylabel=v,xlabel=xlabel,filename=filename)

'''
def save_raw(d):
    if not os.path.exists(constants.RESULT_DIR):
        os.makedirs(constants.RESULT_DIR)

    r  = {}

    for v in constants.constants_readable.keys():
        r[v] = {}

        for k, av in d.items():
            if k not in r[v]:
                r[v][k] = None

            for ak, av in av.items():
                print ("v==ak - %s == %s" % (v, ak))
                if v == ak:
                    r[v][k] = av

    print (r)
'''

def default_main_behavior():
    dic = {}
    matplotlib.rcParams.update({'font.size' : 12})

    for d in dirs:
        value = read_dirs(d[0])
        #store by label
        dic[d[1]] = value

    calc_statistics(dic) #modify the value of dic
    extract_and_save(dic)


def main():
    check_args()
    default_main_behavior()

    #r = extract_from_dict(dic, constants.DELIVERY_PROB)
    #print_graph(r, style='grayscale', filename='name.eps')
    #extract_and_save(dic) #extract and save all vars
    #print_graph(r)
    #print(r)
    #test_statistics()

if __name__ == '__main__':
    main()