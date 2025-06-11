#!/usr/bin/python3
# SPDX-License-Identifier: BSD-2-Clause

# ELIXIR Training Metrics Database Parser
# Author: Gil Poiares-Oliveira <gpo@biodata.pt>
# © 2025 Associação BIP4DAB

import argparse
import polars as pl

DEMOGRAPHIC = {"keywords": [
    "course advertised",
    "career stage",
    "employment sector",
    "your country",
    "gender"
], "ids": [
    "demographic-heard_from",
    "demographic-career_stage",
    "demographic-employment_sector",
    "demographic-employment_country",
    "demographic-gender"]
}

QUALITY = {"keywords": [
    "you used the tool",
    "you use the tool",
    "you recommend",
    "overall rating",
    "balance of theoretical and practical content",
    "contact you by email"
], "ids": [
    "quality-used_resources_before",
    "quality-used_resources_future",
    "quality-recommend_course",
    "quality-course_rating",
    "quality-balance",
    "quality-email_contact"
]}

def match_and_replace(df: pl.DataFrame, col_matches: dict[str, list[str]]) -> pl.DataFrame:
    # Get current column names
    columns = df.columns
    new_columns = {}
    columns_to_keep = []
    
    # For each column name
    for col in columns:
        # Check if any keyword is a substring of the column name (case-insensitive)
        for idx, keyword in enumerate(col_matches["keywords"]):
            if keyword.lower() in col.lower():
                # If match found, store the new name mapping
                new_columns[col] = col_matches["ids"][idx]
                columns_to_keep.append(col)
                break
    
    # Drop columns that didn't match any keywords and rename the matching ones
    return df.select(columns_to_keep).rename(new_columns)


def reorder_columns(df: pl.DataFrame, column_order: list[str]) -> pl.DataFrame:
    """
    Reorder columns in a Polars DataFrame based on a provided list of column names.
    Any columns not specified in column_order will be placed at the end of the DataFrame.
    Missing columns will be added as empty columns in their expected positions.

    Args:
        df: polars.DataFrame - Input Polars DataFrame
        column_order: list - List of column names in desired order

    Returns:
        polars.DataFrame - DataFrame with reordered columns, including new empty columns
    """
    # Get all column names from the DataFrame
    all_columns = df.columns

    # Find columns that are not in the column_order list
    remaining_columns = [col for col in all_columns if col not in column_order]

    # For each missing column, add it as an empty column
    for col in column_order:
        if col not in all_columns:
            df = df.with_columns(pl.lit(None).alias(col))

    # Create final column order by combining specified order and remaining columns
    final_order = column_order + remaining_columns

    # Return DataFrame with reordered columns
    return df.select(final_order)

def tmd_parser(event_id: int, file):
    data = pl.read_csv(file)

    # For demographic data
    data_demographic = match_and_replace(data, DEMOGRAPHIC)

    # For quality data
    data_quality = match_and_replace(data, QUALITY)

    #Add event id
    data_demographic = data_demographic.with_columns(pl.lit(event_id).alias("event_id"))
    data_quality = data_quality.with_columns(pl.lit(event_id).alias("event_id"))

    DEMOGRAPHIC_OUTPUT_COLUMNS = ["event_id"] + DEMOGRAPHIC["ids"]
    QUALITY_OUTPUT_COLUMNS = ["event_id"] + QUALITY["ids"]

    data_demographic = reorder_columns(data_demographic, DEMOGRAPHIC_OUTPUT_COLUMNS)
    data_quality = reorder_columns(data_quality, QUALITY_OUTPUT_COLUMNS)

    return data_demographic, data_quality


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse data for ELIXIR TMD")
    parser.add_argument("id", help="ID of the event to parse")
    parser.add_argument("-f", "--f", help="Name of the CSV file to parse", default="submissions.csv")

    args = parser.parse_args()

    data_demographic, data_quality = tmd_parser(args.id, args.f)

    data_demographic.write_csv(f"{args.id}_demographic.csv")
    data_quality.write_csv(f"{args.id}_quality.csv")
