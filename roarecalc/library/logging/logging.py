import logging

#logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)
def printLog(
    dataProcessed : int,
    companyName : str,
    netIncome_0 : float,
    totalAssets_0 : float,
    netIncome_1 : float,
    totalAssets_1 : float,
    netIncome_2 : float,
    totalAssets_2 : float,
    netIncome_3 : float,
    totalAssets_3 : float,
    roa_0 : float,
    roa_1 : float,
    roa_2 : float,
    roa_3 : float,
) -> None:

    """
    later.
    """

    print("\n")
    logging.info("data processed : No.{}".format(dataProcessed))
    logging.info("company name : {}".format(companyName))
    logging.info("net income-0 : {} (yen)".format(netIncome_0))
    logging.info("total assets-0 : {} (yen)".format(totalAssets_0))
    logging.info("net income-1 : {} (yen)".format(netIncome_1))
    logging.info("total assets-1 : {} (yen)".format(totalAssets_1))
    logging.info("net income-2 : {} (yen)".format(netIncome_2))
    logging.info("total assets-2 : {} (yen)".format(totalAssets_2))
    logging.info("net income-3 : {} (yen)".format(netIncome_3))
    logging.info("total assets-3 : {} (yen)".format(totalAssets_3))
    logging.info("ROA-0 : {} (%)".format(roa_0))
    logging.info("ROA-1 : {} (%)".format(roa_1))
    logging.info("ROA-2 : {} (%)".format(roa_2))
    logging.info("ROA-3 : {} (%)\n".format(roa_3))