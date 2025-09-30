import optuna
import yfinance as yf
from backtest import backtest_strategy

df = yf.download("NQ=F", period="30d", interval="5m", auto_adjust=True)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0).str.capitalize()
df.index = pd.to_datetime(df.index)
df = df[['Open','High','Low','Close','Volume']].apply(pd.to_numeric, errors='coerce')

def objective(trial):
    ma_short = trial.suggest_int('ma_short', 20, 80)
    ma_long  = trial.suggest_int('ma_long', 100, 200)
    stop_loss_usd = trial.suggest_int('stop_loss_usd', 200, 500)
    max_lots = trial.suggest_int('max_lots', 1, 10)

    result = backtest_strategy(df, ma_short=ma_short, ma_long=ma_long,
                               stop_loss_usd=stop_loss_usd,
                               max_lots=max_lots,
                               initial_capital=50000,
                               risk_per_trade=2000)
    return result['sharpe_ratio']

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

best_params = study.best_params
print("最佳參數:", best_params)

# 套用最佳參數回測
result = backtest_strategy(df, **best_params, initial_capital=50000, risk_per_trade=2000)
print(result)
