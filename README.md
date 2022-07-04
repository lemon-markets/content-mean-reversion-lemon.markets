<h1 align='center'>
  🍋 Mean Reversion Trading Strategy 🍋 
</h1>

## 👋 Introduction 

This is a public [lemon.markets](https://lemon.markets) repository that demonstrates a simple implementation of the mean-reversion trading strategy with the lemon.markets API. 
To get a general understanding of the API, please refer to our [documentation](https://docs.lemon.markets).

A walk-through of this script can be found in our YouTube video.

## 🏃‍♂️ Quick Start
Not interested in reading a novella before you get started? We get it! To get this project up and running quickly, here's what you need to do:
1. Clone this repository;
2. Sign up to [lemon.markets](https://www.lemon.markets/)
3. Configure your environment variables as outlined in the 'Configuration' section;
4. Take a look at the demo functions in main.py, and, if you want to, check out our accompanying YouTube video!
5. Run the script & see how it performs! 


## 🔌 API Usage

This project uses the [lemon.markets API](https://www.lemon.markets/en-de/for-developers) and the lemon.markets Python SDK.

lemon.markets is a brokerage API by developers for developers that allows you to build your own experience at the stock market. 
We will use the Market Data API and Trading API to show you the results you receive when you make calls to the venues, account, and trades endpoints.
If you do not have a lemon.markets account yet, you can sign up at [lemon.markets](https://www.lemon.markets/).

## ⚙️ Configuration

The script uses several environment variables, configure your .env file as follows:

| ENV Variable    |               Explanation               |
|-----------------|:---------------------------------------:|
| DATA_API_KEY    |        Your market data API key         |
| TRADING_API_KEY |    Your paper/money trading API key     |
| MIC             | Market Identifier Code of Trading Venue |


## ☁️ Deploy to Heroku
If you are interested in hosting this project in the cloud, 
we suggest that you use Heroku to do so. To make the hosting 
work, you need to create a new project and connect 
your GitHub repo. You can find a good explanation [here](https://dev.to/josylad/how-to-deploy-a-python-script-or-bot-to-heroku-in-5-minutes-9dp).
Additionally, you need to specify the environment variables
through Heroku directly. You can do so by either using:

```
heroku config:set [KEY_NAME=value …]
```
or by adding them in your project in the Heroku Dashboard under 
/Settings/Config Vars. 

Use this button to deploy to Heroku directly.


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/lemon-markets/content-mean-reversion-lemon.markets)

## Contribute to this repository
lemon.markets is an API from developers for developers and this (and all lemon.markets open source projects) is(are) a work in progress. 
Therefore, we highly encourage you to get involved by opening a PR or contacting us directly via [support@lemon.markets](mailto:support@lemon.markets).

Looking forward to building lemon.markets with you 🍋

