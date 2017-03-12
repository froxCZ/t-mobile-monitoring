import matplotlib.pyplot as plt
from numpy.matlib import corrcoef, arange

import data_query
from config import config
from mediation.api import util

lobsData = [
  {"lobName": 'LTP',
   "data": [3, 1.0001500741307188, 1.000736829541002, 1.0007486242184784, 1.0003030991572663,
            1.0003030967295905, 1.0003325988617446, 3, 1.0002242001281143, 1.0007125320902952,
            1.000980160704198, 1.001692335762959, 0.2068621253497859, 1.000646471797984, 3,
            1.0006287357523085, 1.001252201365785, 1.0009107418226046, 1.0006804549736834,
            0.20674792240032494, 1.0007478684695283, 1]},
  {"lobName": 'M2M',
   "data": [1.0484468579784918, 1.0964284035167453, 1.206406849467235, 1.2185099973516949, 1.0534093936592017,
            1.1225285270095362, 0.9577704802931346, 1.0364809221160105, 0.9744075355192819, 1.04303023440154,
            1.000840419598585, 1.5309395115168098, 0.9481861582001658, 0.9810062239905214, 0.9942351275826409,
            0.9995721357067506, 1.144377760163062, 0.8492560898341184, 0.826109417781681, 0.8398438364858781,
            0.8479997619649791, 1]},
  {"lobName": 'OTA',
   "data": [1.1391062568338086, 1.169059709620443, 1.1244139145132386, 1.050929180900704, 0.9836082481765894,
            1.0195129423086555, 0.99398325071409, 0.9746266944896221, 0.7904316995802427, 0.27120626318782726,
            0.5730288927713794, 0.395031123781099, 0.8911830824165997, 0.9101461206395208, 1.025864916166528,
            1.0905780457212524, 0.6678668244557486, 0.9145399068383282, 0.7346923735613794,
            0.7116740630996835, 0.6838520923996474, 1]},
  {"lobName": 'XTC',
   "data": [1.032952676208933, 1.0651181273229675, 0.985032843504029, 1.0463296693460586, 0.9065594237470067,
            1.1033426478037605, 0.9845638411304785, 1.0828164243690384, 0.8858532852128135,
            0.9792213977164695, 1.0431777445557797, 0.8438298809887996, 0.8302940227651137,
            0.8334352517390138, 0.8322859630709941, 0.84716030252711, 0.7927888265947872, 0.8156047173019134,
            0.9550540677395851, 1.0427726466409535, 1.099879455328812, 1]},
  {"lobName": 'SMS',
   "data": [1.063802535871842, 1.0144607620478892, 1.0884094031553768, 1.0602182556313862, 1.0238181884194877,
            1.101255600796851, 0.9936232086426814, 0.9633439784681891, 0.9350118349751239, 2.4008297870648887,
            0.9132950692234707, 0.8595854995931297, 0.7747145458759027, 0.7417429517362583,
            0.7276582544664865, 0.7307333264950541, 1.1584860334179747, 1.1846393737424814,
            0.8485441335491846, 0.888739131793777, 1.0264946709211429, 1]},
  {"lobName": 'GSM',
   "data": [1.0250730908622343, 1.0227528665845813, 1.053740773043853, 1.0609626684907099, 1.0318892994284379,
            1.0074848712257196, 1.002167486174162, 0.9823800297203595, 0.9040134763624382, 1.5416556537704504,
            0.8138574618477883, 0.7913530477323473, 0.6601436575002679, 0.6678525400537635,
            0.6685882915310963, 0.6638798890923531, 1.0915695615462633, 1.097658793923133, 0.8263016827805155,
            0.9345000799342305, 1.0524605469052164, 1]},
  {"lobName": 'TIT',
   "data": [0.5, 3, 0.5, 0.33333333333333337, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1]},
  {"lobName": 'MMS', "data": [0.9697972901293209, 1.0096444353187182, 0.8500254337053174, 0.8886966214796698,
                              0.9640298164356447, 0.9849524687260285, 1.0253352429616147, 1.0941966195349562,
                              1.4395052199914038, 3, 1.1215421469731408, 0.8897950638976724,
                              1.0378473726591548, 0.8659531940247586, 0.9187856882959243, 1.027823727114375,
                              1.9071830317534073, 1.3379215757545193, 0.9340983259477821, 0.939721891807875,
                              1.0185010996608923, 1]},
  {"lobName": 'ACI',
   "data": [1.02187262644867, 1.0182491646630425, 1.0587572424974563, 1.055485930436303, 1.0366851749933153,
            1.0100798931296748, 0.9982356584766048, 0.9766636504529349, 0.9476912424931508, 2.206448030288809,
            0.8616689218867326, 0.8188325617517296, 0.6770311730775027, 0.6867963840381094,
            0.6837098320618191, 0.6759582304723903, 1.2314929394869247, 1.1817329616273935,
            0.8389039411742394, 0.9075282807562968, 1.0418241390989895, 1]},
  {"lobName": 'TAP',
   "data": [0.9885967991373551, 1.0860667773161072, 1.1128919354782754, 0.924618098708109, 0.6701590734483983,
            1.0478633095297851, 0.8928230422484189, 0.8151320462724964, 0.8522682089560154,
            0.5338247236645453, 0.6635039594937909, 0.34355384800515476, 0.5674854970661345,
            0.7542465471681692, 0.7522228035338332, 0.8698009480293456, 0.7058244485887003,
            0.5620178284458353, 0.5513524445765269, 0.5175901823258091, 0.5513874602630211, 1]},
  {"lobName": 'CIR',
   "data": [1.070098603329334, 0.817455176788755, 1.1331197694521258, 1.3661179717198393, 0.9203493480093887,
            0.9582169327688488, 1.0266070423560814, 0.8122437886140058, 0.5272862205096831,
            0.5117677301057868, 0.4308010456904288, 0.3992631195407671, 0.45285775972886866,
            0.41578280514706406, 0.4499477773484942, 0.3797348506950036, 0.5501062426079711,
            0.8773792738808601, 0.8629275124338318, 1.0392411851327823, 1.105016584179251, 1]},
  {"lobName": 'WHS',
   "data": [1.0465788814722519, 1.0608210577885793, 1.0141572480675947, 1.027842663764324, 1.015983752509963,
            1.1032582159296398, 1.0007351657768344, 1.1404184441939094, 0.9674558435372712,
            1.2682863857635542, 0.9905346096155682, 0.9114278564883174, 0.8420561552253698,
            0.8215865259008855, 0.8216659157580155, 0.8439288684893064, 1.033958298561294, 1.1487582048263545,
            0.8264155353853649, 0.9267669635247769, 1.0105703945587543, 1]},
  {"lobName": 'MNT',
   "data": [1.0241616010653332, 1.012768714743101, 1.0158715046034028, 1.019923186139482, 0.7305753544747675,
            1.02997312852569, 1.0132522298746753, 1.0008185615897032, 0.9915249457088868, 0.9535613295122393,
            1.2529912325941206, 0.7468508592248619, 0.6968111609367215, 0.7908311475872183,
            0.8088623779037519, 0.7956042301757555, 0.8073806780855176, 1.0611488176954362,
            0.6968791925627789, 1.1184281638084834, 1.130643483516292, 1]},
  {"lobName": 'TOC', "data": [1.0313150097151367, 1.0600265406315057, 1.0199478235251758, 1.0797630182721303,
                              0.8617841227481503, 0.9738849288462293, 0.9939528864726817, 0.9975280051611066,
                              0.9806355026594856, 0.9037698754585447, 0.9240928503711889, 0.9103732878466232,
                              0.8932266307917598, 1.0686124020962486, 1.046226612898262, 1.1246407484430656,
                              1.1115332332212375, 1.4898889297238875, 1.084204776916775, 1.1369392100107096,
                              1.1506164997622323, 1]},
  {"lobName": 'TCF', "data": [1.0271777695779285, 0.9798639956611044, 0.9924578713855419, 1.0106605729352127,
                              1.0247326481016867, 1.021415673607012, 0.9537814578879399, 0.9807352598436516,
                              0.9740254365578095, 1.0105736388245856, 1.0029823330187364, 0.9491515949845548,
                              0.9799078424405864, 1.0521321366385883, 1.035630504681807, 1.01303248245012,
                              1.0170563273860915, 0.9358866682368892, 0.921268727841104, 1.0081131172426505,
                              1.0003458824021862, 1]},
  {"lobName": 'VMS',
   "data": [0.95, 0.8947368421052632, 1, 0.6666666666666667, 1.263157894736842, 1.1578947368421053, 1, 0.95,
            1, 0.9375, 1.1818181818181819, 1.1666666666666667, 0.8, 0.8, 0.7894736842105263,
            0.736842105263158, 0.625, 0.9230769230769231, 0.8947368421052632, 1.1764705882352942,
            0.8947368421052632, 1]},
  {"lobName": 'VOP', "data": [1, 1, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
  {"lobName": 'PCF',
   "data": [1.018572003969978, 1.0396053984489286, 1.0291072652948738, 1.0238064111300202, 0.9955754340252458,
            1.0234924257567481, 0.9785761052889057, 0.9767435207761473, 0.9396179672149693,
            1.0483071404848292, 1.0299700209888294, 0.9272019251921271, 0.9369143117639024, 0.901042698575755,
            0.9064391085560024, 0.8923273499588672, 0.9809218663384062, 0.9860284533576034,
            0.9256002216678509, 1.0357396454855607, 1.0202762786965, 1]},
  {"lobName": 'SIS',
   "data": [1.01519341675788, 0.9930902118712136, 1.02876839922265, 1.0366997578029693, 1.0108041757986204,
            1.0061352555150396, 0.9780229595106439, 0.9625416272228556, 1.0473921143759377, 3,
            1.136806815681272, 0.9282931731713381, 0.8107179774309278, 0.7978338537668311, 0.7744007143138288,
            0.7813467976996669, 1.3139484048522312, 1.5899596649154857, 0.8707873124894051,
            0.9468545188426255, 1.0267395769488246, 1]},
  {"lobName": 'RRA', "data": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
  {"lobName": 'BVS',
   "data": [0.9477194588319134, 0.8655111652979679, 3, 1.3006898918032217, 1.0561343552109523,
            0.9251313799388621, 0.8887011357615616, 0.7608416767100752, 0.43477218264802653,
            0.6402514820117884, 0.7018226922111028, 3, 0.47076175507339746, 0.458420812931122,
            0.4619713209715238, 0.3868839851207432, 0.7569788566949117, 0.8736325753142159,
            1.1831518341189178, 1.2580477705390427, 1.261232970749009, 1]},
  {"lobName": 'EPC', "data": [1.0126439856398148, 1.0233858768941109, 0.9969790404415368, 1.0115845237857402,
                              1.0029617671394457, 1.004881306538, 1.0039627830086215, 0.9964238930408419,
                              0.9488993219521427, 0.9505196031635414, 0.9936363464595204, 0.9614799365516908,
                              0.9221108113075724, 0.928386500381433, 0.9326949164565899, 0.9353040188617474,
                              1.0006899251005255, 1.0409016925090855, 0.955597145085123, 1.0373479534144558,
                              1.0520327622990497, 1]},
  {"lobName": 'SBC',
   "data": [1.0179472264145424, 1.005072200757835, 1.10358105398002, 1.1425521017855038, 1.0297948360705236,
            1.0437124750024387, 1.0266029438990918, 0.9819222215903646, 0.8004022719053583,
            0.8791818190401006, 0.7687731240712268, 0.9240053790067688, 0.5887594356837744,
            0.6109889993956448, 0.617818096189973, 0.6046417227234346, 1.0279525420836453, 1.2643433207851886,
            0.8080552280121766, 1.0927837592837548, 1.1570536525372015, 1]},
  {"lobName": 'EWH',
   "data": [0.9057142857142857, 0.834054834054834, 1, 1, 1.665680473372781, 0.9292929292929293,
            0.908284023668639, 0.8188622754491018, 0.5812883435582822, 3, 1, 0.8394495412844036,
            0.5838509316770186, 0.6151419558359621, 0.6042345276872965, 0.5588235294117647, 3, 1,
            1.303473491773309, 1.3272394881170018, 1.3053016453382085, 1]},
  {"lobName": 'MWB',
   "data": [1.028754699563755, 1.0239697354311517, 1.057241118603757, 1.058220785162893, 1.0213482855992742,
            1.0184288686183298, 0.9997087063107046, 0.9794718725283431, 0.9179959272307153, 1.774049289138556,
            0.8366908443534534, 0.808588298845024, 0.6849845219843043, 0.6850167512962171, 0.6817220416150447,
            0.6800983158826759, 1.1087332820251057, 1.1336484352915748, 0.8304387405164452,
            0.9218485864374494, 1.0469242037560706, 1]},
  {"lobName": 'SMG',
   "data": [1.067285242002993, 1.0402644695420495, 1.093851266601077, 1.0806540073187085, 1.0419740185879023,
            0.9975391977993021, 0.9707264900239215, 0.9237808201937249, 0.8803411621776898, 2.233760603764576,
            0.9284709656191604, 1.055733424570058, 0.7801461079839338, 0.7750268791085073, 0.7711260660414474,
            0.7917889238026722, 1.2475830522841647, 1.362697587262841, 0.937892125115673, 1.0577903535607887,
            1.0918595239830824, 1]},
  {"lobName": 'KPI', "data": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
  {"lobName": 'ICG',
   "data": [0.9798489795984063, 0.8581705940868567, 1.001635667813602, 0.9974209543710949, 1.0555000885212054,
            0.9380804248022879, 0.8923833350124889, 0.7480988064031435, 0.41826192943484763,
            0.5027533976741481, 0.5811905292941031, 0.47187114013079356, 0.470494199279379,
            0.49711563147577115, 0.49995301778995793, 0.44575744142703544, 0.7298914176716808,
            0.6807867556028697, 1.1784667596811589, 1.2715404781560184, 1.3211547914322228, 1]},
  {"lobName": 'PPC',
   "data": [1.044762356869006, 1.0984022423588973, 1.0632166976251798, 1.0973021070934714, 1.0530652572134263,
            1.0581624575906792, 1.0746421173206937, 1.0956168292235628, 1.1355650901926304, 1.897116737845239,
            1.0115779422965112, 0.9019568493659925, 0.8223512787473676, 0.8186280378420259,
            0.8119124116231919, 0.8243094484719963, 1.19475036836537, 1.1932909903391213, 0.8401549053598285,
            0.847245464474436, 1.031434967393417, 1]},
  {"lobName": 'RES',
   "data": [1.006298754521198, 1.013430727972369, 1.0115554206123867, 1.0310575572648457, 1.004833485342551,
            1.0139961750765596, 1.002207323278802, 1.0182459426393686, 1.0093769825649266, 1.0038600850976378,
            1.0038843983631864, 1.0187443232566777, 0.9874381192298082, 1.00779376903699, 1.0136171821723483,
            1.0081292198577756, 1.0672168583639459, 1.0098475641796032, 0.9831996868624313,
            1.0042841937914042, 0.9839848278727525, 1]},
  {"lobName": 'MTS',
   "data": [1.0334577559617066, 1.0279071463068128, 1.055819673902175, 1.0640576879403167, 1.0430714492478292,
            1.0295993002889368, 1.0327412877214817, 1.0045419119188685, 0.8743983331651766, 0.920115083954218,
            0.8963204483044813, 0.9832361989833713, 0.7176796540487163, 0.7277737617994646,
            0.7350921360102042, 0.7256011381229203, 1.0283528026556432, 1.0784484853248324,
            0.8752693764822699, 1.0568292246716309, 1.1077642103619518, 1]},
  {"lobName": 'SCF',
   "data": [1.0213622397199387, 1.0216914635504966, 1.22486191051017, 1.0421275125926523, 1.036449967487539,
            1.022590865392599, 1.0245159412339475, 1.00006045251036, 0.882320339950107, 0.9110920812110389,
            0.8990191238983304, 1.0736900109275975, 0.7410277919021928, 0.7509900762751359,
            0.7579202117540721, 0.7487077830145565, 1.0068416145749073, 1.0617640608493935,
            0.8778502763307404, 1.0473372505764227, 1.0893466042837943, 1]},
  {"lobName": 'DWA',
   "data": [1.027109056231988, 1.0227026411089868, 1.0560145722799168, 1.0608957656960631, 1.0290808502063589,
            1.0099868101974625, 1.0027654853827817, 0.9814972645063643, 0.9099956015682067,
            1.6439632558688602, 0.8187118148820904, 0.799938242881235, 0.6639136224811569, 0.6706895022731061,
            0.6718280617168788, 0.668664605067464, 1.0986748582379864, 1.1234929944846272, 0.8270270034648204,
            0.9296071394189257, 1.0511349806440013, 1]},
  {"lobName": 'ATS', "data": [0.9587738038950148, 0.9216705324329235, 0.9715334172464981, 0.9716188152233044,
                              1.1004737834134393, 1.1760765058369442, 1.0223719805917304, 1.0746937230957987,
                              1.5379550856255795, 2.4967811214887394, 1.0322382110820525, 0.8750833384303104,
                              0.9351116323393887, 0.9316203882420373, 0.8876043139977815, 1.0547320054416707,
                              1.4940260575959783, 1.2209902069335916, 0.8958909194577681, 0.8491333608287595,
                              0.8913731163815807, 1]},
  {"lobName": 'WEL', "data": [1.0281910461009065, 1.0136753853683287, 1.0027949039129838, 1.0432368126756202,
                              0.8619514047662193, 0.9002907064866645, 0.866489109650183, 0.8002825595652635,
                              0.6950119971300562, 0.444051816684957, 0.6856118356800814, 0.3995007378779385,
                              0.8760696800918556, 1.001436105502735, 1.0561984581892903, 1.06123397911515,
                              0.7794046759425958, 0.9081046924551507, 0.6932925790204156, 0.7267103080250902,
                              0.7500996036912403, 1]},
  {"lobName": 'PST', "data": [1.0053506263588279, 0.9884984616167531, 1.0593362413264185, 1.0760251831498369,
                              1.0231310000601692, 0.991294723535605, 0.9914115099799333, 0.9417176769186425,
                              0.7473790831591209, 1.000911380996422, 0.8482498382452137, 0.7104468036410383,
                              0.5474608626259305, 0.5620854225841376, 0.5624253362413503, 0.537464387955453,
                              0.8812749640767757, 1.231734864295313, 0.8235080538757483, 1.072404977597064,
                              1.1418942018162448, 1]},
  {"lobName": 'DAR',
   "data": [0.9958272244603938, 1.0027030805632184, 0.948859489047194, 0.9626678792159733, 0.9890522264344703,
            0.9917198236903131, 0.9900539386574569, 0.9768790448978295, 0.9265307691787227,
            1.0189091595285058, 0.9580810121005495, 0.8962113807910338, 0.9025984457499139,
            0.9017314857001582, 0.9066055541600218, 0.9065311268259822, 0.9983750009797012, 1.053273216829667,
            0.9431545867671056, 1.042199291251676, 1.0512797547094825, 1]},
  {"lobName": 'LAS', "data": [1.1678654748984216, 0.9757689897052867, 1.1673959995374714, 1.1003025296462585,
                              1.0385051857815315, 1.2088075635158375, 0.9881772385114214, 0.9356260904440574,
                              0.7077053058503675, 0.7822982241805494, 0.7618263051111293, 0.8128865357023669,
                              0.7316606142291391, 0.6847395165062086, 0.6560257705412892, 0.6647498305813742,
                              0.796042342418818, 0.9346540748162848, 0.7939754809772508, 0.962470501562014,
                              0.9929573860362824, 1]},
  {"lobName": 'EWG',
   "data": [0.9761478362504887, 0.9583614156352167, 1.2336652720530112, 1.1580357149388305, 1.090568389327002,
            0.9600084918076629, 0.9568424857376663, 0.8256895883325289, 0.5914861789815206,
            1.0121511182076122, 0.8653533492971078, 0.5704172842604073, 0.538653445993039, 0.5164638232491638,
            0.4858079169661382, 0.41779533433377064, 0.7993573176963311, 0.9092267083181577,
            1.007730199059085, 1.0702191864202208, 0.9082408024540793, 1]},
  {"lobName": 'TPP', "data": [0.9994509893629189, 0.9329863891112891, 0.8681779342746304, 0.8697074230973179,
                              0.8752423267949921, 0.8735428814090898, 0.872957061838658, 0.8761341580186848,
                              0.8998970751542529, 0.8653601909437505, 0.8668891761965745, 0.7537979083127982,
                              0.9302389942504077, 0.9967766261759137, 0.9968273519280757, 0.9897328514978554,
                              0.8680083180866294, 0.9732343917814772, 0.9873704480552615, 0.9832499869540516,
                              0.9831210955086642, 1]}]


def getdayDifference(lobName, granularity=0):
  fromDate = util.jsStringToDate("2016-12-15T00:00:00.000Z").replace(hour=0, minute=0, second=0)
  toDate = util.jsStringToDate("2017-01-05T00:00:00.000Z").replace(hour=0, minute=0, second=0)
  response = {}
  mongoQuery = data_query.DateRangeGroupQuery(fromDate, toDate, [lobName], granularity)
  data = mongoQuery.execute()
  metrics = {}
  metricsList = mongoQuery.metrics
  metadata = mongoQuery.metadata
  data = data_query.medianDateRange(fromDate, toDate, lobName, granularity, data)
  return util.dateDataListToList(data, "dayDifference")


def lobData(lobName):
  for lobData in lobsData:
    if lobData["lobName"] == lobName:
      return lobData["data"]
  raise Exception("data not found " + lobName)


CZ_LOBS = config.getLobsConfig()["lobs"]["CZ"]
# CZ_LOBS = ["SMS", "GSM", "MMS","SMG","ATS","OTA"]


data = []
lobsNameList = []
for lob in CZ_LOBS:
  data.append(lobData(lob))
  lobsNameList.append(lob)

R = corrcoef(data)
print(R)
plt.pcolor(R)
plt.colorbar()
plt.yticks(arange(0.5, len(CZ_LOBS) + 0.5), CZ_LOBS)
plt.xticks(arange(0.5, len(CZ_LOBS) + 0.5), CZ_LOBS)
#plt.show()


def dendo():
  from matplotlib import pyplot as plt
  from scipy.cluster.hierarchy import dendrogram, linkage
  import numpy as np

  np.random.seed(4711)  # for repeatability of this tutorial
  a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100, ])
  b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50, ])
  X = R
  Z = linkage(X, 'ward')
  plt.figure(figsize=(25, 10))
  plt.title('Hierarchical Clustering Dendrogram')
  plt.xlabel('sample index')
  plt.ylabel('distance')
  print(Z.shape)
  def llf(id):
    if id >= 0 and id < len(lobsNameList):
      return lobsNameList[id]
    return str(id)
  dendrogram(
    Z,
    leaf_font_size=8.,  # font size for the x axis labels
    # labels=CZ_LOBS
    leaf_label_func=llf
  )
  plt.show()

dendo()
