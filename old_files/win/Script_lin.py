import sys
import psycopg2
import settings_script

argv=sys.argv

prod_cd		=argv[1]  				#  char(21) not null unique,
whs_num		=argv[2]  				#  char(8) not null unique,
in_stock	=argv[3]  				#  numeric(21,6) not null,
lastrcv_qty	=float(argv[4]) 		#  numeric(21,6),
LASTRCV_DT	=float(argv[5]) 		#  numeric(8,0),
price_base	=float(argv[6])		 	#  numeric(21,6),
FRT_CUS		=float(argv[7])		 	#  numeric(21,6),
PROD_DUTY	=float(argv[8])		 	#  numeric(21,6),
HANDL_FEE 	=float(argv[9])		 	#  numeric(21,6),
MISC_FEE 	=float(argv[10])	 	#  numeric(21,6),
AVG_COST 	=float(argv[11])		#  numeric(21,6),
LT_SL_DT 	=float(argv[12])	 	#  numeric(8,0),
VENDOR 		=argv[13] 				#  char(10),
LST_ORDER 	=float(argv[14]) 		#  numeric(21,6),
ORD_DT 		=float(argv[15])		#  numeric(8,0),
STK_IND 	=argv[16] 				#  char(1),
BACK_QTY 	=float(argv[17])		#  numeric(21,6),
ORDER_QTY 	=float(argv[18]) 		#  numeric(21,6),
ON_ORDER_QTY=float(argv[19]) 		#  numeric(21,6),
WIP_QTY 	=float(argv[20]) 		#  numeric(21,6),
RMA_QTY 	=float(argv[21]) 		#  numeric(21,6),
WATER_QTY 	=float(argv[22])	 	#  numeric(21,6),
ORDERSIZE 	=float(argv[23]) 		#  numeric(21,6),
MINSTOCK 	=float(argv[24]) 		#  numeric(21,6),
INV_LOC 	=argv[25] 				#  char(20),
UNIT_COLOR 	=argv[26] 				#  char(11)
CLASS_CD 	=argv[27]				#  char(20)
DESCRIP 	=argv[28]				# char(61)
DEF_UNIT 	=argv[29] 				#  char(2),
UPDT_DT 	=float(argv[30])	 	#  numeric(8,0),
PHYC_DT 	=float(argv[31])	 	#  numeric(21,6),
IMAGE_NM 	=argv[32] 				#  char(80),
OEM_CD 		=argv[33] 				#  char(20),
ALT_CD 		=argv[34] 				#  char(20),
UPDT_BY  	=argv[35] 				#  char(8),
CURRENCY_COST=float(argv[36]) 		#  numeric(21,6),
COST_FACTOR  =float(argv[37])		#  numeric(21,6));


print 'end'



