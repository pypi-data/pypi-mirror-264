# multiplication.py file 
# Each new plugin class has to be named Plugin  
class Plugin:
    # This is the feature offer by this plugin.
    # it prints the result of multiplying 2 numbers 
    def process(self, num1, num2):
        print("This is my multiplication plugin")
        print(num1 * num2) 