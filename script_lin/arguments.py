from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ", version="%prog 1.0")
parser.add_option( "--prod_cd",dest="prod_cd",default=None)
parser.add_option( "--whs_num", dest="whs_num", default=None)
parser.add_option( "--lastrcv_qty", dest="lastrcv_qty",type="float", default=None)
parser.add_option( "--lastrcv_dt", dest="lastrcv_dt",default=None)
parser.add_option( "--price_base", dest="price_base",default=None)
parser.add_option( "--frt_cus", dest="frt_cus",default=None)
parser.add_option( "--prod_duty", dest="prod_duty",default=None)
parser.add_option( "--handl_fee", dest="handl_fee",default=None)
parser.add_option( "--misc_fee", dest="misc_fee",default=None)
parser.add_option( "--avg_cost", dest="avg_cost",default=None)
parser.add_option( "--lt_sl_dt", dest="lt_sl_dt",default=None)
parser.add_option( "--vendor", dest="vendor",default=None)
parser.add_option( "--lst_order", dest="lst_order",default=None)
parser.add_option( "--ord_dt", dest="ord_dt",default=None)
parser.add_option( "--stk_ind", dest="stk_ind",default=None)
parser.add_option( "--back_qty", dest="back_qty",default=None)
parser.add_option( "--order_qty", dest="order_qty",default=None)
parser.add_option( "--on_order_qty", dest="on_order_qty",default=None)
parser.add_option( "--wip_qty", dest="wip_qty",default=None)
parser.add_option( "--rma_qty", dest="rma_qty",default=None)
parser.add_option( "--water_qty", dest="water_qty",default=None)
parser.add_option( "--ordersize", dest="ordersize",default=None)
parser.add_option( "--minstock", dest="minstock",default=None)
parser.add_option( "--inv_loc", dest="inv_loc",default=None)
parser.add_option( "--unit_color", dest="unit_color",default=None)
parser.add_option( "--class_cd", dest="class_cd",default=None)
parser.add_option( "--descrip", dest="descrip",default=None)
parser.add_option( "--def_unit", dest="def_unit",default=None)
parser.add_option( "--updt_dt", dest="updt_dt",default=None)
parser.add_option( "--phyc_dt", dest="phyc_dt",default=None)
parser.add_option( "--image_nm", dest="image_nm",default=None)
parser.add_option( "--oem_cd", dest="oem_cd",default=None)
parser.add_option( "--alt_cd", dest="alt_cd",default=None)
parser.add_option( "--updt_by", dest="updt_by",default=None)
parser.add_option( "--currency_cost", dest="currency_cost",default=None)
parser.add_option( "--cost_factor", dest="cost_factor",default=None)
(options, args) = parser.parse_args()


if options.prod_cd == None:
	print 'prod_cd can not be null'
else:
	print options.prod_cd

sql_script="INSERT INTO inv_data VALUES(%s,%s,%s,%s,%s,%s,
										  %s,%s,%s,%s,%s,%s,
										  %s,%s,%s,%s,%s,%s,
										  %s,%s,%s,%s,%s,%s,
										  %s,%s,%s,%s,%s,%s,
										  %s,%s,%s,%s,%s,%s)"%(options.prod_cd,
																options.whs_num		,
																options.in_stock	,
																options.lastrcv_qty	,
																options.lastrcv_dt	,
																options.price_base	,
																options.frt_cus		,
																options.prod_duty	,
																options.handl_fee 	,
																options.misc_fee 	,
																options.avg_cost 	,
																options.lt_sl_dt 	,
																options.vendor 		,
																options.lst_order 	,
																options.ord_dt 		,
																options.stk_ind 	,
																options.back_qty 	,
																options.order_qty 	,
																options.on_order_qty,
																options.wip_qty 	,
																options.rma_qty 	,
																options.water_qty 	,
																options.ordersize 	,
																options.minstock 	,
																options.inv_loc 	,
																options.unit_color 	,
																options.class_cd 	,
																options.descrip 	,
																options.def_unit 	,
																options.updt_dt 	,
																options.phyc_dt 	,
																options.image_nm 	,
																options.oem_cd 		,
																options.alt_cd 		,
																options.updt_by  	,
																options.currency_cost,
																options.cost_factor )

print sql_script

	
	
