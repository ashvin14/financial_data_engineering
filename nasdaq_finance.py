{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "usage: ipykernel_launcher.py [-h] ticker\n",
      "ipykernel_launcher.py: error: unrecognized arguments: -f\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "2",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 2\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\ProgramData\\Anaconda3\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3334: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "#!/usr/bin/env python\n",
    "# -*- coding: utf-8 -*-\n",
    "\n",
    "from lxml import html\n",
    "import requests\n",
    "from time import sleep\n",
    "import json\n",
    "import argparse\n",
    "from random import randint\n",
    "\n",
    "def parse_finance_page(ticker):\n",
    "\n",
    "  key_stock_dict = {}\n",
    "  headers = {\n",
    "        \"Accept\":\"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\",\n",
    "        \"Accept-Encoding\":\"gzip, deflate\",\n",
    "        \"Accept-Language\":\"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7\",\n",
    "        \"Connection\":\"keep-alive\",\n",
    "        \"Host\":\"www.nasdaq.com\",\n",
    "        \"Referer\":\"http://www.nasdaq.com\",\n",
    "        \"Upgrade-Insecure-Requests\":\"1\",\n",
    "        \"User-Agent\":\"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36\"\n",
    "  }\n",
    "\n",
    "  # Retrying for failed request\n",
    "  for retries in range(5):\n",
    "    try:    \n",
    "      url = \"http://www.nasdaq.com/symbol/%s\"%(ticker)\n",
    "      response = requests.get(url, headers = headers, verify=False)\n",
    "      \n",
    "      if response.status_code!=200:\n",
    "        raise ValueError(\"Invalid Response Received From Webserver\")\n",
    "\n",
    "      print(\"Parsing %s\"%(url))\n",
    "      # Adding random delay\n",
    "      sleep(randint(1,3))   \n",
    "      parser = html.fromstring(response.text)\n",
    "      xpath_head = \"//div[@id='qwidget_pageheader']//h1//text()\"\n",
    "      xpath_key_stock_table = '//div[@class=\"row overview-results relativeP\"]//div[contains(@class,\"table-table\")]/div'\n",
    "      xpath_open_price = '//b[contains(text(),\"Open Price:\")]/following-sibling::span/text()'\n",
    "      xpath_open_date = '//b[contains(text(),\"Open Date:\")]/following-sibling::span/text()'\n",
    "      xpath_close_price = '//b[contains(text(),\"Close Price:\")]/following-sibling::span/text()'\n",
    "      xpath_close_date = '//b[contains(text(),\"Close Date:\")]/following-sibling::span/text()'\n",
    "      xpath_key = './/div[@class=\"table-cell\"]/b/text()'\n",
    "      xpath_value = './/div[@class=\"table-cell\"]/text()'\n",
    "\n",
    "      raw_name = parser.xpath(xpath_head)\n",
    "      key_stock_table =  parser.xpath(xpath_key_stock_table)\n",
    "      raw_open_price = parser.xpath(xpath_open_price)\n",
    "      raw_open_date = parser.xpath(xpath_open_date)\n",
    "      raw_close_price = parser.xpath(xpath_close_price)\n",
    "      raw_close_date = parser.xpath(xpath_close_date)\n",
    "\n",
    "      company_name = raw_name[0].replace(\"Common Stock Quote & Summary Data\",\"\").strip() if raw_name else ''\n",
    "      open_price =raw_open_price[0].strip() if raw_open_price else None\n",
    "      open_date = raw_open_date[0].strip() if raw_open_date else None\n",
    "      close_price = raw_close_price[0].strip() if raw_close_price else None\n",
    "      close_date = raw_close_date[0].strip() if raw_close_date else None\n",
    "\n",
    "      # Grabbing ans cleaning keystock data\n",
    "      for i in key_stock_table:\n",
    "        key = i.xpath(xpath_key)\n",
    "        value = i.xpath(xpath_value)\n",
    "        key = ''.join(key).strip() \n",
    "        value = ' '.join(''.join(value).split()) \n",
    "        key_stock_dict[key] = value\n",
    "\n",
    "      nasdaq_data = {\n",
    "\n",
    "              \"company_name\":company_name,\n",
    "              \"ticker\":ticker,\n",
    "              \"url\":url,\n",
    "              \"open price\":open_price,\n",
    "              \"open_date\":open_date,\n",
    "              \"close_price\":close_price,\n",
    "              \"close_date\":close_date,\n",
    "              \"key_stock_data\":key_stock_dict\n",
    "      }\n",
    "      return nasdaq_data\n",
    "\n",
    "    except Exception as e:\n",
    "      print(\"Failed to process the request, Exception:%s\"%(e))\n",
    "\n",
    "if __name__==\"__main__\":\n",
    "\n",
    "  argparser = argparse.ArgumentParser()\n",
    "  argparser.add_argument('ticker',help = 'Company stock symbol')\n",
    "  args = argparser.parse_args()\n",
    "  ticker = args.ticker\n",
    "  print(\"Fetching data for %s\"%(ticker))\n",
    "  scraped_data = parse_finance_page(ticker)\n",
    "  print(\"Writing scraped data to output file\")\n",
    "\n",
    "  with open('%s-summary.json'%(ticker),'w') as fp:\n",
    "    json.dump(scraped_data,fp,indent = 4,ensure_ascii=False)\n",
    "    \n",
    "    \n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
