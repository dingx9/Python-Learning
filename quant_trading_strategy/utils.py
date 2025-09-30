import numpy as np

def calculate_metrics(equity_curve, trades):
    """計算績效指標"""
    final_capital = equity_curve[-1]
    initial_capital = equity_curve[0]

    total_profit = sum([t['profit'] for t in trades if t['profit'] > 0])
    total_loss   = sum([t['profit'] for t in trades if t['profit'] < 0])
    win_rate = len([t for t in trades if t['profit'] > 0]) / len(trades) if trades else 0
    max_loss = min([t['profit'] for t in trades], default=0)

    # 最大回撤
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = running_max - equity_curve
    max_drawdown = np.max(drawdown)
    max_drawdown_pct = max_drawdown / running_max[np.argmax(drawdown)]

    # 盈虧比
    profit_loss_ratio = abs(total_profit / total_loss) if total_loss != 0 else np.inf

    # 夏普比率
    returns = np.diff(equity_curve) / equity_curve[:-1]
    sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0

    return {
        "initial_capital": initial_capital,
        "final_capital": final_capital,
        "total_profit": total_profit,
        "total_loss": total_loss,
        "win_rate": win_rate,
        "max_loss": max_loss,
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": max_drawdown_pct,
        "profit_loss_ratio": profit_loss_ratio,
        "sharpe_ratio": sharpe_ratio
    }
