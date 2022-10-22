import logging

#logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)
def printLog(headers : list, values : list) -> None:

    """
    later.
    """

    print("\n")
    for header, value in zip(headers, values) :
        logging.info("{} : {}".format(header, value))
    print("\n")