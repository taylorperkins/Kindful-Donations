# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def last_year_range(date):
    upper_bound = datetime(date.year, date.month, 1)
    lower_bound = upper_bound - relativedelta(years=1, months=1)
    return lower_bound, upper_bound - relativedelta(days=1)


def create_top5_bottom5(df):
    top_5_bottom_5 = pd.DataFrame(columns=['year', 'month', 'rank', 'id', 'amount', 'category'])

    for (year, month), df in df.groupby([
        df.created_at.dt.year,
        df.created_at.dt.month
    ]):
        sum_per_id = df[['id', 'amount']] \
            .groupby('id') \
            .sum() \
            .sort_values('amount', ascending=False) \
            .reset_index()

        sum_per_id.loc[:, 'year'] = year
        sum_per_id.loc[:, 'month'] = month

        top_5 = sum_per_id.head(5)
        top_5.loc[:, 'rank'] = top_5.index + 1
        top_5.loc[:, 'category'] = 'top'

        # this should now be reversed. The donor that gave the least is ranked at #1
        bottom_5 = sum_per_id.tail(5) \
            .sort_values('amount') \
            .reset_index()

        bottom_5.loc[:, 'rank'] = bottom_5.index + 1
        bottom_5.loc[:, 'category'] = 'bottom'

        top_5_bottom_5 = pd.concat([top_5_bottom_5, top_5, bottom_5], sort=False)

    top_5_bottom_5['date'] = top_5_bottom_5.apply(lambda x: datetime(x.year, x.month, 1), axis=1)
    return top_5_bottom_5.drop(columns=['index'])


def get_year_month_df(df):
    return df['created_at'].groupby([
        df.created_at.dt.year,
        df.created_at.dt.month
    ]).count() \
        .rename_axis(['year', 'month']) \
        .reset_index() \
        .drop(columns=['created_at'])


def create_top5_bottom5_donor_history_df(donations_df, donor_ids):
    year_month_df = get_year_month_df(donations_df)

    top_or_bottom_5_donor_history_df_output = pd.DataFrame(columns=['year', 'month', 'id', 'amount'])
    top_or_bottom_5_donor_history_df = donations_df[donations_df.id.isin(donor_ids)]

    for donor_id, df in top_or_bottom_5_donor_history_df.groupby('id'):
        sum_per_month = df[['amount', 'created_at']].groupby([
            df.created_at.dt.year,
            df.created_at.dt.month
        ]).sum() \
            .rename_axis(['year', 'month']) \
            .reset_index()

        amount_for_all_months = pd.merge(
            year_month_df,
            sum_per_month,
            on=['year', 'month'],
            how='left'
        )

        amount_for_all_months['id'] = donor_id

        top_or_bottom_5_donor_history_df_output = pd.concat(
            [top_or_bottom_5_donor_history_df_output, amount_for_all_months],
            sort=False)

    return top_or_bottom_5_donor_history_df_output


def rolling_windows(series, donor_history_df):
    date, donor_id = series.date, series.id

    last_year_lower_bound, last_year_upper_bound = last_year_range(date)
    prev_year_lower_bound, prev_year_upper_bound = last_year_range(last_year_lower_bound)

    last_year_sum = donor_history_df[
        (donor_history_df.id == donor_id) &
        (donor_history_df.date >= last_year_lower_bound) &
        (donor_history_df.date <= last_year_upper_bound)
    ].amount.sum()

    prev_year_sum = donor_history_df[
        (donor_history_df.id == donor_id) &
        (donor_history_df.date >= prev_year_lower_bound) &
        (donor_history_df.date <= prev_year_upper_bound)
    ].amount.sum()

    return pd.Series([
        last_year_sum,
        prev_year_sum,
        prev_year_lower_bound,
        prev_year_upper_bound,
        last_year_lower_bound,
        last_year_upper_bound])


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_folder', type=click.Path())
def main(input_filepath, output_folder):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info('Making datasets to support shiny app.')

    donations = pd.read_csv(input_filepath)
    donations['created_at'] = pd.to_datetime(donations.created_at, format='%Y-%m-%d %H:%M:%S')

    logger.info('Creating initial top 5 dataset.')
    top_5_bottom_5 = create_top5_bottom5(donations)

    logger.info('Creating history for top and bottom 5 donors.')
    top_or_bottom_5_donor_history_df_output = create_top5_bottom5_donor_history_df(donations, top_5_bottom_5.id)

    logger.info('Saving donor history.')
    top_or_bottom_5_donor_history_df_output.to_csv(
        f'{output_folder}/top_or_bottom_5_donor_history_df_output.csv',
        index=False
    )

    # add in date columns so I can compare them.
    top_or_bottom_5_donor_history_df_output['date'] = top_or_bottom_5_donor_history_df_output.apply(
        lambda x: datetime(x.year, x.month, day=1),
        axis=1
    )

    logger.info('Calculating rolling windows')
    top_5_bottom_5[[
        'last_year_rolling',
        'prev_year_rolling',
        'prev_year_lower_bound',
        'prev_year_upper_bound',
        'last_year_upper_bound',
        'last_year_lower_bound'
    ]] = top_5_bottom_5[['date', 'id']] \
        .apply(lambda x: rolling_windows(x, top_or_bottom_5_donor_history_df_output), axis=1)

    top_5_bottom_5['rolling_diff'] = top_5_bottom_5.last_year_rolling - top_5_bottom_5.prev_year_rolling

    logger.info('Saving off df with rolling windows.')
    top_5_bottom_5.to_csv(f'{output_folder}/top_5_bottom_5_with_rolling.csv', index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
