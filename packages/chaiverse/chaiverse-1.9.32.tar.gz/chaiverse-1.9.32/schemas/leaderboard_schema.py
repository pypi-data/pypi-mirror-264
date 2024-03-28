from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
from pydantic import BaseModel, Extra, Field

from chaiverse import config
from chaiverse.lib.now import utcnow
from chaiverse.schemas.leaderboard_row_schema import LeaderboardRow



DEFAULT_LEADERBOARD_HEADER_MAPPING = {
    'double_thumbs_up_ratio': '👍👍_ratio',
    'thumbs_up_ratio': '👍👍+👍_ratio',
    'single_thumbs_up_ratio': '👍_ratio',
    'thumbs_down_ratio': '👎_ratio',
}

DEFAULT_LEADERBOARD_INCLUDES = [
    'developer_uid',
    'submission_id',
    'elo_rating',
    'win_ratio',
    'num_battles',
    'double_thumbs_up_ratio',
    'thumbs_down_ratio',
    'feedback_count',
    'model_score',
    'safety_score',
    'best_of',
    'max_input_tokens',
    'model_repo',
    'reward_repo',
    'model_name',
    'us_pacific_date',
]

DEFAULT_LEADERBOARD_EXCLUDES = []

DEFAULT_LEADERBOARD_SORT_PARAMS = {
    'by': 'elo_rating',
    'ascending': False
}

DEFAULT_TABULATE_OPTIIONS = {
    'numalign': 'decimal',
}


class Leaderboard(BaseModel, extra=Extra.allow):
    timestamp: datetime = Field(default_factory=lambda: utcnow())
    leaderboard_rows: List[LeaderboardRow]

    @property
    def df(self) -> pd.DataFrame:
        leaderboard_rows = [row.all_fields_dict() for row in self.leaderboard_rows]
        df = pd.DataFrame.from_records(leaderboard_rows)
        df = _sort_by_values(df, **DEFAULT_LEADERBOARD_SORT_PARAMS)
        return df

    def to_display_df(self, includes=None, excludes=None, sort_params=None, header_mapping=None) -> pd.DataFrame:
        includes = includes or DEFAULT_LEADERBOARD_INCLUDES
        excludes = excludes or DEFAULT_LEADERBOARD_EXCLUDES
        sort_params = sort_params or DEFAULT_LEADERBOARD_SORT_PARAMS
        header_mapping = header_mapping or DEFAULT_LEADERBOARD_HEADER_MAPPING
        df = self.df
        if len(df) > 0:
            df = _add_repo_aggregate_columns(df)
            df = _include_listed_columns(df, includes)
            df = _exclude_listed_columns(df, excludes)
            df = _sort_by_values(df, **sort_params)
            df['elo_rating']=df.elo_rating.astype(int)
            df = df.round(2)
            df = df.rename(columns=header_mapping)
        return df

    def to_html(self, includes=None, header_mapping=None, submission_type="basic"):
        includes = includes or DEFAULT_LEADERBOARD_INCLUDES
        df = self.to_display_df(includes=includes, header_mapping=header_mapping)
        df = df[df[header_mapping["submission_type"]] == submission_type]
        html = df.to_html(classes="leaderboard-table table display nowrap", index=False, justify="center", escape=False)
        return html

    @property
    def auto_deactivation_candidates(self):
        rows = _get_can_auto_deactivate_rows(self.leaderboard_rows)
        rows = _sort_auto_deactivate_rows(rows)
        rows = _remove_top_models(rows)
        rows = [row.submission_id for row in rows]
        return rows


def _add_repo_aggregate_columns(df):
    for column in ["elo_rating", "double_thumbs_up_ratio", "thumbs_down_ratio", "win_ratio", "safety_score", "model_score"]:
        df[f"{column}_by_repo"] = df.groupby("model_repo")[column].transform("max")
    for column in ["feedback_count", "num_battles"]:
        df[f"{column}_by_repo"] = df.groupby("model_repo")[column].transform("sum")
    return df


def _include_listed_columns(df, includes):
    df = df[[column for column in includes if column in df.columns]]
    return df


def _exclude_listed_columns(df, excludes):
    df = df[[column for column in df.columns if column not in excludes]]
    return df


def _sort_by_values(df, by: List[str], ascending: bool):
    if len(df) > 0:
        df = df.sort_values(by=by, ascending=ascending, na_position='last', ignore_index=True)
        df.index = np.arange(1, len(df)+1)
    return df


def _get_can_auto_deactivate_rows(rows: List[LeaderboardRow]): 
    rows = [row for row in rows if row.can_auto_deactivate()]
    return rows


def _sort_auto_deactivate_rows(rows: List[LeaderboardRow]):
    rows = sorted(rows, key=lambda row: row.elo_rating, reverse=True)
    return rows


def _remove_top_models(rows: List[LeaderboardRow]):
    rows = rows[config.AUTO_DEACTIVATION_MIN_RANK-1:]
    return rows
