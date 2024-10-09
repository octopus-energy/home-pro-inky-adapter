# home-pro-inky-adapter

This allows you to use the display image functionality of the [Pimoroni Inky pHAT](https://shop.pimoroni.com/products/inky-phat) with the Home Pro. Currently it's set up to work with the 5.7 inch 7 color display by default, but also can be used for the 7.3 inch and 4 inch versions. The gpiod libraries used in the Inky pHAT library are not available in the Home Pro SDK, so this project replaces gpiod functions with those of the Octace_GPIO api.


## Running in the home pro sdk
Attach the hat to the 40-pin header on the Home pro. Load the project in the Home Pro SDK. To display an image, run the project with: `python3 image_display.py --file <filename>`. For example, to use the test image included here, use `python3 image_display.py --file images/test_image_5-7.png`. To use the 7.3 inch display, use `python3 image_display.py --file images/test_image_7-3.png --device Impression7-3`. To use the 4 inch display, use `python3 image_display.py --file images/test_image_4.png --device Impression4`.


## Show the agile tariff as a line plot
Run `python3 show_agile.py` to show the agile tariff as a line plot on the Inky pHAT. It shows the previous 6 hours and following 12 hours of import and export tariff price including VAT for a location in London. The data is fetched from Octopus Energy's REST API. It currently just runs as a once off in the devloper SDK as an demonstration of the Inky hat and it isn't a dockerised app yet. It uses the seaborn library for plotting which can be installed with `pip install seaborn`.

![Image of HomePro in the wild.](assets/Pro_agile_display.jpg)
