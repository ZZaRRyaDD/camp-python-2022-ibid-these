from apps.lots import factories

LOTS_COUNT = 5
IMAGES_PER_LOT = 2
BIDS_PER_LOT_COUNT = 5


def run():
    """Generate examples of Lot, LotImage, Bid models."""
    lots = factories.LotFactory.create_batch(size=LOTS_COUNT)
    for lot in lots:
        factories.LotImageFactory.create_batch(
            size=IMAGES_PER_LOT,
            lot=lot,
        )
        factories.BidFactory.create_batch(
            size=BIDS_PER_LOT_COUNT,
            lot=lot,
        )
