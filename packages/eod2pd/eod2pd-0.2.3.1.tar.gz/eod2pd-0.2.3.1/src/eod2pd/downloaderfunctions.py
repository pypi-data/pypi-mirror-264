"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple library to quere EODHistoricalData in a multithreaded environment
#
# =============================================================================
"""

import datetime
from dataclasses import dataclass
from typing import Callable, List

import basefunctions
import basefunctions.threadpool
import decouple
import pandas as pd

import eod2pd.downloader

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


@dataclass
class EOD2PDFormatOptions:
    """
    This class defines the format options for the EOD2PD message handler.

    """

    combine: bool = (False,)
    normalize: bool = (False,)
    dropna_tickers: bool = (False,)
    dropna: bool = (False,)
    drop_volume: bool = (False,)
    capitalize: bool = (False,)
    format_stockstats: bool = (False,)


@dataclass
class EOD2PDMessageContent:
    """
    This class defines the message content for the EOD2PD message handler.

    """

    type: str = None
    key: str = None
    url: str = None
    params: dict = None


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  start jobs get list of exchanges from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_exchanges(params: dict = None, hook: Callable = None) -> None:
    """
    Get the list of exchanges from EODHistoricalData.

    Parameters
    ----------
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of exchanges.
    """
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    # build url
    url = f"https://eodhistoricaldata.com/api/exchanges-list/" f"?api_token={api_key}" f"&fmt=json"

    # create message content
    message_content = EOD2PDMessageContent()
    message_content.type = "exchanges"
    message_content.key = "exchanges"
    message_content.url = url
    message_content.params = params

    # put message into input queue
    send_message(message_content, hook)


# -------------------------------------------------------------
#  get list of exchanges from EODHistoricalData
# -------------------------------------------------------------
def get_exchanges() -> pd.DataFrame:
    """
    Get the list of exchanges from EODHistoricalData.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of exchanges.
    """
    # start jobs to get exchanges
    start_jobs_get_exchanges()

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue()


# -------------------------------------------------------------
#  start jobs get list of symbols for a specific exchange from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_exchanges_symbols(
    exchange: str = "XETRA", params: dict = None, hook: Callable = None
) -> None:
    """
    Get the list of symbols for a specific exchange from EODHistoricalData.

    Parameters
    ----------
    exchangeCode : str, optional
        The code of the exchange, default: "XETRA"
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of symbols for the specified exchange.
    """
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    # build url
    url = (
        f"https://eodhistoricaldata.com/api/exchange-symbol-list/"
        f"{exchange}"
        f"?api_token={api_key}"
        f"&fmt=json"
    )

    # create message content
    message_content = EOD2PDMessageContent()
    message_content.type = "exchange-symbols-list"
    message_content.key = exchange
    message_content.url = url
    message_content.params = params

    # put message into input queue
    send_message(message_content, hook)


# -------------------------------------------------------------
#  get list of symbols for a specific exchange from EODHistoricalData
# -------------------------------------------------------------
def get_exchanges_symbols(
    exchanges: List[str] = None,
) -> dict:
    """
    Get the list of symbols for a specific exchanges from EODHistoricalData.

    Parameters
    ----------
    exchanges : list, optional
        A list of exchanges, default: None

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of symbols for the specified exchange.
    """
    # check if exchanges is None
    if exchanges is None:
        exchanges = ["XETRA"]

    # loop over all exchanges
    for exchange in exchanges:
        # start jobs to get symbols for exchange
        start_jobs_get_exchanges_symbols(exchange.upper())

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue()


# -------------------------------------------------------------
#  start jobs get symbol prices in a bulk message from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_symbols_prices_bulk(
    exchange: str = "XETRA",
    start: str | datetime.date = None,
    end: str | datetime.date = None,
    params: dict = None,
    hook: Callable = None,
) -> None:
    """
    Get bulk symbol prices for the given exchange and date.

    Parameters
    ----------
    exchange : str, optional
        The code of the exchange, default: "XETRA"
    start : str, optional
        The start date of the prices data, the format is "YY-mm-dd",
        default: None
    end : str, optional
        The end date of the prices data, the format is "YY-mm-dd",
        default: None
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the bulk symbol prices for the given
        exchange and date.
    """
    # make exchange uppercase
    exchange = exchange.upper()
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    if start is None:
        start = datetime.datetime.today()
    if end is None:
        end = datetime.datetime.today()
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
    # check if date range is too big, we only allow a range of 30 days
    if (end - start).days > 30:
        raise ValueError("##FAILURE## date range is too big, we only allow a range of 30 days")
    # loop over all dates
    for date in pd.date_range(start=start, end=end):
        # build the url for the request
        url = (
            f"https://eodhistoricaldata.com/api/eod-bulk-last-day/"
            f"{exchange}"
            f"?api_token={api_key}"
            f"&date={date.date()}"
            f"&fmt=json"
        )

        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchange-symbols-prices-bulk"
        message_content.key = (exchange, date.date())
        message_content.url = url
        message_content.params = params

        # put message into input queue
        send_message(message_content, hook)


# -------------------------------------------------------------
#  get symbol prices in a bulk message from EODHistoricalData
# -------------------------------------------------------------
def get_symbols_prices_bulk(
    exchanges: List[str] = None,
    start: str = None,
    end: str = None,
) -> dict:
    """
    Get bulk symbol prices for the given exchanges and date.

    Parameters
    ----------
    exchanges : str, optional
        A list of exchanges, default: ["XETRA"]
    start : str, optional
        The start date of the prices data, the format is "YY-mm-dd",
        default: None
    end : str, optional
        The end date of the prices data, the format is "YY-mm-dd",
        default: None

    Returns
    -------
    dict
        A dictionary containing the bulk symbol prices for the given
        exchange and date.
    """
    # check if exchanges is None
    if exchanges is None:
        exchanges = ["XETRA"]

    # loop over all exchanges
    for exchange in exchanges:
        # start jobs to get symbols bulk prices
        start_jobs_get_symbols_prices_bulk(exchange, start, end)

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue()


# -------------------------------------------------------------
#  start_jobs_get symbol prices from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_symbols_prices(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
    freq: str = "D",
    params: dict = None,
    hook: Callable = None,
) -> None:
    """
    Get symbol prices for the given symbols and date.

    Parameters
    ----------
    symbols : list, optional
        The list of symbols to be used, default: None
    start : str, optional
        The start date of the prices data, the format is "YY-mm-dd",
        default: "1900-01-01"
    end : str, optional
        The end date of the prices data, the format is "YY-mm-dd",
        default: "2999-12-31"
    freq : str, optional
        The frequency of the prices data, default: "D"
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the symbol prices for the given symbols and date.
    """
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    if symbols is None:
        symbols = ["BMW.XETRA"]
    for symbol in symbols:
        # make symbol uppercase
        symbol = symbol.upper()
        # build the url for the request
        url = (
            f"https://eodhistoricaldata.com/api/eod/{symbol}"
            f"?api_token={api_key}"
            f"&from={start}"
            f"&to={end}"
            f"&period={freq}"
            f"&fmt=json"
        )
        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchange-symbols-prices"
        message_content.key = symbol
        message_content.url = url
        message_content.params = params

        # put message into input queue
        send_message(message_content, hook)


# -------------------------------------------------------------
#  get symbol prices from EODHistoricalData
# -------------------------------------------------------------
def get_symbols_prices(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
    freq: str = "D",
    combine_dict: bool = False,
) -> dict:
    """
    Get symbol prices for the given symbols and date.

    Parameters
    ----------
    symbols : list, optional
        The list of symbols to be used, default: None
    start : str, optional
        The start date of the prices data, the format is "YY-mm-dd",
        default: "1900-01-01"
    end : str, optional
        The end date of the prices data, the format is "YY-mm-dd",
        default: "2999-12-31"
    freq : str, optional
        The frequency of the prices data, default: "D"

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the symbol prices for the given symbols and date.
    """
    # start jobs to get symbols prices
    start_jobs_get_symbols_prices(symbols, start, end, freq)

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue(
        combine_dict=combine_dict,
    )


# -------------------------------------------------------------
#  start jobs get symbol dividends from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_symbols_dividends(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
    params: dict = None,
    hook: Callable = None,
) -> None:
    """
    Get historical symbol dividends for the given symbols.

    Parameters
    ----------
    symbols : list of str, optional
        The symbols to retrieve dividends for, default: "BMW.XETRA"
    start : str, optional
        The start date of the dividends data, default: "1900-01-01"
    end : str, optional
        The end date of the dividends, default: "2999-12-31"
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical symbol dividends for the
        given symbols.
    """
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    # check if symbol is a list
    if symbols is None:
        symbols = ["BMW.XETRA"]
    for symbol in symbols:
        # make symbol uppercase
        symbol = symbol.upper()
        url = (
            f"https://eodhistoricaldata.com/api/div/{symbol}"
            f"?api_token={api_key}"
            f"&from={start}"
            f"&to={end}"
            f"&fmt=json"
        )
        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchange-symbols-dividends"
        message_content.key = symbol
        message_content.url = url
        message_content.params = params

        # put message into input queue
        send_message(message_content, hook)


# -------------------------------------------------------------
#  get symbol dividends from EODHistoricalData
# -------------------------------------------------------------
def get_symbols_dividends(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
) -> dict:
    """
    Get historical symbol dividends for the given symbols.

    Parameters
    ----------
    symbols : list of str, optional
        The symbols to retrieve dividends for, default: "BMW.XETRA"
    start : str, optional
        The start date of the dividends data, default: "1900-01-01"
    end : str, optional
        The end date of the dividends, default: "2999-12-31"

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical symbol dividends for the
        given symbols.
    """
    # start jobs to get symbols dividends
    start_jobs_get_symbols_dividends(symbols, start, end)

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue()


# -------------------------------------------------------------
#  start jobs get symbol splits from EODHistoricalData
# -------------------------------------------------------------
def start_jobs_get_symbols_splits(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
    params: dict = None,
    hook: Callable = None,
) -> None:
    """
    Get historical symbol splits for the given symbols.

    Parameters
    ----------
    symbols : list of str, optional
        The symbols to retrieve splits for, default: "BMW.XETRA"
    start : str, optional
        The start date of the splits data, default: "1900-01-01"
    end : str, optional
        The end date of the splits, default: "2999-12-31"
    params : dict, optional
        Additional parameters to be used, default: None
    hook: Callable, optional
        A hook to be used, default: None

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical symbol dividends for the
        given symbols.
    """
    # load api key from environment
    api_key = decouple.config("EOD2PD_API_KEY", default=None)
    if api_key is None:
        raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
    # check if symbol is a list
    if symbols is None:
        symbols = ["BMW.XETRA"]
    for symbol in symbols:
        # make symbol uppercase
        symbol = symbol.upper()
        url = (
            f"https://eodhistoricaldata.com/api/splits/{symbol}"
            f"?api_token={api_key}"
            f"&from={start}"
            f"&to={end}"
            f"&fmt=json"
        )
        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchange-symbols-splits"
        message_content.key = symbol
        message_content.url = url
        message_content.params = params

        # put message into input queue
        send_message(message_content, hook)


# -------------------------------------------------------------
#  get symbol splits from EODHistoricalData
# -------------------------------------------------------------
def get_symbols_splits(
    symbols: List[str] | None,
    start: str = "1900-01-01",
    end: str = "2999-12-31",
) -> dict:
    """
    Get historical symbol splits for the given symbols.

    Parameters
    ----------
    symbols : list of str, optional
        The symbols to retrieve splits for, default: "BMW.XETRA"
    start : str, optional
        The start date of the splits data, default: "1900-01-01"
    end : str, optional
        The end date of the splits, default: "2999-12-31"

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical symbol dividends for the
        given symbols.
    """
    # start jobs to get symbols splits
    start_jobs_get_symbols_splits(symbols, start, end)

    # wait until all jobs are done
    basefunctions.default_threadpool.get_input_queue().join()

    # get dataframes from output queue
    return basefunctions.default_threadpool.get_dataframes_from_output_queue()


# =========================================================================
#
# helper functions
#
# =========================================================================
def send_message(content: EOD2PDMessageContent, hook: Callable = None):
    """
    Send a message to the EOD2PD message handler.

    Parameters
    ----------
    message_content : EOD2PDMessageContent
        The content of the message to be sent.
    """
    timeout = decouple.config("EOD2PD_TIMEOUT", default=10, cast=int)
    message = basefunctions.threadpool.create_threadpool_message(
        _type=eod2pd.EOD2PDMESSAGEIDENTIFIER,
        content=content,
        timeout=timeout,
        hook=hook,
    )
    basefunctions.default_threadpool.get_input_queue().put(message)
