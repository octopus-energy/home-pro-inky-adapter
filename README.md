# home-pro-inky-adapter

This allows you to use the display image functionality of the [Pimoroni Inky pHAT](https://shop.pimoroni.com/products/inky-phat) with the Home Pro. Currently it's set up to work with the 5.7" 7 color display. The gpiod libraries used in the Inky pHAT library are not available in the Home Pro SDK, so this project replaces gpiod functions with those of the Octace_GPIO api.


## Running in the home pro sdk
Attach the hat to the 40-pin header on the Home pro. Load the project in the Home Pro SDK and run the project with: `python3 image_display.py --file <filename>`. For example, to use the beachanchors image included here, use `python3 image_display.py --file images/inky-4.0-beachanchors.jpg`.
