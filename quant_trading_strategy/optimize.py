import optuna
import yfinance as yf
from backtest import backtest_strategy

# 下載一次資料，避免每個 trial 重複下載
def load_data():
    df = yf.download("NQ=F", period="30d", interval="5m", auto_adjust=True)
    df = df[['Open','High','Low','Close','Volume']]
    df.index = df.index.tz_localize(None)  # 移除時區
    return df

df = load_data()

def objective(trial):
    ma_short = trial.suggest_int('ma_short', 20, 80)
    ma_long  = trial.suggest_int('ma_long', 100, 200)
    stop_loss_usd = trial.suggest_int('stop_loss_usd', 200, 500)
    max_lots = trial.suggest_int('max_lots', 1, 8)

    result = backtest_strategy(
        df, ma_short=ma_short, ma_long=ma_long,
        stop_loss_usd=stop_loss_usd, max_lots=max_lots,
        initial_capital=50000, risk_per_trade=2000
    )
    return result['sharpe_ratio']

def run_optimization(n_trials=50):
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

if __name__ == "__main__":
    best_params = run_optimization(n_trials=50)
    print("最佳參數:", best_params)
