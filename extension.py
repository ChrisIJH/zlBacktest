from zipline.data.bundles import register

from zipline.data.bundles.google import google_equities, viacsv

equities2 = {
	'JSE:ADR',
}
eqSym = {
    "F",
#    "DJI",
#    "GDAXI",
#    "GSPC",
#    "HSI",
#    "N225",
#    "NYA",
}

register(
	'csv',
	viacsv(eqSym)
#	'ch_bundle',
#	google_equities(equities2)
)

