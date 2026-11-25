# Exploratory Data Analysis (EDA) Phase

## 1. Purpose and scope

The EDA phase explores the UK train-ticket dataset to understand what it contains, check its basic quality, and answer descriptive business questions. The analysis is based on ticket transactions; it does **not** establish the number of unique passengers, verified boardings, train services, or live railway performance.

The project analyzes records from the raw file `railway.csv`, which contains 31,653 transactions and 18 columns. The purchase period runs from December 8, 2023 to April 30, 2024, while the journey period runs from January 1 to April 30, 2024.

> **Interpretation note:** The source does not specify the currency. Although the project assumes GBP in places, the safer wording is “price units.” Recorded prices are before refunds and are not confirmed net revenue, profit, or final collected payments.

## 2. Initial data checks

The EDA notebook checks the dataset's structure and foundational data quality, including:

- Number of rows and columns
- Uniqueness of transaction IDs and duplicate full rows
- Validity of purchase and journey dates
- Price statistics
- Missing and blank values
- Railcard categories

The dataset has 31,653 unique transaction IDs and no duplicate full rows. The `None` value in the Railcard field means that no Railcard was used; it is a valid category, not missing information.

## 3. Ticket, channel, and payment analysis

The notebook compares ticket counts and recorded prices across ticket types (`Advance`, `Anytime`, and `Off-Peak`), ticket classes (`Standard` and `First Class`), and Railcard categories. These comparisons are descriptive. For example, a lower observed average price for a Railcard group would not, by itself, prove that Railcards caused prices to be lower; route, timing, and ticket type may also differ.

The project also examines online versus station purchases, payment methods (Credit Card, Contactless, and Debit Card), and how purchase channel and payment method relate.

## 4. Route analysis

Records are grouped by directional route (departure station to arrival destination). For each route, the analysis calculates:

- Number of ticket records
- Number of usable price values
- Total recorded sales value
- Average recorded price

Routes are ranked by recorded sales value. The most valuable route reported in the project is London Kings Cross to York. “Sales value” here means the sum of recorded ticket prices; it should not be interpreted as profit or net revenue.

## 5. Time-based activity

The analysis studies ticket activity by purchase date and month, and by journey date and month. It also looks at daily ticket volume and daily recorded sales value.

Where appropriate, the notebook fills missing calendar dates with zero ticket records. It distinguishes between two different situations:

1. A date with no ticket transactions.
2. A date with ticket transactions but no usable prices.

This distinction matters because a missing date in an aggregate series does not always mean missing source data.

## 6. Reliability, disruption, and refund requests

The notebook examines journey outcomes and disruption information. The reported journey-status distribution is:

| Journey status | Records | Share |
|---|---:|---:|
| On Time | 27,481 | 86.82% |
| Delayed | 2,292 | 7.24% |
| Cancelled | 1,880 | 5.94% |

It also analyzes delay and cancellation reasons and compares refund-request rates by journey status. Reported refund-request rates are 23.82% for delayed journeys and 30.43% for cancelled journeys.

A refund request is only a request. The dataset does not show whether it was approved or paid, so these figures should not be described as actual refunds.

## 7. Missing values and unusual records

Some blank values are meaningful in context. For example, an actual arrival time may be blank for a cancelled journey, and a delay reason may be blank for an on-time journey. These should not automatically be imputed with averages or generic labels during EDA.

The notebook identifies 18 records marked `Delayed` whose actual arrival time is at or before the scheduled arrival time. The records are retained and treated as review flags rather than automatically corrected.

## 8. Price summary and reconciliation

Reported price statistics are:

| Metric | Value |
|---|---:|
| Total recorded sales value | 741,921 price units |
| Average price | 23.44 price units |
| Median price | 11 price units |
| Minimum | 1 price unit |
| Maximum | 267 price units |

The notebook reconciles totals across route, daily purchase activity, monthly purchase activity, overall price totals, and category counts. The reported total reconciles to 741,921 price units.

## 9. Main EDA conclusions and boundaries

The EDA provides a descriptive picture of ticket transactions, observed prices, routes, purchase patterns, and journey outcomes. It does not establish causal effects, confirmed refunds, passenger counts, or operational performance beyond the information represented in this dataset.

Important limits include the short historical period (about four months), unspecified source currency, absence of unique passenger and verified boarding information, and unresolved unusual records. The process by which the dataset extract was produced is also undocumented.

## 10. Notebook reference

The main analysis is in `01_EDA.ipynb`. The notebook is described as checking data structure and quality, analyzing ticket and purchase categories, grouping routes, studying activity over time, evaluating reliability and refund requests, and reconciling totals.
