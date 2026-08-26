# How much do n and σ actually matter for recovering β?

I wanted to actually test this instead of just assuming "more data = better, more
noise = worse" and moving on. So I ran a grid: 6 values of n (10 up to 20,000) crossed
with 5 values of σ (0.1 up to 40), generated fake data with a known β for each
combination, ran gradient descent on it, and measured how far off the recovered β
landed. Did 8 repeats per combo and averaged them, because at n=10 a single run can
just get lucky or unlucky and I didn't want to draw conclusions off one weird draw.

## First, a gut check before trusting anything

Before reading into the numbers, I checked them against what the math says should
happen — recovery error should roughly follow `σ × √((m+1)/n)`. I divided the actual
error by that predicted value for every cell in the grid, and it stayed in a tight
band (roughly 0.7 to 1.5) the whole way across, no matter how far apart the n or σ
values were. That was a relief, honestly — it means the numbers below are real
behavior of the algorithm, not some bug quietly making things look better or worse
than they are.

## The results

| n \ σ |   0.1 |     1 |     5 |     15 |     40 |
| -----: | ----: | ----: | ----: | -----: | -----: |
|     10 | 0.093 | 0.565 | 3.225 | 11.914 | 36.349 |
|     50 | 0.031 | 0.267 | 1.564 |  4.988 | 13.870 |
|    200 | 0.014 | 0.106 | 0.666 |  2.416 |  5.663 |
|  1,000 | 0.007 | 0.059 | 0.243 |  1.064 |  1.935 |
|  5,000 | 0.002 | 0.033 | 0.105 |  0.413 |  1.225 |
| 20,000 | 0.001 | 0.011 | 0.054 |  0.201 |  0.410 |

(lower number = closer to the real β = better)

## What I actually learned from this

**Throwing more data at a noisy problem works, but it's not a straight trade.** Look
down the σ=15 column — going from n=10 to n=1,000 (100x the data) cuts the error from
~11.9 down to ~1.06, so roughly 10x better. But then going from n=1,000 to n=20,000
(another 20x data) only gets you from ~1.06 to ~0.20 — about 5x better. You're paying
way more data for less and less improvement each time. That's the classic
diminishing-returns curve you'd expect from a square-root relationship — doubling your
dataset doesn't halve your error, it shrinks it by about √2. So if someone tells you
"just collect more data" as the fix for a noisy model, it's true, but it gets
expensive fast.

**Noise on its own is roughly proportional — but scale bails you out of it.** If I
crank σ up 400x (from 0.1 to 40) at n=10, the error blows up by a similar
~390x — basically noise punches through 1-for-1 when you don't have much data to
average it out. But at n=20,000, that exact same 400x noise increase still leaves you
with an error around 0.41, which is genuinely usable. So the *relative* damage from
noise doesn't really change with n, but the *absolute* damage becomes way easier to
live with once you've got enough data — a big enough sample size basically buys you
insurance against noisy measurements.

**The bad corner is exactly where you'd guess it'd be.** n=10 with σ=40 gives an error
over 36 — at that point the recovered β isn't telling you anything real, it's
basically noise dressed up as a coefficient. And no amount of tweaking the learning
rate or running more iterations fixes that, because the problem isn't the optimizer —
it's that the data itself just doesn't contain enough signal to pin down the answer.
Gradient descent will happily converge to *something*, but "converged" and "correct"
aren't the same thing when the underlying data can't support the answer.

## Bottom line

Both n and σ push in the direction you'd expect, but not at the same rate — n helps on
a slow square-root curve, σ hurts almost linearly. Practically: if your data's noisy
and you can't do anything about that, budget for a lot more data than you'd
instinctively guess, and don't waste time tuning gradient descent hyperparameters to
fix what's really a "not enough signal" problem.
