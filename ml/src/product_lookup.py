import pandas as pd


# ==========================
# LOAD ARTICLES DATA
# ==========================

articles_df = pd.read_csv(
    "ml/data/raw/articles.csv"
)

articles_df[
    "article_id"
] = (
    articles_df[
        "article_id"
    ].astype(str)
)


# ==========================
# GET PRODUCT DETAILS
# ==========================

def get_product_details(
    article_ids
):

    products = articles_df[

        articles_df[
            "article_id"
        ].isin(
            article_ids
        )

    ][
        [
            "article_id",
            "prod_name",
            "product_type_name",
            "product_group_name",
            "graphical_appearance_name",
            "colour_group_name"
        ]
    ]

    return products.to_dict(
        orient="records"
    )