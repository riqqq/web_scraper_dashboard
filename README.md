# Web Scraper Dashboard

This project utilizes Python and Selenium for web scraping. It collects headlines from a chosen news website, analyzes the data, and presents the findings through visualizations using Matplotlib and WordCloud. The results are displayed via a Flask-based web interface.

## Features

- **Headline Scraping:** Extracts headlines from a selected news website.
- **Word Frequency Analysis:** Examines the frequency of words within the headlines.
- **Sentiment Analysis:** Assesses the sentiment of headlines (positive, negative, or neutral).
- **Topic Modeling:** Identifies prevalent topics within the headlines using Latent Dirichlet Allocation (LDA).
- **Phrase Generation:** Creates a phrase using a subset of the most frequent words.
- **Web Interface:** Presents the results through a web interface developed with Flask.

## Usage

1. Clone the repository: `git clone https://github.com/riqqq/web_scraper_dashboard.git`
2. Install dependencies: Make sure you have Python and pip installed, then run:
`pip install flask matplotlib wordcloud textblob scikit-learn selenium webdriver-manager`
3. Run `scraper.py`
4. Run `process_data.py`
5. Run the Flask application: `python app.py`
6. Access the web interface at `http://localhost:5000` in your browser.

## Credits

- **Author:** Krzysztof Pisarczyk

## License

This project is licensed under the MIT License.

© 2024 Krzysztof Pisarczyk. All rights reserved.
