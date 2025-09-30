import optuna
from backtest import backtest_strategy

def objective(trial, df):
    ma_short = trial.suggest_int('ma_short', 20, 80)
    ma_long  = trial.suggest_int('ma_long', 100, 200)
    stop_loss_usd = trial.suggest_int('stop_loss_usd', 200, 500)
    max_lots = trial.suggest_int('max_lots', 1, 8)

    result = backtest_strategy(df, ma_short=ma_short, ma_long=ma_long,
                               stop_loss_usd=stop_loss_usd, max_lots=max_lots)
    return result['sharpe_ratio']

def run_optimization(df, n_trials=50):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, df), n_trials=n_trials)
    return study.best_params
