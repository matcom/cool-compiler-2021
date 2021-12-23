
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programarroba case ccur class colon comma cpar div dot else equal esac false fi id if in inherits isvoid larrow less lesseq let loop minus new not nox num ocur of opar plus pool rarrow semi star string then true type whileprogram : class_listclass_list : def_class class_list\n                      | def_classclass_list : error class_listepsilon :def_class : class type ocur feature_list ccur semi \n                     | class type inherits type ocur feature_list ccur semidef_class : class error ocur feature_list ccur semi \n                     | class type ocur feature_list ccur error   \n                     | class error inherits type ocur feature_list ccur semi\n                     | class error inherits error ocur feature_list ccur semi\n                     | class type inherits error ocur feature_list ccur semi\n                     | class type inherits type ocur feature_list ccur errorfeature_list : epsilon\n                        | def_attr semi feature_list\n                        | def_func semi feature_listfeature_list : error feature_listdef_attr : id colon type\n                    | id colon type larrow exprdef_attr : error colon type\n                    | id colon error\n                    | error colon type larrow expr\n                    | id colon error larrow expr\n                    | id colon type larrow errordef_func : id opar formals cpar colon type ocur expr ccurdef_func : error opar formals cpar colon type ocur expr ccur\n                    | id opar error cpar colon type ocur expr ccur\n                    | id opar formals cpar colon error ocur expr ccur\n                    | id opar formals cpar colon type ocur error ccurformals : param_list\n                   | param_list_emptyparam_list : param\n                      | param comma param_listparam_list_empty : epsilonparam : id colon typelet_list : let_assign\n                    | let_assign comma let_listlet_assign : param larrow expr\n                      | paramcases_list : casep semi\n                      | casep semi cases_listcases_list : error cases_list\n                      | error semicasep : id colon type rarrow exprexpr : id larrow expr\n                | compcomp : comp less op\n                | comp lesseq op\n                | comp equal op\n                | opop : op plus term\n              | op minus term\n              | termterm : term star base_call\n                | term div base_call\n                | base_callterm : term star error\n                | term div errorbase_call : factor arroba type dot func_call\n                     | factorbase_call : error arroba type dot func_call\n                     | factor arroba error dot func_callfactor : atom\n                  | opar expr cparfactor : factor dot func_call\n                  | not expr\n                  | func_callfactor : isvoid base_call\n                  | nox base_callfactor : let let_list in exprfactor : case expr of cases_list esacfactor : if expr then expr else expr fifactor : while expr loop expr poolatom : numatom : idatom : new typeatom : ocur block ccuratom : error block ccur\n                | ocur error ccur\n                | ocur block erroratom : true\n                | falseatom : stringblock : expr semi\n                 | expr semi blockblock : error block\n                 | error semifunc_call : id opar args cparfunc_call : id opar error cpar\n                     | error opar args cparargs : arg_list\n                | arg_list_emptyarg_list : expr  \n                    | expr comma arg_listarg_list : error arg_listarg_list_empty : epsilon'
    
_lr_action_items = {'error':([0,3,4,5,10,11,12,13,15,25,29,30,31,32,33,34,36,37,38,39,55,58,62,63,66,70,80,81,82,83,85,86,87,90,98,100,102,103,104,105,106,107,110,112,113,114,115,116,117,118,119,120,121,122,135,136,141,142,145,151,154,162,164,171,173,174,175,176,180,181,182,183,184,185,189,190,193,194,195,201,207,215,219,229,],[4,4,4,9,15,21,15,23,15,39,15,15,50,52,15,15,15,15,-6,-9,-8,70,98,70,103,107,70,70,70,70,70,70,70,136,107,139,-7,-13,-12,-11,-10,107,145,70,154,70,70,70,70,70,162,164,166,169,178,107,-86,-87,185,107,185,107,107,70,70,201,70,70,70,207,70,70,169,185,145,-85,169,169,145,201,107,201,70,70,]),'class':([0,3,4,38,39,55,102,103,104,105,106,],[5,5,5,-6,-9,-8,-7,-13,-12,-11,-10,]),'$end':([1,2,3,6,7,38,39,55,102,103,104,105,106,],[0,-1,-3,-2,-4,-6,-9,-8,-7,-13,-12,-11,-10,]),'type':([5,11,13,27,31,61,89,94,100,101,108,121,218,],[8,20,24,40,49,96,134,137,138,140,143,165,227,]),'ocur':([8,9,20,21,23,24,58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,137,138,139,140,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[10,12,33,34,36,37,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,180,181,182,183,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,]),'inherits':([8,9,],[11,13,]),'ccur':([10,12,14,15,16,22,26,29,30,33,34,36,37,47,48,53,54,56,57,72,73,74,75,76,77,78,79,88,91,92,93,109,124,125,126,127,134,135,136,141,142,144,151,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,190,191,192,196,205,206,207,208,209,210,212,213,214,220,230,],[-5,-5,25,-5,-14,35,-17,-5,-5,-5,-5,-5,-5,-15,-16,66,67,68,69,-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,144,-66,-68,-75,-69,-76,177,179,144,-87,-78,-84,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-85,-88,-89,-70,221,222,223,224,225,-61,-59,-62,-71,-73,-72,]),'id':([10,12,15,28,29,30,32,33,34,36,37,58,60,62,63,70,80,81,82,83,84,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,122,136,145,151,154,162,164,171,172,173,174,175,176,180,181,182,183,184,185,189,193,194,195,201,207,215,219,229,],[19,19,19,46,19,19,46,19,19,19,19,72,46,72,72,72,72,72,126,126,46,72,72,72,72,72,72,72,72,72,126,126,126,126,126,126,126,168,72,72,72,72,72,72,72,46,72,202,72,72,72,72,72,72,168,72,72,168,168,72,202,72,202,72,72,]),'colon':([15,19,46,59,64,65,202,],[27,31,61,94,100,101,218,]),'opar':([15,19,58,62,63,70,72,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,126,136,145,151,154,162,164,168,169,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[28,32,80,80,80,110,113,80,80,80,80,80,80,80,80,110,110,80,80,80,80,80,80,80,80,80,80,113,110,110,80,110,110,110,113,195,80,80,80,80,80,80,80,80,110,80,80,110,80,80,]),'semi':([17,18,25,35,40,49,50,66,67,68,69,71,72,73,74,75,76,77,78,79,88,91,92,93,97,98,99,107,111,124,125,126,127,134,136,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,185,187,188,191,192,196,200,201,210,212,213,214,220,221,222,223,224,225,230,231,],[29,30,38,55,-20,-18,-21,102,104,105,106,-22,-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-19,-24,-23,142,151,-66,-68,-75,-69,-76,142,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,142,151,-90,-88,-89,-70,215,217,-61,-59,-62,-71,-73,-26,-25,-29,-28,-27,-72,-44,]),'cpar':([28,32,41,42,43,44,45,51,52,72,73,74,75,76,77,78,79,88,91,92,93,95,96,110,113,123,124,125,126,127,134,144,146,147,148,149,150,152,153,154,155,156,157,158,159,160,161,162,163,164,167,170,177,178,179,186,187,188,191,192,195,196,210,211,212,213,214,220,230,],[-5,-5,59,-30,-31,-32,-34,64,65,-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-33,-35,-5,-5,170,-66,-68,-75,-69,-76,-78,188,170,-91,-92,-96,-45,191,192,-93,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-95,-93,-90,-88,-89,-5,-70,-61,-94,-59,-62,-71,-73,-72,]),'larrow':([40,49,50,72,96,130,],[58,62,63,112,-35,173,]),'comma':([44,72,73,74,75,76,77,78,79,88,91,92,93,96,124,125,126,127,129,130,134,144,147,152,155,156,157,158,159,160,161,162,163,164,167,170,177,178,179,187,188,191,192,196,198,210,212,213,214,220,230,],[60,-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-35,-66,-68,-75,-69,172,-39,-76,-78,189,-45,189,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,189,-90,-88,-89,-70,-38,-61,-59,-62,-71,-73,-72,]),'not':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,]),'isvoid':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,]),'nox':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,]),'let':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,]),'case':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,]),'if':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,]),'while':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,]),'num':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,]),'new':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'true':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,]),'false':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,]),'string':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,]),'arroba':([70,72,73,74,75,76,77,78,79,88,91,92,93,98,107,124,125,126,127,134,136,144,145,152,154,156,157,158,159,160,161,162,163,164,167,170,177,178,179,185,188,191,192,196,207,210,212,213,214,220,230,],[108,-75,-46,-50,-53,-56,121,-67,-63,-74,-81,-82,-83,108,108,-66,-68,-75,-69,-76,108,-78,108,-45,108,-47,-48,-49,-51,-52,-54,108,-55,108,-65,-64,-77,-80,-79,108,-90,-88,-89,-70,108,-61,-59,-62,-71,-73,-72,]),'dot':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,143,144,152,156,157,158,159,160,161,162,163,164,165,166,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,122,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,184,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,193,194,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'star':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,119,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,119,119,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'div':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,120,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,120,120,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'plus':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,117,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,117,117,117,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'minus':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,118,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,118,118,118,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'less':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,114,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'lesseq':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,115,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'equal':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,116,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'of':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,131,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,174,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'then':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,132,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,175,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'loop':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,133,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,176,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,-72,]),'in':([72,73,74,75,76,77,78,79,88,91,92,93,96,124,125,126,127,128,129,130,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,197,198,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-35,-66,-68,-75,-69,171,-36,-39,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-37,-38,-61,-59,-62,-71,-73,-72,]),'else':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,203,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,219,-61,-59,-62,-71,-73,-72,]),'pool':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,204,210,212,213,214,220,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,220,-61,-59,-62,-71,-73,-72,]),'fi':([72,73,74,75,76,77,78,79,88,91,92,93,124,125,126,127,134,144,152,156,157,158,159,160,161,162,163,164,167,170,177,178,179,188,191,192,196,210,212,213,214,220,228,230,],[-75,-46,-50,-53,-56,-60,-67,-63,-74,-81,-82,-83,-66,-68,-75,-69,-76,-78,-45,-47,-48,-49,-51,-52,-54,-57,-55,-58,-65,-64,-77,-80,-79,-90,-88,-89,-70,-61,-59,-62,-71,-73,230,-72,]),'esac':([199,215,216,217,226,],[214,-40,-42,-43,-41,]),'rarrow':([227,],[229,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,3,4,],[2,6,7,]),'def_class':([0,3,4,],[3,3,3,]),'feature_list':([10,12,15,29,30,33,34,36,37,],[14,22,26,47,48,53,54,56,57,]),'epsilon':([10,12,15,28,29,30,32,33,34,36,37,110,113,195,],[16,16,16,45,16,16,45,16,16,16,16,150,150,150,]),'def_attr':([10,12,15,29,30,33,34,36,37,],[17,17,17,17,17,17,17,17,17,]),'def_func':([10,12,15,29,30,33,34,36,37,],[18,18,18,18,18,18,18,18,18,]),'formals':([28,32,],[41,51,]),'param_list':([28,32,60,],[42,42,95,]),'param_list_empty':([28,32,],[43,43,]),'param':([28,32,60,84,172,],[44,44,44,130,130,]),'expr':([58,62,63,70,80,81,85,86,87,90,98,107,110,112,113,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[71,97,99,111,123,124,131,132,133,111,111,111,147,152,155,111,187,111,187,111,111,196,198,203,204,205,206,208,209,187,155,155,111,228,231,]),'comp':([58,62,63,70,80,81,85,86,87,90,98,107,110,112,113,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,]),'op':([58,62,63,70,80,81,85,86,87,90,98,107,110,112,113,114,115,116,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,156,157,158,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,]),'term':([58,62,63,70,80,81,85,86,87,90,98,107,110,112,113,114,115,116,117,118,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,159,160,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,]),'base_call':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[76,76,76,76,76,76,125,127,76,76,76,76,76,76,76,76,76,76,76,76,76,76,161,163,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,]),'factor':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,]),'func_call':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,122,136,145,151,154,162,164,171,173,175,176,180,181,182,183,184,185,189,193,194,195,207,219,229,],[78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,167,78,78,78,78,78,78,78,78,78,78,78,78,78,78,210,78,78,212,213,78,78,78,78,]),'atom':([58,62,63,70,80,81,82,83,85,86,87,90,98,107,110,112,113,114,115,116,117,118,119,120,136,145,151,154,162,164,171,173,175,176,180,181,182,183,185,189,195,207,219,229,],[79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,]),'block':([70,90,98,107,136,145,151,154,162,164,185,207,],[109,135,109,141,141,109,190,109,109,109,141,109,]),'let_list':([84,172,],[128,197,]),'let_assign':([84,172,],[129,129,]),'args':([110,113,195,],[146,153,146,]),'arg_list':([110,113,145,154,185,189,195,],[148,148,186,186,186,211,148,]),'arg_list_empty':([110,113,195,],[149,149,149,]),'cases_list':([174,201,215,],[199,216,226,]),'casep':([174,201,215,],[200,200,200,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','parser.py',30),
  ('class_list -> def_class class_list','class_list',2,'p_class_list','parser.py',35),
  ('class_list -> def_class','class_list',1,'p_class_list','parser.py',36),
  ('class_list -> error class_list','class_list',2,'p_class_list_error','parser.py',41),
  ('epsilon -> <empty>','epsilon',0,'p_epsilon','parser.py',46),
  ('def_class -> class type ocur feature_list ccur semi','def_class',6,'p_def_class','parser.py',50),
  ('def_class -> class type inherits type ocur feature_list ccur semi','def_class',8,'p_def_class','parser.py',51),
  ('def_class -> class error ocur feature_list ccur semi','def_class',6,'p_def_class_error','parser.py',57),
  ('def_class -> class type ocur feature_list ccur error','def_class',6,'p_def_class_error','parser.py',58),
  ('def_class -> class error inherits type ocur feature_list ccur semi','def_class',8,'p_def_class_error','parser.py',59),
  ('def_class -> class error inherits error ocur feature_list ccur semi','def_class',8,'p_def_class_error','parser.py',60),
  ('def_class -> class type inherits error ocur feature_list ccur semi','def_class',8,'p_def_class_error','parser.py',61),
  ('def_class -> class type inherits type ocur feature_list ccur error','def_class',8,'p_def_class_error','parser.py',62),
  ('feature_list -> epsilon','feature_list',1,'p_feature_list','parser.py',67),
  ('feature_list -> def_attr semi feature_list','feature_list',3,'p_feature_list','parser.py',68),
  ('feature_list -> def_func semi feature_list','feature_list',3,'p_feature_list','parser.py',69),
  ('feature_list -> error feature_list','feature_list',2,'p_feature_list_error','parser.py',74),
  ('def_attr -> id colon type','def_attr',3,'p_def_attr','parser.py',79),
  ('def_attr -> id colon type larrow expr','def_attr',5,'p_def_attr','parser.py',80),
  ('def_attr -> error colon type','def_attr',3,'p_def_attr_error','parser.py',86),
  ('def_attr -> id colon error','def_attr',3,'p_def_attr_error','parser.py',87),
  ('def_attr -> error colon type larrow expr','def_attr',5,'p_def_attr_error','parser.py',88),
  ('def_attr -> id colon error larrow expr','def_attr',5,'p_def_attr_error','parser.py',89),
  ('def_attr -> id colon type larrow error','def_attr',5,'p_def_attr_error','parser.py',90),
  ('def_func -> id opar formals cpar colon type ocur expr ccur','def_func',9,'p_def_func','parser.py',95),
  ('def_func -> error opar formals cpar colon type ocur expr ccur','def_func',9,'p_def_func_error','parser.py',100),
  ('def_func -> id opar error cpar colon type ocur expr ccur','def_func',9,'p_def_func_error','parser.py',101),
  ('def_func -> id opar formals cpar colon error ocur expr ccur','def_func',9,'p_def_func_error','parser.py',102),
  ('def_func -> id opar formals cpar colon type ocur error ccur','def_func',9,'p_def_func_error','parser.py',103),
  ('formals -> param_list','formals',1,'p_formals','parser.py',108),
  ('formals -> param_list_empty','formals',1,'p_formals','parser.py',109),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',114),
  ('param_list -> param comma param_list','param_list',3,'p_param_list','parser.py',115),
  ('param_list_empty -> epsilon','param_list_empty',1,'p_param_list_empty','parser.py',120),
  ('param -> id colon type','param',3,'p_param','parser.py',125),
  ('let_list -> let_assign','let_list',1,'p_let_list','parser.py',130),
  ('let_list -> let_assign comma let_list','let_list',3,'p_let_list','parser.py',131),
  ('let_assign -> param larrow expr','let_assign',3,'p_let_assign','parser.py',136),
  ('let_assign -> param','let_assign',1,'p_let_assign','parser.py',137),
  ('cases_list -> casep semi','cases_list',2,'p_cases_list','parser.py',143),
  ('cases_list -> casep semi cases_list','cases_list',3,'p_cases_list','parser.py',144),
  ('cases_list -> error cases_list','cases_list',2,'p_cases_list_error','parser.py',149),
  ('cases_list -> error semi','cases_list',2,'p_cases_list_error','parser.py',150),
  ('casep -> id colon type rarrow expr','casep',5,'p_case','parser.py',155),
  ('expr -> id larrow expr','expr',3,'p_expr','parser.py',160),
  ('expr -> comp','expr',1,'p_expr','parser.py',161),
  ('comp -> comp less op','comp',3,'p_comp','parser.py',166),
  ('comp -> comp lesseq op','comp',3,'p_comp','parser.py',167),
  ('comp -> comp equal op','comp',3,'p_comp','parser.py',168),
  ('comp -> op','comp',1,'p_comp','parser.py',169),
  ('op -> op plus term','op',3,'p_op','parser.py',181),
  ('op -> op minus term','op',3,'p_op','parser.py',182),
  ('op -> term','op',1,'p_op','parser.py',183),
  ('term -> term star base_call','term',3,'p_term','parser.py',193),
  ('term -> term div base_call','term',3,'p_term','parser.py',194),
  ('term -> base_call','term',1,'p_term','parser.py',195),
  ('term -> term star error','term',3,'p_term_error','parser.py',205),
  ('term -> term div error','term',3,'p_term_error','parser.py',206),
  ('base_call -> factor arroba type dot func_call','base_call',5,'p_base_call','parser.py',211),
  ('base_call -> factor','base_call',1,'p_base_call','parser.py',212),
  ('base_call -> error arroba type dot func_call','base_call',5,'p_base_call_error','parser.py',217),
  ('base_call -> factor arroba error dot func_call','base_call',5,'p_base_call_error','parser.py',218),
  ('factor -> atom','factor',1,'p_factor1','parser.py',223),
  ('factor -> opar expr cpar','factor',3,'p_factor1','parser.py',224),
  ('factor -> factor dot func_call','factor',3,'p_factor2','parser.py',229),
  ('factor -> not expr','factor',2,'p_factor2','parser.py',230),
  ('factor -> func_call','factor',1,'p_factor2','parser.py',231),
  ('factor -> isvoid base_call','factor',2,'p_factor3','parser.py',241),
  ('factor -> nox base_call','factor',2,'p_factor3','parser.py',242),
  ('factor -> let let_list in expr','factor',4,'p_expr_let','parser.py',247),
  ('factor -> case expr of cases_list esac','factor',5,'p_expr_case','parser.py',252),
  ('factor -> if expr then expr else expr fi','factor',7,'p_expr_if','parser.py',257),
  ('factor -> while expr loop expr pool','factor',5,'p_expr_while','parser.py',262),
  ('atom -> num','atom',1,'p_atom_num','parser.py',267),
  ('atom -> id','atom',1,'p_atom_id','parser.py',272),
  ('atom -> new type','atom',2,'p_atom_new','parser.py',277),
  ('atom -> ocur block ccur','atom',3,'p_atom_block','parser.py',282),
  ('atom -> error block ccur','atom',3,'p_atom_block_error','parser.py',287),
  ('atom -> ocur error ccur','atom',3,'p_atom_block_error','parser.py',288),
  ('atom -> ocur block error','atom',3,'p_atom_block_error','parser.py',289),
  ('atom -> true','atom',1,'p_atom_boolean','parser.py',294),
  ('atom -> false','atom',1,'p_atom_boolean','parser.py',295),
  ('atom -> string','atom',1,'p_atom_string','parser.py',300),
  ('block -> expr semi','block',2,'p_block','parser.py',305),
  ('block -> expr semi block','block',3,'p_block','parser.py',306),
  ('block -> error block','block',2,'p_block_error','parser.py',311),
  ('block -> error semi','block',2,'p_block_error','parser.py',312),
  ('func_call -> id opar args cpar','func_call',4,'p_func_call','parser.py',317),
  ('func_call -> id opar error cpar','func_call',4,'p_func_call_error','parser.py',322),
  ('func_call -> error opar args cpar','func_call',4,'p_func_call_error','parser.py',323),
  ('args -> arg_list','args',1,'p_args','parser.py',328),
  ('args -> arg_list_empty','args',1,'p_args','parser.py',329),
  ('arg_list -> expr','arg_list',1,'p_arg_list','parser.py',334),
  ('arg_list -> expr comma arg_list','arg_list',3,'p_arg_list','parser.py',335),
  ('arg_list -> error arg_list','arg_list',2,'p_arg_list_error','parser.py',341),
  ('arg_list_empty -> epsilon','arg_list_empty',1,'p_arg_list_empty','parser.py',346),
]