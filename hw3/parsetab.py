
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ARROW COMMA DOLLAR EQUALS LBRACE LPAREN LSQUARE NAME NUMBER RBRACE RPAREN RSQUARE SERVER SET STRINGconfig : server_block\n              | setlistsetlist : set\n               | set setlistset : NAME EQUALS value SEMIvalue : NUMBER\n             | STRING\n             | array\n             | dict\n             | dollar_exprarray : LSQUARE values RSQUAREvalues : value\n              | value COMMA valuesdict : LBRACE pairs RBRACEpairs : pair\n             | pair COMMA pairspair : NAME MINUS GREATER valuedollar_expr : DOLLAR LPAREN NAME RPARENSEMI : MINUS : '-' GREATER : '>' server_block : SERVER LBRACE server_options RBRACEserver_options : option\n                      | option server_optionsoption : NAME EQUALS value SEMI"
    
_lr_action_items = {'SERVER':([0,],[4,]),'NAME':([0,5,7,11,13,14,15,16,17,18,20,25,31,32,33,35,36,40,45,],[6,6,12,12,-19,-6,-7,-8,-9,-10,30,-5,39,-19,-11,-14,30,-25,-18,]),'$end':([1,2,3,5,8,13,14,15,16,17,18,22,25,33,35,45,],[0,-1,-2,-3,-4,-19,-6,-7,-8,-9,-10,-22,-5,-11,-14,-18,]),'LBRACE':([4,9,19,24,34,43,44,],[7,20,20,20,20,20,-21,]),'EQUALS':([6,12,],[9,24,]),'NUMBER':([9,19,24,34,43,44,],[14,14,14,14,14,-21,]),'STRING':([9,19,24,34,43,44,],[15,15,15,15,15,-21,]),'LSQUARE':([9,19,24,34,43,44,],[19,19,19,19,19,-21,]),'DOLLAR':([9,19,24,34,43,44,],[21,21,21,21,21,-21,]),'RBRACE':([10,11,14,15,16,17,18,23,28,29,32,33,35,40,42,45,46,],[22,-23,-6,-7,-8,-9,-10,-24,35,-15,-19,-11,-14,-25,-16,-18,-17,]),'COMMA':([14,15,16,17,18,27,29,33,35,45,46,],[-6,-7,-8,-9,-10,34,36,-11,-14,-18,-17,]),'RSQUARE':([14,15,16,17,18,26,27,33,35,41,45,],[-6,-7,-8,-9,-10,33,-12,-11,-14,-13,-18,]),'LPAREN':([21,],[31,]),'-':([30,],[38,]),'>':([37,38,],[44,-20,]),'RPAREN':([39,],[45,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'config':([0,],[1,]),'server_block':([0,],[2,]),'setlist':([0,5,],[3,8,]),'set':([0,5,],[5,5,]),'server_options':([7,11,],[10,23,]),'option':([7,11,],[11,11,]),'value':([9,19,24,34,43,],[13,27,32,27,46,]),'array':([9,19,24,34,43,],[16,16,16,16,16,]),'dict':([9,19,24,34,43,],[17,17,17,17,17,]),'dollar_expr':([9,19,24,34,43,],[18,18,18,18,18,]),'SEMI':([13,32,],[25,40,]),'values':([19,34,],[26,41,]),'pairs':([20,36,],[28,42,]),'pair':([20,36,],[29,29,]),'MINUS':([30,],[37,]),'GREATER':([37,],[43,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> config","S'",1,None,None,None),
  ('config -> server_block','config',1,'p_config','my_parser.py',7),
  ('config -> setlist','config',1,'p_config','my_parser.py',8),
  ('setlist -> set','setlist',1,'p_setlist','my_parser.py',12),
  ('setlist -> set setlist','setlist',2,'p_setlist','my_parser.py',13),
  ('set -> NAME EQUALS value SEMI','set',4,'p_set','my_parser.py',20),
  ('value -> NUMBER','value',1,'p_value','my_parser.py',24),
  ('value -> STRING','value',1,'p_value','my_parser.py',25),
  ('value -> array','value',1,'p_value','my_parser.py',26),
  ('value -> dict','value',1,'p_value','my_parser.py',27),
  ('value -> dollar_expr','value',1,'p_value','my_parser.py',28),
  ('array -> LSQUARE values RSQUARE','array',3,'p_array','my_parser.py',32),
  ('values -> value','values',1,'p_values','my_parser.py',36),
  ('values -> value COMMA values','values',3,'p_values','my_parser.py',37),
  ('dict -> LBRACE pairs RBRACE','dict',3,'p_dict','my_parser.py',44),
  ('pairs -> pair','pairs',1,'p_pairs','my_parser.py',48),
  ('pairs -> pair COMMA pairs','pairs',3,'p_pairs','my_parser.py',49),
  ('pair -> NAME MINUS GREATER value','pair',4,'p_pair','my_parser.py',56),
  ('dollar_expr -> DOLLAR LPAREN NAME RPAREN','dollar_expr',4,'p_dollar_expr','my_parser.py',60),
  ('SEMI -> <empty>','SEMI',0,'p_semi','my_parser.py',64),
  ('MINUS -> -','MINUS',1,'p_minus','my_parser.py',68),
  ('GREATER -> >','GREATER',1,'p_greater','my_parser.py',72),
  ('server_block -> SERVER LBRACE server_options RBRACE','server_block',4,'p_server_block','my_parser.py',87),
  ('server_options -> option','server_options',1,'p_server_options','my_parser.py',91),
  ('server_options -> option server_options','server_options',2,'p_server_options','my_parser.py',92),
  ('option -> NAME EQUALS value SEMI','option',4,'p_option','my_parser.py',99),
]
