ORDER_STATUS = (
    (1, "Otwarte"),
    (2, "W przygotowaniu"),
    (3, "W dostawie"),
    (4, "Gotowe do odbioru"),
    (5, "Zrealizowane"),
    (6, "Anulowane"),
)
ORDER_STATUS = sorted(ORDER_STATUS)

PAY_ORDER_STATUS = (
    (1, "Otwarte"),
    (2, "Do zapłaty"),
    (3, "Zapłacone"),
)
PAY_ORDER_STATUS = sorted(PAY_ORDER_STATUS)

DELIVERY_TYPE = (
    (1, "Odbiór osobisty"),
    (2, "Dostawa"),
)
DELIVERY_TYPE = sorted(DELIVERY_TYPE)

PAY_METHOD = ((1, "gotówka"), (2, "karta"), (3, "przelew"), (4, "przelew p24"))
PAY_METHOD = sorted(PAY_METHOD)

STAMP_COLORS = (
    (1, "Czarne"),
    (2, "Czerwone"),
    (3, "Niebieskie"),
    (4, "Zielone"),
    (5, "Fioletowe"),
)
STAMP_COLORS = sorted(STAMP_COLORS)

STAMP_COLORS_TEXT = (
    (0, "text-dark"),
    (1, "text-danger"),
    (2, "text-primary"),
    (3, "text-success"),
    (4, "violet"),
)
