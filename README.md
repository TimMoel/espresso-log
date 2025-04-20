# EspressoLog

A Streamlit-based web application for logging and tracking espresso brewing parameters and results. Perfect for coffee enthusiasts who want to improve their espresso brewing skills through data-driven insights.

## Features

- Log detailed brewing parameters (dose, grind size, pre-infusion time, yield, shot time)
- Rate your brews on multiple attributes (sourness, bitterness, sweetness, body)
- Get intelligent suggestions for improving your next shot based on ratings
- Track your favorite recipes
- View historical brewing data
- Batch manage your brewing records

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TimMoel/espresso-log.git
cd espresso-log
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Start logging your espresso shots!

## Data Storage

All brew data is stored locally in a CSV file (`brew_log.csv`). This file is automatically created when you save your first brew.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements! 