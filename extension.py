from zipline.data.bundles import register

from zipline.data.bundles.google import google_equities

equities2 = {
	'JSE:ADR',
}

register(
	'ch_bundle',
	google_equities(equities2)
	)