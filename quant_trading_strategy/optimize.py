import optuna
import yfinance as yf
from backtest import backtest_strategy

def objective(trial):
    ma_short = trial.suggest_int('ma_short', 20, 80)
    ma_long  = trial.suggest_int('ma_long', 100, 200)
    stop_loss_usd = trial.suggest_int('stop_loss_usd', 200, 500)
    max_lots = trial.suggest_int('max_lots', 1, 8)

    df = yf.download("NQ=F", period="30d", interval="5m", auto_adjust=True)
    df = df[['Open','High','Low','Close','Volume']]

    result = backtest_strategy(
        df, ma_short=ma_short, ma_long=ma_long,
        stop_loss_usd=stop_loss_usd, max_lots=max_lots,
        initial_capital=50000, risk_per_trade=2000
    )
    return result['sharpe_ratio']

if __name__ == "__main__":
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=50)
    print("最佳參數:", study.best_params)
