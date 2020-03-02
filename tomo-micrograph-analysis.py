#!/fbs/emsoftware2/env-modules/install/anaconda/2018.12/bin/python

# micrograph analysis of tomography files with the naming conventions from serialEM and tomo-rename
# update 20190212 - MGI
    # naming convention seems to have changed
    # new convention MotionCorr/job002/Raw_data/060219_50PDMS_2_018[-34_00]-80236.mrc
    #                                           tomo name------    tilt----
    # EPA estimated resolution was removed
    # updated for relion 3
    # made output a bit cleaner looking, removed screen barf
    # fixed naming issues
    ### NEEDS TO  BE TESTED ON PHASE SHIFT DATA
    
import sys
import warnings
vers = '0.4'
# check for matplot lib
warnings.filterwarnings("ignore", module="matplotlib")
try:
    import matplotlib.pyplot as plt
except ImportError:
    sys.exit('ERROR: matplotlib is not installed ')
if len(sys.argv) != 2:
    sys.exit('USAGE: tomo-micrograph-analysis.py <ctf star file>')
    
###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        else:
            if len(i.split()) > 0:
                data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#
# get the data from the starfile - decide if to use phase shift
(labels,header,data) = read_starfile(sys.argv[1])
if '_rlnPhaseShift ' in labels:
    phaseshift = True
else:
    phaseshift = False
## make a dict of the tmograms
#tomograms = {}              #{name:[tilt,defocusU defocusV,estimatedres,phaseshift],[for each frame]}
#for i in data:
#    tomosplit = i[labels['_rlnMicrographName ']].split('/')[-1]
#    namesplit = tomosplit.split('_')
#    tomoname = '_'.join(namesplit[0:2])
#    if tomoname not in tomograms:
#        if phaseshift == True:
#            tomograms[tomoname] = [(tomosplit.split('_')[3].replace('p','.'),i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']], i[labels['_rlnCtfMaxResolution ']],i[labels['_rlnPhaseShift ']])]
#        else:
#            tomograms[tomoname] = [(tomosplit.split('_')[3].replace('p','.'),i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']], i[labels['_rlnCtfMaxResolution ']])]
#    else:
#        if phaseshift == True:
#            tomograms[tomoname].append((tomosplit.split('_')[3].replace('p','.'),i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']], i[labels['_rlnCtfMaxResolution ']],i[labels['_rlnPhaseShift ']]))
#        else:
#            tomograms[tomoname].append((tomosplit.split('_')[3].replace('p','.'),i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']], i[labels['_rlnCtfMaxResolution ']]))
# make a dict of the tmograms - removed references to EPA resolution
tomograms = {}              #{name:[tilt,defocusU defocusV,phaseshift],[for each frame]}
for i in data:
    tomosplit = i[labels['_rlnMicrographName ']].split('/')[-1]         # naming convention has changed .... 
    
    #namesplit = tomosplit.split('_')
            
    tiltsplit1 = tomosplit.split('[')                             # new way of finding tilt with new naming convention
    tilt = tiltsplit1[1].split(']')[0].replace('_','.')           # 
    namesplit = tiltsplit1[0].split('_')[:-1]    
    tomoname = '_'.join(namesplit)                             # changed to [0:3] for new naming convention
    if tomoname not in tomograms:
        if phaseshift == True:
            tomograms[tomoname] = [(tilt,i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']],i[labels['_rlnPhaseShift ']])]   # removed '_rlnCTFMaxResolution'
        else:
            tomograms[tomoname] = [(tilt,i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']])]                                # removed '_rlnCTFMaxResolution'
    else:
        if phaseshift == True:
            tomograms[tomoname].append((tilt,i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']],i[labels['_rlnPhaseShift ']])) # removed '_rlnCTFMaxResolution'
        else:
            tomograms[tomoname].append((tilt,i[labels['_rlnDefocusU ']],i[labels['_rlnDefocusV ']]))                            # removed '_rlnCTFMaxResolution'
#----- function: sort a dic by tilt ------------------------#
def sort_dic_tilt(dictionary):
    sorteddic = []
    keys = dictionary.keys()
    keys.sort()
    for i in keys:
        sorteddic.append(dictionary[i])
    return(keys,sorteddic)
#-----------------------------------------------------------#
#------ function make the graphs for a tomogram ------------#
def make_tomo_graph(name):
    defocusUdic = {}
    defocusVdic = {}
    astigdic = {}
    tilt = []
    #resolutiondic = {}                             # removed
    phaseshiftsdic = {}
    meanDFdic = {}
    
    print(name)
    for i in tomograms[name]:
        #print(i)
        thetilt = float(i[0])
        tilt.append(thetilt)
        defocusUdic[thetilt] = float(i[1])/10000
        defocusVdic[thetilt] = float(i[2])/10000
        astigdic[thetilt] = abs(float(i[1])-float(i[2]))/10000
        #resolutiondic[thetilt] = float(i[3])                    # removed 
        meanDFdic[thetilt] = (float(i[1]) + float(i[2]))/20000
        if phaseshift == True:
            phaseshiftsdic[thetilt] = float(i[3])                  # changed to i[3] becuase there's one fewer catagory now
    
    #defocus graph
    tilt,meanDF = sort_dic_tilt(meanDFdic)
    tilt,DFU = sort_dic_tilt(defocusUdic)
    tilt,DFV = sort_dic_tilt(defocusVdic)
    tilt,astig = sort_dic_tilt(astigdic)
    if phaseshift == False:                         # made pretty
        plt.subplot2grid((1,1), (0, 0))             #
    else:                                           #
        plt.subplot2grid((2,1), (0, 0))             #
    plt.title(name)
    plt.plot(tilt,meanDF,label='defocus')
    plt.scatter(tilt,DFU,s=10,c='blue')
    plt.scatter(tilt,DFV,s=10,c='red')
    plt.plot(tilt,astig,color='red',label='astigmatism')
    plt.xlabel('Tilt',fontsize=10)
    plt.ylabel('micron',fontsize=10)
    plt.grid()
    plt.legend(loc='best')    
    
    ##resolution graph                              # removed
    #tilt,res = sort_dic_tilt(resolutiondic)        #
    #plt.subplot2grid((2,3), (1, 0))                #
    #plt.plot(tilt,res)                             # 
    #plt.xlabel('Tilt',fontsize=10)                 #
    #plt.ylabel('Estimated resolution (Angstrom)',fontsize=10)
    
    # phase shift graph
    if phaseshift == True:
        tilt,PS = sort_dic_tilt(phaseshiftsdic)
        plt.subplot2grid((2,1), (1, 0))
        plt.plot(tilt,PS)
        plt.xlabel('Tilt',fontsize=10)
        plt.ylabel('Phase shift (degrees)',fontsize=10)    
        plt.grid()
    plt.tight_layout()
    plt.savefig('{0}.png'.format(name))
    plt.close()
#-----------------------------------------------------------#
print('{0} Tomorgrams'.format(len(tomograms.keys())))               # added informative output
print('Phase shift = {0}'.format(phaseshift))                       #
for i in tomograms:
    make_tomo_graph(i)
    
