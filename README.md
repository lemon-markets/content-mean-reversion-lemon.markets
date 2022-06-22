# Mean Reversion Strategy with the lemon.markets API
This repository contains a Python Script that implements the mean reversion
strategy using the [lemon.markets](https://www.lemon.markets/) API.
## Project Structure
The models folder contains TradingVenue, with helper functions dedicated to calculating wait times for your mean-reversion
trading algorithm when the market is closed. 

The actual mean reversion is logic is defined in the **main.py** file with 
mean_reversion() being the main function. 

## Set up
To test locally, clone this repo, use the IDE of your choice to run (although we highly recommend PyCharm) and install
all required packages through the provided requirements.txt file. This project uses the lemon.markets Python SDK, which 
you will find listed in the requirements.

### Set environment variables
If you want to test locally, you need to define a number of environment variables.

| ENV Variable |               Explanation               |  
|--------------|:---------------------------------------:|
| DATA_API_KEY |        Your market data API key         |
 | TRADING_API_KEY |    Your paper/money trading API key     |
| MIC          | Market Identifier Code of Trading Venue |

## Deploy to Heroku
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
lemon.markets is an API from developers for developers. Therefore, we highly encourage you 
to get involved by opening a PR or contacting us directly via 
[support@lemon.markets](mailto:support@lemon.markets).

---

Have fun and happy coding,

your 🍋.markets team
