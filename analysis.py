from news_scrap import google_news_scrap
from text_cleaner import text_cleaning
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
import base64
from datetime import date


def word_freq(text):
    str_frequency = []
    dict_freq = {}

    for i in text:
        # checking for the duplicacy
        if i not in str_frequency:
            # insert value in str2
            str_frequency.append (i)

    # Create a dictionnary of words and their frequency
    for i in range (0, len (str_frequency)):
        # count the frequency of each word(present
        # in str2) in str and print
        dict_freq.update({i: [str_frequency[i], text.count (str_frequency[i])]})

    # Create data frame with dictionnary, and sort it by frequency
    df = pd.DataFrame(dict_freq).transpose()
    df.columns = ['keyword', 'count']
    df = df.sort_values(by='count', ascending=False)

    return df


def clean_date(dates):
    # Dates must be a list
    clean_dates = {}

    for i, d in enumerate(dates):
        clean_dates.update({i: [d[:9], d[11:18]]})

    return clean_dates


def fig_wordcloud(text, dim):
    # text must be a string and dim represents the dimension of the wordcloud in pixel
    wordcloud = WordCloud(width=dim, height=dim, background_color='white', min_font_size=10).generate(' '.join(text))
    fig = wordcloud.to_image()

    with BytesIO() as buffer:
        fig.save(buffer, 'png')
        fig = base64.b64encode(buffer.getvalue()).decode()

    return fig


def get_full_text(text_list):
    # text_list must be a list
    full_text = []
    for text in text_list:
        full_text += text_cleaning(text, 'french')

    return full_text


def fig_freq(sources):
    # Sources must be a list
    # source frequency
    all_sources = [s.lower() for s in sources]
    df_freq = word_freq(all_sources)

    fig = px.bar(df_freq.head(25), x='keyword', y='count',
                 height=600, width=600,
                 labels={'keyword': 'Sources', 'count': 'Number of articles'},
                 title='Number of articles per source')

    return fig


def update_db():
    # Scrap
    titles, sources, datetimes = google_news_scrap()

    # Create a dico from the scrap, while removing imcomplete rows
    di = {}
    try:
        for i, elt in enumerate(titles):
            di.update({i: [titles[i], sources[i], datetimes[i]]})
    except IndexError:
        pass

    # Create df from the dico and add today's date as extract_day
    df_today = pd.DataFrame(di).transpose()
    df_today.columns = ['titles', 'sources', 'datetimes']
    df_today['extract_day'] = date.today()

    # Import previous df from csv
    df = pd.read_csv('db.csv', encoding='UTF-8')

    # Update df without duplicate titles
    for i in range(len(df_today)):
        if df_today['titles'][i] not in list(df['titles']):
            df = df.append(df_today.iloc[i])

    # Save updated df and return it
    df.to_csv('db.csv', index=False, encoding='UTF-8')

    return df


# def fig_wc_source(df, indice):
#     filtered_text = []
#     all_sources = [s.lower () for s in df['sources']]
#     s_freq = word_freq (all_sources)
#     df_sfreq = create_df (s_freq)
#
#     for i in range(len(df)):
#         # print((type(df['sources'][i])))
#         if df['sources'][i].lower() == df_sfreq['keyword'][indice]:
#             filtered_text.append(df['titles'][i])
#
#     fig = fig_wordcloud(get_full_text(filtered_text), 200)
#
#     return fig
#
#
# def words_source(df, indice):
#     filtered_text = []
#     all_sources = [s.lower () for s in df['sources']]
#     s_freq = word_freq (all_sources)
#     df_sfreq = create_df (s_freq)
#
#     for i in range(len(df)):
#         # print((type(df['sources'][i])))
#         if df['sources'][i].lower() == df_sfreq['keyword'][indice]:
#             filtered_text.append(df['titles'][i])
#
#     df_word_freq = create_df(word_freq(get_full_text(filtered_text)))
#     df_dispersion = create_df(word_freq(list(df_word_freq['count'])))
#     print(df_dispersion)
#     fig = px.bar(df_dispersion, x="keyword", y="count")
#
#     return fig
